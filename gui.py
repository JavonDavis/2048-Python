import Tkinter as tk
from PIL import Image, ImageTk
from random import randint, choice, shuffle

numbers = {}

UP = 1
DOWN = 2
RIGHT = 3
LEFT = 4

directions = {"Right": 3, "Up": 1, "Left": 4, "Down": 2}
grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]


class GameBoard(tk.Frame):
    def __init__(self, parent, rows=4, columns=4, size=140, color="#CBBFB2", background_color="#BBADA0"):
        """size is the size of a square, in pixels"""

        self.rows = rows
        self.columns = columns
        self.size = size
        self.color = color
        self.numbers = {}
        self.score = 0

        canvas_width = columns * size
        canvas_height = rows * size + 100

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height, background=background_color)
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)

        self.score_text = self.canvas.create_text(100, rows * size + 50, text=("Score:", self.score), font=(
            "Comic Sans", 24))  # This is the first appereance of the score on screen, or the first creation.

        # this binding will cause a refresh if the user interactively
        # changes the window size
        self.canvas.bind("<Configure>", self.refresh)

    def add_number(self, name, number, row=0, column=0):
        """Add a number to the playing board"""
        global grid
        self.canvas.create_image(0, 0, image=number.image, tags=(name, "piece"), anchor="c")
        grid[row][column] = number.value
        self.place_number(name, row, column)

    def place_number(self, key, row, column):
        """Place a number at the given row/column"""
        self.numbers[key] = (row, column)
        x0 = (column * self.size + 5) + int(self.size / 2)
        y0 = (row * self.size + 5) + int(self.size / 2)
        self.canvas.coords(key, x0, y0)

    def move_number(self, key, direction):
        """Move a number to a given row column"""
        grid_row, grid_column = self.numbers[key]
        x1 = (grid_column * self.size + 5) + int(self.size / 2)
        y1 = (grid_row * self.size + 5) + int(self.size / 2)

        new_grid_row, new_grid_column = update_grid(grid_row, grid_column, direction)
        if new_grid_row != grid_row or new_grid_column != grid_column:
            self.numbers[key] = new_grid_row, new_grid_column
            x0 = (new_grid_column * self.size + 5) + int(self.size / 2)
            y0 = (new_grid_row * self.size + 5) + int(self.size / 2)

            dx = abs(x0 - x1)
            dy = abs(y0 - y1)

            self.animate_move_number(key, dx, dy, direction)

    def animate_move_number(self, key, dx, dy, direction=None):
        """Animate the movement of a number from one slot to another"""
        transition_value = 5
        transition_value_neg = -1 * transition_value

        def helper_horizontal(transition, distance):
            if distance < abs(transition):
                self.canvas.move(key, distance * (transition / abs(transition)), 0)
                self.canvas.update()
            else:
                self.canvas.move(key, transition, 0)
                distance -= abs(transition)
                self.canvas.update()
                self.after(100, helper_horizontal(transition, distance))

        def helper_vertical(transition, distance):
            if distance < abs(transition):
                self.canvas.move(key, 0, distance * (transition / abs(transition)))
                self.canvas.update()
            else:
                self.canvas.move(key, 0, transition)
                distance -= abs(transition)
                self.canvas.update()
                return helper_vertical(transition, distance)

        if direction == RIGHT:
            helper_horizontal(transition_value, dx)
        elif direction == DOWN:
            return helper_vertical(transition_value, dy)
        elif direction == LEFT:
            helper_horizontal(transition_value_neg, dx)
        elif direction == UP:
            return helper_vertical(transition_value_neg, dy)
        else:
            return Exception("Invalid direction")

    def refresh(self, event):
        """Redraw the board, possibly in response to window being resized"""
        xsize = int((event.width - 1) / self.columns)
        ysize = int((event.height - 1) / self.rows)
        self.size = min(xsize, ysize)
        self.canvas.delete("square")
        self.score += 10492
        self.canvas.itemconfig(self.score_text, text=("Score:", self.score))
        # self.number = self.canvas.create_text(5, 5, text=2, font=(
        #     "Comic Sans", 36), anchor="nw")
        # r = self.canvas.create_rectangle(self.canvas.bbox(self.number), fill="white")
        # self.canvas.move(r, 200, 200)
        # self.canvas.tag_lower(r, self.number)
        for row in range(self.rows):
            for col in range(self.columns):
                x1 = (col * self.size) + 5
                y1 = (row * self.size) + 5
                x2 = x1 + self.size - 5
                y2 = y1 + self.size - 5
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=self.color, tags="square")
        for key in self.numbers:
            self.place_number(key, self.numbers[key][0], self.numbers[key][1])
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")


class Numbers:
    def __init__(self):
        image2 = Image.open("img/img_2.jpg")
        image4 = Image.open("img/img_4.jpg")
        image8 = Image.open("img/img_8.jpg")
        image16 = Image.open("img/img_16.jpg")

        self.number_2 = Number(ImageTk.PhotoImage(image2), 2)
        self.number_4 = Number(ImageTk.PhotoImage(image4), 4)
        self.number_8 = Number(ImageTk.PhotoImage(image8), 8)
        self.number_16 = Number(ImageTk.PhotoImage(image16), 16)
        self.numbers = {"2": self.number_2, "4": self.number_4, "8": self.number_8, "16": self.number_16}

    def number(self, num):
        return self.numbers[num]

    def random_number(self):
        number_choices = ['2'] * 95 + ['4'] * 5
        return self.number_2 if choice(number_choices) == '2' else self.number_4


class Number:
    def __init__(self, image, value):
        self.image = image
        self.value = value


def test(event):
    print event.keysym


def move_right():
    pass


def empty_slots():
    slots = []
    for i in range(0, 4):
        for j in range(0, 4):
            if grid[i][j] == 0:
                slots.append((i, j))
    return slots


def random_position():
    return choice(empty_slots())


def update_grid(grid_row, grid_column, direction):
    num1 = grid[grid_row][grid_column]
    if direction == UP and grid_row > 0:
        new_grid_row, new_grid_column = grid_row - 1, grid_column
    elif direction == DOWN and grid_row < 3:
        new_grid_row, new_grid_column = grid_row + 1, grid_column
    elif direction == RIGHT and grid_column < 3:
        new_grid_row, new_grid_column = grid_row, grid_column + 1
    elif direction == LEFT and grid_column > 0:
        new_grid_row, new_grid_column = grid_row, grid_column - 1
    else:
        return grid_row, grid_column
    if grid[new_grid_row][new_grid_column] == 0:
        grid[new_grid_row][new_grid_column] = num1
        grid[grid_row][grid_column] = 0
        return new_grid_row, new_grid_column

    return grid_row, grid_column


def find_key(board, grid_row, grid_column):
    for key,value in board.numbers:
        if value[0] == grid_row and value[1] == grid_column:
            return key
    return None


def move(event, key):
    board.move_number(key, directions[event.keysym])
    print grid


if __name__ == "__main__":
    root = tk.Tk()
    board = GameBoard(root)

    numbers = Numbers()

    number_count = 0

    board.pack(side="top", fill="both", expand="true", padx=4, pady=4)

    row, column = random_position()
    board.add_number("Count {}".format(number_count), numbers.random_number(), row, column)

    number_count += 1
    row, column = random_position()
    board.add_number("Count {}".format(number_count), numbers.random_number(), row, column)
    print grid

    root.bind("<Right>", move)
    root.bind("<Left>", move)
    root.bind("<Up>", move)
    root.bind("<Down>", move)
    root.resizable(width=False, height=False)
    root.mainloop()
