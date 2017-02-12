import pygame, Utils, BasicEnemy
from GenericPlayer import PlayerActive


pygame.init()

# Globals
gameWindow = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("MN Shooter")
clock = pygame.time.Clock()
FPS = 60

enemies = BasicEnemy.Enemy.enemies

player = PlayerActive(Utils.green)
enemyOrigin = BasicEnemy.Enemy()
enemies.add(enemyOrigin)

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
    cur = pygame.mouse.get_pos()

    gameWindow.fill(Utils.white)

    # Math stuff
    if mouseClick[0]:
        player.shoot(cur)

    # Collisions
    playerCollisions = pygame.sprite.spritecollide(player, enemies, False)
    for enemy in playerCollisions:
        enemy.destroy()

    bulletCollisions = pygame.sprite.groupcollide(enemies, player.bullets, False, True)
    for enemy in bulletCollisions:
        enemy.getDmg()

    # Spawning
    BasicEnemy.spawn()

    # UPDATES
    player.update(gameWindow)

    enemies.update(player)
    enemies.draw(gameWindow)

    # END Drawing Stuff
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
quit()
