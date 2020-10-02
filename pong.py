import pygame
import os
from random import choice

pygame.mixer.pre_init(22050, -16, 2, 1024)
pygame.init()
pygame.mixer.init(22050, -16, 2, 1024)
pygame.display.set_caption("Pong")

white = (255, 255, 255)
black = (0, 0, 0)
directory = os.getcwd()
collision_sound = directory + "/sounds/ping_pong_8bit_plop.ogg"
point_sound = directory + "/sounds/ping_pong_8bit_beeep.ogg"
lightTheme = False

class Player(pygame.sprite.Sprite):
    def __init__(self, x, key_up, key_down, isAi, ball=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([10, 80])
        #ADD LIGHT THEME
        
        if lightTheme:
            self.image.fill(black)
        else:
            self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 260
        self.points = 0
        self.key_up = key_up
        self.key_down = key_down
        self.isAi = isAi
        self.ball = ball

    def updateBall(self, newBall):
        self.ball = newBall

    def update(self):
        if self.isAi == False:
            if pygame.key.get_pressed()[self.key_down]:
                if self.rect.bottom < 600:
                    self.rect.y += 5

            if pygame.key.get_pressed()[self.key_up]:
                if self.rect.top > 0:
                    self.rect.y -= 5
        else:
                self.rect.y = self.ball.rect.y
        
        game.screen.blit(self.image, (self.rect.x, self.rect.y))


class Ball(pygame.sprite.Sprite):
    def __init__(self, direction, speed=2):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([12, 12])
        if lightTheme:
            self.image.fill(black)
        else:
            self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = choice([10, 590])
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

        game.screen.blit(self.image, (self.rect.x, self.rect.y))


class Pong():
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.player1 = Player(10, pygame.K_w, pygame.K_s, isAi=False)
        self.ball = Ball(choice([1, -1]))
        self.player2 = Player(780, pygame.K_UP, pygame.K_DOWN, isAi=True, ball=self.ball)
        self.clock = pygame.time.Clock()

    def update(self):
        #ADD LIGHT THEME
        if lightTheme:
            self.screen.fill(white)
        else:
            self.screen.fill(black)
        self.ball.update()
        self.player1.update()
        self.player2.update()
        self.show_points()
        self.check_colisions()
        self.check_point()
        if lightTheme:
            pygame.draw.rect(self.screen, black, (400, 0, 3, 800))
        else:    
            pygame.draw.rect(self.screen, white, (400, 0, 3, 800))
        pygame.display.update()

    def check_colisions(self):

        if pygame.sprite.collide_rect(self.player1, self.ball) or \
                pygame.sprite.collide_rect(self.player2, self.ball):
            pygame.mixer.music.load(collision_sound)
            pygame.mixer.music.play()
            self.ball.direction_x *= -1
            self.ball.speed += 0.5

    def check_point(self):

        if self.ball.rect.left < self.player1.rect.left:
            pygame.mixer.music.load(point_sound)
            pygame.mixer.music.play()
            self.player2.points += 1
            self.ball = Ball(1)

        if self.ball.rect.right > self.player2.rect.right:
            pygame.mixer.music.load(point_sound)
            pygame.mixer.music.play()
            self.player1.points += 1
            self.ball = Ball(-1)

        if self.player1.isAi:
            self.player1.updateBall(self.ball)

        if self.player2.isAi:
            self.player2.updateBall(self.ball)

    def show_points(self):
        p1_points = str(self.player1.points)
        p2_points = str(self.player2.points)

        font = pygame.font.Font(directory + '/font/AtariSmall.ttf', 80)
        if lightTheme:
            text1 = font.render(p1_points, True, black)
            text2 = font.render(p2_points, True, black)
        else:
            text1 = font.render(p1_points, True, white)
            text2 = font.render(p2_points, True, white)

        text1_rect = text1.get_rect(center=(200, 50))
        text2_rect = text2.get_rect(center=(600, 50))
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

    def start(self):
        group = pygame.sprite.Group()
        group.add(Ball(-1))
        group.add(Ball(1))
        global lightTheme
        running = True
        font = pygame.font.Font(directory + '/font/AtariSmall.ttf', 110)
        
        title = font.render("Pong", True, white)    
        title_rect = title.get_rect(center=(400, 200))

        font = pygame.font.Font(directory + '/font/AtariSmall.ttf', 20)
        subtitle = font.render("Press SPACE to start in black theme.", True, white)
        subtitle2 = font.render("Press a to start in white theme", True, white)
        subtitle_rect = subtitle.get_rect(center=(400, 300))
        subtitle2_rect = subtitle2.get_rect(center=(400, 350))    
        while running:
            self.screen.fill(black)
            self.screen.blit(title, title_rect)
            self.screen.blit(subtitle, subtitle_rect)
            self.screen.blit(subtitle2, subtitle2_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if pygame.key.get_pressed()[pygame.K_SPACE]:
                break
            elif pygame.key.get_pressed()[pygame.K_a]:
                
                lightTheme = True
                self.__init__()
                break

            for b in group:
                if (b.rect.x <= 0 or b.rect.x >= 800):
                    b.direction_x *= -1

                if (b.rect.y >= 600 or b.rect.y <= 0):
                    b.direction_y *= -1

                b.rect.y += b.direction_y * b.speed
                b.rect.x += b.direction_x * b.speed
                self.screen.blit(b.image, b.rect)

            pygame.display.update()

        if running:
            
            self.main()
        else:
            pygame.quit()


if __name__ == '__main__':
    game = Pong()
    game.start()
