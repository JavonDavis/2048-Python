import Tkinter as tk
from PIL import Image, ImageTk
from random import randint, choice, shuffle

UP = 1
DOWN = 2
RIGHT = 3
LEFT = 4

directions = {"Right": 3, "Up": 1, "Left": 4, "Down": 2}
empty_slots = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2), (1, 3), (2, 0), (2, 1), (2, 2), (2, 3), (3, 0), (3, 1), (3, 2), (3, 3)]

image2 = Image.open("img/img_2.jpg")
image4 = Image.open("img/img_4.jpg")

number_2 = ImageTk.PhotoImage(image2)
number_4 = ImageTk.PhotoImage(image4)


class GameBoard(tk.Frame):
    def __init__(self, parent, rows=4, columns=4, size=138, color="#CBBFB2", background_color="#BBADA0"):
        '''size is the size of a square, in pixels'''

        self.rows = rows
        self.columns = columns
        self.size = size
        self.color = color
        self.pieces = {}
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

    def add_number(self, name, image, row=0, column=0):
        '''Add a piece to the playing board'''
        self.canvas.create_image(0, 0, image=image, tags=(name, "piece"), anchor="c")
        self.place_number(name, row, column)

    def place_number(self, name, row, column):
        '''Place a piece at the given row/column'''
        self.pieces[name] = (row, column)
        x0 = (column * self.size + 5) + int(self.size / 2)
        y0 = (row * self.size + 5) + int(self.size / 2)
        self.canvas.coords(name, x0, y0)

    def move_number(self, name, row, column, direction):
        '''Move a number to a given row column'''
        (row1, column1) = self.pieces[name]
        x1 = (column1 * self.size + 5) + int(self.size / 2)
        y1 = (row1 * self.size + 5) + int(self.size / 2)
        self.pieces[name] = (row, column)
        x0 = (column * self.size + 5) + int(self.size / 2)
        y0 = (row * self.size + 5) + int(self.size / 2)

        dx = abs(x0 - x1)
        dy = abs(y0 - y1)
        self.animate_move_number(name, x1, y1, dx, dy, direction)

    def animate_move_number(self, name, x, y, dx, dy, direction=None):
        transition_value = 5
        transition_value_neg = -1 * transition_value

        def helper_horizontal(transition, distance):
            if distance < abs(transition):
                self.canvas.move(name, distance * (transition/abs(transition)), 0)
                self.canvas.update()
            else:
                self.canvas.move(name, transition, 0)
                distance -= abs(transition)
                self.canvas.update()
                self.after(100, helper_horizontal(transition, distance))

        def helper_vertical(transition, distance):
            if distance < abs(transition):
                self.canvas.move(name, 0, distance *(transition/abs(transition)))
                self.canvas.update()
            else:
                self.canvas.move(name, 0, transition)
                distance -= abs(transition)
                self.canvas.update()
                return helper_vertical(transition, distance)

        def add(num1, num2):
            return num1 + num2

        def subtract(num1, num2):
            return num1 - num2

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
        '''Redraw the board, possibly in response to window being resized'''
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
        for name in self.pieces:
            self.place_number(name, self.pieces[name][0], self.pieces[name][1])
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")


def test(event):
    print event.keysym


def move_right():
    pass


def random_number():
    number_choices = ['2'] * 90 + ['4'] * 10
    return number_2 if choice(number_choices) == '2' else number_4


def random_position():
    shuffle(empty_slots)
    return empty_slots.pop()


if __name__ == "__main__":
    root = tk.Tk()
    board = GameBoard(root)

    number_count = 0

    board.pack(side="top", fill="both", expand="true", padx=4, pady=4)

    row,column = random_position()

    board.add_number("Count {}".format(number_count), random_number(), row, column)
    root.bind("<Right>", lambda event: board.move_number("img_2", 0, 2, directions[event.keysym]))
    root.bind("<Left>", lambda event: board.move_number("img_2", 0, 1, directions[event.keysym]))
    root.resizable(width=False, height=False)
    root.mainloop()
