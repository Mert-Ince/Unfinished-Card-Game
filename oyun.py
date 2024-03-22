import pygame
import images
import player
import screen
import button
import draw_text
import fonts
import random
from save import SaveLoadSystem
import battles
import sounds
import items_and_potions

pygame.init()

window = screen.screen
screen_h = screen.SCREEN_HEIGHT
screen_w = screen.SCREEN_WIDTH

save_load_manager = SaveLoadSystem(".save", "save_data")

screen = screen.screen
pygame.display.set_caption("Sprite Groups"),

cards = pygame.sprite.Group()
tooltip_text_group = draw_text.tooltip_text_group

current_deck = player.starting_deck
deck = current_deck
cards_in_hand = []
discard = []
hand_size = player.draw_size

def combat(enemy_type):
  current_fighter = 1
  enemy_list = []
  action_cooldown = 0
  action_wait_time = 80
  potion = False
  potions_effect = 15
  game_over = 0
  button_pressed = ""
  game_uninteractable = False
  paused = False
  round_ended = False
  card_select = True
  
  potion_button = button.Button(window, 100, 900, images.potion_img, 42, 69)
  restart_button = button.Button_Text(window, 880, 745, "next")
  end_button = button.Button(window, 1700, 755, images.end_img, 133, 92)
  discard_button = button.Button(window, 1700, 1000, images.discard_img, 133, 92)
  draw_deck_button = button.Button(window, 100, 1000, images.draw_deck_img, 133, 92)
  damage_text_group = draw_text.damage_text_group
  
  hand_sizes = [891, 786, 693, 627, 570, 525, 492, 471, 462, 465]
  round_start = True
  
  potion = False
  target = None
  game_start = True
  clock = pygame.time.Clock()
  FPS = 120

  def check_win(list):
      dead_enemies = 0
      for enemy in list:
       if enemy.alive == False:
          dead_enemies += 1
      if dead_enemies == len(list):
         return True
  
  def requires_target(card_name):
    # List of cards that require a target
    cards_requiring_target = ["poisoned_shiv", "hearts_burst", "attack", "weaken", "unnamed_ritual", "unnamed_ritual_2"]

    # Check if the card is in the list
    return card_name in cards_requiring_target

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
      self.drag_image = images.card_img_sm(name)
      self.hover_image = images.card_img(name)
      self.image = images.card_img_sm(name)
      self.rect = pygame.Rect(x, y, 135, 210)
      self.drag = DragOperator(self.rect, x, y)
      self.name = name
      self.start_pos = (x + 67, y + 105)
      self.x = x
      self.y = y
      self.hover_rect = pygame.Rect(self.rect.x - 67, self.rect.y - 430, self.rect.width, self.rect.height)
      self.clicked = False
      global target
    def update(self, event_list, target):
      global screen_h   
      self.drag.update(event_list) 
      if self.rect.collidepoint(pygame.mouse.get_pos()) and self.drag.dragging == False:
        self.image.set_alpha(0)
        screen.blit(self.hover_image, self.hover_rect)
      else:
        self.image = self.drag_image
        self.image.set_alpha(255)
      for event in event_list:
        if event.type == pygame.MOUSEBUTTONUP: 
            global screen_h
            if self.rect.centery < ((2 * screen_h) / 3):
                if target is not None or not requires_target(self.name):
                    getattr(player, self.name)(target)
                    discard.append(self.name)
                    cards_in_hand.remove(self.name)
                    self.kill()
                else:
                    self.rect.center = self.start_pos
            else:
                self.rect.center = self.start_pos
  while True:
    clock.tick(FPS)
    if game_start == True:
      #deck.extend(starting_deck)
      random.shuffle(deck)
      if enemy_type == "normal":
        random_battle = random.randint(1, 3)
        battle = save_load_manager.load_game_data(["enemies_data"], [f'battle_{random_battle}'])
      elif enemy_type == "boss":
        random_battle = random.randint(1, 3)
        battle = save_load_manager.load_game_data(["enemies_data"], [f'boss_battle_{random_battle}'])
      elif enemy_type == "elite":
        random_battle = random.randint(1, 3)
        battle = save_load_manager.load_game_data(["enemies_data"], [f'elite_battle_{random_battle}'])
      elif enemy_type == "0":
        battle = save_load_manager.load_game_data(["enemies_data"], [])
      save_load_manager.save_data(current_deck,  "current_deck_data")
      save_load_manager.save_game_data([battle], ["enemies_data"])
      enemy_list = getattr(battles, battle)
      player.enemies = enemy_list
      game_state = "combat"
      save_load_manager.save_game_data([game_state], ["game_state"])
      game_start = False

    images.draw_bg()
    clock.tick()
    print(clock.get_fps())

    if player.items != []:
        for i in range(len(player.items)):
          item = button.ItemBar(window, 50 + (100 * i), 50, images.get_item(player.items[i]), 64, 64)
          if item.draw():
            if len(tooltip_text_group) <= 1:
             tooltip_text = draw_text.tooltip_text(player.rect.centerx, player.rect.y, items_and_potions.descriptions[player.items[i]], fonts.white)
             tooltip_text_group.add(tooltip_text)

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
      pygame.draw.rect(window, fonts.dark_green, (enemy_list[i - 1].enemy_x + 125, enemy_list[i - 1].enemy_y + 400, (enemy_list[i - 1].hp/enemy_list[i - 1].max_hp) * 150, 15))
      pygame.draw.rect(window, fonts.blood_red, (enemy_list[i - 1].enemy_x + 125, enemy_list[i - 1].enemy_y + 400, ((enemy_list[i - 1].hp - enemy_list[i - 1].poison_counter)/enemy_list[i - 1].max_hp) * 150, 15))
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
      
    window.blit(player.animation_list[player.action][player.frame], (player.player_x, player.player_y))
    draw_text.draw_text(str(player.potions), fonts.font_2, fonts.blood_red, 150, 920)
    draw_text.draw_text(str(player.armor), fonts.font_2, fonts.grey, 150, 820)
  
    if potion_button.draw():  
      if game_uninteractable == False:     
        potion = True
    
    if discard_button.draw():
      if game_uninteractable == False:
        button_pressed = 'discard'
        game_uninteractable = True
        
    if button.deck_button.draw():
     if game_uninteractable == False:       
      button_pressed = 'deck'
      game_uninteractable = True
      
    if draw_deck_button.draw():  
     if game_uninteractable == False:     
      button_pressed = 'deck_draw'
      game_uninteractable = True 
    
    if check_win(enemy_list):
        game_over = 1
      
    if end_button.draw():
     if game_uninteractable == False:
      for i in range(len(cards_in_hand)):
         discard.append(cards_in_hand[i - 1])
      cards.empty()
      current_fighter = 2

    if game_uninteractable:
     if paused == False:
      if button.exit_button.draw():
       game_uninteractable = False
      s = pygame.Surface((screen_w, screen_h))  # the size of your rect
      s.set_alpha(128)                # alpha level
      s.fill((0,0,0))           # this fills the entire surface
      screen.blit(s, (0,0))
      card_count = 0
      if button_pressed == 'discard':
        card_list = discard
      elif button_pressed == 'deck':
        card_list = current_deck
      elif button_pressed == 'deck_draw':
        card_list = deck
      else:
        card_list = []
      for y in range(10):
        for x in range(5):
            if card_count == len(card_list):
                break 
            screen.blit(images.card_img_sm(card_list[card_count]), (200 + (x * 250), 200 + (y * 300)))
            card_count += 1
        if card_count == len(card_list):
            break
     elif paused == True:
      s = pygame.Surface((screen_w, screen_h))  # the size of your rect
      s.set_alpha(256)                # alpha level
      s.fill((0,0,0))           # this fills the entire surface
      screen.blit(s, (0,0))
      if button.continue_button.draw():
        game_uninteractable = False
        paused = False
      if button.menu_button.draw():
        pass
      if button.settings_button.draw():
        pass
      if button.quit_button.draw():
        pygame.quit()
  
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
                  if len(deck) < hand_size:
                      deck.extend(discard)
                      discard.clear()
                      random.shuffle(deck) 
                  for i in range(hand_size):
                      cards_in_hand.append(deck[0])
                      deck.pop(0)
                  for i in range(hand_size):
                    card_obj = Card(cards_in_hand[i - 1], hand_sizes[hand_size - 1] + ((210 - hand_size * 12) * i), 850)
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
                    sounds.get_sound("poison_hit").play()
                    enemy.hurt()
                    if enemy.hp < 1:
                      enemy.hp = 0
                      enemy.alive = False
                      enemy.dead()
                    damage_text = draw_text.poison_text(enemy.rect.centerx, enemy.rect.y, str(enemy.poison_counter), fonts.dark_green)
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
          if game_over == 1:
              card_1 = button.Button(window, 600, 300, images.card_img(player.card_pool[0]), 270, 420)
              card_2 = button.Button(window, 1000, 300, images.card_img(player.card_pool[1]), 270, 420)
              if card_select == True:
                if card_1.draw():
                  player.deck.append(player.card_pool[0])
                  print("here")
                  card_select = False
                if card_2.draw():
                  player.deck.append(player.card_pool[1])
                  card_select = False
              if restart_button.draw():
                 save_load_manager.delete_game_data("enemies_data")
                 cards_in_hand.clear()
                 for enemy in enemy_list:
                  enemy.reset()
                  enemy.weak_counter = 0
                  enemy.poison_counter = 0
                  enemy.bleed_counter = 0
                 deck.clear()
                 cards.empty()
                 discard.clear()
                 current_fighter = 1
                 action_cooldown = 0
                 game_over = 0
                 game_start = True
                 round_start = True
                 if enemy_type == "boss":
                   town()
                 else:
                   map()
          if game_over == -1:
            images.draw_defeat()
            if restart_button.draw():
              save_load_manager.delete_game_data("enemies_data")
              player.reset()  
              cards_in_hand.clear()
              for enemy in enemy_list:
                enemy.reset()
              deck.clear()
              cards.empty()
              discard.clear()
              current_fighter = 1
              action_cooldown = 0
              game_over = 0
              game_start = True
              round_start = True

    damage_text_group.update()
    damage_text_group.draw(window)
    tooltip_text_group.update()
    tooltip_text_group.draw(window)
                
    event_list = pygame.event.get()
    for event in event_list:
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          if paused == False:
            paused = True
            game_uninteractable = True
          else:
            paused = False
            game_uninteractable = False
      if event.type == pygame.QUIT:
        pygame.quit()
    
    if game_uninteractable == False:
      cards.update(event_list, target)
      target = None
    
    pygame.display.flip()

