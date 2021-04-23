import random
import math

import pygame as pg
from pygame import mixer

# initializing pygame
pg.init()

# creating screen(width,height)
screen = pg.display.set_mode((1100, 700))

# background image
background = pg.image.load("sky.png")

# Background
mixer.music.load("background.wav")
mixer.music.play(-1)

# display icon and title
pg.display.set_caption("Alien Invasion")
icon = pg.image.load("001-ufo.png")
pg.display.set_icon(icon)


def player(x, y):
    # display player image
    playerImg = pg.image.load("001-spaceship.png")
    screen.blit(playerImg, (x, y))


# initializing x and y location of player
playerX = 520
playerY = 580
player_changeX = 0
player_changeY = 0

alienImg = []
alienX = []
alienY = []
alien_changeX = []
alien_changeY = []

number_of_enemies = 8


def alien(x, y, i):
    # display alien image
    screen.blit(alienImg[i], (x, y))


# loading bullet
bulletImg = pg.image.load("001-bullet.png")
bulletX = 0
bulletY = 580
bullet_changeY = 20

# ready state - you can't see the bullet
# fire state - bullet is moving
bullet_state = "ready"

# Score

score_value = 0
font = pg.font.Font('SCOREBOARD.ttf', 40)

ScoreX = 10
ScoreY = 10


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (0, 0, 0))
    screen.blit(score, (x, y))


def bullet_fire(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(alienX, alienY, bulletX, bulletY):
    distance = math.sqrt((math.pow((alienX - bulletX), 2)) + (math.pow((alienY - bulletY), 2)))
    if distance < 32:
        return True
    return False


# Game Over
over_font = pg.font.Font("freesansbold.ttf", 64)


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (350, 300))


# Lifes
life = 3

lifeImg = []

def lifes(x, y, i):
    # display player image
    screen.blit(lifeImg[i], (x, y))


running = True
while running:

    # Adding rgb color on screen
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        # checking and moving according to the key pressed
        # KEYDOWN is when the button is pressed
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                player_changeX = -11
            if event.key == pg.K_RIGHT:
                player_changeX = 11
            if event.key == pg.K_SPACE:
                # checks whether the bullet is on the screen or not
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    # get the current x and y coordinate of spaceship
                    bulletX = playerX
                    bullet_fire(bulletX, bulletY)
        # KEYUP is when key is released
        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                player_changeX = 0
    playerX += player_changeX

    # boundary
    if playerX <= 0:
        playerX = 0
    elif playerX >= 1036:
        playerX = 1036

    # enemy movement
    for i in range(number_of_enemies):
        alienImg.append(pg.image.load("001-space-ship.png"))
        alienX.append(random.randint(0, 1036))
        alienY.append(random.randint(40, 150))
        alien_changeX.append(10)
        alien_changeY.append(40)
        # Game Over
        if alienY[i] > 540:
            life = life - 1
            alienY[i] = random.randint(40, 150)
            alienX[i] = random.randint(0, 1036)
            if life < 1:
                for j in range(number_of_enemies):
                    alienY[j] = 2000
                game_over_text()
                break

        alienX[i] += alien_changeX[i]
        if alienX[i] <= 0:
            alien_changeX[i] = 10
            alienY[i] += alien_changeY[i]
        elif alienX[i] >= 1036:
            alien_changeX[i] = -10
            alienY[i] += alien_changeY[i]

        # collision
        collision = isCollision(alienX[i], alienY[i], bulletX, bulletY)
        if collision:
            if number_of_enemies < 40:
                number_of_enemies += 1
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 580
            bullet_state = "ready"
            score_value += 1
            alienX[i] = random.randint(0, 1036)
            alienY[i] = random.randint(40, 150)

        # calling alien function
        alien(alienX[i], alienY[i], i)

    # To shoot multiple bullet
    if bulletY <= 0:
        bulletY = 580
        bullet_state = "ready"
        # Bullet movement
    if bullet_state == "fire":
        bullet_fire(bulletX, bulletY)
        bulletY -= bullet_changeY

    # calling player function
    player(playerX, playerY)
    show_score(ScoreX, ScoreY)
    life_changeX = 10
    for i in range(life):
        lifeImg.append(pg.image.load("001-heart.png"))
        lifeX = life_changeX
        lifeY = 45
        if life > -1:
            lifes(lifeX, lifeY, i)
        life_changeX += 35
    # updating display of pygame
    pg.display.update()
