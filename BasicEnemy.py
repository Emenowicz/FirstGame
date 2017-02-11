import pygame, Utils, math
pygame.init()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((50,50))
        self.image.fill(Utils.red)
        self.rect = self.image.get_rect()

        self.hp = 3
        self.speed = speed

    def stalkPlayer(self, player):

        xdiff = (player.rect.x + player.rect.width/2) - self.rect.x + self.rect.width / 2
        ydiff = (player.rect.y + player.rect.height/2) - self.rect.y + self.rect.height / 4

        magnitude = math.sqrt(float(xdiff ** 2 + ydiff ** 2))
        numFrames = magnitude / self.speed

        xmove = int(xdiff / numFrames)
        ymove = int(ydiff / numFrames)

        self.rect.x += xmove
        self.rect.y += ymove

    def destroy(self):
        self.kill()

    def getDmg(self):
        self.hp -= 1
        if self.hp <= 0:
            self.destroy()

    def update(self, player):
        self.stalkPlayer(player)

