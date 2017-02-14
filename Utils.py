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
