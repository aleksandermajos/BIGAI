import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 640, 480
BLOCK_SIZE = 20
FPS = 10

# Set up some colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set up the font
font = pygame.font.Font(None, 36)

class SnakeGame:
    def __init__(self):
        self.snake = [(200, 200), (220, 200), (240, 200)]
        self.direction = 'RIGHT'
        self.apple = self.set_new_apple()

    def set_new_apple(self):
        while True:
            x = random.randint(0, WIDTH - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE
            y = random.randint(0, HEIGHT - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE
            if (x, y) not in self.snake:
                return (x, y)

    def update(self):
        head = self.snake[-1]
        if self.direction == 'RIGHT':
            new_head = (head[0] + BLOCK_SIZE, head[1])
        elif self.direction == 'LEFT':
            new_head = (head[0] - BLOCK_SIZE, head[1])
        elif self.direction == 'UP':
            new_head = (head[0], head[1] - BLOCK_SIZE)
        elif self.direction == 'DOWN':
            new_head = (head[0], head[1] + BLOCK_SIZE)

        self.snake.append(new_head)
        if self.snake[-1] == self.apple:
            self.apple = self.set_new_apple()
        else:
            self.snake.pop(0)

        if (self.snake[-1][0] < 0 or self.snake[-1][0] >= WIDTH or
                self.snake[-1][1] < 0 or self.snake[-1][1] >= HEIGHT or
                self.snake[-1] in self.snake[:-1]):
            pygame.quit()
            sys.exit()

    def draw(self):
        screen.fill(WHITE)
        for x, y in self.snake:
            pygame.draw.rect(screen, GREEN, (x, y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(screen, RED, (*self.apple, BLOCK_SIZE, BLOCK_SIZE))
        text = font.render(f'Score: {len(self.snake)}', True, (0, 0, 0))
        screen.blit(text, (10, 10))
        pygame.display.flip()

def main():
    clock = pygame.time.Clock()
    game = SnakeGame()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and game.direction != 'DOWN':
                    game.direction = 'UP'
                elif event.key == pygame.K_DOWN and game.direction != 'UP':
                    game.direction = 'DOWN'
                elif event.key == pygame.K_LEFT and game.direction != 'RIGHT':
                    game.direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and game.direction != 'LEFT':
                    game.direction = 'RIGHT'

        game.update()
        game.draw()
        clock.tick(FPS)

if __name__ == '__main__':
    main()
