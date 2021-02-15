import pygame, sys
from KLassenlocal import *

pygame.init()
clock = pygame.time.Clock()
clock.tick(30)
#Variablen
width = 900
height = 500
black = (0,0,0)
white = (255, 255, 255)
bg_color = pygame.Color('grey12')
light_grey = (200,200,200)

#Screen Setup
screen = pygame.display.set_mode((width , height))
pygame.display.set_caption("PONG")


#Funktionen
def paint_back():
    screen.fill(bg_color)
    pygame.draw.line(screen, white,(width//2, 0), (width//2, height),7 )



def restart():
    paint_back()
    score1.restart()
    score2.restart()
    ball.restart_pos()
    paddle1.restart_pos()
    paddle2.restart_pos()

paint_back()

#Objekte
ball = Ball( screen, white, width//2, height//2, 15 )
paddle1 = Paddle(screen, light_grey, 15, height//2 - 60, 20,120)
paddle2 = Paddle(screen, light_grey,width - 20 - 15, height//2 - 60, 20,120)
collision = Collision_Manager()
score1 = Score(screen, "0", width//4, 15)
score2 = Score(screen, "0", width - width//4, 15)
singleplayer = Button(light_grey, 200, 200, 200, 100, "Single Player" )
multiplayer = Button(light_grey, 500, 200, 200, 100, "Multi Player" )
#Variables
playing = False
singleplayer.state = "visible"
multiplayer.state = "visible"
gamemode = ""


def two():
    paint_back()
    ball.move()
    ball.draw()
    paddle1.move()
    paddle1.clamp()
    paddle1.draw()

    paddle2.clamp()
    paddle2.move()
    paddle2.draw()
def one():
    paint_back()
    ball.move()
    ball.draw()
    paddle1.dx = 0
    paddle1.move_on(ball)
    paddle1.clamp()
    paddle1.draw()

    paddle2.clamp()
    paddle2.move()
    paddle2.draw()


while True:
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if singleplayer.isOver(pos):
                gamemode = 0
                playing = True
                ball.start_moving()
            if multiplayer.isOver(pos):
                gamemode = 1
                playing = True
                ball.start_moving()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                ball.start_moving()
                playing = True

            if event.key == pygame.K_r:
                restart()
                playing = False
                singleplayer.state = "visible"
                multiplayer.state = "visible"

            if event.key == pygame.K_UP:
                paddle2.state = "up"
            if event.key == pygame.K_DOWN:
                paddle2.state = "down"
            if event.key == pygame.K_w:
                paddle1.state = "up"
            if event.key == pygame.K_s:
                paddle1.state = "down"
        #if event.type == pygame.KEYUP:
            #paddle2.state = "stopped"
            #paddle1.state = "stopped"

    if not playing:
        paint_back()
        counter = 0
        counter1 = 0
        counter2 = 0
        if singleplayer.state == "visible" and multiplayer.state == "visible":
            singleplayer.draw(screen, light_grey)
            multiplayer.draw(screen, light_grey)
            paddle1.draw()
            paddle2.draw()

        elif multiplayer.state == "unvisible" and singleplayer.state == "unvisible":
            counter1 = 0
            counter2 = 0
            paddle1.move()
            paddle1.clamp()
            paddle1.draw()

            paddle2.clamp()
            paddle2.move()
            paddle2.draw()
            ball.move()
            ball.restart_pos()
            ball.draw()
            counter = 0


    if playing:
        singleplayer.state = "unvisible"
        multiplayer.state = "unvisible"


        if gamemode == 0:
            one()


        if gamemode == 1:
            two()
            print(paddle1.dy)
            print(paddle2.dy)




        if collision.between_ball_and_paddle1(ball, paddle1):
            ball.paddle_collision(counter, counter1, paddle1)
            counter += 1
            counter1 += 1
        if collision.between_ball_and_paddle2(ball, paddle2):
            ball.paddle_collision(counter, counter2, paddle2)
            counter += 1
            counter2 += 1
        if collision.between_ball_and_walls(ball):
            ball.wall_collision()

        if collision.check_goal_player1(ball):
            paint_back()
            score1.increase()
            ball.restart_pos()
            paddle1.restart_pos()
            paddle2.restart_pos()
            paddle1.dy = 0
            paddle2.dy = 0
            #ball.dx = 0
            playing = False
        if collision.check_goal_player2(ball):
            paint_back()
            score2.increase()
            ball.restart_pos()
            paddle1.restart_pos()
            paddle2.restart_pos()
            paddle1.dy = 0
            paddle2.dy = 0
            #ball.dx = 0
            playing = False


    score1.draw()
    score2.draw()
    pygame.display.update()