def treasure():
   game_uninteractable = False
   paused = False
   choice = []
   button_pressed = ""
   rng_1 = random.randint(0, len(items_and_potions.items) - 1)
   item_name_1 = items_and_potions.items[rng_1]
   item_1 = button.Button(window, 632, 412, images.get_item(item_name_1), 256, 256)
   choice.append(items_and_potions.items[rng_1])
   items_and_potions.items.pop(rng_1)
   rng_2 = random.randint(0, len(items_and_potions.items) - 1)
   item_name_2 = items_and_potions.items[rng_2]
   item_2 = button.Button(window, 1032, 412, images.get_item(item_name_2), 256, 256)
   choice.append(items_and_potions.items[rng_2])
   items_and_potions.items.pop(rng_2)
   check_save = True

   while True:
      if check_save == True:
        game_state = "treasure"
        save_load_manager.save_game_data([game_state], ["game_state"]) 
        save_load_manager.save_game_data([player.items], ["items_data"])   
        check_save = False
      screen.fill(fonts.black)

      if player.items != []:
        for i in range(len(player.items)):
          item = button.ItemBar(window, 50 + (100 * i), 50, images.get_item(player.items[i]), 64, 64)
          if item.draw():
            if len(tooltip_text_group) <= 1:
             tooltip_text = draw_text.tooltip_text(player.rect.centerx, player.rect.y, items_and_potions.descriptions[player.items[i]], fonts.white)
             tooltip_text_group.add(tooltip_text)

      draw_text.draw_desc(items_and_potions.descriptions[choice[0]], fonts.font_desc, fonts.white, 760, 712)
      draw_text.draw_desc(items_and_potions.descriptions[choice[1]], fonts.font_desc, fonts.white, 1160, 712)

      if item_1.draw():
         getattr(items_and_potions, item_name_1)()
         player.items.append(choice[0])
         items_and_potions.items.append(choice[1])
         choice.clear()
         map()
      if item_2.draw():
         getattr(items_and_potions, item_name_2)()
         player.items.append(choice[1])
         items_and_potions.items.append(choice[0])
         choice.clear()
         map()
      
      tooltip_text_group.update()
      tooltip_text_group.draw(window)

      if button.deck_button.draw():
       if game_uninteractable == False:       
        button_pressed = 'deck'
        game_uninteractable = True

      if game_uninteractable:
       if paused == False:
        if button.exit_button.draw():
          game_uninteractable = False
        s = pygame.Surface((screen_w, screen_h))  # the size of your rect
        s.set_alpha(128)                # alpha level
        s.fill((0,0,0))           # this fills the entire surface
        screen.blit(s, (0,0))
        card_count = 0
        if button_pressed == 'discard':
          card_list = discard
        elif button_pressed == 'deck':
          card_list = current_deck
        elif button_pressed == 'deck_draw':
          card_list = deck
        else:
          card_list = []
        for y in range(10):
          for x in range(5):
              if card_count == len(card_list):
                  break 
              screen.blit(images.card_img_sm(card_list[card_count]), (200 + (x * 250), 200 + (y * 300)))
              card_count += 1
          if card_count == len(card_list):
              break
      elif paused == True:
        s = pygame.Surface((screen_w, screen_h))  # the size of your rect
        s.set_alpha(256)                # alpha level
        s.fill((0,0,0))           # this fills the entire surface
        screen.blit(s, (0,0))
        if button.continue_button.draw():
          game_uninteractable = False
          paused = False
        if button.menu_button.draw():
          pass
        if button.settings_button.draw():
          pass
        if button.quit_button.draw():
          pygame.quit()

      event_list = pygame.event.get()
      for event in event_list:
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            if paused == False:
              paused = True
              game_uninteractable = True
            else:
              paused = False
              game_uninteractable = False
        if event.type == pygame.QUIT:
          pygame.quit()
        pygame.display.update()
      
