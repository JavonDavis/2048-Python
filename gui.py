import Tkinter as tk


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

    def remove_number(self, key):
        self.canvas.delete(key)

    def update_score(self):
        self.canvas.itemconfig(self.score_text, text=("Score:", self.score))

    def game_over(self, winner):
        if winner:
            self.canvas.itemconfig(self.score_text, text="Winner!!")
        else:
            self.canvas.itemconfig(self.score_text, text="Awww Better luck next time!")

    def refresh(self, event):
        """Draw the board"""
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
            row, column = self.numbers[key][0], self.numbers[key][1]
            self.numbers[key] = (row, column)
            x0 = (column * self.size + 5) + int(self.size / 2)
            y0 = (row * self.size + 5) + int(self.size / 2)
            self.canvas.coords(key, x0, y0)
        self.canvas.tag_lower("square")


def setup():
    root = tk.Tk()
    board = GameBoard(root)

    board.pack(side="top", fill="both", expand="true", padx=4, pady=4)
    return root, board


def start(root):
    root.resizable(width=False, height=False)
    root.mainloop()
