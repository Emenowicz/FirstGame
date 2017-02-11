import pygame, Utils
from GenericPlayer import PlayerActive
from BasicEnemy import Enemy

pygame.init()

# Globals
gameWindow = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("MN Shooter")
clock = pygame.time.Clock()
FPS = 60
player = PlayerActive(Utils.green)
enemy1 = Enemy(4)
enemy2 = Enemy(3)

gameActive = True

while gameActive:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameActive = False

    activeKey = pygame.key.get_pressed()

    if activeKey[pygame.K_d]:
        player.move(1, 0)
    if activeKey[pygame.K_a]:
        player.move(-1, 0)
    if activeKey[pygame.K_w]:
        player.move(0, -1)
    if activeKey[pygame.K_s]:
        player.move(0, 1)

    mouseClick = pygame.mouse.get_pressed()
    gameWindow.fill(Utils.white)

    # Math stuff
    if mouseClick[0]:
        player.shoot()

    # UPDATES
    player.update(gameWindow)
    enemy1.update(gameWindow, player)
    enemy2.update(gameWindow, player)

    # END Drawing Stuff
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
quit()
