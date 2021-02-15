import pygame, sys
from KLassenlocal import *

#Pygame initialisieren
pygame.init()

#Frame Rate des Spiels festlegen
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
#Paint_back() färbt den Hintergrund des Spielfelds und erstellt die weiße Mittellinie
def paint_back():
    screen.fill(bg_color)
    pygame.draw.line(screen, white,(width//2, 0), (width//2, height),7 )

#restart setzt Scores, Paddle positionen sowie den Ball zurück
def restart():
    paint_back()
    score1.restart()
    score2.restart()
    ball.restart_pos()
    paddle1.restart_pos()
    paddle2.restart_pos()

#regelt was passiert wenn multiplayer gespielt werden will
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

#regelt was passiert wenn singleplayer gespielt werden will
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

#Objekte werden erzeugt
ball = Ball( screen, white, width//2, height//2, 15 )
paddle1 = Paddle(screen, light_grey, 15, height//2 - 60, 20,120)
paddle2 = Paddle(screen, light_grey,width - 20 - 15, height//2 - 60, 20,120)
collision = Collision_Manager()
score1 = Score(screen, "0", width//4, 15)
score2 = Score(screen, "0", width - width//4, 15)
singleplayer = Button(light_grey, 200, 200, 200, 100, "Single Player" )
multiplayer = Button(light_grey, 500, 200, 200, 100, "Multi Player" )
play = Button(light_grey, 310, 430, 100, 50, "Play", 20 )
neustarten = Button(light_grey, 490, 430, 100, 50, "Reset", 20 )
home = Button(light_grey, 10, 10, 70, 50, "Home", 20 )

#Variablen und Parameter von Button Objekten
playing = False
singleplayer.state = "visible"
multiplayer.state = "visible"
gamemode = ""

#Funltionsaufrufe
paint_back()

#While Schleife für game
while True:
    for event in pygame.event.get():
        #maus position wird jeden Durchlauf in einem Tupel gespeichert
        pos = pygame.mouse.get_pos()
        #Wenn rotes Kreuz gedrückt wird --> exit
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Wenn Maus auf Multiplayer down Multiplayer Modus
            if multiplayer.isOver(pos):
                gamemode = 1
                playing = True
                ball.start_moving()
            #Wenn Maus auf Singleplayer down Singleplayer Modus
            if singleplayer.isOver(pos):
                gamemode = 0
                playing = True
                ball.start_moving()
            #Wenn Maus auf Play down Playing = True und ball fängt an zu moven
            if play.isOver(pos):
                playing = True
                ball.start_moving()
            #Wenn Maus auf neustarten down Punktestand und Pos resetten
            if neustarten.isOver(pos):
                restart()
                playing = False
            #Wenn Maus auf home down zurück zu Auswahlbildschirm
            if home.isOver(pos):
                restart()
                playing = False
                singleplayer.state = "visible"
                multiplayer.state = "visible"

        '''if event.type == pygame.KEYDOWN:
            #Steuerung der Paddles mit Keys
            if event.key == pygame.K_UP:
                paddle2.state = "up"
            if event.key == pygame.K_DOWN:
                paddle2.state = "down"
            if event.key == pygame.K_w:
                paddle1.state = "up"
            if event.key == pygame.K_s:
                paddle1.state = "down"'''

        #Auskommentieren wenn man stockende Bewegung der Paddles will wenn man Taste loslässt
        if event.type == pygame.KEYUP:
            paddle2.state = "stopped"
            paddle1.state = "stopped"

    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_UP]:
        paddle2.state = "up"
    if keys_pressed[pygame.K_DOWN]:
        paddle2.state = "down"
    if keys_pressed[pygame.K_w]:
        paddle1.state = "up"
    if keys_pressed[pygame.K_s]:
        paddle1.state = "down"

    #Variable playing auf False -> es wird nicht gespielt
    if not playing:
        paint_back()
        counter = 0
        counter1 = 0
        counter2 = 0
        if multiplayer.state == "unvisible" and singleplayer.state == "unvisible":
            play.draw(screen, light_grey)
            neustarten.draw(screen, light_grey)
            home.draw(screen, light_grey)
        # Knöpfe nur zeigen wenn ihr Parameter auf Visible
        if singleplayer.state == "visible" and multiplayer.state == "visible":
            singleplayer.draw(screen, light_grey)
            multiplayer.draw(screen, light_grey)
            paddle1.draw()
            paddle2.draw()
        #Wenn Knöpfe auf unvisible Spiefeld in Ausgangsposition ohne Knöpfe
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

    #Wenn gespielt wird
    if playing:
        #Knöpfe unsichtbar
        singleplayer.state = "unvisible"
        multiplayer.state = "unvisible"

        #Auswahl des Spielmodus
        if gamemode == 0:
            one()

        if gamemode == 1:
            two()

        #Wenn ball und paddle berühren counter hochzählen
        if collision.between_ball_and_paddle1(ball, paddle1):
            ball.paddle_collision(counter, counter1, paddle1)
            counter += 1
            counter1 += 1

        # Wenn ball und paddle berühren counter hochzählen
        if collision.between_ball_and_paddle2(ball, paddle2):
            ball.paddle_collision(counter, counter2, paddle2)
            counter += 1
            counter2 += 1

        # Wenn ball und wand berühren posY reversen
        if collision.between_ball_and_walls(ball):
            ball.wall_collision()

        #Wenn Tor für Player1 Score erhöhen, Positionen resetten und Richtungen wieder auf 0, playing auf False
        if collision.check_goal_player1(ball):
            paint_back()
            score1.increase()
            ball.restart_pos()
            paddle1.restart_pos()
            paddle2.restart_pos()
            play.state = "visible"
            restart.state = "visible"
            playing = False

        # Wenn Tor für Player2 Score erhöhen, Positionen resetten und Richtungen wieder auf 0, playing auf False
        if collision.check_goal_player2(ball):
            paint_back()
            score2.increase()
            ball.restart_pos()
            paddle1.restart_pos()
            paddle2.restart_pos()
            playing = False

    #Dauerhaft Score anzeigen und Display updaten
    score1.draw()
    score2.draw()
    pygame.display.update()