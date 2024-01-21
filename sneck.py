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
TOMATO = (255, 81, 87)
CORNFLOWER = (87, 137, 255)

# directions do not touch


class FRUIT:

    def __init__(self):
        self.randomize()

    def draw_fruit(self, screen):

        fruit_rect = pygame.Rect(
            int(self.pos.x * CELL_SIZE), int(self.pos.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)

        pygame.draw.rect(screen, TOMATO, fruit_rect)

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

    def draw_snake(self, screen):

        for block in self.body:

            block_rect = pygame.Rect(
                int(block.x * CELL_SIZE), int(block.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)

            pygame.draw.rect(screen, CORNFLOWER, block_rect)

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


class MAIN:

    def __init__(self):

        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):

        self.snake.move_snake()
        self.check_eat_fruit()
        self.check_collisions()

    def draw_elements(self, screen):
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
    pygame.time.set_timer(SCREEN_UPDATE, 150)

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
