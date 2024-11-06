import flet as ft
import asyncio
import random

# Game settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
BALL_RADIUS = 10
BALL_SPEED_X = 4
BALL_SPEED_Y = -4
BRICK_ROWS = 5
BRICK_COLUMNS = 10
BRICK_WIDTH = 70
BRICK_HEIGHT = 30
BRICK_PADDING = 10
BRICK_OFFSET_TOP = 60
BRICK_OFFSET_LEFT = (SCREEN_WIDTH - (BRICK_COLUMNS * (BRICK_WIDTH + BRICK_PADDING))) // 2
FPS = 60  # Frames per second

# Colors
WHITE = "white"
GREY = "grey"
RED = "red"
GREEN = "green"
BLUE = "blue"
YELLOW = "yellow"
ORANGE = "orange"
CYAN = "cyan"
MAGENTA = "magenta"
BLACK = "black"

BRICK_COLORS = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, MAGENTA]

class Paddle:
    def __init__(self, canvas: ft.canvas):
        self.canvas = canvas
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.x = (SCREEN_WIDTH - self.width) / 2
        self.y = SCREEN_HEIGHT - self.height - 30
        self.speed = 7
        self.rect = ft.Rect(
            left=self.x,
            top=self.y,
            width=self.width,
            height=self.height,
            fill=GREY,
            border_radius=ft.BorderRadius.all(5),
        )
        self.canvas.shapes.append(self.rect)
        self.canvas.update()

    def move_left(self):
        self.x -= self.speed
        if self.x < 0:
            self.x = 0
        self.rect.left = self.x
        self.canvas.update()

    def move_right(self):
        self.x += self.speed
        if self.x + self.width > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.width
        self.rect.left = self.x
        self.canvas.update()

class Ball:
    def __init__(self, canvas: ft.canvas, paddle: Paddle, bricks: ft.ShapeGroup, score_text: ft.Text, game_over_dialog: ft.AlertDialog):
        self.canvas = canvas
        self.paddle = paddle
        self.bricks = bricks
        self.score_text = score_text
        self.game_over_dialog = game_over_dialog
        self.radius = BALL_RADIUS
        self.x = paddle.x + paddle.width / 2
        self.y = paddle.y - self.radius - 1
        self.speed_x = BALL_SPEED_X * random.choice([-1, 1])
        self.speed_y = BALL_SPEED_Y
        self.circle = ft.Ellipse(
            left=self.x - self.radius,
            top=self.y - self.radius,
            width=self.radius * 2,
            height=self.radius * 2,
            fill=WHITE,
        )
        self.canvas.shapes.append(self.circle)
        self.canvas.update()
        self.stuck = True
        self.score = 0

    def launch(self):
        if self.stuck:
            self.stuck = False

    def reset_position(self):
        self.x = self.paddle.x + self.paddle.width / 2
        self.y = self.paddle.y - self.radius - 1
        self.speed_x = BALL_SPEED_X * random.choice([-1, 1])
        self.speed_y = BALL_SPEED_Y
        self.stuck = True
        self.circle.left = self.x - self.radius
        self.circle.top = self.y - self.radius
        self.canvas.update()

    def move(self):
        if self.stuck:
            self.x = self.paddle.x + self.paddle.width / 2
            self.y = self.paddle.y - self.radius - 1
            self.circle.left = self.x - self.radius
            self.circle.top = self.y - self.radius
        else:
            self.x += self.speed_x
            self.y += self.speed_y
            self.circle.left = self.x - self.radius
            self.circle.top = self.y - self.radius

            # Collision with walls
            if self.x - self.radius <= 0:
                self.x = self.radius
                self.speed_x *= -1
            if self.x + self.radius >= SCREEN_WIDTH:
                self.x = SCREEN_WIDTH - self.radius
                self.speed_x *= -1
            if self.y - self.radius <= 0:
                self.y = self.radius
                self.speed_y *= -1

            # Collision with paddle
            if (self.y + self.radius >= self.paddle.y and
                self.x >= self.paddle.x and
                self.x <= self.paddle.x + self.paddle.width and
                self.speed_y > 0):
                self.y = self.paddle.y - self.radius - 1
                self.speed_y *= -1
                # Adjust ball's horizontal speed based on where it hit the paddle
                hit_pos = (self.x - self.paddle.x) / self.paddle.width  # 0 to 1
                self.speed_x = BALL_SPEED_X * (hit_pos - 0.5) * 2  # Range: -BALL_SPEED_X to BALL_SPEED_X

            # Collision with bricks
            for brick in self.bricks.shapes[:]:
                if (self.x + self.radius >= brick.left and
                    self.x - self.radius <= brick.left + brick.width and
                    self.y + self.radius >= brick.top and
                    self.y - self.radius <= brick.top + brick.height):
                    self.speed_y *= -1
                    self.bricks.shapes.remove(brick)
                    self.canvas.shapes.remove(brick)
                    self.score += 10
                    self.score_text.value = f"Score: {self.score}"
                    self.score_text.update()
                    break  # Only handle one brick collision per frame

            # Check for game over
            if self.y - self.radius > SCREEN_HEIGHT:
                self.game_over()

        self.canvas.update()

    def game_over(self):
        self.canvas.update()
        self.game_over_dialog.title = ft.Text("Game Over!")
        self.game_over_dialog.content = ft.Text(f"Your Score: {self.score}")
        self.game_over_dialog.actions = [
            ft.TextButton("Restart", on_click=lambda _: self.restart_game()),
            ft.TextButton("Quit", on_click=lambda _: self.quit_game()),
        ]
        self.game_over_dialog.open = True
        self.canvas.page.update()

    def restart_game(self):
        # Reset game state
        self.canvas.shapes = [shape for shape in self.canvas.shapes if not isinstance(shape, ft.Ellipse)]
        self.reset_position()
        self.bricks.shapes = []
        self.create_bricks()
        self.score = 0
        self.score_text.value = f"Score: {self.score}"
        self.score_text.update()
        self.game_over_dialog.open = False
        self.canvas.update()

    def quit_game(self):
        self.canvas.page.window_close()

    def create_bricks(self):
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLUMNS):
                x = BRICK_OFFSET_LEFT + col * (BRICK_WIDTH + BRICK_PADDING)
                y = BRICK_OFFSET_TOP + row * (BRICK_HEIGHT + BRICK_PADDING)
                color = BRICK_COLORS[row % len(BRICK_COLORS)]
                brick = ft.Rect(
                    left=x,
                    top=y,
                    width=BRICK_WIDTH,
                    height=BRICK_HEIGHT,
                    fill=color,
                    border_radius=ft.BorderRadius.all(3),
                )
                self.bricks.shapes.append(brick)
        self.canvas.update()

