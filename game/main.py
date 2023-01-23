import sys, pygame, random
from pygame import mixer
from random import randint


pygame.init()
pygame.font.init()
pygame.mixer.init()
clock = pygame.time.Clock()

MAX_SPEED = 15

WIDTH = 400
HEIGHT = 600  
screen = pygame.display.set_mode((WIDTH, HEIGHT+20))
pygame.display.set_caption("Breads and Birds")

background = pygame.image.load('back.png')
background = pygame.transform.scale(background, (background.get_width()/1.5, background.get_height()/1.28))

sound = True
score = 0
count = 0
font = pygame.font.SysFont('arial', 30, True, True)
mixer.music.load('videoplayback.wav')
mixer.music.play(-1)

bread_img = pygame.image.load('bread.png')
bread_img = pygame.transform.scale(bread_img, (bread_img.get_width()/2, bread_img.get_height()/2))
breads = [bread_img.get_rect() for _ in range(4)]
for bread in breads:
    x = randint(0, WIDTH-bread.width)
    y = randint(0, HEIGHT-bread.height)
    bread.topleft = (x, y)

bird_img = pygame.image.load('bird.png')
bird_img = pygame.transform.scale(bird_img, (bird_img.get_width()/2.5, bird_img.get_height()/2.5))

bar_timer = 0.0

space_just_pressed = False

class Bird:
    speed_x = 4
    speed_y = 0
    rect = bird_img.get_rect()

    def update(self):
        if self.rect.top < 0:
            self.rect.top = 0
            self.speed_y = 0
        elif self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.speed_y = -10

        if self.rect.right >= WIDTH: self.speed_x = -abs(self.speed_x)
        elif self.rect.left <= 0: self.speed_x = abs(self.speed_x)

        self.speed_y += 0.5
        self.speed_y = min(self.speed_y, MAX_SPEED)
        self.rect = self.rect.move(self.speed_x, self.speed_y)

    def draw(self):
        if self.speed_x >= 0:
            bird_img_blit = pygame.transform.rotate(bird_img, -self.speed_y*2)
        else:
            bird_img_blit = pygame.transform.flip(bird_img, True, False)
            bird_img_blit = pygame.transform.rotate(bird_img_blit, self.speed_y*2)

        screen.blit(bird_img_blit, self.rect)

bird = Bird()

def reset():
    global bird
    global bar_timer
    global space_just_pressed
    global score
    global count
    global breads

    bird = Bird()
    bar_timer = 0
    space_just_pressed = False

    score = 0
    count = 0

    for bread in breads:
        x = randint(0, WIDTH-bread.width)
        y = randint(0, HEIGHT-bread.height)
        bread.topleft = (x, y)

def handle_input(keys):
    global space_just_pressed

    if not space_just_pressed and keys[pygame.K_SPACE]:
        space_just_pressed = True
        bird.speed_y = -10

    elif not keys[pygame.K_SPACE]:
        space_just_pressed = False
    
    if keys[pygame.K_m]:
        sound = False


def update_breads(breads):
    global bird
    global count
    global score
    global bar_timer

    for bread in breads:
        if bread.colliderect(bird.rect):
            bread.topleft = (WIDTH+1, HEIGHT+1)
            count += 1
            score += 1
            if sound:
                pick_s = mixer.Sound('pick.wav')
                pick_s.play()        
        if count == 4:
            count = 0
            bar_timer = 0
            for bread in breads:
                x = randint(0, WIDTH-bread.width)
                y = randint(0, HEIGHT-bread.height)
                bread.topleft = (x, y)

def draw():
    screen.blit(background,(0,0))

    for bread in breads:
        screen.blit(bread_img, bread)

    bird.draw()

    screen.blit(font.render(f'Pontos: {score}', True, (255, 255, 255)), (30, 30))
    pygame.draw.rect(screen, (255, 255, 0), (0, HEIGHT, WIDTH-(bar_timer*WIDTH/4), HEIGHT+20))
    pygame.display.flip()

def game():
    global bar_timer
    global breads
    global sound

    reset()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        handle_input(pygame.key.get_pressed())
        bird.update()
        update_breads(breads)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_m]:
            sound = not sound
        if not sound:
            mixer.music.load('videoplayback.wav')
            mixer.music.play(-1)

        bar_timer += 1/60
        if bar_timer >= 4:
            break
        draw()
        clock.tick(60)

    menu()

def menu():
    global sound
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            break
        if keys[pygame.K_m]:
            sound = not sound
        if not sound:
            mixer.music.load('videoplayback.wav')
            mixer.music.play(-1)

        screen.blit(background,(0,0))
        screen.blit(font.render(f'Breads and Birds', True, (255, 255, 255)), (75, 30))
        screen.blit(font.render(f'Espaço para jogar', True, (255, 255, 255)), (70, 250))
        pygame.display.flip()
        clock.tick(60)

    game()

menu()
