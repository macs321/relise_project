import pygame
import random 
import time

WIDTH = 1200
HEIGHT = 650
SIZE = (WIDTH, HEIGHT)
FPS = 60

score = 0
cars_pics = ["car3.png","car2.png","car1.png","car0.png"]
bullets = pygame.sprite.Group()
window = pygame.display.set_mode(SIZE)
background = pygame.transform.scale(
    pygame.image.load("IMG_6339.jpg"),
    SIZE)
pygame.display.set_caption("Третій рівень підвалу Порошенка,ти близько до істини. Автора не скажу бо він мене знайде")
clock = pygame.time.Clock()

pygame.font.init()
medium_font = pygame.font.SysFont("Helvetica", 24)
big_font = pygame.font.SysFont("Impact", 35)





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
    def __init__(self, filename, size, coords, speed):
        super().__init__(filename, size, coords, speed)
        self.health = 3

    def update(self):
        keys = pygame.key.get_pressed() 
        if keys[pygame.K_RIGHT]and self.rect.x <= WIDTH - self.rect.width:
            self.rect.x += 10
        if keys[pygame.K_LEFT]and self.rect.x >= 0:
            self.rect.x -= 10
    def update_pictures(self):
        self.image = pygame.transform.scale(pygame.image.load(cars_pics[-1-self.health]), self.rect.size)
    def fire(self):
        new_bullet = Bullet("bazuka.png",
                             (15,20),
                             (self.rect.centerx,self.rect.top),
                             20
                             )
        bullets.add(new_bullet)
        

class ROSHEN(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT :
            self.rect.y = 0
            self.rect.x = random.randint(50,WIDTH-50)
            self.health = random.randint(2,5)

class Wall(GameSprite):
    def __init__(self, filename, size, coords, speed):
        super().__init__(filename, size, coords, speed)
        self.health = random.randint(2,5)
        
    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT or self.health <= 0 :
            self.rect.y = 0
            self.rect.x = random.randint(50,WIDTH-50)
            self.health = random.randint(2,5)
        
            

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed

        if self.rect.bottom < 0:
            self.kill()
    


# class Wall_2(GameSprite):
#     def __init__(self, filename, size, coords, speed):
#         super().__init__(filename, size, coords, speed)
        
#         self.health_2 = 1
#     def update(self):
#         self.rect.y += self.speed

#         if self.rect.top > HEIGHT:
#             self.rect.y = 0
#             self.rect.x = random.randint(50,WIDTH-50)
#             self.health_2 = 1


player = Player("car3.png",(50,70),(HEIGHT//2 + 200,WIDTH//2),10)
walls_grup = pygame.sprite.Group()
wals_num = 3

roshen_grup = pygame.sprite.Group()
roshen_num = 1

# bad_walls_group =pygame.sprite.Group()
# bad_walls_num = 1

for i in range(5):
    wall = Wall("wall.png",(random.randint(100,500),70),(random.randint(0,WIDTH-50),random.choice((0,70,210,140))),10)
    while pygame.sprite.spritecollideany(wall,walls_grup):
        wall = Wall("wall.png",(random.randint(100,500),70),(random.randint(0,WIDTH-50),random.choice((0,70,210,140))),10)
    walls_grup.add(wall)

for i in range(6):
    roshen = ROSHEN("roshen.png",(120,30),(random.randint(0,WIDTH-50),random.choice((0,50,210,140))),10)
    while pygame.sprite.spritecollideany(roshen,roshen_grup):
        roshen = ROSHEN("roshen.png",(120,30),(random.randint(0,WIDTH-50),50),10)
    roshen_grup.add(roshen)



game = True
finish = False
restart = False
start_time = time.time()
cur_time = start_time


while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:

            game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                player.fire()


    if not finish and not restart:
        window.blit(background, (0,0))

        new_time = time.time()


        player.update()
        player.reset(window)
        walls_grup.update()
        walls_grup.draw(window)
        bullets.update()
        bullets.draw(window)
        roshen_grup.update()
        roshen_grup.draw(window)

        take_text = medium_font.render("take roshens " + str(score), True, (255,25,55))
        window.blit(take_text,(WIDTH-400,0))

        health_text = medium_font.render("lives " + str(player.health), True, (255,25,55))
        window.blit(health_text,(WIDTH-100,0))

        time_text = medium_font.render("time " + str(round(new_time - start_time,1)), True, (255,25,55))
        window.blit(time_text,(WIDTH-200,0))      
        
        if pygame.sprite.spritecollide(player,roshen_grup,True):
             score += 1

        if pygame.sprite.spritecollide(player,walls_grup,True):
            player.health -=1
            player.update_pictures()
        if player.health <-0:
            porazka_text = big_font.render("На жаль порошенко знайшов тебе,ти був близько до істини " + str(), True, (255,25,55))
            window.blit(porazka_text,(WIDTH-1050,HEIGHT - 325)) 
            finish = True
        for w  in pygame.sprite.groupcollide(walls_grup,bullets,False,True):
            w.health -=1

        if new_time - start_time >= 20 or score == 5:
            win_text = big_font.render("you won the 3rd level of the basement Poroshenko, my congratulations " + str(), True, (255,25,55))
            window.blit(win_text,(WIDTH-1138,HEIGHT - 325)) 
            finish = True


        # for w in walls_grup:
        #     pygame.draw.rect(window,(255,0,0),w.rect,1)
    if restart:
        pass
    
    pygame.display.update()
    clock.tick(FPS)