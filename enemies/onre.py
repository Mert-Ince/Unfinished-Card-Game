import pygame
import spritesheet
import random
import draw_text
import fonts
import screen

BLACK = (0, 0, 0)

enemy_x = 1400
enemy_y = ((2 * screen.SCREEN_HEIGHT) / 5)

max_hp = 20
hp = max_hp
strength = 7
alive = True
weak_counter = 0
poison_counter = 0
bleed_counter = 0
enemy_name = "onre"
image_x = 128
image_y = 128
image_scale = 3

animation_names = ["attack", "hurt", "idle", "dead"]
animations = []

for animation in animation_names:
 sprite = spritesheet.SpriteSheet(pygame.image.load(f'img/enemies/{enemy_name}/{animation}.png').convert_alpha())
 animations.append(sprite)

animation_list = []
animation_steps = [5, 3, 6, 6]
action = 2
last_update = pygame.time.get_ticks()
animation_cooldown = 140
frame = 0
step_counter = 0

for x in range(len(animations)):
    temp_img_list = []
    for i in range(animation_steps[x]):
        temp_img_list.append(animations[x].get_image(i, image_x, image_y, image_scale, BLACK))
    animation_list.append(temp_img_list)
damage_text_group = draw_text.damage_text_group

def attack(target):
    global action
    global frame
    global weak_counter
    rand = random.randint(5, 5)
    if weak_counter != 0:
        damage = int((strength) * 0.75)
        weak_counter -= 1
    else:
        damage = strength
    
    if target.armor > damage:
        target.armor = target.armor - damage
    else: 
        target.hp -= damage - target.armor
    target.hurt()
    if target.hp < 1:
        target.hp = 0
        target.alive = False
        target.dead()
    if target.armor < 1:
        target.armor = 0
    damage_text = draw_text.damage_text(target.rect.centerx, target.rect.y, str(damage), fonts.blood_red)
    damage_text_group.add(damage_text)
    if weak_counter == 0:
        weak = False
    action = 0
    frame = 0
 
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
    hp = max_hp
    frame = 0
    action = 2
    update_time = pygame.time.get_ticks()

rect = pygame.Rect((enemy_x + 155, enemy_y + 200), (image_x, image_y * (image_scale/2)))
