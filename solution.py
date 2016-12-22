from copy import deepcopy

import gui
from random import choice

"""
2048 Game
Please read the comments to help clear up any confusion about what the purpose of the various variables are

Before submitting ensure to edit this comment block to include the ID numbers of both group members
Group Member:
Group Member:
"""

# Give grid the appropriate value
grid = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]]

# Values to represent the directions the tiles could move
UP = 1
DOWN = 2
RIGHT = 3
LEFT = 4

# Dictionary that might be useful
helper = {"count": 0, "Right": RIGHT, "Up": UP, "Left": LEFT, "Down": DOWN}

# Used to store the available keyboard controls
controls = ["<Right>", "<Left>", "<Up>", "<Down>"]

# used to help animate the movement from one tile to another, if functions are implemented correctly increasing
# this will increase the speed at which the tiles move and decreasing it will also cause the tiles to move slower
transition_value = 20


# Question #2
def empty_slots():
    return [(i, j) for i in xrange(4) for j in xrange(4) if grid[i][j] == 0]  # Assume the grid will always be a 4x4


# Question #3
def random_position():
    return choice(empty_slots())


# Question #4
def add_random_number(game_board):
    helper['count'] += 1
    row, column = random_position()
    number = gui.random_number()
    grid[row][column] = number.value
    gui.put(game_board, "Count {}".format(helper['count']), number, row, column)
    return row, column


# Helper function for testing
def add_random_number_at(game_board, row, column):
    helper['count'] += 1
    number = gui.random_number()
    grid[row][column] = number.value
    gui.put(game_board, "Count {}".format(helper['count']), number, row, column)
    return row, column


# Question 5
def find_identifier(game_board, grid_row, grid_column):
    for key, value in game_board.numbers.iteritems():
        if value[0] == grid_row and value[1] == grid_column:
            return key
    return None


# Question 6
def update_grid(row, column, direction):
    num1 = grid[row][column]
    if direction == UP and row > 0:
        new_row, new_column = row - 1, column
    elif direction == DOWN and row < 3:
        new_row, new_column = row + 1, column
    elif direction == RIGHT and column < 3:
        new_row, new_column = row, column + 1
    elif direction == LEFT and column > 0:
        new_row, new_column = row, column - 1
    else:
        return row, column
    if grid[new_row][new_column] == 0:
        grid[new_row][new_column] = num1
        grid[row][column] = 0
        return new_row, new_column
    elif grid[new_row][new_column] == grid[row][column]:
        grid[new_row][new_column] = num1 * 2
        grid[row][column] = 0
        return new_row, new_column
    return row, column


# Question 7 - does not include merge in answer
# def animate_movement(game_board, key, horizontal_distance, vertical_distance, direction=None):
#     """Animate the movement of a number from one slot to another"""
#
#     def helper_horizontal(transition, distance):
#         if distance < transition_value:
#             gui.move_tile(game_board, key, distance * transition_value/transition, 0)
#             return True
#         else:
#             gui.move_tile(game_board, key, transition, 0)
#             return helper_horizontal(transition, distance - transition_value)
#
#     def helper_vertical(transition, distance):
#         if distance < transition_value:
#             gui.move_tile(game_board, key, 0, distance * transition_value/transition)
#             return True
#         else:
#             gui.move_tile(game_board, key, 0, transition)
#             return helper_vertical(transition, distance - transition_value)
#
#     if direction == RIGHT:
#         return helper_horizontal(transition_value, horizontal_distance)
#     elif direction == DOWN:
#         return helper_vertical(transition_value, vertical_distance)
#     elif direction == LEFT:
#         return helper_horizontal(-1 * transition_value, horizontal_distance)
#     elif direction == UP:
#         return helper_vertical(-1 * transition_value, vertical_distance)
#     else:
#         return Exception("Invalid direction")


# Question 8
def move(game_board, key, direction):
    if gui.move_number(game_board, key, direction, update_grid, animate_movement):
        move(game_board, key, direction)


# Question 9
def move_all_down(game_board):
    for j in xrange(0, 4):
        for i in xrange(3, -1, -1):
            key = find_identifier(game_board, i, j)
            if key is not None:
                move(game_board, key, DOWN)


# Question 10
def move_all_up(game_board):
    for j in xrange(0, 4):
        for i in xrange(0, 4):
            key = find_identifier(game_board, i, j)
            if key is not None:
                move(game_board, key, UP)


