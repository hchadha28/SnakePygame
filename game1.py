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

cell_size = 25
number_of_cells = 25

OFFSET = 60
#make a food class, since we will call it again and again 
class Food:
    #constructor of object 
    def __init__(self, snake_body):
        self.position = self.generate_random_pos(snake_body)

    def draw(self):
        food_rect = pygame.Rect(OFFSET + self.position.x * cell_size, OFFSET + self.position.y * cell_size, cell_size, cell_size)
        screen.blit(food_surface, food_rect)
    
    def generate_random_cell(self):
        x = random.randint(0, number_of_cells - 1)
        y = random.randint(0, number_of_cells - 1)
        return Vector2(x, y)

    def generate_random_pos(self, snake_body):
        position = self.generate_random_cell()
        while position in snake_body: 
            position = self.generate_random_cell()   
        return position  
    
    # quirk 
    def generate_food_near_head(self, snake_body):
        head = snake_body[0]

        # Try in x-direction first
        candidate = Vector2(head.x + 1, head.y)
        if self.is_valid(candidate, snake_body):
            return candidate

        # If blocked, try left
        candidate = Vector2(head.x - 1, head.y)
        if self.is_valid(candidate, snake_body):
            return candidate

        # Then try below
        candidate = Vector2(head.x, head.y + 1)
        if self.is_valid(candidate, snake_body):
            return candidate

        # Then try above
        candidate = Vector2(head.x, head.y - 1)
        if self.is_valid(candidate, snake_body):
            return candidate

        # If nothing valid, fall back to random
        return self.generate_random_pos(snake_body)

    def is_valid(self, pos, snake_body):
        return (
            0 <= pos.x < number_of_cells
            and 0 <= pos.y < number_of_cells
            and pos not in snake_body
        )
#make a snake class, since we will call it again and again 
class Snake:
    def __init__(self):
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direction = Vector2(1, 0)
        self.add_segment = False

    def draw(self):
        for segment in self.body:
            segment_rect = (OFFSET + segment.x * cell_size, OFFSET + segment.y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, DARK_PURPLE, segment_rect, 0, 7)
            # 0 means rect filled with color, 7 is border radius 
    
    def update(self):
        self.body.insert(0, self.body[0] + self.direction)
        if self.add_segment == True:
            self.add_segment = False
        else:
            self.body = self.body[:-1] # selecting all elements from beginning to second last element, so we remove the last segment 
        
    def reset(self):
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direction = Vector2(1, 0)
    
#make a class that calls Snake and Food class
class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.state = "RUNNING"
    
    def draw(self):
        self.food.draw()
        self.snake.draw()
    
    def update(self):
        if self.state == "RUNNING":
            self.snake.update()
            self.check_collision_with_food()
            self.check_collision_with_walls()
            self.check_collision_with_tail()

    def check_collision_with_food(self):
        if self.snake.body[0] == self.food.position:
            self.food.position = self.food.generate_random_pos(self.snake.body) 
            self.snake.add_segment = True
    
    def check_collision_with_walls(self):
        if self.snake.body[0].x == -1 or self.snake.body[0].x == number_of_cells or self.snake.body[0].y == -1 or self.snake.body[0].y == number_of_cells:
            self.game_over()

    def check_collision_with_tail(self):
        headless_body = self.snake.body[1:]
        if self.snake.body[0] in headless_body:
            self.game_over()
    
    def game_over(self):
        self.snake.reset()
        self.food.position = self.food.generate_random_pos(self.snake.body)
        self.state = "STOPPED"

#make screen is as an object
screen = pygame.display.set_mode((2*OFFSET + number_of_cells * cell_size, 2*OFFSET + number_of_cells * cell_size))
pygame.display.set_caption("Retro Snake")

clock = pygame.time.Clock()

#game loop 3 parts
# 1. event handling
# 2. update positions as per event listeners
# 3. drawing objects in new positions 

game = Game()
food_surface = pygame.image.load("food.png")

SNAKE_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_UPDATE, 200) # invoked every 200ms 

# GAME LOOP
while True:
    # 1. event handling
    for event in pygame.event.get(): #.event.get() stores all previous events in list
        if event.type == SNAKE_UPDATE:
            game.update()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if game.state == "STOPPED": 
                game.state = "RUNNING"
            if event.key == pygame.K_UP and game.snake.direction != Vector2(0, 1):
                game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN and game.snake.direction != Vector2(0, -1):
                game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT and game.snake.direction != Vector2(1, 0):
                game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT and game.snake.direction != Vector2(-1, 0):
                game.snake.direction = Vector2(1, 0)
    # if we place the snake.update() here then the update will be called 60 times per second
    # therefore we declare a user event invoked every 200ms and it is stored inside .event.get()

    #Drawing 
    screen.fill(MAUVE)
    pygame.draw.rect(screen, DARK_PURPLE, 
                     (OFFSET - 5, OFFSET - 5, cell_size*number_of_cells + 10, cell_size*number_of_cells + 10), 5)
    game.draw()
    pygame.display.update()
    clock.tick(60)
