from random import choice
from copy import deepcopy
import gui

controls = ["<Right>", "<Left>", "<Up>", "<Down>"]

UP = 1
DOWN = 2
RIGHT = 3
LEFT = 4

grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
number_count = 0
transition_value = 20

directions = {"Right": RIGHT, "Up": UP, "Left": LEFT, "Down": DOWN}


def keyboard_callback(event, game_frame, game_board):
    unbind(game_frame)

    old_state = deepcopy(grid)
    move_all(event, game_board)
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
    global number_count, grid
    number_count += 1
    grid_row, grid_column = random_position()
    number = gui.random_number()
    grid[grid_row][grid_column] = number.value
    gui.put(game_board, "Count {}".format(number_count), number, grid_row, grid_column)
    print grid


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


# Question #1
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
    global grid
    grid_row, grid_column = game_board.numbers[key]
    for k, v in game_board.numbers.iteritems():
        if k != key and v == (grid_row, grid_column):
            game_board.numbers.pop(k)
            num = grid[grid_row][grid_column]
            number = gui.find_number(num)
            gui.remove_number(game_board, k)
            gui.remove_number(game_board, key)
            game_board.score += number.value
            gui.update_score(game_board)
            grid[grid_row][grid_column] = number.value
            return gui.put(game_board, key, number, grid_row, grid_column)
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
    elif grid[new_grid_row][new_grid_column] == grid[grid_row][grid_column]:
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
    if gui.move_number(game_board, key, direction, update_grid, move_by_distance):
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