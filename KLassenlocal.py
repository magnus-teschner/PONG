import pygame
import time
import random

#Farben
light_grey = (200,200,200)

class Ball:
    def __init__(self, screen, color, posX, posY, radius):
        self.screen = screen
        self.color = color
        self.posX = posX
        self.posY = posY
        self.radius = radius
        self.dx = 0
        self.dy = 0
        self.dx = 0
        self.dy = 0
        self.counter = 0
        self.draw()

    #Kreis zeichnen
    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.posX, self.posY), self.radius)

    #Start Moving in zufällige Richtung
    def start_moving(self):
        a = random.randint(0,1)
        liste = [0.3, -0.3]
        self.dx = liste[a]
        y = 0
        while  -0.1 < y < 0.1:
            y = random.uniform(-0.33, 0.33)
        self.dy = y

    #Moving mit Richtung dx, dy
    def move(self):
        self.posX += self.dx
        self.posY += self.dy

    #Wenn auf wall trifft reverse dy
    def wall_collision(self):
        self.dy = -self.dy

    #Paddle Collision
    def paddle_collision(self, counter, counter1, paddle):
        #Wenn erster Kontakt dx hoch
        if self.dx > 0 and counter == 0:
            self.dx = 0.6
        elif self.dx < 0 and counter == 0:
            self.dx = -0.6
        self.dx = -self.dx
        #Nach jedem Paddle Kontakt wird Ball, Paddle schneller
        if self.dx > 0:
            self.dx += 0.01
        elif self.dx < 0:
            self.dx -= 0.01
        if counter1 != 0:
            paddle.dy += 0.02

    #Restart Position und dx, dy
    def restart_pos(self):
        if self.posX <= 4 or self.posX >= 895:
            self.posX = 450
            self.posY = 250
            self.dx = 0
            self.dy = 0
            self.draw()



class Paddle:
    def __init__(self ,screen, color, posX, posY, width , height):
        self.screen = screen
        self.color = color
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height
        self.state = "stopped"
        self.dy = 0
        self.draw()

    #Rechteck zeichnen
    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.posX, self.posY, self.width, self.height) )

    #Nachverfolgung Ball, Singleplayer
    def move_on(self, ball):
        if ball.posY > self.posY - 10 and ball.posX < 450:
            self.posY += 0.45 + self.dy

        if ball.posY < self.posY + 10 and ball.posX < 450:
            self.posY -= 0.45 + self.dy

    #Moven auf Pfeiltasten
    def move(self):
        if self.state == "up":
            self.posY -= 0.45 + self.dy
        elif self.state == "down":
            self.posY += 0.45 + self.dy

    #Nicht über Rand hinaus moven
    def clamp(self):
        if self.posY <= 0:
            self.posY = 0
        if self.posY + self.height >= 500:
            self.posY = 500 - self.height
    #Restart Position und dy
    def restart_pos(self):
        self.posY = 500//2 - 60
        self.draw()
        self.state = "stopped"
        self.dy = 0

class Collision_Manager:

    #Collision ball paddle2 return True
    def between_ball_and_paddle1(self, ball, paddle1):
        if ball.posY + ball.radius > paddle1.posY and ball.posY - ball.radius < paddle1.posY + paddle1.height:
            if ball.posX - ball.radius <= paddle1.posX + paddle1.width:
                return True
        return False

    # Collision ball paddle2 return True
    def between_ball_and_paddle2(self, ball, paddle2):
        if ball.posY + ball.radius > paddle2.posY and ball.posY - ball.radius < paddle2.posY + paddle2.height:
            if ball.posX + ball.radius >= paddle2.posX:
                return True
        return False

    #Ball walls return True
    def between_ball_and_walls(self,ball):
        #top
        if ball.posY -ball.radius <= 0:
            return True
        #bottom
        if ball.posY + ball.radius >= 500:
            return True
        return False

    #Goal1: über x Koordinate x = 852 hinaus return True
    def check_goal_player1(self, ball):
        return ball.posX  >= 852

    # Goal2: über x Koordinate x = 48 hinaus return True
    def check_goal_player2(self, ball):
        return ball.posX  <= 48




class Score:
    def __init__(self, screen, points, posX, posY):
        self.screen = screen
        self.points = points
        self.posX = posX
        self.posY = posY
        self.font = pygame.font.SysFont("monospace", 80, bold = True)
        self.label = self.font.render(self.points, 0, light_grey )
        self.draw()

    #Label zeichnen
    def draw(self):
        self.screen.blit(self.label, (self.posX - self.label.get_rect().width // 2, self.posY))

    #Punkte erhöhen und Label neu rendern
    def increase(self):
        points = int(self.points) + 1
        self.points = str(points)
        self.label = self.font.render(self.points, 0, light_grey)

    #Punkte auf null und neu rendern
    def restart(self):
        self.points = "0"
        self.label = self.font.render(self.points, 0, light_grey)


class Button:
    def __init__(self, color, posX, posY, width, height, text='', size = 25):
        self.color = color
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height
        self.text = text
        self.size = size
        self.state = "unvisible"

    #Draw button
    def draw(self, screen, outline=None):
        #Wenn Outline größeres Rechteck mit anderer Farbe unten drunter
        if outline:
            pygame.draw.rect(screen, outline, (self.posX - 2, self.posY - 2, self.width + 4, self.height + 4), 0)

        #Rechteck zeichnen
        pygame.draw.rect(screen, self.color, (self.posX, self.posY, self.width, self.height), 0)

        #Wenn Text nicht leer ist
        if self.text != '':
            font = pygame.font.SysFont('monospace', self.size, bold = True)
            text = font.render(self.text, 1, (0, 0, 0))
            screen.blit(text, (
            self.posX + (self.width / 2 - text.get_width() / 2), self.posY + (self.height / 2 - text.get_height() / 2)))

    #Checken ob Maus über Button, wenn ja return True
    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.posX and pos[0] < self.posX + self.width:
            if pos[1] > self.posY and pos[1] < self.posY + self.height:
                return True

        return False
