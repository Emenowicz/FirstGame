import pygame, Utils, BasicEnemy
from GenericPlayer import PlayerActive,Objective


pygame.init()

# Globals
gameWindow = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("MN Shooter")
clock = pygame.time.Clock()
FPS = 60

objv = Objective()

player = PlayerActive(Utils.green)

enemies = BasicEnemy.Enemy.enemies
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
    if activeKey[pygame.K_SPACE]:
        player.doObjective(objv)

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

    objvCollision = pygame.sprite.spritecollide(objv, player.bullets, False)
    for bullet in objvCollision:
        tempLetter = objv.winMessage[len(objv.displayMessage)]
        if tempLetter.upper() == bullet.name:
            objv.displayMessage += tempLetter
            objv.redraw()
            bullet.destroy()
            if objv.winMessage[len(objv.displayMessage)] == " ":
                objv.displayMessage += " "

    # Spawning
    BasicEnemy.spawn()

    # UPDATES
    objv.update(gameWindow)

    player.update(gameWindow)

    enemies.update(player)
    enemies.draw(gameWindow)

    # END Drawing Stuff
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
quit()
