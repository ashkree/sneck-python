import pygame
import sys
import random
from pygame.math import Vector2


# settings

FPS = 60

# cells
CELL_SIZE = 40
CELL_NUMBER = 20

# window
SCREEN_WIDTH = SCREEN_HEIGHT = CELL_SIZE * CELL_NUMBER

# colours
CONIFER = (175, 215, 70)
CAMO = (127, 153, 66)
TOMATO = (255, 81, 87)
CORNFLOWER = (87, 137, 255)

# directions do not touch


class FRUIT:

    def __init__(self):
        self.randomize()
        self.apple = pygame.image.load('graphics/apple.png').convert_alpha()

    def draw_fruit(self, screen):

        fruit_rect = pygame.Rect(
            int(self.pos.x * CELL_SIZE), int(self.pos.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)

        screen.blit(self.apple, fruit_rect)

    def randomize(self):
        self.x = self.y = random.randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)


class SNAKE:

    UP = Vector2(0, -1)
    DOWN = Vector2(0, 1)
    RIGHT = Vector2(1, 0)
    LEFT = Vector2(-1, 0)

    def __init__(self) -> None:

        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = self.RIGHT
        self.new_block = False
        self.load_graphics()

    def draw_snake(self, screen):

        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):

            x_pos = int(block.x * CELL_SIZE)
            y_pos = int(block.y * CELL_SIZE)

            block_rect = pygame.Rect(
                x_pos, y_pos, CELL_SIZE, CELL_SIZE)

            if index == 0:

                screen.blit(self.head, block_rect)

            elif index == len(self.body) - 1:

                screen.blit(self.tail, block_rect)

            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block

                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if (previous_block.x == -1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x == -1):
                        screen.blit(self.body_tl, block_rect)

                    elif (previous_block.x == -1 and next_block.y == 1) or (previous_block.y == 1 and next_block.x == -1):
                        screen.blit(self.body_bl, block_rect)

                    elif (previous_block.x == 1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x == 1):
                        screen.blit(self.body_tr, block_rect)
                    else:
                        screen.blit(self.body_br, block_rect)

    def move_snake(self):

        if self.new_block:
            body_copy = self.body[:]
        else:
            body_copy = self.body[:-1]

        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy[:]
        self.new_block = False

    def add_block(self):
        self.new_block = True

    def load_graphics(self):

        GRAPHICS = ["head_up", "head_down", "head_right", "head_left",
                    "tail_up", "tail_down", "tail_right", "tail_left",
                    "body_tr", "body_tl", "body_br", "body_bl",
                    "body_horizontal", "body_vertical"]

        for i in range(len(GRAPHICS)):

            name = GRAPHICS[i]
            path = f"graphics/body/{name}.png"

            setattr(self, name, pygame.image.load(
                path).convert_alpha())

    def update_head_graphics(self):

        # relative position of the head in relation to the first piece of the body
        head_position = self.body[0] - self.body[1]

        if head_position == self.RIGHT:
            self.head = self.head_right
        elif head_position == self.LEFT:
            self.head = self.head_left
        elif head_position == self.UP:
            self.head = self.head_up
        else:
            self.head = self.head_down

    def update_tail_graphics(self):

        # relative position of the tail in relation to the body
        tail_position = self.body[-1] - self.body[-2]

        if tail_position == self.RIGHT:
            self.tail = self.tail_right
        elif tail_position == self.LEFT:
            self.tail = self.tail_left
        elif tail_position == self.UP:
            self.tail = self.tail_up
        else:
            self.tail = self.tail_down


class MAIN:

    def __init__(self):

        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):

        self.snake.move_snake()
        self.check_eat_fruit()
        self.check_collisions()

    def draw_elements(self, screen):
        self.draw_grass(screen)
        self.fruit.draw_fruit(screen)
        self.snake.draw_snake(screen)

    def check_eat_fruit(self):

        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()

    def check_collisions(self):

        if not 0 <= self.snake.body[0].x < CELL_NUMBER or not 0 <= self.snake.body[0].y < CELL_NUMBER:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        pygame.quit()
        sys.exit()

    def draw_grass(self, screen):

        for row in range(CELL_NUMBER):

            if row % 2 == 0:

                for col in range(CELL_NUMBER):

                    grass_rect = pygame.Rect(
                        col * CELL_SIZE,
                        row * CELL_SIZE, CELL_SIZE, CELL_SIZE)

                    if (col % 2) == 0:
                        pygame.draw.rect(screen, CAMO, grass_rect)
            else:
                for col in range(CELL_NUMBER):

                    grass_rect = pygame.Rect(
                        col * CELL_SIZE,
                        row * CELL_SIZE, CELL_SIZE, CELL_SIZE)

                    if (col % 2) == 1:
                        pygame.draw.rect(screen, CAMO, grass_rect)


# handlers


def main():

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snek")

    clock = pygame.time.Clock()
    main_game = MAIN()

    snake = main_game.snake

    # event timer, handles when to redraw the snake
    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE, 125)

    while True:

        # Get User Input
        for e in pygame.event.get():

            # end program when quit is clicked
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == SCREEN_UPDATE:
                main_game.update()

            if e.type == pygame.KEYDOWN:

                if (e.key == pygame.K_w or e.key == pygame.K_UP):
                    if snake.direction != snake.DOWN:
                        snake.direction = snake.UP

                if (e.key == pygame.K_s or e.key == pygame.K_DOWN):
                    if snake.direction != snake.UP:
                        snake.direction = snake.DOWN

                if (e.key == pygame.K_a or e.key == pygame.K_LEFT):
                    if snake.direction != snake.RIGHT:
                        snake.direction = snake.LEFT

                if (e.key == pygame.K_d or e.key == pygame.K_RIGHT):
                    if snake.direction != snake.LEFT:
                        snake.direction = snake.RIGHT

        # Draw Elements
        screen.fill(CONIFER)
        main_game.draw_elements(screen)
        pygame.display.update()
        clock.tick(FPS)

    return 0


if __name__ == "__main__":
    main()