class ArkanoidGame:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Arkanoid Game"
        self.page.window_width = SCREEN_WIDTH
        self.page.window_height = SCREEN_HEIGHT
        self.page.bgcolor = BLACK

        # Create Canvas
        self.canvas = ft.Canvas(
            width=SCREEN_WIDTH,
            height=SCREEN_HEIGHT,
            bg=BLACK,
        )

        # Add score text
        self.score_text = ft.Text(value="Score: 0", size=24, color=WHITE, left=10, top=10)

        # Create game over dialog
        self.game_over_dialog = ft.AlertDialog(
            title=ft.Text("Game Over!"),
            content=ft.Text(""),
            actions=[],  # To be filled dynamically
            modal=True,
            close_on_click=False,
        )
        self.page.dialog = self.game_over_dialog

        # Add components to the page
        self.page.add(self.canvas, self.score_text)

        # Create Paddle
        self.paddle = Paddle(self.canvas)

        # Create Bricks
        self.bricks = ft.ShapeGroup()
        self.canvas.shapes.append(self.bricks)

        # Create Ball
        self.ball = Ball(self.canvas, self.paddle, self.bricks, self.score_text, self.game_over_dialog)
        self.ball.create_bricks()

        # Handle keyboard input
        self.page.on_key_down = self.on_key_down

        # Start the game loop
        asyncio.create_task(self.game_loop())

    async def game_loop(self):
        while True:
            self.ball.move()
            await asyncio.sleep(1 / FPS)

    def on_key_down(self, e: ft.KeyboardEvent):
        if e.key == "ArrowLeft":
            self.paddle.move_left()
        elif e.key == "ArrowRight":
            self.paddle.move_right()
        elif e.key == "Space":
            self.ball.launch()
        elif e.key.lower() == "r" and self.game_over_dialog.open:
            self.ball.restart_game()
        elif e.key.lower() == "q" and self.game_over_dialog.open:
            self.ball.quit_game()

def main(page: ft.Page):
    ArkanoidGame(page)

# Run the app
ft.app(target=main)
