import pygame, random, math, Utils
from GenericPlayer import PlayerActive
pygame.init()

# Globals
gameWindow = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("MN Shooter")
clock = pygame.time.Clock()
FPS = 60
player = PlayerActive(Utils.green)
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

    # START Draw Stuff
    gameWindow.blit(player.image, player.rect)

    # UPDATES
    player.update(gameWindow)

    # END Drawing Stuff
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
quit()
