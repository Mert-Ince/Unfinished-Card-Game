import pygame 
import fonts
import images
import screen

window = screen.screen
screen_h = screen.SCREEN_HEIGHT
screen_w = screen.SCREEN_WIDTH

class Button():
	def __init__(self, surface, x, y, image, size_x, size_y):
		self.image = pygame.transform.scale(image, (size_x, size_y))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False
		self.surface = surface

	def draw(self):
		action = False

		pos = pygame.mouse.get_pos()

		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
		
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 0 and self.clicked == True:
				action = True
				self.clicked = False

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		self.surface.blit(self.image, (self.rect.x, self.rect.y))

		return action

class Button_Text():
	def __init__(self, surface, x, y, name):
		self.name = name
		self.image = images.get_text_img(name, fonts.white)
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False
		self.surface = surface

	def draw(self):
		action = False

		pos = pygame.mouse.get_pos()

		if self.rect.collidepoint(pos):
			self.image = images.get_text_img(self.name, fonts.blood_red)
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
		else:
			self.image = images.get_text_img(self.name, fonts.white)

		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 0 and self.clicked == True:
				action = True
				self.clicked = False

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		self.surface.blit(self.image, (self.rect.x, self.rect.y))

		return action

class Pause_Button_Text():
	def __init__(self, surface, x, y, name):
		self.name = name
		self.image = images.get_text_img(name, fonts.white)
		self.rect = self.image.get_rect()
		self.rect.center = ((screen.SCREEN_WIDTH/2), y)
		self.clicked = False
		self.surface = surface

	def draw(self):
		action = False

		pos = pygame.mouse.get_pos()

		if self.rect.collidepoint(pos):
			self.image = images.get_text_img(self.name, fonts.blood_red)
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
		else:
			self.image = images.get_text_img(self.name, fonts.white)

		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 0 and self.clicked == True:
				action = True
				self.clicked = False

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		self.surface.blit(self.image, (self.rect.x, self.rect.y))

		return action
	
class ItemBar():
	def __init__(self, surface, x, y, image, size_x, size_y):
		self.image = pygame.transform.scale(image, (size_x, size_y))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.surface = surface

	def draw(self):
		action = False
		pos = pygame.mouse.get_pos()

		if self.rect.collidepoint(pos):
			action = True

		self.surface.blit(self.image, (self.rect.x, self.rect.y))

		return action

continue_button = Pause_Button_Text(window, (6 * screen_w / 14), (5 * screen_h / 24), "Continue")
menu_button = Pause_Button_Text(window, (6 * screen_w / 14), (8 * screen_h / 24), "Main Menu")
settings_button = Pause_Button_Text(window, (6 * screen_w / 14), (11 * screen_h / 24), "Settings")
quit_button = Pause_Button_Text(window, (6 * screen_w / 14), (14 * screen_h / 24), "Quit")
select_button = Pause_Button_Text(window, (6 * screen_w / 14), (20 * screen_h / 24), "Select")
deck_button = Button(window, 1700, 0, images.deck_img, 133, 92)
exit_button = Button(window, 1700, 200, images.exit_img, 50, 50)