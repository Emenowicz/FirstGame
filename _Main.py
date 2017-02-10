import pygame, random, math

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

# Globals
charList = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z".split()
bullets = []
FPS = 60


def getFont(name="Courier New", size=20, style='bold'):
    return pygame.font.SysFont(name, size, style)


class Bullets:
    def __init__(self):

        self.image = getFont(size=random.randint(20,30)).render(random.choice(charList), True, black)
        self.rect = self.image.get_rect()

        self.rect.x = random.randint(0, 100 - self.rect.width)
        self.rect.y = random.randint(0, 100 - self.rect.height)

        self.xmove = random.choice([-1, 1])
        self.ymove = random.choice([-1, 1])

        self.speed = 10

    def getTarget(self):
        cur = pygame.mouse.get_pos()
        xdiff = cur[0] - self.rect.x - self.rect.width/2
        ydiff = cur[1] - self.rect.y - self.rect.height/4

        magnitude = math.sqrt(float(xdiff**2 + ydiff**2))
        numFrames = int(magnitude / self.speed)

        self.xmove = xdiff/numFrames
        self.ymove = ydiff/numFrames

        xtravel = self.xmove * numFrames
        ytravel = self.ymove * numFrames

        self.rect.x += xdiff - xtravel
        self.rect.y += ydiff - ytravel

    def travel(self):
        self.rect.x += self.xmove
        self.rect.y += self.ymove


class PlayerActive:
    def __init__(self):

        self.image = pygame.Surface((100, 100))
        self.image.fill(green)
        self.rect = self.image.get_rect()

        self.rect.x = 500 - self.rect.width/2
        self.rect.y = 300 - self.rect.height/2

        self.speed = 5

        self.spawnDelay = 0
        self.spawnDelayMax = 25
        self.ammo = []
        self.bullets = []
        self.cooldown = 20
        self.cooldownMax = 20

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
            elif obj.rect.x <= 0:
                obj.xmove *= -1

            if obj.rect.y + obj.rect.height >= self.rect.height:
                obj.ymove *= -1
            elif obj.rect.y <= 0:
                obj.ymove *= -1

            obj.rect.x += obj.xmove
            obj.rect.y += obj.ymove

            self.image.blit(obj.image, obj.rect)

    def shoot(self):
        if self.cooldown <= 0 and self.ammo:
            self.cooldown = self.cooldownMax
            bullet = self.ammo.pop()

            bullet.rect.x = self.rect.x + self.rect.width/2 - bullet.rect.width/2
            bullet.rect.y = self.rect.y + self.rect.height/2 - bullet.rect.height/2

            bullet.getTarget()
            self.bullets.append(bullet)

    def update(self):
        self.cooldown -= 1
        self.spawnDelay -= 1
        if self.spawnDelay <= 0:
            self.spawnAmmo()
            self.spawnDelay = self.spawnDelayMax
        self.moveAmmo()

        # Active in scene
        for obj in self.bullets:
            obj.travel()
            gameWindow.blit(obj.image, obj.rect)

player = PlayerActive()
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
    gameWindow.fill(white)

    # Math stuff
    if mouseClick[0]:
        player.shoot()

    # START Draw Stuff
    gameWindow.blit(player.image, player.rect)

    # UPDATES
    player.update()

    # END Drawing Stuff
    pygame.display.update()
    clock.tick(FPS)


pygame.quit()
quit()
