import pygame
import screen

pygame.init()

screen = screen.screen

def draw_bg():
    background_img = pygame.image.load('img/Background/background.jpg')
    screen.blit(background_img, (0, 0))

def draw_menu_bg():
    background_img = pygame.image.load('img/Background/menu_bg.jpeg')
    screen.blit(background_img, (0, 0))


def draw_victory():
    victory_img = pygame.image.load('img/icons/victory.png').convert_alpha()
    screen.blit(victory_img, (672, 70))

def draw_defeat():
    defeat_img = pygame.image.load('img/icons/defeat.jpeg').convert_alpha()
    defeat_img = pygame.transform.scale(defeat_img, (600, 600))
    screen.blit(defeat_img, (660, 70))
        
def card_img(card_name):
    card_img = pygame.image.load(f'img/cards/{card_name}.png').convert_alpha()
    card_img = pygame.transform.scale(card_img, (360, 560))
    return card_img

def card_img_sm(card_name):
    card_img = pygame.image.load(f'img/cards/{card_name}.png').convert_alpha()
    card_img = pygame.transform.scale(card_img, (180, 280))
    return card_img

potion_img = pygame.image.load('img/icons/potion2.png').convert_alpha()
end_img = pygame.image.load('img/icons/end.png').convert_alpha()
continue_img = pygame.image.load('img/icons/continue.png').convert_alpha()
play_img = pygame.image.load('img/icons/play.png').convert_alpha()
settings_img = pygame.image.load('img/icons/settings.png').convert_alpha()
armor_img = pygame.image.load('img/icons/armor.png').convert_alpha()
armor_img = pygame.transform.scale(armor_img, (52, 69))