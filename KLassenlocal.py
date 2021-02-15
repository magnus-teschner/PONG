import pygame
import time
import random
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

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.posX, self.posY), self.radius)

    def start_moving(self):
        a = random.randint(0,1)
        liste = [0.3, -0.3]
        self.dx = liste[a]
        x = 0
        while  -0.1 < x < 0.1:
            x = random.uniform(-0.33, 0.33)
        self.dy = x

    def move(self):
        self.posX += self.dx
        self.posY += self.dy

    def wall_collision(self):
        self.dy = -self.dy

    def paddle_collision(self, counter, counter1, paddle):
        if self.dx > 0 and counter == 0:
            self.dx = 0.6
        elif self.dx < 0 and counter == 0:
            self.dx = -0.6
        self.dx = -self.dx
        if self.dx > 0:
            self.dx += 0.01
        elif self.dx < 0:
            self.dx -= 0.01
        if counter1 != 0:
            paddle.dy += 0.02


    def restart_pos(self):
        if self.posX <=4 or self.posX >= 895:
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

    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.posX, self.posY, self.width, self.height) )

    def move_on(self, ball):
        if ball.posY > self.posY - 2 and ball.posX < 450:
            self.posY += 0.6

        if ball.posY < self.posY + 2 and ball.posX < 450:
            self.posY -= 0.6

    def move(self):
        if self.state == "up":
            self.posY -= 0.45 + self.dy
        elif self.state == "down":
            self.posY += 0.45 + self.dy

        #print(self.dy)
    def clamp(self):
        if self.posY <= 0:
            self.posY = 0
        if self.posY + self.height >= 500:
            self.posY = 500 - self.height
    def restart_pos(self):
        self.posY = 500//2 - 60
        self.draw()
        self.state = "stopped"

class Collision_Manager:
    def between_ball_and_paddle1(self, ball, paddle1):
        if ball.posY + ball.radius > paddle1.posY and ball.posY - ball.radius < paddle1.posY + paddle1.height:
            if ball.posX - ball.radius <= paddle1.posX + paddle1.width:
                return True
        return False
    def between_ball_and_paddle2(self, ball, paddle2):
        if ball.posY + ball.radius > paddle2.posY and ball.posY - ball.radius < paddle2.posY + paddle2.height:
            if ball.posX + ball.radius >= paddle2.posX:
                return True
        return False

    def between_ball_and_walls(self,ball):
        #top
        if ball.posY -ball.radius <= 0:
            return True
        #bottom
        if ball.posY + ball.radius >= 500:
            return True
        return False

    def check_goal_player1(self, ball):

        return ball.posX  >= 852
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

    def draw(self):
        self.screen.blit(self.label, (self.posX - self.label.get_rect().width // 2, self.posY))
    def increase(self):
        points = int(self.points) + 1
        self.points = str(points)
        self.label = self.font.render(self.points, 0, light_grey)
    def restart(self):
        self.points = "0"
        self.label = self.font.render(self.points, 0, light_grey)
    def restart(self):
        self.points = "0"
        self.label = self.font.render(self.points, 0, light_grey)
