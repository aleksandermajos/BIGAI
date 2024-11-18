import time
import random

import flet as ft


def main(page: ft.Page):
    page.title = "Snake Game"
    page.window_width = 600
    page.window_height = 400

    snake = [(200, 200), (180, 200), (160, 200)]
    direction = ft.Vector(10, 0)
    food = (random.randint(0, page.width // 10) * 10, random.randint(0,
                                                                     page.height // 10) * 10)

    def update():
        nonlocal snake, direction, food

        head = snake[0]
        new_head = (head[0] + direction.x, head[1] + direction.y)

        # Check if the snake collides with the walls or itself
        if not (0 <= new_head[0] < page.width and 0 <= new_head[1] <
                page.height) or new_head in snake:
            page.window_close()

        # Check if the snake eats the food
        if new_head == food:
            snake.append(new_head)
            food = (random.randint(0, page.width // 10) * 10,
                    random.randint(0, page.height // 10) * 10)

        else:
            snake.pop()

        # Update the snake's position
        snake.insert(0, new_head)

        for segment in snake:
            page.canvas.add(ft.CircleSegment(center=ft.Point(segment[0],
                                                             segment[1]), radius=8, color="green"))

        page.canvas.add(ft.CircleSegment(center=ft.Point(food[0],
                                                         food[1]), radius=8, color="red"))
        page.update()

    def on_key(event):
        nonlocal direction

        if event.key == "ArrowUp" and direction.y != 10:
            direction = ft.Vector(0, -10)
        elif event.key == "ArrowDown" and direction.y != -10:
            direction = ft.Vector(0, 10)
        elif event.key == "ArrowLeft" and direction.x != 10:
            direction = ft.Vector(-10, 0)
        elif event.key == "ArrowRight" and direction.x != -10:
            direction = ft.Vector(10, 0)

    page.on_key_event = on_key

    while True:
        update()
        time.sleep(0.25)


ft.app(target=main)