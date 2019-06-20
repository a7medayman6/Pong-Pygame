import pygame
from random import choice

pygame.init()
pygame.display.set_caption("Pong")
white = (255, 255, 255)
black = (0,0,0)

class Pad(pygame.sprite.Sprite):
	
	def __init__(self, x, key_up, key_down):
		pygame.sprite.Sprite.__init__(self)
		self.surface = pygame.Surface( [10,60] )
		self.surface.fill(white)
		self.rect = self.surface.get_rect()
		self.rect.x = x
		self.rect.y = 50
		self.point = 0
		self.key_up = key_up
		self.key_down = key_down

	def update(self):
		
		if pygame.key.get_pressed()[self.key_down]:
			if self.rect.bottom < 598:
				self.rect.y += 2
			
		if pygame.key.get_pressed()[self.key_up]:
			if self.rect.y > 2:
				self.rect.y -= 2
		
		game.screen.blit(self.surface, (self.rect.x, self.rect.y))

class Ball(pygame.sprite.Sprite):
	
	def __init__(self, direction):
		pygame.sprite.Sprite.__init__(self)
		self.surface = pygame.Surface([10,10])
		self.surface.fill(white)
		self.rect = self.surface.get_rect()
		self.rect.x = 400
		self.rect.y = choice([10,590])
		self.direction_x = direction
		self.direction_y = direction
	
	def update(self):
		
		if (self.rect.y >= 600 or self.rect.y <= 0):
			self.direction_y *= -1
		
		if (self.rect.x <= 0 or self.rect.x >= 800):
			self.direction_x *= -1
			
		self.rect.y += self.direction_y
		self.rect.x += self.direction_x
		
		pygame.draw.circle(game.screen, white, (self.rect.x, self.rect.y), 5)
		
class Pong():		
	
	def __init__(self):
		self.screen = pygame.display.set_mode((800, 600))
		self.player1 = Pad(10, pygame.K_UP, pygame.K_DOWN)
		self.player2 = Pad(780, pygame.K_w, pygame.K_s)
		self.ball = Ball( choice([1,-1]) )
		
	def update(self):
		self.screen.fill(black)
		self.player1.update()
		self.player2.update()
		self.ball.update()
		pygame.draw.rect(self.screen, white, (400, 0, 3,800))
		pygame.display.update()
				
	def main(self):
		run = True
		while run:
			for event in pygame.event.get():
				
				if event.type == pygame.QUIT:
					run = False
			
			self.update()

if __name__ == '__main__':
	game = Pong()
	game.main()

