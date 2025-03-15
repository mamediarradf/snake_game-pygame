from typing import Self
import pygame
import random
from sys import exit 
from pygame.math import Vector2

class SNAKE:
    #create a Vector with positions
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0,0)
        self.new_block = False

        self.head_up = pygame.image.load('immagini/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('immagini/head_down.png').convert_alpha()
        self.head_left = pygame.image.load('immagini/head_left.png').convert_alpha()
        self.head_right = pygame.image.load('immagini/head_right.png').convert_alpha()

        self.tail_up = pygame.image.load('immagini/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('immagini/tail_down.png').convert_alpha()
        self.tail_left = pygame.image.load('immagini/tail_left.png').convert_alpha()
        self.tail_right = pygame.image.load('immagini/tail_right.png').convert_alpha()

        self.body_vertical = pygame.image.load('immagini/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('immagini/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('immagini/body_topright.png').convert_alpha()
        self.body_tl = pygame.image.load('immagini/body_topleft.png').convert_alpha()
        self.body_br = pygame.image.load('immagini/body_bottomright.png').convert_alpha()
        self.body_bl = pygame.image.load('immagini/body_bottomleft.png').convert_alpha()

        self.crunck_sound = pygame.mixer.Sound('sound/apple.mp3')

        

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index,block in enumerate(self.body):
            block_rect = pygame.Rect(block.x * cell_size,block.y * cell_size,cell_size,cell_size)
            if index == 0:
                screen.blit(self.head,block_rect)
            elif index == len(self.body)-1:
                screen.blit(self.tail,block_rect)
            else:
                previous_block = self.body[index+1] - block
                next_block = self.body[index-1] - block
                if previous_block.x == next_block.x:
                     screen.blit(self.body_vertical,block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal,block_rect) 
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl,block_rect)

                    elif previous_block.y == -1 and next_block.x == +1 or previous_block.x == +1 and next_block.y == -1:
                        screen.blit(self.body_tr,block_rect)   

                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl,block_rect) 

                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br,block_rect) 

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0):
            self.head = self.head_left
        elif head_relation == Vector2(-1,0):
            self.head = self.head_right
        elif head_relation == Vector2(0,1):
            self.head = self.head_up
        elif head_relation == Vector2(0,-1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1,0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0,1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0,-1):
            self.tail = self.tail_down

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]  
            self.new_block = False  
        else:
            body_copy = self.body[:-1]   

        body_copy.insert(0,(body_copy[0] + self.direction))  
        self.body = body_copy[:]  
    
    def play_crunch(self):
        self.crunck_sound.play()

    def reset(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0,0)

class FRUIT:
    #create an x and y position
    def __init__(self):
        self.randomize()

    #draw square 
    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x * cell_size,self.pos.y * cell_size,cell_size,cell_size)
        screen.blit(apple,fruit_rect)
    
    def randomize(self):
        self.x = random.randint(0,cell_number - 1)
        self.y = random.randint(0,cell_number -1 )
        self.pos = Vector2(self.x,self.y)


class MAIN:

    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake() 
        self.check_collision()
        self.check_fail()
    
    def draw_elements(self):
        self.draw_grass()
        self.draw_score()
        self.fruit.draw_fruit()
        self.snake.draw_snake()



    def check_collision(self):
        #reposition the fruit 
        #add another block to the snake 
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.new_block = True
            self.snake.play_crunch()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.snake.reset()

    def draw_grass(self):
        grass_color = (167,209,61)
        for row in range(cell_number):
            if row % 2 ==0:
                 for col in range(cell_number):
                    if col%2 ==0:
                        grass_rect = pygame.Rect(col*cell_size,row*cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)
            else:
                for col in range(cell_number):
                    if col%2!=0:
                        grass_rect = pygame.Rect(col*cell_size,row*cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body)-3)
        score_surface = game_font.render(score_text,True,(56,74,12))
        score_x= cell_size*cell_number-60
        score_y = cell_size*cell_number-40
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        apple_rect = apple.get_rect(midright = (score_rect.left,score_rect.centery))

        screen.blit(score_surface,score_rect)
        screen.blit(apple,apple_rect)

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
cell_size = 36
cell_number = 18
screen = pygame.display.set_mode((cell_number * cell_size,cell_number * cell_size))
pygame.display.set_caption("My Snake Game ")
clock = pygame.time.Clock()
apple = pygame.image.load('immagini/apple.png').convert_alpha()
game_font = pygame.font.Font(None,25)



#creating a timer foor a event 
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)

main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()   
            exit()

        if event.type == SCREEN_UPDATE:   
            main_game.update()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0,-1)    
            elif event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0,1)    
            elif event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1,0) 
            elif event.key == pygame.K_RIGHT:
                 if main_game.snake.direction.x != -1:
                     main_game.snake.direction = Vector2(1,0) 


    screen.fill((175,215,70))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)        
     