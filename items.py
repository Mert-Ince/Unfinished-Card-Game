import pygame
import player

items = ["gauntlet","apple","mortar_pestle","necronomicon"]
descriptions = {
  "gauntlet": "gain 1 strength",
  "apple": "heal for 10",
  "mortar_pestle": "increase max health by 3",
  "necronomicon": "draw 1 more card per turn"
}


def gauntlet():
    player.strength += 1

def apple():
    player.hp += 10
    if player.hp > player.max_hp:
        player.hp = player.max_hp

def mortar_pestle():
    player.max_hp += 3

def necronomicon():
    player.draw_size += 1