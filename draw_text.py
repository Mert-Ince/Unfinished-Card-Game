import pygame
import screen
import fonts
import images

screen = screen.screen

damage_text_group = pygame.sprite.Group()
tooltip_text_group = pygame.sprite.Group()

def draw_text(text , font, text_col, x, y):
    image = font.render(text, True, text_col)
    screen.blit(image, (x, y))

def draw_desc(text , font, text_col, x, y):
    image = font.render(text, True, text_col)
    text_rect = image.get_rect(center=(x, y))
    screen.blit(image, text_rect)

class damage_text(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = fonts.font_1.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        self.rect.y -= 1
        self.counter += 1
        if self.counter > 80:
            self.kill()

class poison_text(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = fonts.font_1.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        screen.blit(images.poison_img, self.rect)
        self.rect.y -= 1
        self.counter += 1
        if self.counter > 80:
            self.kill()

class tooltip_text(pygame.sprite.Sprite):
    def __init__(self, x, y, desc, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = fonts.font_tooltip.render(desc, True, color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.counter = 0

    def update(self):
        self.counter += 1
        x, y = pygame.mouse.get_pos()
        self.rect.topleft = (x + 10, y + 10)
        if self.counter >= 5:
            self.kill()
