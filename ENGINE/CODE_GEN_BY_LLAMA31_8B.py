import pygame
import sys
import time
import random

# Game Variables
screen_width = 800
screen_height = 600
block_size = 20
bg_color = (0, 0, 0)
snake_block_color = (0, 255, 0)
food_block_color = (255, 0, 0)

class SnakeGame:
    def __init__(self):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.block_size = block_size
        self.bg_color = bg_color
        self.snake_block_color = snake_block_color
        self.food_block_color = food_block_color

        pygame.init()
        self.display = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()

    def draw_snake(self, snake_list):
        for i in range(len(snake_list)):
            if snake_list[i] == 1:
                pygame.draw.rect(self.display, self.snake_block_color, [i * self.block_size, 0, self.block_size,
self.block_size])
            elif snake_list[i] == -1:
                pygame.draw.rect(self.display, self.snake_block_color, [(len(snake_list) - i - 1) *
self.block_size, screen_height - self.block_size, self.block_size, self.block_size])

    def draw_food(self, food_pos):
        for pos in food_pos:
            pygame.draw.rect(self.display, self.food_block_color, [pos[0] * self.block_size, pos[1] *
self.block_size, self.block_size, self.block_size])

    def run_game(self):
        snake_list = [1, 1, 1, 1]
        x = len(snake_list) // 2
        y = screen_height // 2

        snake_pos = [(x - i) * block_size for i in range(len(snake_list))]
        food_pos = [[random.randint(0, self.screen_width // block_size - 1), random.randint(0, self.screen_height
// block_size - 1)] for _ in range(10)]

        score = 0

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and y > 0:
                y -= block_size
            elif keys[pygame.K_DOWN] and y < screen_height - block_size:
                y += block_size
            elif keys[pygame.K_LEFT] and x > 0:
                x -= block_size
            elif keys[pygame.K_RIGHT] and x < self.screen_width - block_size:
                x += block_size

            snake_list.pop(0)
            if (x // block_size, y // block_size) not in food_pos:
                snake_list.append(-1)
                score -= 1
            else:
                snake_list.append(1)
                snake_pos.append((x // block_size, y // block_size))
                x = len(snake_list) // 2 * self.block_size
                y = screen_height // 2 * self.block_size

            food_pos.pop(random.randint(0, len(food_pos) - 1))

            if (len(snake_list) > len(snake_pos) or snake_list[-1] == -1):
                while (snake_list[-1] != -1):
                    snake_list.pop(-1)
                    score -= 1
                x = y = screen_height // 2

            self.display.fill(self.bg_color)
            self.draw_snake(snake_list)
            self.draw_food(food_pos)
            pygame.display.flip()
            self.clock.tick(5)

if __name__ == "__main__":
    game = SnakeGame()
    game.run_game()
