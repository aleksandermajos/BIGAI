import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
BALL_RADIUS = 20
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up display
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arkanoid")


class Ball:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - BALL_RADIUS * 2
        self.speed_x = 5
        self.speed_y = -5

    def move(self):
        if self.x < BALL_RADIUS or self.x > WIDTH - BALL_RADIUS:
            self.speed_x *= -1
        if self.y < BALL_RADIUS:
            self.speed_y *= -1
        self.x += self.speed_x
        self.y += self.speed_y


class Paddle:
    def __init__(self):
        self.x = (WIDTH - PADDLE_WIDTH) // 2
        self.y = HEIGHT - PADDLE_HEIGHT - 20

    def move(self, direction):
        if direction == 'left' and self.x > 0:
            self.x -= 8
        elif direction == 'right' and self.x < WIDTH - PADDLE_WIDTH:
            self.x += 8


def create_bricks():
    brick_width = 80
    brick_height = 30
    bricks = []
    for i in range(5):
        row = []
        for j in range(10):
            x = 50 + j * (brick_width + 5)
            y = 50 + i * (brick_height + 5)
            row.append((x, y))
        bricks.append(row)
    return bricks


def draw_bricks(bricks):
    brick_width = 80
    brick_height = 30
    for row in bricks:
        for brick in row:
            pygame.draw.rect(SCREEN, WHITE, (brick[0], brick[1], brick_width, brick_height), 2)


def main():
    clock = pygame.time.Clock()
    paddle = Paddle()
    ball = Ball()
    bricks = create_bricks()

    # Sound effects
    hit_paddle = pygame.mixer.Sound('hit_paddle.wav')
    hit_brick = pygame.mixer.Sound('hit_brick.wav')

    score = 0
    lives = 3

    font = pygame.font.Font(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move('left')
        if keys[pygame.K_RIGHT]:
            paddle.move('right')

        SCREEN.fill(BLACK)

        # Move ball
        ball.move()
        draw_bricks(bricks)

        # Check collision with paddle
        if (ball.y + BALL_RADIUS > paddle.y and
                ball.x > paddle.x and
                ball.x < paddle.x + PADDLE_WIDTH):
            ball.speed_y *= -1
            hit_paddle.play()

        # Check for brick collisions
        for i in range(len(bricks)):
            for j in range(len(bricks[i])):
                x, y = bricks[i][j]
                if (ball.x > x and
                        ball.x < x + 80 and
                        ball.y > y and
                        ball.y < y + 30):
                    ball.speed_y *= -1
                    hit_brick.play()
                    del bricks[i][j]
                    score += 10

        # Check game over condition
        if ball.y > HEIGHT:
            lives -= 1
            if lives == 0:
                print("Game Over! Final Score:", score)
                pygame.quit()
                sys.exit()
            else:
                ball.x = WIDTH // 2
                ball.y = HEIGHT - BALL_RADIUS * 2

        # Draw elements
        pygame.draw.circle(SCREEN, WHITE, (ball.x, ball.y), BALL_RADIUS)
        pygame.draw.rect(SCREEN, WHITE, (paddle.x, paddle.y, PADDLE_WIDTH, PADDLE_HEIGHT))

        score_text = font.render(f'Score: {score} Lives: {lives}', True, WHITE)
        SCREEN.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()