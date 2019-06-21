import pygame
import os
from random import choice

pygame.mixer.pre_init(22050, -16, 2, 1024)
pygame.init()
pygame.mixer.init(22050, -16, 2, 1024)
pygame.display.set_caption("Pong")

white = (255, 255, 255)
black = (0,0,0)
directory = os.getcwd()
collision_sound = directory + "/sounds/ping_pong_8bit_plop.ogg"
point_sound = directory + "/sounds/ping_pong_8bit_beeep.ogg"

class Player(pygame.sprite.Sprite):
	
	def __init__(self, x, key_up, key_down):
		pygame.sprite.Sprite.__init__(self)
		self.surface = pygame.Surface( [10,80] )
		self.surface.fill(white)
		self.rect = self.surface.get_rect()
		self.rect.x = x
		self.rect.y = 260
		self.points = 0
		self.key_up = key_up
		self.key_down = key_down

	def update(self):
		
		if pygame.key.get_pressed()[self.key_down]:
			if self.rect.bottom < 600:
				self.rect.y += 5
			
		if pygame.key.get_pressed()[self.key_up]:
			if self.rect.top > 0:
				self.rect.y -= 5
		
		game.screen.blit(self.surface, (self.rect.x, self.rect.y))


class Ball(pygame.sprite.Sprite):
	
	def __init__(self, direction, speed=2):
		pygame.sprite.Sprite.__init__(self)
		self.surface = pygame.Surface([12,12])
		self.surface.fill(white)
		self.rect = self.surface.get_rect()
		self.rect.x = 400
		self.rect.y = choice([10,590])
		self.direction_x = direction
		self.direction_y = direction
		self.speed = speed
	
	def update(self):
		
		if (self.rect.y >= 600 or self.rect.y <= 0):
			pygame.mixer.music.load(collision_sound)
			pygame.mixer.music.play()
			self.direction_y *= -1
	
		self.rect.y += self.direction_y * self.speed
		self.rect.x += self.direction_x * self.speed
		
		game.screen.blit(self.surface, (self.rect.x, self.rect.y))


class Pong():
	
	def __init__(self):
		self.screen = pygame.display.set_mode((800, 600))
		self.player1 = pygame.sprite.GroupSingle(Player(10, pygame.K_UP, pygame.K_DOWN))
		self.player2 = pygame.sprite.GroupSingle(Player(780, pygame.K_w, pygame.K_s))
		self.ball = pygame.sprite.GroupSingle(Ball( choice([1,-1]) ))
		self.clock = pygame.time.Clock()
		

	def update(self):
		self.screen.fill(black)
		self.player1.update()
		self.player2.update()
		self.ball.update()
		self.show_points()
		self.check_colisions()
		self.check_point()
		pygame.draw.rect(self.screen, white, (400, 0, 3,800))
		pygame.display.update()
	
	def check_colisions(self):
		
		if pygame.sprite.groupcollide(self.player1, self.ball, False, False) or\
		   pygame.sprite.groupcollide(self.player2, self.ball, False, False):
			
				b = self.ball.sprites()[0]
				b.direction_x *= -1
				b.speed += 0.5
				pygame.mixer.music.load(collision_sound)
				pygame.mixer.music.play()
		
	def check_point(self):
	
		ball = self.ball.sprites()[0]
		if ball.rect.x <= 8:
			pygame.mixer.music.load(point_sound)
			pygame.mixer.music.play()
			self.player2.sprites()[0].points += 1
			self.ball.remove()
			self.ball.add(Ball(1))

		if ball.rect.x >= 785:
			pygame.mixer.music.load(point_sound)
			pygame.mixer.music.play()
			self.player1.sprites()[0].points += 1
			self.ball.remove()
			self.ball.add(Ball(-1))
			
	def show_points(self):
		p1_points = str(self.player1.sprites()[0].points)
		p2_points = str(self.player2.sprites()[0].points)
		
		font = pygame.font.Font(directory + '/font/AtariSmall.ttf', 80)		
		text1 = font.render(p1_points, True, white)
		text2 = font.render(p2_points, True, white)
		
		text1_rect = text1.get_rect( center=(200, 50) )
		text2_rect = text2.get_rect( center=(600, 50) )
		self.screen.blit(text1, text1_rect)
		self.screen.blit(text2, text2_rect)
		
	def main(self):
		run = True
		while run:
			for event in pygame.event.get():
				
				if event.type == pygame.QUIT:
					run = False
			
			self.update()
			self.clock.tick(120)

if __name__ == '__main__':
	game = Pong()
	game.main()

