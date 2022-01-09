import pygame
import random
import math

module_charge = pygame.init()

# screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
font = pygame.font.SysFont(None, 48)
RED = (255, 0, 0)
loop = True
width = 1000
height = 800

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Invader 3000")

# Background
background = pygame.image.load("assets/background.jpg").convert()
background = pygame.transform.scale(surface=background, size=(1000, 800))

# Spaceship
spaceship = pygame.image.load("assets/spaceship.png").convert()
spaceship = pygame.transform.scale(surface=spaceship, size=(50, 50))
shipX = 480
shipY = 650
shipX_change = 0

# Bullet
bulletPicture = pygame.image.load("assets/kindpng_1414280.png").convert()
bulletPicture = pygame.transform.scale(surface=bulletPicture, size=(20, 20))
bulletX = 0
bulletX_change = 0
bulletY = 630
bulletY_change = 20
is_shot = False

# Enemy
enemy = []
enemyX = []
enemyX_change = []
enemyY = []
enemyY_change = []
nb_enemies = 10

for i in range(nb_enemies):
    enemy.append(pygame.image.load("assets/alien (1).png").convert())
    enemyX.append(random.randint(100, 800))
    enemyX_change.append(5)
    enemyY.append(50)
    enemyY_change.append(0)


def shoot_bullet(x, y):
    global is_shot
    is_shot = True
    screen.blit(bulletPicture, (x+15, y-16))


def move_spaceship(x, y):
    screen.blit(spaceship, (x, y))


def move_enemy(x, y, i):
    screen.blit(enemy[i], (x, y))


def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance <= 30:
        return True


while loop:
    screen.blit(background, [0, 0])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False

        if event.type == pygame.KEYDOWN:
            # Quit the game
            if event.key == pygame.K_ESCAPE:
                loop = False
            # Move spaceship
            elif event.key == pygame.K_q:
                shipX_change = -10
            elif event.key == pygame.K_d:
                shipX_change = 10
            # Shoot
            elif event.key == pygame.K_p or event.key == pygame.K_SPACE:
                bulletX = shipX
                shoot_bullet(bulletX, shipY)
            # Restart game
            elif event.key == pygame.K_RETURN:
                shipX = 480
                shipY = 650
                screen.blit(background, [0, 0])
                screen.blit(spaceship, (shipX, shipY))
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d or event.key == pygame.K_q:
                shipX_change = 0

    # Continuous bullet
    if is_shot:
        shoot_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    if bulletY <= 0:
        bulletX = 0
        bulletY = 630
        is_shot = False

    # Borders
    if shipX <= 0:
        shipX = 0
    elif shipX >= 950:
        shipX = 950

    shipX += shipX_change
    move_spaceship(shipX, shipY)

    for i in range(nb_enemies):
        # Movements
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 5
            enemyY_change[i] = 80
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 950:
            enemyX_change[i] = -5
            enemyY_change[i] = 80
            enemyY[i] += enemyY_change[i]
        # Collisions
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 630
            is_shot = False
            enemyX[i] = 2000
            enemyY_change[i] = -5
            nb_enemies -= 1
        # Game over condition
        #if enemyY[i] >= shipY:
        #   screen.fill((0, 0, 0))
        #   text = font.render("GAME OVER", True, RED)
        #   screen.blit(text, (400, 300))
        move_enemy(enemyX[i], enemyY[i], i)

    pygame.display.flip()
pygame.quit()
