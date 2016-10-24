import Tkinter as tk
from helpers import find_number, random_number
from random import choice
from copy import deepcopy

controls = ["<Right>","<Left>","<Up>","<Down>"]

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
            "Comic Sans", 24))  # This is the first appearance of the score on screen, or the first creation.

        # this binding will cause a refresh if the user interactively
        # changes the window size
        self.canvas.bind("<Configure>", self.refresh)

    def add_number(self, name, number, row=0, column=0):
        """Add a number to the playing board"""
        global grid
        self.canvas.create_image(0, 0, image=number.image, tags=(name, "piece"), anchor="c")
        grid[row][column] = number.value
        self.place_number(name, row, column)
        return True

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

            return self.animate_move_number(key, dx, dy, direction)
        else:
            return False

    def animate_move_number(self, key, dx, dy, direction=None):
        """Animate the movement of a number from one slot to another"""
        transition_value = 5

        def helper_horizontal(transition, distance):
            if distance < abs(transition):
                self.canvas.move(key, distance * (transition / abs(transition)), 0)
                self.canvas.update()
                if self.merge(key):
                    return False
                return True
            else:
                self.canvas.move(key, transition, 0)
                self.canvas.update()
                return helper_horizontal(transition, distance - abs(transition))

        def helper_vertical(transition, distance):
            if distance < abs(transition):
                self.canvas.move(key, 0, distance * (transition / abs(transition)))
                self.canvas.update()
                if self.merge(key):
                    return False
                return True
            else:
                self.canvas.move(key, 0, transition)
                self.canvas.update()
                return helper_vertical(transition, distance - abs(transition))

        if direction == RIGHT:
            return helper_horizontal(transition_value, dx)
        elif direction == DOWN:
            return helper_vertical(transition_value, dy)
        elif direction == LEFT:
            return helper_horizontal(-1 * transition_value, dx)
        elif direction == UP:
            return helper_vertical(-1 * transition_value, dy)
        else:
            return Exception("Invalid direction")

    def remove_number(self, key):
        self.canvas.delete(key)

    def merge(self, key):
        grid_row, grid_column = self.numbers[key]
        for k,v in self.numbers.iteritems():
            if k != key and v == (grid_row, grid_column):
                self.numbers.pop(k)
                num = grid[grid_row][grid_column]
                number = find_number(num)
                self.remove_number(k)
                self.remove_number(key)
                self.score += number.value
                self.update_score()
                return self.add_number(key, number, grid_row, grid_column)
        return False

    def update_score(self):
        self.canvas.itemconfig(self.score_text, text=("Score:", self.score))

    def refresh(self, event):
        """Redraw the board, possibly in response to window being resized"""
        xsize = int((event.width - 1) / self.columns)
        ysize = int((event.height - 1) / self.rows)
        self.size = min(xsize, ysize)
        self.canvas.delete("square")
        self.update_score()

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


def empty_slots():
    slots = []
    for i in xrange(0, 4):
        for j in xrange(0, 4):
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
    elif grid[new_grid_row][new_grid_column] == grid[grid_row][grid_column]:
        grid[new_grid_row][new_grid_column] = num1*2
        grid[grid_row][grid_column] = 0
        return new_grid_row, new_grid_column

    return grid_row, grid_column


def find_key(board, grid_row, grid_column):
    for key, value in board.numbers.iteritems():
        if value[0] == grid_row and value[1] == grid_column:
            return key
    return None


def move_all(event):
    direction = directions[event.keysym]
    if direction == UP:
        move_all_up()
    elif direction == DOWN:
        move_all_down()
    elif direction == RIGHT:
        move_all_right()
    elif direction == LEFT:
        move_all_left()


def move_all_up():
    for i in xrange(0, 4):
        for j in xrange(0, 4):
            key = find_key(board, i, j)
            if key is not None:
                move(key, UP)


def move_all_down():
    for i in xrange(3, -1, -1):
        for j in xrange(0, 4):
            key = find_key(board, i, j)
            if key is not None:
                move(key, DOWN)


def move_all_left():
    for i in xrange(0, 4):
        for j in xrange(0, 4):
            key = find_key(board, i, j)
            if key is not None:
                move(key, LEFT)


def move_all_right():
    for j in xrange(3, -1, -1):
        for i in xrange(0, 4):
            key = find_key(board, i, j)
            if key is not None:
                move(key, RIGHT)


def move(key, direction):
    print grid
    if board.move_number(key, direction):
        move(key, direction)


def keyboard_callback(event, frame, game_board):
    unbind(frame)

    current_state = deepcopy(grid)
    move_all(event)

    new_state = deepcopy(grid)
    if current_state != new_state:
        add_random_number(game_board)

    bind(frame, game_board)


def bind(frame, game_board):
    map(lambda x: frame.bind(x, lambda event: keyboard_callback(event, frame, game_board)), controls)


def unbind(frame):
    map(lambda x: frame.unbind(x), controls)


def add_random_number(game_board):
    global number_count
    number_count += 1
    grid_row, grid_column = random_position()
    game_board.add_number("Count {}".format(number_count), random_number(), grid_row, grid_column)
    print grid

if __name__ == "__main__":
    root = tk.Tk()
    board = GameBoard(root)

    number_count = 0

    board.pack(side="top", fill="both", expand="true", padx=4, pady=4)

    add_random_number(board)
    add_random_number(board)

    bind(root, board)
    root.resizable(width=False, height=False)
    root.mainloop()
