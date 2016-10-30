"""
Shanice's gui.py
Do not modify any of the code in this file
"""

import Tkinter as tk
from PIL import Image, ImageTk
from random import choice

number2 = None
number4 = None
number8 = None
number16 = None
number32 = None
number64 = None
number128 = None
number256 = None
number512 = None
number1024 = None
number2048 = None


class NumberTile:
    def __init__(self, image, value):
        self.image = image
        self.value = value


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

        self.score_text = self.canvas.create_text(200, rows * size + 50, text=("Score:", self.score), font=(
            "Comic Sans", 24))  # This is the first appearance of the score on screen, or the first creation.

        self.canvas.bind("<Configure>", self.refresh)

    def refresh(self, event):
        """Draw the board"""
        xsize = int((event.width - 1) / self.columns)
        ysize = int((event.height - 1) / self.rows)
        self.size = min(xsize, ysize)
        self.canvas.delete("square")
        update_score(self)

        for row in range(self.rows):
            for col in range(self.columns):
                x1 = (col * self.size) + 5
                y1 = (row * self.size) + 5
                x2 = x1 + self.size - 5
                y2 = y1 + self.size - 5
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=self.color, tags="square")
        for key in self.numbers:
            row, column = self.numbers[key][0], self.numbers[key][1]
            self.numbers[key] = (row, column)
            x0 = (column * self.size + 5) + int(self.size / 2)
            y0 = (row * self.size + 5) + int(self.size / 2)
            self.canvas.coords(key, x0, y0)
        self.canvas.tag_lower("square")


def find_number(num):
    global number2, number4, number8, number16, number32, number64, number128, number256, number512, number1024 \
        , number2048
    if num == 2:
        if number2 is None:
            image = Image.open("img/img_2.jpg")
            number2 = NumberTile(ImageTk.PhotoImage(image), 2)
        return number2
    elif num == 4:
        if number4 is None:
            image = Image.open("img/img_4.jpg")
            number4 = NumberTile(ImageTk.PhotoImage(image), 4)
        return number4
    elif num == 8:
        if number8 is None:
            image = Image.open("img/img_8.jpg")
            number8 = NumberTile(ImageTk.PhotoImage(image), 8)
        return number8
    elif num == 16:
        if number16 is None:
            image = Image.open("img/img_16.jpg")
            number16 = NumberTile(ImageTk.PhotoImage(image), 16)
        return number16
    elif num == 32:
        if number32 is None:
            image = Image.open("img/img_32.jpg")
            number32 = NumberTile(ImageTk.PhotoImage(image), 32)
        return number32
    elif num == 64:
        if number64 is None:
            image = Image.open("img/img_64.jpeg")
            number64 = NumberTile(ImageTk.PhotoImage(image), 64)
        return number64
    elif num == 128:
        if number128 is None:
            image = Image.open("img/img_128.jpg")
            number128 = NumberTile(ImageTk.PhotoImage(image), 128)
        return number128
    elif num == 256:
        if number256 is None:
            image = Image.open("img/img_256.jpg")
            number256 = NumberTile(ImageTk.PhotoImage(image), 256)
        return number256
    elif num == 512:
        if number512 is None:
            image = Image.open("img/img_512.jpg")
            number512 = NumberTile(ImageTk.PhotoImage(image), 512)
        return number512
    elif num == 1024:
        if number1024 is None:
            image = Image.open("img/img_1024.jpg")
            number1024 = NumberTile(ImageTk.PhotoImage(image), 1024)
        return number1024
    elif num == 2048:
        if number2048 is None:
            image = Image.open("img/img_2048.jpeg")
            number2048 = NumberTile(ImageTk.PhotoImage(image), 2048)
        return number2048


def random_number():
    global number2, number4
    if number2 is None:
        image2 = Image.open("img/img_2.jpg")
        number2 = NumberTile(ImageTk.PhotoImage(image2), 2)

    if number4 is None:
        image4 = Image.open("img/img_4.jpg")
        number4 = NumberTile(ImageTk.PhotoImage(image4), 4)

    number_choices = ['2'] * 96 + ['4'] * 5
    return number2 if choice(number_choices) == '2' else number4


def move_number(game_board, key, direction, update_grid, move_by_distance):
    """Move a number to a given row column"""
    grid_row, grid_column = game_board.numbers[key]
    x1 = (grid_column * game_board.size + 5) + int(game_board.size / 2)
    y1 = (grid_row * game_board.size + 5) + int(game_board.size / 2)

    new_grid_row, new_grid_column = update_grid(grid_row, grid_column, direction)
    if new_grid_row != grid_row or new_grid_column != grid_column:
        game_board.numbers[key] = new_grid_row, new_grid_column
        x0 = (new_grid_column * game_board.size + 5) + int(game_board.size / 2)
        y0 = (new_grid_row * game_board.size + 5) + int(game_board.size / 2)

        dx = abs(x0 - x1)
        dy = abs(y0 - y1)

        return move_by_distance(game_board, key, dx, dy, direction)
    else:
        return False


def put(game_board, key, number, row=0, column=0):
    """Place a number to the playing board"""
    game_board.canvas.create_image(0, 0, image=number.image, tags=(key, "piece"), anchor="c")
    game_board.numbers[key] = (row, column)
    x0 = (column * game_board.size + 5) + int(game_board.size / 2)
    y0 = (row * game_board.size + 5) + int(game_board.size / 2)
    game_board.canvas.coords(key, x0, y0)
    return True


def move_tile(game_board, key, horizontal, vertical):
    game_board.canvas.move(key, horizontal, vertical)
    game_board.canvas.update()


def find_position(game_board, key):
    return game_board.numbers[key]


def remove_number(game_board, key):
    game_board.canvas.delete(key)


def update_score(game_board):
    game_board.canvas.itemconfig(game_board.score_text, text=("Score:", game_board.score))


def game_over(game_board, winner):
    if winner:
        game_board.canvas.itemconfig(game_board.score_text, text="Winner!!")
    else:
        game_board.canvas.itemconfig(game_board.score_text, text="Awww Better luck next time!")


def setup():
    root = tk.Tk()
    board = GameBoard(root)

    board.pack(side="top", fill="both", expand="true", padx=4, pady=4)
    return root, board


def start(root):
    root.resizable(width=False, height=False)
    root.mainloop()
