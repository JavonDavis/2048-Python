from helpers import find_number, random_number
from random import choice
from copy import deepcopy
import gui

merged_slots = []

controls = ["<Right>", "<Left>", "<Up>", "<Down>"]

UP = 1
DOWN = 2
RIGHT = 3
LEFT = 4

grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
number_count = 0
transition_value = 20

directions = {"Right": 3, "Up": 1, "Left": 4, "Down": 2}


def keyboard_callback(event, game_frame, game_board):
    global merged_slots
    unbind(game_frame)

    old_state = deepcopy(grid)
    move_all(event, game_board)
    merged_slots = []
    new_state = deepcopy(grid)

    if old_state != new_state:
        add_random_number(game_board)

    if not is_game_over(game_board):
        bind(game_frame, game_board)


def bind(game_frame, game_board):
    map(lambda x: game_frame.bind(x, lambda event: keyboard_callback(event, game_frame, game_board)), controls)


def unbind(game_frame):
    map(lambda x: game_frame.unbind(x), controls)


def add_random_number(game_board):
    global number_count
    number_count += 1
    grid_row, grid_column = random_position()
    put(game_board, "Count {}".format(number_count), random_number(), grid_row, grid_column)
    print grid


def put(game_board, key, number, row=0, column=0):
    """Place a number to the playing board"""
    global grid
    game_board.canvas.create_image(0, 0, image=number.image, tags=(key, "piece"), anchor="c")
    grid[row][column] = number.value
    game_board.numbers[key] = (row, column)
    x0 = (column * game_board.size + 5) + int(game_board.size / 2)
    y0 = (row * game_board.size + 5) + int(game_board.size / 2)
    game_board.canvas.coords(key, x0, y0)
    return True


def move_piece(game_board, key, left, right):
    game_board.move(key, left, right)
    game_board.update()


def move_all(event, game_board):
    direction = directions[event.keysym]
    if direction == UP:
        move_all_up(game_board)
    elif direction == DOWN:
        move_all_down(game_board)
    elif direction == RIGHT:
        move_all_right(game_board)
    elif direction == LEFT:
        move_all_left(game_board)
    else:
        return Exception("Invalid direction")


def move_number(game_board, key, direction):
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


def move_by_distance(game_board, key, horizontal_distance, vertical_distance, direction=None):
    """Animate the movement of a number from one slot to another"""

    def helper_horizontal(transition, distance):
        if distance < abs(transition):
            move_piece(game_board.canvas, key, transition, 0)
            if merge(game_board, key):
                return False
            return True
        else:
            move_piece(game_board.canvas, key, transition, 0)
            return helper_horizontal(transition, distance - abs(transition))

    def helper_vertical(transition, distance):
        if distance < abs(transition):
            move_piece(game_board.canvas, key, 0, transition)
            if merge(game_board, key):
                return False
            return True
        else:
            move_piece(game_board.canvas, key, 0, transition)
            return helper_vertical(transition, distance - abs(transition))

    if direction == RIGHT:
        return helper_horizontal(transition_value, horizontal_distance)
    elif direction == DOWN:
        return helper_vertical(transition_value, vertical_distance)
    elif direction == LEFT:
        return helper_horizontal(-1 * transition_value, horizontal_distance)
    elif direction == UP:
        return helper_vertical(-1 * transition_value, vertical_distance)
    else:
        return Exception("Invalid direction")


def empty_slots():
    slots = []
    for i in xrange(0, 4):
        for j in xrange(0, 4):
            if grid[i][j] == 0:
                slots.append((i, j))
    return slots


def random_position():
    return choice(empty_slots())


def merge(game_board, key):
    grid_row, grid_column = game_board.numbers[key]
    for k, v in game_board.numbers.iteritems():
        if k != key and v == (grid_row, grid_column):
            game_board.numbers.pop(k)
            num = grid[grid_row][grid_column]
            number = find_number(num)
            game_board.remove_number(k)
            game_board.remove_number(key)
            game_board.score += number.value
            game_board.update_score()
            merged_slots.append((grid_row, grid_column))
            return put(game_board, key, number, grid_row, grid_column)
    return False


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
    elif grid[new_grid_row][new_grid_column] == grid[grid_row][grid_column] \
            and (grid_row, grid_column) not in merged_slots:
        grid[new_grid_row][new_grid_column] = num1 * 2
        grid[grid_row][grid_column] = 0
        return new_grid_row, new_grid_column

    return grid_row, grid_column


def find_key(game_board, grid_row, grid_column):
    for key, value in game_board.numbers.iteritems():
        if value[0] == grid_row and value[1] == grid_column:
            return key
    return None


def move_all_up(game_board):
    for j in xrange(0, 4):
        for i in xrange(0, 4):
            key = find_key(game_board, i, j)
            if key is not None:
                move(key, UP, game_board)


def move_all_down(game_board):
    for j in xrange(0, 4):
        for i in xrange(3, -1, -1):
            key = find_key(game_board, i, j)
            if key is not None:
                move(key, DOWN, game_board)


def move_all_left(game_board):
    for i in xrange(0, 4):
        for j in xrange(0, 4):
            key = find_key(game_board, i, j)
            if key is not None:
                move(key, LEFT, game_board)


def move_all_right(game_board):
    for j in xrange(3, -1, -1):
        for i in xrange(0, 4):
            key = find_key(game_board, i, j)
            if key is not None:
                move(key, RIGHT, game_board)


def move(key, direction, game_board):
    print grid
    if move_number(game_board, key, direction):
        move(key, direction, game_board)


def is_game_over(game_board):
    result = True
    winner = False
    for i in xrange(0,4):
        for j in range(0,4):
            if grid[i][j] == 2048:
                winner = True
                break

    if not empty_slots():
        for i in xrange(0, 4):
            for j in range(0, 4):
                num = grid[i][j]
                if i > 0:
                    if grid[i-1][j] == num:
                        result = False
                        break
                if i < 3:
                    if grid[i+1][j] == num:
                        result = False
                        break
                if j > 0:
                    if grid[i][j-1] == num:
                        result = False
                        break
                if j < 3:
                    if grid[i][j+1] == num:
                        result = False
                        break
    else:
        result = False

    if result:
        game_board.game_over(winner)
    return result


if __name__ == '__main__':
    frame, board = gui.setup()

    add_random_number(board)
    add_random_number(board)

    bind(frame, board)
    gui.start(frame)