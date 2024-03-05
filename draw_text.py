import pygame
import screen
import fonts

screen = screen.screen

damage_text_group = pygame.sprite.Group()

def draw_text(text , font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

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