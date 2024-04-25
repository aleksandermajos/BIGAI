import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake Game")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Define game parameters
CELL_SIZE = 20
SNAKE_SPEED = 10

# Initialize the snake
snake_body = [(400, 300), (380, 300), (360, 300)]
snake_direction = "right"

# Initialize the food
food_pos = (random.randint(0, WINDOW_WIDTH // CELL_SIZE - 1) * CELL_SIZE,
            random.randint(0, WINDOW_HEIGHT // CELL_SIZE - 1) * CELL_SIZE)

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and snake_direction != "right":
                snake_direction = "left"
            elif event.key == pygame.K_RIGHT and snake_direction != "left":
                snake_direction = "right"
            elif event.key == pygame.K_UP and snake_direction != "down":
                snake_direction = "up"
            elif event.key == pygame.K_DOWN and snake_direction != "up":
                snake_direction = "down"

    # Move the snake
    new_head = list(snake_body[0])
    if snake_direction == "right":
        new_head[0] += CELL_SIZE
    elif snake_direction == "left":
        new_head[0] -= CELL_SIZE
    elif snake_direction == "up":
        new_head[1] -= CELL_SIZE
    elif snake_direction == "down":
        new_head[1] += CELL_SIZE

    # Check for collision with the game window
    if new_head[0] < 0 or new_head[0] >= WINDOW_WIDTH or new_head[1] < 0 or new_head[1] >= WINDOW_HEIGHT:
        running = False

    # Check for collision with the snake body
    if new_head in snake_body:
        running = False

    # Add the new head to the snake body
    snake_body.insert(0, tuple(new_head))

    # Check for collision with the food
    if new_head[0] == food_pos[0] and new_head[1] == food_pos[1]:
        food_pos = (random.randint(0, WINDOW_WIDTH // CELL_SIZE - 1) * CELL_SIZE,
                    random.randint(0, WINDOW_HEIGHT // CELL_SIZE - 1) * CELL_SIZE)
    else:
        snake_body.pop()

    # Clear the game window
    game_window.fill(BLACK)

    # Draw the snake
    for segment in snake_body:
        pygame.draw.rect(game_window, WHITE, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

    # Draw the food
    pygame.draw.rect(game_window, RED, (food_pos[0], food_pos[1], CELL_SIZE, CELL_SIZE))

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    pygame.time.Clock().tick(SNAKE_SPEED)

# Quit Pygame
pygame.quit()