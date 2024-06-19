import tkinter as tk


class SnakeGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Snake game")

        # Create canvas
        self.canvas = tk.Canvas(self.root, width=500, height=500, bg="white")
        self.canvas.pack()

        # Snake position and direction
        self.snake_pos = [[100, 100], [90, 100], [80, 100]]
        self.direction = 'Right'

        # Food for snake
        self.food_pos = self.set_food()

        # Binding keys to change direction of the snake
        self.root.bind('<KeyPress>', self.change_dir)

        self.run_game()

    def run_game(self):
        self.clear_canvas()

        # If snake hits itself or wall, then game over
        if any(block in self.snake_pos[1:] for block in [self.snake_pos[0]]) \
                or not 0 <= self.snake_pos[0][0] <= 490 \
                or not 0 <= self.snake_pos[0][1] <= 490:
            self.game_over()
        else:
            # Move snake
            self.move_snake()

            # If the snake eats food, generate new food and increase length of snake
            if self.snake_pos[0] == self.food_pos:
                self.food_pos = self.set_food()
                self.snake_pos.append(self.snake_pos[-1])
            else:
                self.snake_pos.pop()

            self.draw_game_elements()

            # update game every 250 milliseconds
            self.root.after(250, self.run_game)

    def clear_canvas(self):
        self.canvas.delete("all")

    def change_dir(self, event=None):
        if (self.direction == "Right" and not event.keysym == "Left") or \
                (self.direction == "Left" and not event.keysym == "Right") or \
                (self.direction == "Up" and not event.keysym == "Down") or \
                (self.direction == "Down" and not event.keysym == "Up"):
            self.direction = event.keysym

    def move_snake(self):
        head_x, head_y = self.snake_pos[0]

        if self.direction == 'Right':
            self.snake_pos.insert(0, [head_x + 10, head_y])
        elif self.direction == 'Left':
            self.snake_pos.insert(0, [head_x - 10, head_y])
        elif self.direction == 'Up':
            self.snake_pos.insert(0, [head_x, head_y - 10])
        else:
            self.snake_pos.insert(0, [head_x, head_y + 10])

    def set_food(self):
        return [self.canvas.create_oval(250, 250, 260, 260, fill="red"), 255, 255]

    def draw_game_elements(self):
        for pos in self.snake_pos:
            self.canvas.create_rectangle(pos[0], pos[1], pos[0] + 10, pos[1] + 10, fill="green")

        # Draw Food
        self.canvas.create_rectangle(self.food_pos[0], self.food_pos[1],
                                     self.food_pos[0] + 10, self.food_pos[1] + 10, fill='red')

    def game_over(self):
        self.clear_canvas()
        self.canvas.create_text(250, 250, text='Game Over!', font=('TkDefaultFont', 30), fill='red')


SnakeGame().root.mainloop()