import pygame
from pygame import mixer
from Player import Player

pygame.init()

#create window
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

#colors
RED = (255,0,0)
YELLOW = (255,255,0)
WHITE = (255,255,255)
BLUE = (0,50,255)

#game varables 
intro_count = 3
last_count_update = pygame.time.get_ticks() 
score = [0,0] #player scores [p1, p2]
round_over = False
ROUND_OVER_COOLDOWN = 2000

WARRIOR_SIZE = 162
WARRIOR_SCALE =4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112,107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE,WIZARD_OFFSET]

#load music and sound effects
pygame.mixer.music.load("Assets/audio/music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)

sword_fx = pygame.mixer.Sound("Assets/audio/sword.wav")
magic_fx = pygame.mixer.Sound("Assets/audio/magic.wav")
sword_fx.set_volume(0.7)
magic_fx.set_volume(0.8)


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("MROK")

#framerate
clock = pygame.time.Clock()
FPS = 60

#image loading
bg_image = pygame.image.load("Assets/background/Sprite-0001.png").convert_alpha()

#load spritesheets
warrior_spritesheet = pygame.image.load("Assets/warrior/Sprites/warrior.png").convert_alpha()
wizard_spritesheet = pygame.image.load("Assets/wizard/Sprites/wizard.png").convert_alpha()

#load victory image
victory_img = pygame.image.load("Assets/icons/victory.png")
#define number of steps in animation
WARRIOR_ANIMATION_STEPS = [10, 8, 1 ,7 ,7 , 3 , 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

#draw font
count_font = pygame.font.Font("Assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("Assets/fonts/turok.ttf", 20)

#function for drawing txt

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))


def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0,0)) 

#function for health bars
def draw_health_bars(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, BLUE, (x - 2, y - 2, 104, 24) )
    pygame.draw.rect(screen, RED, (x, y, 100, 20))
    pygame.draw.rect(screen, YELLOW, (x, y, 100 * ratio, 20))
    


#creating players
player_1 = Player(1,65, 30, False,WARRIOR_DATA, warrior_spritesheet, WARRIOR_ANIMATION_STEPS, sword_fx)
player_2 = Player(2, 390,240, True,WIZARD_DATA, wizard_spritesheet, WIZARD_ANIMATION_STEPS, magic_fx)
#game loop
run = True
while run:

    clock.tick(FPS)
    #draw background
    draw_bg()

    draw_health_bars(player_1.health, 20, 20)
    draw_health_bars(player_2.health, 380, 20)
    draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
    draw_text("P2: " + str(score[1]), score_font, RED, 380, 60)


    #update countdown
    if intro_count <= 0:
        player_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, player_2, round_over)
        player_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, player_1, round_over)
    else:
        #display count
        draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        #update count timer
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks() 

    #update frames
    player_1.update()
    player_2.update()

    player_1.draw(screen)
    player_2.draw(screen)

    #check for defeat
    if round_over == False:
        if player_1.alive == False:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif player_2.alive == False:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
        screen.blit(victory_img, (110, 150))
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = 3
            player_1 = Player(1, 65 , 30, False,WARRIOR_DATA, warrior_spritesheet, WARRIOR_ANIMATION_STEPS, sword_fx)
            player_2 = Player(2, 390,240, True,WIZARD_DATA, wizard_spritesheet, WIZARD_ANIMATION_STEPS, magic_fx)


        


    #for loop for quitting
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    #updating display
    pygame.display.update()

pygame.quit()