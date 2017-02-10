import pygame, random

pygame.init()
gameWindow = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("MN Shooter")
clock = pygame.time.Clock()

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

class Bullets():
    def __init__(self):

        self.image = pygame.font.SysFont("Courier New", 15, 'bold').render("A", True, black)
        self.rect = self.image.get_rect()

        self.rect.x = random.randint(5, 75)
        self.rect.y = random.randint(5, 75)

        self.xmove = random.choice([-1, 1])
        self.ymove = random.choice([-1, 1])

    def travel(self):
        pass


class PlayerActive():
    def __init__(self):

        self.image = pygame.Surface((100, 100))
        self.image.fill(green)
        self.rect = self.image.get_rect()

        self.rect.x = 100
        self.rect.y = 100

        self.speed = 5

        self.ammo = []

    def move(self, xdir, ydir):
        self.rect.x += xdir * self.speed
        self.rect.y += ydir * self.speed

    def spawnAmmo(self):
        self.ammo.append(Bullets())

    def moveAmmo(self):
        self.image.fill(green)

        for obj in self.ammo:

            if obj.rect.x + obj.rect.width >= self.rect.width:
                obj.xmove *= -1
            if obj.rect.y + obj.rect.height >= self.rect.height:
                obj.ymove *= -1
            if obj.rect.x <= 0:
                obj.xmove *= -1
            if obj.rect.y <= 0:
                obj.ymove *= -1

            obj.rect.x += obj.xmove
            obj.rect.y += obj.ymove

            self.image.blit(obj.image, obj.rect)
player = PlayerActive()

spawnDelay = 0
spawnDelayMax = 60

FPS = 60
gameActive = True

while gameActive:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameActive = False

    activeKey = pygame.key.get_pressed();

    if activeKey[pygame.K_RIGHT]:
        player.move(1, 0)
    if activeKey[pygame.K_LEFT]:
        player.move(-1, 0)
    if activeKey[pygame.K_UP]:
        player.move(0, -1)
    if activeKey[pygame.K_DOWN]:
        player.move(0, 1)

    gameWindow.fill(white)
    # Math stuff
    spawnDelay -=1
    if spawnDelay <= 0:
        player.spawnAmmo()
        spawnDelay = spawnDelayMax

    player.moveAmmo()

    # START Draw Stuff
    gameWindow.blit(player.image, player.rect)

    # END Drawing Stuff
    pygame.display.update()
    clock.tick(FPS)


pygame.quit()
quit()
