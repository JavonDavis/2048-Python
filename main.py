import gui

"""
2048 Game
Please read the comments to help clear up any confusion about what the purpose of the various variables are

Before submitting ensure to edit this comment block to include the ID numbers of both group members
Group Member:
Group Member:
"""

# Give grid the appropriate value
grid = None

# Values to represent the directions the tiles could move
UP = 1
DOWN = 2
RIGHT = 3
LEFT = 4

directions = {"Right": RIGHT, "Up": UP, "Left": LEFT, "Down": DOWN}

# Used to store the available keyboard controls
controls = ["<Right>", "<Left>", "<Up>", "<Down>"]

# use this variable to help keep track of the numbers on the board, remember each number needs a unique ID
number_count = 0

# used to help animate the movement from one tile to another, if functions are implemented correctly increasing
# this will increase the speed at which the tiles move and decreasing it will also cause the tiles to move slower
transition_value = 20


if __name__ == '__main__':
    """Your Program will start here"""

    frame, board = gui.setup()

    # Finishing setting up your GameBoard here, answer to Question 17 should go here

    gui.start(frame)
