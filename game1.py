# Snake Game using pygame
# by @hchadha28
# Steps involved : 
# 1. Installing Pygame
# 2. Create a blank screen
# 3. Create the food
# 4. Create the snake
# 5. Move the snake
# 6. Make the snake eat the food
# 7. Make the snake grow
# 8. Checking for collisions
# 9. Adding title & frame
# 10. Adding score
# 11. Adding sounds

import pygame, sys, random
from pygame.math import Vector2

#basic setup of game, definitions
pygame.init()

DARK_PURPLE = (48, 25, 52)
MAUVE = (224, 176, 255)

cell_size = 30
number_of_cells = 25

#make a food class, since we will call it again and again 
class Food:
    #constructor of object 
    def __init__(self):
        self.position = self.generate_random_pos()

    def draw(self):
        food_rect = pygame.Rect(self.position.x * cell_size, self.position.y * cell_size, cell_size, cell_size)
        screen.blit(food_surface, food_rect)
    
    def generate_random_pos(self):
        x = random.randint(0, number_of_cells - 1)
        y = random.randint(0, number_of_cells - 1)
        position = Vector2(x, y)
        return position
    
class Snake:
    def __init__(self):
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
    
    def draw(self):
        for segment in self.body:
            segment_rect = (segment.x * cell_size, segment.y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, DARK_PURPLE, segment_rect, 0, 7)
            # 0 means rect filled with color, 7 is border radius 
 
#make screen is as an object
screen = pygame.display.set_mode((number_of_cells * cell_size, number_of_cells * cell_size))
pygame.display.set_caption("Retro Snake")

clock = pygame.time.Clock()

#game loop 3 parts
# 1. event handling
# 2. update positions as per event listeners
# 3. drawing objects in new positions 

food = Food()
snake = Snake()
food_surface = pygame.image.load("food.png")


# GAME LOOP
while True:
    # 1. event handling
    for event in pygame.event.get(): #.event.get() stores all previous events in list
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    

    screen.fill(MAUVE)
    food.draw()
    snake.draw()
    pygame.display.update()
    clock.tick(60)
