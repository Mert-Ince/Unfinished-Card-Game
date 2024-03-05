import pygame
import images
import player
import screen
import button
import spritesheet
import draw_text
import fonts
import random
from save import SaveLoadSystem
import battles
import sounds

pygame.init()

window = screen.screen
screen_h = screen.SCREEN_HEIGHT
screen_w = screen.SCREEN_WIDTH

save_load_manager = SaveLoadSystem(".save", "save_data")

screen = screen.screen
pygame.display.set_caption("Sprite Groups"),

cards = pygame.sprite.Group()

def play():
  potion_img = images.potion_img
  end_img = images.end_img
  
  current_fighter = 1
  enemy_list = []
  action_cooldown = 0
  action_wait_time = 80
  potion = False
  potions_effect = 15
  game_over = 0
  paused = False
  
  potion_button = button.Button(window, 100, 900, potion_img, 42, 69)
  restart_img = pygame.image.load('img/icons/play.png').convert_alpha()
  restart_img = spritesheet.SpriteSheet(restart_img)
  restart_img = restart_img.get_image(1, 341, 594, 1, fonts.black)
  restart_button = button.Button(window, 896, 600, restart_img, 170, 297)
  end_button = button.Button(window, 1700, 755, end_img, 133, 92)
  damage_text_group = draw_text.damage_text_group

  starting_deck = ["poisoned_shiv","poisoned_shiv", "poisoned_shiv", "poisoned_shiv", "hearts_burst", "hearts_burst", "hearts_burst", "block", "block", "weaken", "block", "block", "weaken","attack", "attack", "block", "block", "weaken","attack", "attack", "attack_all"]
  current_deck = []
  deck = []
  cards_in_hand = []
  discard = []
  draw_size = 5
  hand_size = draw_size
  hand_sizes = [891, 786, 693, 627, 570, 525, 492, 471, 462, 465]
  round_start = True
  
  potion = False
  target = None
  clock = pygame.time.Clock()
  game_start = True
  clock = pygame.time.Clock()
  FPS = 60

  def check_win(list):
      dead_enemies = 0
      for enemy in list:
       if enemy.alive == False:
          dead_enemies += 1
      if dead_enemies == len(list):
         return True

  class DragOperator:
    def __init__(self, rect, x, y):
        self.rect = rect
        self.dragging = False
        self.rel_pos = (0, 0)
    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.dragging = self.rect.collidepoint(event.pos)
                self.rel_pos = event.pos[0] - self.rect.x, event.pos[1] - self.rect.y
            if event.type == pygame.MOUSEBUTTONUP:
                self.dragging = False
            if event.type == pygame.MOUSEMOTION and self.dragging:
                self.rect.topleft = event.pos[0] - self.rel_pos[0], event.pos[1] - self.rel_pos[1]

  class Card(pygame.sprite.Sprite):
    def __init__(self, name, x, y):
      pygame.sprite.Sprite.__init__(self)
      self.drag_image = images.card_img(name)
      self.image = images.card_img(name)
      self.rect = pygame.Rect(x, y, 135, 210)
      self.drag = DragOperator(self.rect, x, y)
      self.name = name
      self.start_pos = (x + 67, y + 105)
      self.x = x
      self.y = y
      global target
    def update(self, event_list, target, pos):
      global screen_h
      global screen_w    
      self.drag.update(event_list) 
      self.image = self.drag_image if self.drag.dragging else self.image
      for event in event_list:
        if self.rect.collidepoint(pos):
          self.image = images.card_img(self.name)
          self.drag_image = images.card_img(self.name)
        else:
           self.image = images.card_img_sm(self.name)
        if event.type == pygame.MOUSEBUTTONUP: 
          if self.rect.centery < ((2 * screen_h) / 3):
           getattr(player, self.name)(target)
           discard.append(self.name)
           cards_in_hand.remove(self.name)
           self.kill()
          else:
             self.rect.center = self.start_pos

  while True:
    clock.tick(FPS)
    if game_start == True:
      deck.extend(starting_deck)
      random.shuffle(deck)
      random_battle = random.randint(1, 3)
      battle = save_load_manager.load_game_data(["enemies_data"], [f'battle_{random_battle}'])
      save_load_manager.save_data(current_deck,  "current_deck_data")
      save_load_manager.save_game_data([battle], ["enemies_data"])
      enemy_list = getattr(battles, battle)
      player.enemies = enemy_list
      game_start = False

    images.draw_bg()
    
    if paused == True:
      images.draw_menu_bg
  
    screen.blit(images.armor_img, (95, 800))
    pygame.draw.rect(window, fonts.grey, (player.player_x + 115, player.player_y + 400, 150, 15))
    pygame.draw.rect(window, fonts.blood_red, (player.player_x + 115, player.player_y + 400, (player.hp/player.max_hp) * 150, 15))
    draw_text.draw_text(f'{player.hp}/{player.max_hp}', fonts.font, fonts.white, player.player_x + 165, player.player_y + 395)
  
    current_time = pygame.time.get_ticks()
  
    for i in range(len(enemy_list)):
      if current_time - enemy_list[i - 1].last_update >= enemy_list[i - 1].animation_cooldown:
        enemy_list[i - 1].frame += 1
        enemy_list[i - 1].last_update = current_time
        if enemy_list[i - 1].frame >= len(enemy_list[i - 1].animation_list[enemy_list[i - 1].action]):
          if enemy_list[i - 1].action == 3:
            enemy_list[i - 1].frame = len(enemy_list[i - 1].animation_list[enemy_list[i - 1].action]) - 1
          else:
            enemy_list[i - 1].idle()  
      window.blit(enemy_list[i - 1].animation_list[enemy_list[i - 1].action][enemy_list[i - 1].frame], (enemy_list[i - 1].enemy_x, enemy_list[i - 1].enemy_y))
      pygame.draw.rect(window, fonts.grey, (enemy_list[i - 1].enemy_x + 125, enemy_list[i - 1].enemy_y + 400, 150, 15))
      pygame.draw.rect(window, fonts.blood_red, (enemy_list[i - 1].enemy_x + 125, enemy_list[i - 1].enemy_y + 400, (enemy_list[i - 1].hp/enemy_list[i - 1].max_hp) * 150, 15))
      draw_text.draw_text(f'{enemy_list[i - 1].hp}/{enemy_list[i - 1].max_hp}', fonts.font, fonts.white, enemy_list[i - 1].enemy_x + 175, enemy_list[i - 1].enemy_y + 395)
  
    if current_time - player.last_update >= player.animation_cooldown:
      player.frame += 1
      player.last_update = current_time
      if player.frame >= len(player.animation_list[player.action]):
        if player.action == 3:
          player.frame = len(player.animation_list[player.action]) - 1
        else:
          player.idle()
  
    pos = pygame.mouse.get_pos()
  
    cards.draw(screen)
    
    if paused == True:
       images.draw_menu_bg
  
    if potion_button.draw():       
      potion = True
      
    if end_button.draw():
      if check_win(enemy_list):
         game_over = 1
      for i in range(len(cards_in_hand)):
         discard.append(cards_in_hand[i - 1])
      cards.empty()
      current_fighter = 2
  
    for count, enemy in enumerate(enemy_list):
      if enemy.rect.collidepoint(pos):
        #pygame.mouse.set_visible(False)
        #screen.blit(sword_img, pos)
        if enemy.alive == True:
          target = enemy_list[count]
  
    if player.alive == True:
      if current_fighter == 1:
              if round_start == True:
                  cards_in_hand.clear()
                  if len(deck) < draw_size:
                      deck.extend(discard)
                      discard.clear()
                      random.shuffle(deck) 
                  for i in range(draw_size):
                      cards_in_hand.append(deck[0])
                      deck.pop(0)
                  for i in range(hand_size):
                    card_obj = Card(cards_in_hand[i - 1], hand_sizes[hand_size - 1] + ((210 - draw_size * 12) * i), 850)
                    cards.add(card_obj)
                  round_start = False
              if potion == True:
                 if player.potions > 0:
                    if player.max_hp - player.hp > potions_effect:
                       heal_amount = potions_effect
                    else:
                        heal_amount = player.max_hp - player.hp
                        player.hp += heal_amount
                        player.potions -= 1
                        damage_text = draw_text.damage_text(player.rect.centerx, player.rect.y, str(heal_amount), fonts.green)
                        damage_text_group.add(damage_text)
              potion = False
  
    else:
          game_over = -1

    for count, enemy in enumerate(enemy_list):
      if current_fighter == 2 + count:
        if enemy.alive == True:
              action_cooldown += 1
              if action_cooldown >= action_wait_time:
                  if enemy.poison_counter != 0:
                    enemy.hp -= enemy.poison_counter
                    sounds.poison_hit_sfx.play()
                    enemy.hurt()
                    if enemy.hp < 1:
                      enemy.hp = 0
                      enemy.alive = False
                      enemy.dead()
                    damage_text = draw_text.damage_text(enemy.rect.centerx, enemy.rect.y, str(enemy.poison_counter), fonts.dark_green)
                    damage_text_group.add(damage_text)  
                    action = 0
                    frame = 0
                    enemy.poison_counter -= 1
                  enemy_list[current_fighter - 2].attack(player)
                  current_fighter += 1
                  action_cooldown = 0
        else:
           current_fighter += 1
    if current_fighter > len(enemy_list) + 1:
       player.armor = 0
       round_start = True
       current_fighter = 1

    if game_over != 0:
          for enemy in enemy_list:
                 enemy.reset()
          if game_over == 1:
              images.draw_victory()
              if restart_button.draw():
                 map()
          if game_over == -1:
            images.draw_defeat()
            if restart_button.draw():
              save_load_manager.delete_game_data("enemies_data")
              player.reset()  
              deck.clear()
              cards.empty()
              cards_in_hand.clear()
              discard.clear()
              current_fighter = 1
              action_cooldown = 0
              game_over = 0
              game_start = True
              round_start = True
  
    window.blit(player.animation_list[player.action][player.frame], (player.player_x, player.player_y))
    damage_text_group.update()
    damage_text_group.draw(window)
  
    draw_text.draw_text(str(player.potions), fonts.font_2, fonts.blood_red, 150, 920)
    draw_text.draw_text(str(player.armor), fonts.font_2, fonts.grey, 150, 820)
                
    event_list = pygame.event.get()
    for event in event_list:
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          if paused == False:
            paused = True
          else:
            paused = False
          print(paused)
      if event.type == pygame.QUIT:
        run = False
        pygame.quit()
    
    cards.update(event_list, target, pos)
    
    pygame.display.flip()

def map():
   while True:
      screen.fill(fonts.black)
      mouse_pos = pygame.mouse.get_pos()

      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            pygame.quit()
      pygame.display.update()

def main_menu():
   continue_button = button.Button(window, (screen_w / 12), (8 * screen_h / 24), images.continue_img, 133, 207)
   play_button = button.Button(window, (screen_w / 12), (13 * screen_h / 24), images.play_img, 131, 206)
   settings_button = button.Button(window, (screen_w / 12), (18 * screen_h / 24), images.settings_img, 129, 206)
   quit_button = 1
   while True:
      images.draw_menu_bg()
      mouse_pos = pygame.mouse.get_pos()

      if continue_button.draw():
         print("continue")
      if play_button.draw():
         play()
      if settings_button.draw():
         print("settings")
      
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            pygame.quit()
      pygame.display.update()

main_menu()