def situational():
   check_save = True
   game_uninteractable = False
   paused = False
   while True:
      if check_save == True:
        game_state = "situational"
        save_load_manager.save_game_data([game_state], ["game_state"])   
        check_save = False
      if player.items != []:
        for i in range(len(player.items)):
          item = button.ItemBar(window, 50 + (100 * i), 50, images.get_item(player.items[i]), 64, 64)
          if item.draw():
            if len(tooltip_text_group) <= 1:
             tooltip_text = draw_text.tooltip_text(player.rect.centerx, player.rect.y, items_and_potions.descriptions[player.items[i]], fonts.white)
             tooltip_text_group.add(tooltip_text)

      tooltip_text_group.update()
      tooltip_text_group.draw(window)
      event_list = pygame.event.get()
      for event in event_list:
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            if paused == False:
              paused = True
              game_uninteractable = True
            else:
              paused = False
              game_uninteractable = False
        if event.type == pygame.QUIT:
          pygame.quit()
        pygame.display.update()

def map():
   
   NODE_RADIUS = 6
   LINE_WIDTH = 2
   
   game_uninteractable = False
   paused = False
   map_gen = {}
   map_node = []
   map_data = []
   check_save = True
   generate_map = False
   load_map = False 
   save_game = False
   scroll = 0
   scroll_amount = 0
   position = (0, 16)
   
   boss_node = button.Button(window, 832, -120, images.get_icon("boss"), 256, 256)
  
   def draw_path(path, move):
    for i in range(len(path) - 1):
        pygame.draw.line(window, fonts.grey_2, ((path[i][0] * 100) + 660, (path[i][1] * 90) + (190 - move )), ((path[i+1][0] * 100) + 660, (path[i+1][1] * 90) + (190 - move )), LINE_WIDTH)
        pygame.draw.circle(window, fonts.grey_2, ((path[i][0] * 100) + 660, (path[i][1] * 90) + (190 - move )), NODE_RADIUS)
    pygame.draw.circle(window, fonts.grey_2, ((path[-1][0] * 100) + 660, (path[-1][1] * 90) + (190 - move )), NODE_RADIUS)
    pygame.draw.line(window, fonts.grey_2, ((path[-1][0] * 100) + 660, (path[-1][1] * 90) + (190 - move )), (960, 50 - move), LINE_WIDTH)

   def connect_nodes():
    paths = []
    for _ in range(5):  # Repeat 5 times
        current_y = 15
        current_x = random.randint(0, 6)  # Select a random x for y=15
        current_path = [(current_x, current_y)]
        while current_y > 0:  # Until reaching y=0
            current_y -= 1
            # Select a y=14 node from the closest 3 options
            closest_nodes = sorted([(x, y) for x in range(7) for y in range(15) if y == current_y],
                                   key=lambda node: abs(node[0] - current_x))[:3]
            current_x = random.choice(closest_nodes)[0]
            current_path.append((current_x, current_y))
        paths.append(current_path)

    # Remove paths that end at the same y = 14 node and are further from the center
    paths = sorted(paths, key=lambda path: abs(path[-1][0] - 3.5))  # Sort paths by distance from center
    final_paths = [paths[0]]
    for path in paths[1:]:
        if path[-1] != final_paths[-1][-1]:  # If the current path ends at a different node than the last added path
            final_paths.append(path)  # Add the current path to the final paths
    return final_paths

   while True:
      screen.fill(fonts.black)
      if check_save == True:
        map_data = save_load_manager.load_game_data(["map_data"], [[]])
        map_gen = save_load_manager.load_game_data(["map_gen"], [{}])
        paths = save_load_manager.load_game_data(["paths"], [[]])
        position = save_load_manager.load_game_data(["position"], [(0, 16)])
        if map_data == []:
         paths = connect_nodes()
         generate_map = True
         save_game = True
        else:
         load_map = True
        game_state = "map"
        save_load_manager.save_game_data([game_state], ["game_state"])   
        check_save = False

      if player.items != []:
        for i in range(len(player.items)):
          item = button.ItemBar(window, 50 + (100 * i), 50, images.get_item(player.items[i]), 64, 64)
          if item.draw():
            if len(tooltip_text_group) <= 1:
             tooltip_text = draw_text.tooltip_text(player.rect.centerx, player.rect.y, items_and_potions.descriptions[player.items[i]], fonts.white)
             tooltip_text_group.add(tooltip_text)

      if generate_map == True:
       if not map_gen:
        for path in paths:
          draw_path(path, 0)
          for i in range(len(path)):
            seed = random.randint(1, 100)
            map_gen[path[i]] = seed
            if i == 0:
              map_gen[path[i]] = 31

       else:
        for path in paths:
          draw_path(path, 0)

      if load_map == True:
        node_number = 0
        for y in range(16):
          for x in range(7):
            if map_data[node_number] == "combat":
              node = button.Button(window, (x*100) + 620, (y*90) + 150, images.get_icon("combat"), 80, 80)
            elif map_data[node_number] == "treasure":
              node = button.Button(window, (x*100) + 620, (y*90) + 150, images.get_icon("treasure"), 80, 80)
            elif map_data[node_number] == "situational": 
               node = button.Button(window, (x*100) + 620, (y*90) + 150, images.get_icon("situational"), 80, 80)
            elif map_data[node_number] == "empty": 
               node = button.Button(window, (x*100) + 620, (y*90) + 150, images.get_icon("empty"), 80, 80)
            node_number += 1
            map_node.append(node)
        load_map = False

      if generate_map == True:
        for y in range(16):
          for x in range(7):
            if (x, y) in map_gen:
              seed = map_gen[(x, y)]
            else:
              seed = 0
            if seed > 30:
              node = button.Button(window, (x*100) + 620, (y*90) + 150, images.get_icon("combat"), 80, 80)
              data = "combat"
            elif seed > 20:
              node = button.Button(window, (x*100) + 620, (y*90) + 150, images.get_icon("treasure"), 80, 80)
              data = "treasure"
            elif seed >= 1: 
               node = button.Button(window, (x*100) + 620, (y*90) + 150, images.get_icon("situational"), 80, 80)
               data = "situational"
            else:
              node = button.Button(window, (x*100) + 620, (y*90) + 150, images.get_icon("empty"), 80, 80)
              data = "empty"
            map_node.append(node)
            map_data.append(data)
        generate_map = False
      
      if save_game == True:
        save_load_manager.save_game_data([map_data], ["map_data"])
        save_load_manager.save_game_data([map_gen], ["map_gen"])
        save_load_manager.save_game_data([paths], ["paths"])
        save_game = False

      tooltip_text_group.update()
      tooltip_text_group.draw(window)
      scroll_speed = 40

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
        elif event.type == pygame.MOUSEWHEEL:
        # Check if the boss_node is fully visible before scrolling up
          if event.y > 0 and boss_node.rect.y < 0:
            scroll = event.y * scroll_speed
            scroll_amount -= scroll
        # Check if the last node is fully visible before scrolling down
          elif event.y < 0 and map_node[-1].rect.y + map_node[-1].rect.height > window.get_height():
            scroll = event.y * scroll_speed
            scroll_amount -= scroll
      
      boss_node.rect.y += scroll
      if boss_node.draw():
        if position[1] == 0:
         combat("boss")
      
      for path in paths:
          draw_path(path, scroll_amount)

      for i in range(len(map_node)):
        map_node[i].rect.y += scroll
        if position != (0, 16):
          pygame.draw.circle(window, (255, 0, 0), ((position[0]*100) + 660, (position[1]*90) + 190 - scroll_amount), 50, 2)
        if map_node[i].draw():
         if position == (0, 16) and (105 <= i <= 111):
          if map_data[i] == "combat":
            position = ((i % 7), position[1] - 1)
            save_load_manager.save_game_data([position], ["position"])
            combat("normal")
          elif map_data[i] == "treasure":
            position = ((i % 7), position[1] - 1)
            save_load_manager.save_game_data([position], ["position"])
            treasure()
          elif map_data[i] == "situational":
            position = ((i % 7), position[1] - 1)
            save_load_manager.save_game_data([position], ["position"])
            situational()
         else:
           for path in paths:
            if position in path and (i % 7, position[1] - 1) in path and (i//7) + 1 == position[1]:
              if map_data[i] == "combat":
                position = ((i % 7), position[1] - 1)
                save_load_manager.save_game_data([position], ["position"])
                combat("normal")
              elif map_data[i] == "treasure":
                position = ((i % 7), position[1] - 1)
                save_load_manager.save_game_data([position], ["position"])
                treasure()
              elif map_data[i] == "situational":
                position = ((i % 7), position[1] - 1)
                save_load_manager.save_game_data([position], ["position"])
                situational()

      scroll = 0
      event_list = pygame.event.get()
      for event in event_list:
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            if paused == False:
              paused = True
              game_uninteractable = True
            else:
              paused = False
              game_uninteractable = False
        if event.type == pygame.QUIT:
          pygame.quit()

      pygame.display.update()

def town():
  game_uninteractable = False
  paused = False
  check_save = True
  temple_button = button.Button_Text(window, (6 * screen_w / 14), (5 * screen_h / 24), "Temple")
  merchant_button = button.Button_Text(window, (6 * screen_w / 14), (7 * screen_h / 24), "Merchant")
  blacksmith_button = button.Button_Text(window, (6 * screen_w / 14), (9 * screen_h / 24), "Blacksmith")
  witch_button = button.Button_Text(window, (6 * screen_w / 14), (11 * screen_h / 24), "Witch")
  campfire_button = button.Button_Text(window, (6 * screen_w / 14), (13 * screen_h / 24), "Campfire")

  while True:
    if check_save == True:
        game_state = "town"
        save_load_manager.save_game_data([game_state], ["game_state"])   
        check_save = False
    screen.fill(fonts.black)
    if player.items != []:
      for i in range(len(player.items)):
        item = button.ItemBar(window, 50 + (100 * i), 50, images.get_item(player.items[i]), 64, 64)
        if item.draw():
          if len(tooltip_text_group) <= 1:
            tooltip_text = draw_text.tooltip_text(player.rect.centerx, player.rect.y, items_and_potions.descriptions[player.items[i]], fonts.white)
            tooltip_text_group.add(tooltip_text)

    if temple_button.draw():
      if game_uninteractable == False:
       pass
      #temple() this will be where the player can unlock new "knowledges" depending on their devotion on different gods.
      #devotion can be gained either by doing their quests or using the tokens they get from elite fights.
    if merchant_button.draw():
      if game_uninteractable == False:
       pass
      #merchant() this will be where the player can buy items, potion upgrades or cards and remove cards.
    if blacksmith_button.draw():
      if game_uninteractable == False: 
       pass
      #blacksmith() this will be where the player can upgrade their cards.
    if witch_button.draw():
      if game_uninteractable == False:
       pass 
      #witch() this will be where the player can buy potions, remove curses or buy curses.
    if campfire_button.draw():
      if game_uninteractable == False:
       pass
      #campfire() this will be where the player can rest.
      map()

      event_list = pygame.event.get()
      for event in event_list:
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            if paused == False:
              paused = True
              game_uninteractable = True
            else:
              paused = False
              game_uninteractable = False
        if event.type == pygame.QUIT:
          pygame.quit()
    pygame.display.update()

def main_menu():
  continue_button = button.Button_Text(window, (screen_w / 14), (11 * screen_h / 24), "Continue")
  play_button = button.Button_Text(window, (screen_w / 14), (14 * screen_h / 24), "Play")
  settings_button = button.Button_Text(window, (screen_w / 14), (17 * screen_h / 24), "Settings")
  quit_button = button.Button_Text(window, (screen_w / 14), (20 * screen_h / 24), "Quit")
  state_functions = {
  "map": map,
  "combat": combat,
  "treasure": treasure,
  "situational": situational,
  "town": town
  }
  while True:
      images.draw_menu_bg()

      if continue_button.draw():
         game_state = save_load_manager.load_game_data(["game_state"], [])
         player.items = save_load_manager.load_game_data(["items_data"], [])
         if game_state == "combat":
            combat("0")
         elif game_state in state_functions:
          state_functions[game_state]()
      if play_button.draw():
         save_load_manager.delete_all_game_data()
         map()
      if settings_button.draw():
         print("settings")
      if quit_button.draw():
          pygame.quit()

      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            pygame.quit()
      pygame.display.update()

main_menu()