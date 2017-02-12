import pygame, math, random, Utils
pygame.init()


class PlayerActive(pygame.sprite.Sprite):
    def __init__(self, color):
        pygame.sprite.Sprite.__init__(self)

        self.color = color
        self.image = pygame.Surface((100, 100))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

        self.rect.x = 500 - self.rect.width/2
        self.rect.y = 300 - self.rect.height/2

        self.speed = 5

        self.isAlive = True
        self.spawnDelay = 0
        self.spawnDelayMax = 25
        self.ammo = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

        self.cooldown = 20
        self.cooldownMax = 20

    def move(self, xdir, ydir):
        self.rect.x += xdir * self.speed
        self.rect.y += ydir * self.speed

    def spawnAmmo(self):
        self.ammo.add(Bullets())

    def moveAmmo(self):
        self.image.fill(self.color)

        for obj in self.ammo:

            if obj.rect.x + obj.rect.width >= self.rect.width:
                obj.xmove *= -1
            elif obj.rect.x <= 0:
                obj.xmove *= -1

            if obj.rect.y + obj.rect.height >= self.rect.height:
                obj.ymove *= -1
            elif obj.rect.y <= 0:
                obj.ymove *= -1

            obj.rect.x += obj.xmove
            obj.rect.y += obj.ymove

            self.image.blit(obj.image, obj.rect)

    def shoot(self, target):
        if self.cooldown <= 0 and self.ammo:
            self.cooldown = self.cooldownMax

            bullet = self.ammo.sprites()[0]
            self.ammo.remove(bullet)

            bullet.rect.x = self.rect.x + self.rect.width/2 - bullet.rect.width/2
            bullet.rect.y = self.rect.y + self.rect.height/2 - bullet.rect.height/2

            bullet.getTarget(target)
            self.bullets.add(bullet)

    def update(self, gameWindow):
        self.cooldown -= 1
        self.spawnDelay -= 1
        if self.spawnDelay <= 0:
            self.spawnAmmo()
            self.spawnDelay = self.spawnDelayMax

        self.moveAmmo()

        if self.isAlive:
            gameWindow.blit(self.image, self.rect)

        self.bullets.update()
        self.bullets.draw(gameWindow)


class Bullets(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = Utils.getFont(size=26, style='bold').render("o", True, Utils.black)
        self.rect = self.image.get_rect()

        self.rect.x = random.randint(0, 100 - self.rect.width)
        self.rect.y = random.randint(0, 100 - self.rect.height)

        self.xmove = random.choice([-1, 1])
        self.ymove = random.choice([-1, 1])

        self.speed = 10

    def getTarget(self, target):
        xdiff = target[0] - self.rect.x - self.rect.width/2
        ydiff = target[1] - self.rect.y - self.rect.height/3

        magnitude = math.sqrt(float(xdiff**2 + ydiff**2))
        numFrames = magnitude / self.speed

        self.xmove = int(xdiff/numFrames)
        self.ymove = int(ydiff/numFrames)

        xtravel = self.xmove * numFrames
        ytravel = self.ymove * numFrames

        self.rect.x += xdiff - xtravel
        self.rect.y += ydiff - ytravel

    def update(self):
        self.rect.x += self.xmove
        self.rect.y += self.ymove
