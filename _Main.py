import pygame, Utils, BasicEnemy
from GenericPlayer import PlayerActive,Objective


pygame.init()

class Game():
    def __init__(self):
        self.gameWindow = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption("MN Shooter")
        self.clock = pygame.time.Clock()
        self.FPS = 60

        self.objv = Objective()
        self.scoreBoard = Utils.ScoreBoard()
        self.player = PlayerActive(Utils.green)

        self.enemies = BasicEnemy.Enemy.enemies
        self.enemies.add(BasicEnemy.Enemy())

    def launchMenu(self):
        menu = True
        while menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        menu = False
                print("Intro")

                pygame.display.update()
                self.clock.tick(self.FPS)

    def pause(self):
        pause = True
        text = Utils.getFont(size=96, style="bold").render("Game Paused", True, Utils.black)
        textRect = text.get_rect()
        textRect.center = self.gameWindow.get_rect().center
        while  pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                        print("Game Unpaused")
                        pause = False

                self.gameWindow.blit(text, textRect)

                pygame.display.update()
                self.clock.tick(self.FPS)


    def launchGame(self):
        self.launchMenu()
        gameActive = True
        while gameActive:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameActive = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                        print("Game Paused")
                        self.pause()
            activeKey = pygame.key.get_pressed()

            if activeKey[pygame.K_d]:
                self.player.move(1, 0)
            if activeKey[pygame.K_a]:
                self.player.move(-1, 0)
            if activeKey[pygame.K_w]:
                self.player.move(0, -1)
            if activeKey[pygame.K_s]:
                self.player.move(0, 1)
            if activeKey[pygame.K_SPACE]:
                self.player.doObjective(self.objv)

            mouseClick = pygame.mouse.get_pressed()
            cur = pygame.mouse.get_pos()

            self.gameWindow.fill(Utils.white)

            # Math stuff
            if mouseClick[0]:
                self.player.shoot(cur)

            # Collisions
            playerCollisions = pygame.sprite.spritecollide(self.player, self.enemies, False)
            for enemy in playerCollisions:
                self.player.takeDamage()
                enemy.destroy()

            bulletCollisions = pygame.sprite.groupcollide(self.enemies, self.player.bullets, False, True)
            for enemy in bulletCollisions:
                enemy.getDmg()

            objvCollision = pygame.sprite.spritecollide(self.objv, self.player.bullets, False)
            for bullet in objvCollision:
                tempLetter = self.objv.winMessage[len(self.objv.displayMessage)]
                if tempLetter.upper() == bullet.name:
                    self.objv.displayMessage += tempLetter
                    self.objv.redraw()
                    bullet.destroy()
                    if self.objv.winMessage[len(self.objv.displayMessage)] == " ":
                        self.objv.displayMessage += " "

            # Spawning
            BasicEnemy.spawn()

            # UPDATES
            self.objv.update(self.gameWindow)
            self.scoreBoard.update(self.gameWindow)
            self.player.update(self.gameWindow)

            self.enemies.update(self.player)

            # Drawing
            self.enemies.draw(self.gameWindow)

            # END Drawing Stuff
            pygame.display.update()
            self.clock.tick(self.FPS)

        pygame.quit()
        quit()

game = Game()
game.launchGame()
