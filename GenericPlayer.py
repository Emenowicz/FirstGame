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
        self.lives = 2
        self.spawnDelay = 0
        self.spawnDelayMax = 25
        self.ammo = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

        self.cooldown = 20
        self.cooldownMax = 20

        self.objvCounter = 0
        self.objvCounterMax = 30

    def move(self, xdir, ydir):
        self.rect.x += xdir * self.speed
        self.rect.y += ydir * self.speed

    def spawnAmmo(self):
        if len(self.ammo) < 10:
            self.ammo.add(Bullets())
            Utils.ScoreBoard.playerAmmo = len(self.ammo)

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

    def doObjective(self, objv):

        if self.objvCounter < -30:
            objv.charPos = len(objv.displayMessage)

        if self.objvCounter <= 0 and objv.displayMessage != objv.winMessage:
            self.objvCounter = self.objvCounterMax
            tempLetter = objv.winMessage[objv.charPos]
            if tempLetter == " ":
                objv.charPos += 1
                return
            for shot in self.ammo:
                if shot.name == tempLetter.upper():
                    self.ammo.remove(shot)
                    shot.rect.x = self.rect.x + 25
                    shot.rect.y = self.rect.y + 25
                    shot.getTarget((objv.rect.x + objv.rect.width/2, objv.rect.y + objv.rect.height/2))
                    self.bullets.add(shot)
                    objv.charPos += 1
                    return

    def takeDamage(self):
        self.lives -= 1

        if self.lives <= 0:
            self.destroy()

    def destroy(self):
        self.isAlive = False

    def update(self, gameWindow):
        if self.lives >= 0:
            Utils.ScoreBoard.playerLifes = self.lives
        if self.isAlive:
            self.cooldown -= 1
            self.spawnDelay -= 1
            if self.spawnDelay <= 0:
                self.spawnAmmo()
                self.spawnDelay = self.spawnDelayMax

            self.moveAmmo()

            gameWindow.blit(self.image, self.rect)

            self.bullets.update()
            self.bullets.draw(gameWindow)

            self.objvCounter -= 1

#charList = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z".split()
charList = "I F T H I S I S S P E L L E D T H E N Y O U W I N ".split()

class Bullets(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.name = random.choice(charList)
        self.image = Utils.getFont(size=26, style='bold').render(self.name, True, Utils.black)
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

    def checkDist(self):
        if self.rect.x < -100 or self.rect.x>1100 or self.rect.y < -100 or self.rect.y > 700:
            self.destroy()

    def destroy(self):
        self.kill()

    def update(self):
        self.rect.x += self.xmove
        self.rect.y += self.ymove
        self.checkDist()

class Objective():
    def __init__(self):
        self.winMessage = "If this is spelled then you WIN!"
        self.displayMessage = ""
        self.charPos = 0
        self.image = pygame.Surface((800, 100))
        self.redraw()

    def redraw(self):
        self.image.fill(Utils.green)

        self.ghostText = Utils.getFont(size=20).render(self.winMessage, True, Utils.gray)
        self.image.blit(self.ghostText, (25, 25))

        self.text = Utils.getFont(size=20).render(self.displayMessage, True, Utils.black)
        self.image.blit(self.text, (25, 25))
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 450

    def update(self, gamewindow):
        gamewindow.blit(self.image, self.rect)