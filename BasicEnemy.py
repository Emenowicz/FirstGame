import pygame, Utils, math, random
pygame.init()

spawnCD = 0
spawnCDMax = 360

def spawn():
    global spawnCD,spawnCDMax
    spawnCD -= 1
    if spawnCD <= 0:
        spawnCD = spawnCDMax
        newEnemy = Enemy()
        Enemy.enemies.add(newEnemy)
        newEnemy.rect.x = random.randrange(-100, -50)
        newEnemy.rect.y = random.randrange(-50, 650)


class Enemy(pygame.sprite.Sprite):

    enemies = pygame.sprite.Group()

    def __init__(self, speed=3):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((50,50))
        self.image.fill(Utils.red)
        self.rect = self.image.get_rect()

        self.maxHP = 5
        self.hp = self.maxHP
        self.speed = speed
        self.cooldown = 60
        self.cooldownMax = 240

        Enemy.enemies.add(self)

        self.hbWidth = 40
        self.hbHeight = 8
        self.hbBase = pygame.Surface((self.hbWidth, self.hbHeight))
        self.drawHB()

    def stalkPlayer(self, player):

        xdiff = (player.rect.center[0]) - self.rect.x - self.rect.width / 2
        ydiff = (player.rect.center[1]) - self.rect.y - self.rect.height / 4

        magnitude = math.sqrt(float(xdiff ** 2 + ydiff ** 2))
        numFrames = magnitude / self.speed

        xmove = int(xdiff / numFrames)
        ymove = int(ydiff / numFrames)

        self.rect.x += xmove
        self.rect.y += ymove

    def drawHB(self):
        width = int((self.hp / self.maxHP) * self.hbWidth)

        hb = pygame.Surface((width, self.hbHeight))
        hb.fill(Utils.green)

        self.hbBase.fill(Utils.red)
        self.hbBase.blit(hb, (0,0))

        self.image.blit(self.hbBase, (5, 38))

    def destroy(self):
        self.kill()
        Utils.ScoreBoard.enemiesKilled += 1

    def getDmg(self):
        self.hp -= 1
        self.drawHB()
        if self.hp <= 0:
            self.destroy()

    def update(self, player):
        self.stalkPlayer(player)

