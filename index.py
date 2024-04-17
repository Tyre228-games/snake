import pygame
import math
from random import randint

pygame.init()


# windows set up
WINDOW_WINDTH = 600
WINDOW_HEIGHT = 600

screen = pygame.display.set_mode((WINDOW_WINDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake")


# constants
SQUARE_SIZE = 30


# snake
class Snake():
    def __init__(self, x, y):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.blocks = [[self.x, self.y], [self.x-SQUARE_SIZE, self.y], [self.x-SQUARE_SIZE*2, self.y]]
        self.direction = "right"

    def draw(self):
        color = (222, 0, 0)
        for x, y in self.blocks:
            pygame.draw.rect(screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))

    def move(self):
        if self.direction == "right":
            self.x += SQUARE_SIZE
        elif self.direction == "left":
            self.x -= SQUARE_SIZE
        elif self.direction == "up":
            self.y -= SQUARE_SIZE
        elif self.direction == "down":
            self.y += SQUARE_SIZE

        self.blocks.insert(0, [self.x, self.y])
        self.blocks.pop(-1)

    def is_collision_with_borders(self):
        if self.x+SQUARE_SIZE > WINDOW_WINDTH or self.y+SQUARE_SIZE > WINDOW_HEIGHT or self.x < 0 or self.y < 0:
            return True
        else:
            return False
        
    def is_collision_with_orange(self, orange_x, orange_y):
        if self.x == orange_x and self.y == orange_y:
            return True
        return False
    
    def is_collision_with_itself(self):
        for i in range(2, len(self.blocks)):
            if self.blocks[i][0] == self.x and self.blocks[i][1] == self.y:
                return True
        return False
    
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.direction = "right"
        self.blocks = [[self.x, self.y], [self.x-SQUARE_SIZE, self.y], [self.x-SQUARE_SIZE*2, self.y]]

    def eat(self):
        if self.direction == "right":
            self.x += SQUARE_SIZE
        elif self.direction == "left":
            self.x -= SQUARE_SIZE
        elif self.direction == "up":
            self.y -= SQUARE_SIZE
        elif self.direction == "down":
            self.y += SQUARE_SIZE
        self.blocks.insert(0, [self.x, self.y])


# Orange
class Orange:
    COLOR = (255, 165, 0)
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def draw(self):
        pygame.draw.rect(screen, self.COLOR, (self.x, self.y, SQUARE_SIZE, SQUARE_SIZE))
    def reset(self, x, y):
        self.x = x
        self.y = y

# functions
def flip_color(color):
    if color == (34, 139, 34):
        return (144, 238, 144)
    else:
        return  (34, 139, 34)


def generate_coordinates_for_orange(snake_blocks):
    orange_x = randint(0, WINDOW_WINDTH)//SQUARE_SIZE*SQUARE_SIZE
    orange_y = randint(0, WINDOW_HEIGHT)//SQUARE_SIZE*SQUARE_SIZE

    for x, y in snake_blocks:
        if orange_x == x and orange_y == y:
            return generate_coordinates_for_orange(snake_blocks)
    return orange_x, orange_y

    
def draw_background():
    color = (34, 139, 34)
    for row in range(0, math.ceil(WINDOW_WINDTH/SQUARE_SIZE)):
        color = flip_color(color)
        for cell in range(0, math.ceil(WINDOW_HEIGHT/SQUARE_SIZE)):
            pygame.draw.rect(screen, color, (cell*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            color = flip_color(color)


# game loop variables
running = True
clock = pygame.time.Clock()
FPS = 60
FONT = pygame.font.Font(None, 36)
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

snake = Snake(210, 210)
orange_x, orange_y = generate_coordinates_for_orange(snake.blocks)
orange = Orange(orange_x, orange_y)
counter = 0
score = 0
snakeDirection = "right"

# game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_a or event.key == pygame.K_LEFT) and snake.direction != "right":
                snakeDirection = "left"
            elif (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and snake.direction != "left":
                snakeDirection = "right"
            elif (event.key == pygame.K_w or event.key == pygame.K_UP) and snake.direction != "down":
                snakeDirection = "up"
            elif (event.key == pygame.K_s or event.key == pygame.K_DOWN) and snake.direction != "up":
                snakeDirection = "down"


    # render
    draw_background()
    snake.draw()
    orange.draw()
    screen.blit(FONT.render(str(score), True, (0, 0, 0)), (10, 10))

    if counter >= 5:
        snake.direction = snakeDirection
        snake.move()
        counter = 0
        if snake.is_collision_with_borders() or snake.is_collision_with_itself():
            # rendering the message
            text = FONT.render("You lost, your score is " + str(score), True, (0, 0, 0))
            screen.blit(text, (WINDOW_WINDTH//2 - text.get_width()//2, WINDOW_HEIGHT//2 - text.get_height()//2))
            pygame.display.flip()
            pygame.time.delay(3000)
            # reseting the game
            snake.reset()
            orange_x, orange_y = generate_coordinates_for_orange(snake.blocks)
            orange.reset(orange_x, orange_y)
            snakeDirection = "right"
            snake.direction = "right"
            score = 0
        elif snake.is_collision_with_orange(orange.x, orange.y):
            snake.eat()
            orange_x, orange_y = generate_coordinates_for_orange(snake.blocks)
            orange.reset(orange_x, orange_y)
            score += 1

    else:
        counter += 1


    
    
    pygame.display.flip()
    clock.tick(FPS)