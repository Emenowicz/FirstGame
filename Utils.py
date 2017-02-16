import pygame
pygame.init()

# Colors
black = (0, 0, 0)
gray = (180, 180, 180)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


def getFont(name="Courier New", size=20, style='bold'):
    return pygame.font.SysFont(name, size, style)

class ScoreBoard():
    enemiesKilled = 0
    playerAmmo = 0
    playerLifes = 0

    def __init__(self):

        self.image = pygame.Surface((150, 200))
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.x = 800
        self.rect.y = 10

    def drawEnemiesKilled(self):
        text = getFont(size=20).render(("Killed: " + str(ScoreBoard.enemiesKilled)), True, black)
        self.image.blit(text, (5, 10))

    def drawPlayerAmmo(self):
        text = getFont(size=20).render(("Ammo:   " + str(ScoreBoard.playerAmmo)), True, black)
        self.image.blit(text, (5, 30))

    def drawLifes(self):
        text = getFont(size=20).render(("Lifes:  " + str(ScoreBoard.playerLifes)), True, black)
        self.image.blit(text, (5, 50))

    def update(self, gamewindow):
        self.image.fill(white)
        self.drawEnemiesKilled()
        self.drawLifes()
        self.drawPlayerAmmo()

        gamewindow.blit(self.image, self.rect)
