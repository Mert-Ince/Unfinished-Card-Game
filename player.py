import pygame
import spritesheet
import random
import draw_text
import fonts
import screen

BLACK = (0, 0, 0)

player_x = 100
player_y = ((2 * screen.SCREEN_HEIGHT) / 5)
potion_pool =  []
card_pool = ["lamb_to_the_slaughter", "unnamed_ritual", "unnamed_ritual_2"]
starting_deck = ["attack","attack", "attack", "attack", "block", "block", "block", "block", "block", "attack", "lamb_to_the_slaughter", "unnamed_ritual"]
max_hp = 40
hp = 40
strength = 0
starting_potions = 3
potions = 1
alive = True
starting_armor = 0
armor = starting_armor
draw_size =5
mana = 3

damage_multiplier = 1
dmg_to_bosses_and_elites = 1
lamb = False
sacrifices = 0

enemies = []
items = []

image_x = 128
image_y = 128
image_scale = 3

sprite_sheet_attack = pygame.image.load('img/Vampire_Girl/Attack_1.png').convert_alpha()
sprite_attack = spritesheet.SpriteSheet(sprite_sheet_attack)
sprite_sheet_hurt = pygame.image.load('img/Vampire_Girl/Hurt.png').convert_alpha()
sprite_hurt = spritesheet.SpriteSheet(sprite_sheet_hurt)
sprite_sheet_idle = pygame.image.load('img/Vampire_Girl/Idle.png').convert_alpha()
sprite_idle = spritesheet.SpriteSheet(sprite_sheet_idle)
sprite_sheet_dead = pygame.image.load('img/Vampire_Girl/Dead.png').convert_alpha()
sprite_dead = spritesheet.SpriteSheet(sprite_sheet_dead)

animation_list = []
animation_steps = [5, 2, 5, 10]
action = 2
last_update = pygame.time.get_ticks()
animation_cooldown = 140
frame = 0
step_counter = 0

temp_img_list = []
for i in range(5):
    temp_img_list.append(sprite_attack.get_image(i, image_x, image_y, image_scale, BLACK))
animation_list.append(temp_img_list)

temp_img_list = []
for i in range(2):
    temp_img_list.append(sprite_hurt.get_image(i, image_x, image_y, image_scale, BLACK))
animation_list.append(temp_img_list)

temp_img_list = []
for i in range(5):
    temp_img_list.append(sprite_idle.get_image(i, image_x, image_y, image_scale, BLACK))
animation_list.append(temp_img_list)

temp_img_list = []
for i in range(10):
    temp_img_list.append(sprite_dead.get_image(i, image_x, image_y, image_scale, BLACK))
animation_list.append(temp_img_list)

damage_text_group = draw_text.damage_text_group

def attack_all(target):
    global action
    global frame
    damage = 5 + strength
    for enemy in enemies:
      enemy.hp -= damage
      enemy.hurt()
      if enemy.hp < 1:
        enemy.hp = 0
        enemy.alive = False
        enemy.dead()
      damage_text = draw_text.damage_text(enemy.rect.centerx, enemy.rect.y, str(damage), fonts.blood_red)
      damage_text_group.add(damage_text)  
      action = 0
      frame = 0

def lamb_to_the_slaughter(target):
    global lamb
    global sacrifices
    if lamb == False:
        lamb = True
    elif lamb == True:
        sacrifices += 1

def unnamed_ritual(target):
    global action
    global frame
    global lamb
    global sacrifices
    if lamb == True:
        damage = 13 + strength
        sacrifices += 1
        lamb = False
    else:
        damage = 8 + strength
    target.hp -= damage
    target.hurt()
    if target.hp < 1:
        target.hp = 0
        target.alive = False
        target.dead()
    damage_text = draw_text.damage_text(target.rect.centerx, target.rect.y, str(damage), fonts.blood_red)
    damage_text_group.add(damage_text)
    action = 0
    frame = 0

def unnamed_ritual_2(target):
    global action
    global frame
    damage = 4 + 2 * sacrifices + strength
    target.hp -= damage
    target.hurt()
    if target.hp < 1:
        target.hp = 0
        target.alive = False
        target.dead()
    damage_text = draw_text.damage_text(target.rect.centerx, target.rect.y, str(damage), fonts.blood_red)
    damage_text_group.add(damage_text)
    action = 0
    frame = 0

def attack(target):
    global action
    global frame
    damage = 7 + strength
    target.hp -= damage
    target.hurt()
    if target.hp < 1:
        target.hp = 0
        target.alive = False
        target.dead()
    damage_text = draw_text.damage_text(target.rect.centerx, target.rect.y, str(damage), fonts.blood_red)
    damage_text_group.add(damage_text)
    action = 0
    frame = 0

def weaken(target):
    global action
    global frame
    damage = strength
    target.hp -= damage
    target.weak_counter = 1
    target.hurt()
    if target.hp < 1:
        target.hp = 0
        target.alive = False
        target.dead()
    damage_text = draw_text.damage_text(target.rect.centerx, target.rect.y, str(damage), fonts.blood_red)
    damage_text_group.add(damage_text)
    action = 0
    frame = 0

def poisoned_shiv(target):
    global action
    global frame
    damage = strength + 3
    target.hp -= damage
    target.poison_counter = 3
    target.hurt()
    if target.hp < 1:
        target.hp = 0
        target.alive = False
        target.dead()
    damage_text = draw_text.damage_text(target.rect.centerx, target.rect.y, str(damage), fonts.blood_red)
    damage_text_group.add(damage_text)
    action = 0
    frame = 0

def hearts_burst(target):
    global action
    global frame
    damage = target.poison_counter
    target.hp -= damage
    target.hurt()
    if target.hp < 1:
        target.hp = 0
        target.alive = False
        target.dead()
        for enemy in enemies:
            enemy.poison_counter += target.poison_counter
            enemy.hurt()
    damage_text = draw_text.damage_text(target.rect.centerx, target.rect.y, str(damage), fonts.blood_red)
    damage_text_group.add(damage_text)
    action = 0
    frame = 0
    
def block(target):
    global armor
    armor += 4

def hurt():
    global action
    global frame
    action = 1
    frame = 0

def idle():
    global action
    global frame
    action = 2
    frame = 0

def dead():
    global action
    global frame
    action = 3
    frame = 0

def reset():
    global alive
    global hp
    global frame
    global action
    global update_time
    alive = True
    potions = starting_potions
    hp = max_hp
    frame = 0
    action = 2
    update_time = pygame.time.get_ticks()

rect = pygame.Rect((player_x + 125, player_y + 200), (image_x, image_y * (image_scale/2)))