# Question 11
def move_all_right(game_board):
    for i in xrange(0, 4):
        for j in xrange(3, -1, -1):
            key = find_identifier(game_board, i, j)
            if key is not None:
                move(game_board, key, RIGHT)


# Question 12
def move_all_left(game_board):
    for i in xrange(0, 4):
        for j in xrange(0, 4):
            key = find_identifier(game_board, i, j)
            if key is not None:
                move(game_board, key, LEFT)


# Question 13
def move_all(game_board, event):
    direction = helper[event.keysym]
    if direction == UP:
        move_all_up(game_board)
    elif direction == DOWN:
        move_all_down(game_board)
    elif direction == RIGHT:
        move_all_right(game_board)
    elif direction == LEFT:
        move_all_left(game_board)


# Question 14
# def keyboard_callback(event, game_frame, game_board):
#     old_state = deepcopy(grid)
#     move_all(game_board, event)
#     new_state = deepcopy(grid)
#
#     if old_state != new_state:
#         add_random_number(game_board)


# Question 15
def bind(game_frame, game_board):
    map(lambda x: game_frame.bind(x, lambda event: keyboard_callback(event, game_frame, game_board)), controls)


# Question 16
def unbind(game_frame):
    map(lambda x: game_frame.unbind(x), controls)


# Question 18
def merge(game_board, key):
    grid_row, grid_column = gui.find_position(game_board, key)
    for k, v in game_board.numbers.iteritems():
        if k != key and v == (grid_row, grid_column):
            game_board.numbers.pop(k)
            num = grid[grid_row][grid_column]
            number = gui.find_number(num)
            gui.remove_number(game_board, k)
            gui.remove_number(game_board, key)
            game_board.score += number.value
            gui.update_score(game_board)
            return gui.put(game_board, key, number, grid_row, grid_column)
    return False


# Question 19
def animate_movement(game_board, key, horizontal_distance, vertical_distance, direction=None):
    """Animate the movement of a number from one slot to another"""

    # Handles moving tiles horizontally
    def helper_horizontal(transition, distance):
        if distance < transition_value:
            gui.move_tile(game_board, key, distance * transition_value / transition, 0)
            if merge(game_board, key):
                return False
            return True
        else:
            gui.move_tile(game_board, key, transition, 0)
            return helper_horizontal(transition, distance - transition_value)

    # Handles moving tiles vertically
    def helper_vertical(transition, distance):
        if distance < transition_value:
            gui.move_tile(game_board, key, 0, distance * transition_value / transition)
            if merge(game_board, key):
                return False
            return True
        else:
            gui.move_tile(game_board, key, 0, transition)
            return helper_vertical(transition, distance - transition_value)

    if direction == RIGHT:
        return helper_horizontal(transition_value, horizontal_distance)
    elif direction == DOWN:
        return helper_vertical(transition_value, vertical_distance)
    elif direction == LEFT:
        return helper_horizontal(-1 * transition_value, horizontal_distance)
    elif direction == UP:
        return helper_vertical(-1 * transition_value, vertical_distance)


# Question 20
def is_game_over(game_board):
    result = True
    winner = False
    for i in xrange(0, 4):
        for j in xrange(0, 4):
            if grid[i][j] == 2048:
                winner = True
                break

    if not empty_slots():
        for i in xrange(0, 4):
            for j in xrange(0, 4):
                num = grid[i][j]
                if i > 0:
                    if grid[i - 1][j] == num:
                        result = False
                        break
                if i < 3:
                    if grid[i + 1][j] == num:
                        result = False
                        break
                if j > 0:
                    if grid[i][j - 1] == num:
                        result = False
                        break
                if j < 3:
                    if grid[i][j + 1] == num:
                        result = False
                        break
    else:
        result = False

    if result:
        gui.game_over(game_board, winner)
    return result


# Question 21
def keyboard_callback(event, game_frame, game_board):
    unbind(game_frame)

    old_state = deepcopy(grid)
    move_all(game_board, event)
    new_state = deepcopy(grid)

    if old_state != new_state:
        add_random_number(game_board)

    if not is_game_over(game_board):
        bind(game_frame, game_board)


if __name__ == '__main__':
    """Your Program will start here"""

    frame, board = gui.setup()

    # Finishing setting up your GameBoard here, answer to Question 17 should go here
    add_random_number(board)
    add_random_number(board)

    bind(frame, board)
    gui.start(frame)
