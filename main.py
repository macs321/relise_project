import pygame
import random 

WIDTH = 1200
HEIGHT = 650
SIZE = (WIDTH, HEIGHT)
FPS = 60
lives = 0
baricada_max_lives = 7


window = pygame.display.set_mode(SIZE)
background = pygame.transform.scale(
    pygame.image.load("IMG_6339.jpg"),
    SIZE)
pygame.display.set_caption("Третій рівень підвалу Порошенка,ти близько до істини. Автора не скажу бо він мене знайде")
clock = pygame.time.Clock()

pygame.font.init()
medium_font = pygame.font.SysFont("Helvetica", 24)
big_font = pygame.font.SysFont("Impact", 50)


pygame.mixer.init()

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, filename:str, size:tuple[int,int], coords: tuple[int,int], speed:int):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(filename), size)
        self.rect = self.image.get_rect(center=coords)
        self.speed = speed

    def reset(self, window:pygame.Surface):
        window.blit(self.image, self.rect)


class Player(GameSprite):
    def update(self):
        keys = pygame.key.get_pressed() 
        if keys[pygame.K_RIGHT]and self.rect.x <= WIDTH - self.rect.width:
            self.rect.x += 10
        if keys[pygame.K_LEFT]and self.rect.x >= 0:
            self.rect.x -= 10

class Wall(GameSprite):
    def __init__(self, filename, size, coords, speed):
        ...
    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.rect.y = 0
            self.rect.x = random.randint(50,WIDTH-50)
 
player = Player("car.png",(50,70),(HEIGHT//2,WIDTH//2),10)
wall = Wall("wall.png",(1000,70),(HEIGHT,random.randint(0,WIDTH-50)),10)
Wall= pygame.sprite.Group()
wals_num = 3

game = True
finish = False
restart = False

while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False


    if not finish and not restart:
        window.blit(background, (0,0))
        player.update()
        player.reset(window)
        wall.update()
        wall.reset(window)

    if restart:
        pass
    
    pygame.display.update()
    clock.tick(FPS)