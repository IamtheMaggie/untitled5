import pygame
import math

pygame.init()

screen = pygame.display.set_mode((800, 600))

# Player
playerImg = pygame.image.load(r'C:\Users\Mmwwa\Pictures\tank.png')
playerX = 150
playerY = 150
playerX_change = 0
playerY_change = 0

# Enemy
enemyImg = pygame.image.load(r'C:\Users\Mmwwa\Pictures\tank-2.png')
enemyX = 300
enemyY = 300
enemyX_change = 0
enemyY_change = 0

# Obstacles
wallImg = pygame.image.load(r'C:\Users\Mmwwa\Pictures\medieval-wall.png')
wallX = 200
wallRight = 260
wallLeft = 140
wallY = 200
wallDown = 230
wallUp = 170

# Ball
ballImg = pygame.image.load(r'C:\Users\Mmwwa\Pictures\bullet.png')
ballX_change = .1
ballY_change = .1
ballX = 0
ballY = playerY
ball_state = "ready"

ballImgE = pygame.image.load(r'C:\Users\Mmwwa\Pictures\bullet.png')
ballX_changeE = .1
ballY_changeE = .1
ballXE = 0
ballYE = enemyY
ball_stateE = "ready"

def fire_ball(x,y):
    global ball_state
    ball_state = "fire"
    screen.blit(ballImg, (x, y + 5))

def fire_ballE(x,y):
    global ball_stateE
    ball_stateE = "fire"
    screen.blit(ballImgE, (x, y + 5))


# Caption
pygame.display.set_caption("Our Game")

def ball(x,y):
    screen.blit(ballImg, (ballX, ballY))

def player(x,y):
    screen.blit(playerImg, (x, y))

def enemy(x,y):
    screen.blit(enemyImg, (x, y))

def ballE(x,y):
    screen.blit(ballImgE, (ballXE, ballYE))

# Game Loop
running = True
while running:
    #RBG
    screen.fill((255, 255, 255))
    screen.blit(wallImg, (wallX, wallY))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.1
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.1
            if event.key == pygame.K_UP:
                playerY_change = -0.1
            if event.key == pygame.K_DOWN:
                playerY_change = 0.1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            slopeX, slopeY = pygame.mouse.get_pos()
            m = (slopeY - playerY)/(slopeX - playerX)
            fire_ball(playerX, ballY)

    playerY += playerY_change
    # Outer Boundaries
    if playerY <= -15:
        playerY = -15
    if playerY >= 550:
        playerY = 550

    playerX += playerX_change
    # Outer Boundaries
    if playerX <= 0:
        playerX = 0
    elif playerX >= 735:
        playerX = 735

    # Wall Boundaries
    if wallLeft <= playerX <= wallLeft + 1 and wallUp <= playerY <= wallDown:
        playerX = wallLeft
    if wallRight - 1 <= playerX <= wallRight and wallUp <= playerY <= wallDown:
        playerX = wallRight
    if wallUp <= playerY <= wallUp + 1 and wallLeft <= playerX <= wallRight:
        playerY = wallUp
    if wallDown - 1 <= playerY <= wallDown and wallLeft <= playerX <= wallRight:
        playerY = wallDown

    # Ball Movement
    if ballY < 0 or ballY > 600 or ballX < 0 or ballX > 800:
        ballY = playerY
        ballX = playerX
        ball_state = "ready"
    if ball_state is "ready":
        ballY = playerY
        ballX = playerX
    if ball_state is "fire":
        fire_ball(ballX, ballY)
        if slopeY <= playerY:
            ballY -= ballY_change
            ballX -= ballY_change * (1/m)
        if slopeY > playerY:
            ballY += ballY_change
            ballX += ballY_change * (1/m)
    if wallLeft <= ballX <= wallRight and wallUp <= ballY <= wallDown:
        ball_state = "ready"

# enemy ball

    if ballYE <= 0 or ballYE >= 600 or ballXE <= 0 or ballXE >= 800 or (wallLeft <= ballXE <= wallRight and wallUp <= ballYE <= wallDown):
        ball_stateE = "ready"
        ballYE = enemyY
        ballXE = enemyX
    if ball_stateE is "ready":
        x = playerX
        y = playerY
        ballX_changeE = ((y - enemyY)/(x - enemyX))
        ball_stateE = "fire"
    if ball_stateE is "fire":
        fire_ballE(ballXE, ballYE)
        if playerX - 32 <= ballXE <= playerX + 32 and playerY - 32 <= ballYE <= playerY + 32: #if gets hit
            ball_stateE = "ready"
            ballYE = enemyY
            ballXE = enemyX
        if playerY <= enemyY:
            ballYE -= ballY_changeE
            ballXE -= ballY_changeE / ballX_changeE
        elif playerY > enemyY:
            ballYE += ballY_changeE
            ballXE += ballY_changeE / ballX_changeE

    player(playerX, playerY)
    enemy(enemyX, enemyY)
    pygame.display.update()

