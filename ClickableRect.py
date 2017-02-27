import pygame, Utils

interact = None

#Clickable Rect

class ClickableRect():
    def __init__(self, pos, size):

        self.rect = pygame.Rect((0, 0), size)
        self.rect.center = pos

        self.hasClicked = False

    def isMouseOver(self):
        pos = pygame.mouse.get_pos()
        return self.rect.left < pos[0] < self.rect.right and self.rect.top < pos[1] < self.rect.bottom

    def doMouseOver(self):
        pass

    def isLeftMouseDown(self):
        return self.hasClicked

    def doLeftMouseDown(self):
        pass

    def isClicked(self):
        global interact
        mouse = pygame.mouse.get_pressed()

        if self.isMouseOver():
            if mouse[0] and self.hasClicked == False and not interact:
                self.hasClicked = True
                interact = self
                return True
            if mouse[0] == False and self.hasClicked == True:
                self.hasClicked = False
                interact = None

            return False

    def doClick(self):
        print("You Clicked a rect")

    def update(self, gw):
        if self.isMouseOver():
            self.doMouseOver()

        if self.isLeftMouseDown():
            self.doLeftMouseDown()

        if self.isClicked():
            self.doClick()


class Button(ClickableRect):
    def __init__(self, pos, size, color, action):
        ClickableRect.__init__(self, pos, size)

        self.color = color
        self.image = pygame.Surface(size)
        self.image.fill(self.color)
        self.action = action

    def doMouseOver(self):
        overlay = pygame.Surface(self.rect.size)
        overlay.set_alpha(120)
        overlay.fill(Utils.black)
        self.image.blit(overlay, (0, 0))

    def doLeftMouseDown(self):
        self.image.fill(Utils.green)

    def doClick(self):
        self.action()

    def draw(self, gw):
        gw.blit(self.image, self.rect)

    def update(self, gw):
        self.image.fill(self.color)

        ClickableRect.update(self.gw)

        self.draw(gw)

class TextButton(Button):
    def __init__(self, pos, size, color, text, action):
        Button.__init__(self, pos, size, color, action)

        self.text = Utils.getFont(size=36, style='bold').render(text, True, Utils.black)

    def draw(self, gw):
        self.image.blit(self.text, (10,10))
        Button.draw(self, gw)