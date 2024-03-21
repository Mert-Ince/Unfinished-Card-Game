import pygame

pygame.init

volume = 0.5

def get_sound(name):
    global volume
    path = "sounds/" + name + ".mp3"
    sound = pygame.mixer.Sound(path)
    sound.set_volume(volume)
    return sound