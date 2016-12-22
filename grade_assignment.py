import gui
import sys

from imp import load_source
from bdb import Bdb

try:
    solution = load_source('solution', 'solution.py')
    frame, board = gui.setup()
except Exception:
    raise Exception("Error setting up program to grade")


class MockEvent:

    def __init__(self, direction):
        self.keysym = direction

#
# class RecursionDetectedException(Exception):
#     """
#     Used to indicate when a recursive call takes place
#     """
#     pass
#
#
# class RecursionDetector(Bdb):
#     """
#     Class that checks if a recursive process took place for Problem #8
#     """
#
#     def do_clear(self, arg):
#         pass
#
#     def __init__(self, *args):
#         Bdb.__init__(self, *args)
#         self.count = 0
#         self.stack = set()
#
#     def user_call(self, execution_frame, arguments):
#         code = execution_frame.f_code
#
#         if code in self.stack:
#             raise RecursionDetectedException
#         self.stack.add(code)
#
#     def user_return(self, execution_frame, return_value):
#         self.stack.remove(execution_frame.f_code)


def grade_number_1(assignment):
    """
    Checks to see if the grid is the 4 dimensional list of lists globally
    :param assignment: The student's assignment
    :return: The grade out of 1
    """
    if hasattr(assignment, "grid"):
        if assignment.grid == [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], ]:
            return 1
        else:
            print "Grid is {} when it should be [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], ]".format(
                assignment.grid)
    else:
        print "Assignment does not contain a grid"
    return 0


def grade_number_2(assignment):
    """
    Tests the functionality of the student's empty_slot() function
    :param assignment: The student's assignment
    :return: The grade out of 2
    """

    if not hasattr(assignment, "empty_slots"):
        print "Submission does not contain a global empty_slots function"
        return 0

    print(type(getattr(assignment, "empty_slots")))
    score = 0.
    score_total = 5

    try:
        solution.grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], ]
        assignment.grid = solution.grid
        slots = [(row, column) for row in xrange(0, 4) for column in xrange(0, 4)]
        fail = False
        for test_count in xrange(0, 10):
            empty_slots = assignment.empty_slots()
            if empty_slots != slots:
                print "Failed to return all empty slots"
                fail = True
                break

        if not fail:
            score += 1

        assignment.grid = [[2, 2, 2, 2], [2, 2, 2, 2], [2, 2, 2, 2], [2, 2, 2, 2], ]

        empty_slots = assignment.empty_slots()
        if not empty_slots:
            score += 1
        else:
            print "empty_slots() returned {} instead of {} when grid is {}".format(empty_slots, "[]", assignment.grid)

        assignment.grid = [[2, 2, 2, 2], [2, 2, 2, 2], [2, 2, 2, 2], [2, 2, 0, 2], ]

        empty_slots = assignment.empty_slots()

        if empty_slots == [(3, 2)]:
            score += 1
        else:
            print "empty_slots() returned {} instead of {} when grid is {}".format(empty_slots, "[]", assignment.grid)

        assignment.grid = [[2, 2, 2, 2], [2, 2, 2, 2], [2, 2, 2, 0], [2, 2, 2, 2], ]

        empty_slots = assignment.empty_slots()
        if empty_slots == [(2, 3)]:
            score += 1
        else:
            print "empty_slots() returned {} instead of {} when grid is {}".format(empty_slots, "[]", assignment.grid)

        assignment.grid = [[0, 2, 2, 0], [2, 2, 2, 2], [2, 2, 2, 2], [2, 2, 2, 2], ]

        empty_slots = assignment.empty_slots()
        if empty_slots == [(0, 0), (0, 3)]:
            score += 1
        else:
            print "empty_slots() returned {} instead of {} when grid is {}".format(empty_slots, "[]", assignment.grid)

        return (score / score_total) * 2
    except Exception as e:
        print e.message
        return (score / score_total) * 2
    except SyntaxError as e:
        print e.message
        return (score / score_total) * 5


def grade_number_3(assignment):
    """
    Test the functionality of the student's random_position function
    :param assignment: The student's assignment
    :return: The grade out of 1
    """

    if not hasattr(assignment, "random_position"):
        print "Submission does not contain a global random_position function"
        return 0

    score = 0.
    score_total = 3

    try:
        # Inject correct answers for previous questions from the solution
        solution.grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], ]
        assignment.grid = solution.grid
        assignment.empty_slots = solution.empty_slots

        slots = [(row, column) for row in xrange(0, 4) for column in xrange(0, 4)]
        fail = False
        for test_count in xrange(0, 10):
            empty_slot = assignment.random_position()
            if empty_slot not in slots:
                print "random_position() returned {} which is not an empty slot when grid is {}".format(empty_slot,
                                                                                                        assignment.grid)
                fail = True
                break

        if not fail:
            score += 1

        assignment.grid = [[2, 2, 2, 2], [2, 2, 2, 2], [2, 2, 2, 0], [2, 2, 2, 2], ]
        empty_slot = assignment.random_position()
        if empty_slot == (2, 3):
            score += 1
        else:
            print "random_position() returned {} instead of {} when grid is {}".format(empty_slot, "(2,3)",
                                                                                       assignment.grid)

        assignment.grid = [[0, 2, 2, 0], [2, 2, 2, 2], [2, 2, 2, 2], [2, 2, 2, 2], ]

        empty_slot = assignment.random_position()
        if empty_slot == (0, 0) or (0, 3):
            score += 1
        else:
            print "random_position() returned {} instead of {} when grid is {}".format(empty_slot, "(0,0) or (0,3)",
                                                                                       assignment.grid)

        return (score / score_total) * 1
    except Exception as e:
        print e.message
        return (score / score_total) * 1
    except SyntaxError as e:
        print e.message
        return (score / score_total) * 5


def grade_number_4(assignment):
    """
    Tests the functionality of the student's add_random_number function
    :param assignment: The student's assignment
    :return: The grade out of 3
    """

    if not hasattr(assignment, "add_random_number"):
        print "Submission does not contain a global add_random_number function"
        return 0

    score = 0.
    score_total = 5

    try:
        # Inject correct answers for previous questions from the solution
        solution.grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], ]
        assignment.grid = solution.grid
        assignment.empty_slots = solution.empty_slots
        assignment.random_position = solution.random_position

        new_position1 = assignment.add_random_number(board)
        new_position2 = assignment.add_random_number(board)

        if type(new_position1) == tuple and type(new_position2) == tuple:
            score += 1

        else:
            print "function does not return tuple"

        if new_position1 != new_position2:
            score += 1
        else:
            print "Both positions for the numbers were equal positions:{} and {}".format(new_position1, new_position2)

        if (assignment.grid[new_position1[0]][new_position1[1]] == 2 or assignment.grid[new_position1[0]][
            new_position1[1]] == 4) and (
                        assignment.grid[new_position2[0]][new_position2[1]] == 2 or assignment.grid[new_position2[0]][
                    new_position2[1]] == 2):
            score += 1
        else:
            print "Grid does not contain either a 2 or a 4 for positions {} and {}".format(new_position1, new_position2)

        if len(board.numbers) == 2:
            score += 2
        else:
            print "Length of numbers dictionary is {} instead of 2".format(len(board.numbers))
        return (score / score_total) * 3
    except Exception as e:
        print e.message
        return (score / score_total) * 3
    except SyntaxError as e:
        print e.message
        return (score / score_total) * 5


def grade_number_5(assignment):
    """
    Test the functionality of the student's find_identifier function
    :param assignment: The student's assignment
    :return: The grade out of 2
    """
    if not hasattr(assignment, "find_identifier"):
        print "Submission does not contain a global find_identifier function"
        return 0

    score = 0.
    score_total = 3

    try:
        # Inject correct answers for previous questions from the solution
        solution.grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], ]
        assignment.grid = solution.grid
        assignment.empty_slots = solution.empty_slots
        assignment.random_position = solution.random_position
        assignment.add_random_number = solution.add_random_number

        new_position1 = assignment.add_random_number(board)
        new_position2 = assignment.add_random_number(board)
        attempt = assignment.find_identifier(board, *new_position1)
        answer = solution.find_identifier(board, *new_position1)
        if attempt == answer:
            score += 1
        else:
            print "find_identifier returned {} instead of {}".format(attempt, answer)

        attempt = assignment.find_identifier(board, *new_position2)
        answer = solution.find_identifier(board, *new_position2)
        if attempt == answer:
            score += 1
        else:
            print "find_identifier returned {} instead of {}".format(attempt, answer)

        empty_slot = assignment.random_position()
        attempt = assignment.find_identifier(board, *empty_slot)
        answer = solution.find_identifier(board, *empty_slot)
        if attempt == answer:
            score += 1
        else:
            print "find_identifier returned {} instead of {}".format(attempt, answer)
        return (score / score_total) * 2
    except Exception as e:
        print e.message
        return (score / score_total) * 2
    except SyntaxError as e:
        print e.message
        return (score / score_total) * 5


def grade_number_6(assignment):
    """
    Test the functionality of the student's update_grid function
    :param assignment: The student's assignment
    :return: The grade out of 7
    """

    if not hasattr(assignment, "update_grid"):
        print "Submission does not contain a global update_grid function"
        return 0

    score = 0.
    score_total = 12

    try:
        from copy import deepcopy

        # Inject correct answers for previous questions from the solution
        solution.grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], ]
        assignment.grid = solution.grid
        assignment.empty_slots = solution.empty_slots
        assignment.random_position = solution.random_position
        assignment.add_random_number = solution.add_random_number

        assignment.find_identifier = solution.find_identifier

        options_left = {(0, 1): [[0, 2, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], (0, 0):
            [[2, 2, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], (2, 0):
                            [[2, 0, 0, 0], [0, 0, 0, 0], [2, 0, 0, 0], [0, 0, 0, 0]]}

        for key, value in options_left.iteritems():
            assignment.grid,solution.grid = deepcopy(value),deepcopy(value)
            attempt = assignment.update_grid(key[0], key[1], solution.LEFT)
            assignment.grid,solution.grid = deepcopy(value),deepcopy(value)
            answer = solution.update_grid(key[0], key[1], solution.LEFT)
            if attempt != answer:
                print "update_grid returned {} instead of {} when updating position {} from {} to the Left".format(attempt,answer,key, assignment.grid)
                break
            score += 1

        options_right = {(0, 3): [[0, 2, 0, 2], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], (0, 1):
            [[2, 2, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], (2, 3):
                             [[2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 2], [0, 0, 0, 0]]}

        for key, value in options_right.iteritems():
            assignment.grid,solution.grid = deepcopy(value),deepcopy(value)
            attempt = assignment.update_grid(key[0], key[1], solution.RIGHT)
            assignment.grid,solution.grid = deepcopy(value),deepcopy(value)
            answer = solution.update_grid(key[0], key[1], solution.RIGHT)
            if attempt != answer:
                print "update_grid returned {} instead of {} when updating position {} from {} to the Right".format(attempt,answer, key, assignment.grid)
                break
            score += 1

        options_up = {(0, 1): [[0, 2, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], (2, 1):
            [[2, 2, 0, 0], [0, 0, 0, 0], [0, 2, 0, 0], [0, 0, 0, 0]], (0, 3):
                          [[2, 4, 0, 4], [0, 0, 0, 0], [0, 0, 0, 0], [0, 2, 0, 0]]}

        for key, value in options_up.iteritems():
            assignment.grid,solution.grid = deepcopy(value),deepcopy(value)
            attempt = assignment.update_grid(key[0], key[1], solution.UP)
            assignment.grid,solution.grid = deepcopy(value),deepcopy(value)
            answer = solution.update_grid(key[0], key[1], solution.UP)
            if attempt != answer:
                print "update_grid returned {} instead of {} when updating position {} from {} to the Up".format(attempt,answer,key, assignment.grid)
                break
            score += 1

        options_down = {(0, 1): [[0, 2, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], (2, 1):
            [[2, 2, 0, 0], [0, 0, 0, 0], [0, 0, 2, 0], [0, 0, 0, 0]], (3, 2):
                            [[2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 2, 0, 0]]}

        for key, value in options_down.iteritems():
            assignment.grid,solution.grid = deepcopy(value),deepcopy(value)
            attempt = assignment.update_grid(key[0], key[1], solution.DOWN)
            assignment.grid,solution.grid = deepcopy(value),deepcopy(value)
            answer = solution.update_grid(key[0], key[1], solution.DOWN)
            if attempt != answer:
                print "update_grid returned {} instead of {} when updating position {} from {} to the Down".format(attempt,answer,key, assignment.grid)
                break
            score += 1

        return (score / score_total) * 7
    except Exception as e:
        print e.message
        return (score / score_total) * 7
    except SyntaxError as e:
        print e.message
        return (score / score_total) * 5


def grade_number_7(assignment):
    """
    Test the functionality of the student's animate_movement function. This function was given to them
    no comprehensive test done in the interest of time to submit the grades.
    :param assignment: The student's assignment
    :return: A discrete grade of out of 7
    """

    if not hasattr(assignment, "animate_movement"):
        print "Submission does not contain a global animate_movement function"
        return 0

    score = 0.
    score_total = 1

    try:
        # Inject correct answers for previous questions from the solution
        solution.grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], ]
        assignment.grid = solution.grid
        assignment.empty_slots = solution.empty_slots
        assignment.random_position = solution.random_position
        assignment.add_random_number = solution.add_random_number

        assignment.find_identifier = solution.find_identifier
        assignment.update_grid = solution.update_grid

        assignment.add_random_number_at = solution.add_random_number_at

        assignment.add_random_number_at(board, 0, 0)

        assignment.move_all_right = solution.move_all_right
        assignment.merge = solution.merge
        assignment.move_all_right(board)

        score += 1

        return (score / score_total) * 12
    except Exception as e:
        print e.message
        return (score / score_total) * 12
    except SyntaxError as e:
        print e.message
        return (score / score_total) * 5


# def grade_number_8(assignment):
#     """
#     Test the functionality of the student's move function
#     :param assignment: The student's assignment
#     :return: The grade out of 6
#     """
#
#     def test_recursion(move, params):
#         detector = RecursionDetector()
#         detector.set_trace()
#         try:
#             move(*params)
#         except RecursionDetectedException:
#             return True
#         else:
#             return False
#         finally:
#             sys.settrace(None)
#
#     if not hasattr(assignment, "move"):
#         return 0
#
#     score = 0.
#     score_total = 5
#
#     try:
#         from copy import deepcopy
#
#         # Inject correct answers for previous questions from the solution
#         assignment.grid = deepcopy(solution.grid)
#         assignment.empty_slots = solution.empty_slots
#         assignment.random_position = solution.random_position
#         assignment.add_random_number = solution.add_random_number
#
#         assignment.find_identifier = solution.find_identifier
#         assignment.update_grid = solution.update_grid
#
#         assignment.add_random_number_at = solution.add_random_number_at
#
#         assignment.add_random_number_at(board, 0, 0)
#
#         assignment.animate_movement = solution.animate_movement
#
#         key = assignment.find_identifier(board, 0, 0)
#
#         # Test if the function is recursive
#         if test_recursion(assignment.move, [board, key, solution.RIGHT]):
#             score += 3
#         else:
#             print "Function is not recursive"
#
#         board.numbers = {}
#         assignment.grid = deepcopy(solution.grid)
#         assignment.add_random_number_at(board, 0, 0)
#         key = assignment.find_identifier(board, 0, 0)
#         assignment.move(board, key, solution.RIGHT)
#         if assignment.grid[0][3] != 0:
#             score += 2
#         else:
#             print "grid is {} and does not have value at position (0,3) when it should".format(assignment.grid)
#         return (score / score_total) * 6
#     except Exception as e:
#         print "Exception:" + e.message
#         return (score / score_total) * 6
#     except SyntaxError as e:
#         print e.message
#         return (score / score_total) * 5


def grade_number_9(assignment):
    """
    Test the functionality of the student's move_all_down function
    :param assignment: The student's assignment
    :return: The grade out of 5
    """

    if not hasattr(assignment, "move_all_down"):
        print "Submission does not contain a global move_all_down function"
        return 0

    score = 0.
    score_total = 4

    try:
        # Inject correct answers for previous questions from the solution
        solution.grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], ]
        assignment.grid = solution.grid
        assignment.empty_slots = solution.empty_slots
        assignment.random_position = solution.random_position
        assignment.add_random_number = solution.add_random_number

        assignment.find_identifier = solution.find_identifier
        assignment.update_grid = solution.update_grid
        assignment.merge = solution.merge

        assignment.add_random_number_at = solution.add_random_number_at

        positions = [(0, 0), (0, 1), (0, 2), (0, 3), ]

        map(lambda position: assignment.add_random_number_at(board, *position), positions)

        assignment.animate_movement = solution.animate_movement
        assignment.move = solution.move

        assignment.move_all_down(board)

        results = filter(lambda position: assignment.grid[position[0] + 3][position[1]] == 0, positions)
        if not results:
            score += 4
        else:
            score += (score_total - len(results))
            print "Grid is {} and positions tested were {} hence not all positions were moved correctly Down".format(
                assignment.grid, positions)

        return (score / score_total) * 5
    except Exception as e:
        print e.message
        return (score / score_total) * 5
    except SyntaxError as e:
        print e.message
        return (score / score_total) * 5


def grade_number_10(assignment):
    """
    Test the functionality of the student's move_all_up function
    :param assignment: The student's assignment
    :return: The grade out of 5
    """

    if not hasattr(assignment, "move_all_up"):
        print "Submission does not contain a global move_all_up function"
        return 0

    score = 0.
    score_total = 4

    try:
        # Inject correct answers for previous questions from the solution
        solution.grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], ]
        assignment.grid = solution.grid
        assignment.empty_slots = solution.empty_slots
        assignment.random_position = solution.random_position
        assignment.add_random_number = solution.add_random_number

        assignment.find_identifier = solution.find_identifier
        assignment.update_grid = solution.update_grid

        assignment.add_random_number_at = solution.add_random_number_at
        assignment.merge = solution.merge

        positions = [(3, 0), (3, 1), (3, 2), (3, 3), ]

        map(lambda position: assignment.add_random_number_at(board, *position), positions)

        assignment.animate_movement = solution.animate_movement
        assignment.move = solution.move

        assignment.move_all_up(board)

        results = filter(lambda position: assignment.grid[position[0] - 3][position[1]] == 0, positions)
        if not results:
            score += 4
        else:
            score += (score_total - len(results))
            print "Grid is {} and positions tested were {} hence not all positions were moved correctly Up".format(
                assignment.grid, positions)

        return (score / score_total) * 5
    except Exception as e:
        print e.message
        return (score / score_total) * 5
    except SyntaxError as e:
        print e.message
        return (score / score_total) * 5


def grade_number_11(assignment):
    """
    Test the functionality of the student's move_all_right function
    :param assignment: The student's assignment
    :return: The grade out of 5
    """

    if not hasattr(assignment, "move_all_right"):
        print "Submission does not contain a global move_all_right function"
        return 0

    score = 0.
    score_total = 4

    try:
        # Inject correct answers for previous questions from the solution
        solution.grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], ]
        assignment.grid = solution.grid
        assignment.empty_slots = solution.empty_slots
        assignment.random_position = solution.random_position
        assignment.add_random_number = solution.add_random_number

        assignment.find_identifier = solution.find_identifier
        assignment.update_grid = solution.update_grid

        assignment.add_random_number_at = solution.add_random_number_at
        assignment.merge = solution.merge

        positions = [(0, 0), (1, 0), (2, 0), (3, 0), ]

        map(lambda position: assignment.add_random_number_at(board, *position), positions)

        assignment.animate_movement = solution.animate_movement
        assignment.move = solution.move

        assignment.move_all_right(board)

        results = filter(lambda position: assignment.grid[position[0]][position[1] + 3] == 0, positions)
        if not results:
            score += 4
        else:
            score += (score_total - len(results))
            print "Grid is {} and positions tested were {} hence not all positions were moved correctly Right".format(
                assignment.grid, positions)

        return (score / score_total) * 5
    except Exception as e:
        print e.message
        return (score / score_total) * 5
    except SyntaxError as e:
        print e.message
        return (score / score_total) * 5


def grade_number_12(assignment):
    """
    Test the functionality of the student's move_all_down function
    :param assignment: The student's assignment
    :return: The grade out of 5
    """

    if not hasattr(assignment, "move_all_left"):
        print "Submission does not contain a global move_all_left function"
        return 0

    score = 0.
    score_total = 4

    try:
        # Inject correct answers for previous questions from the solution
        solution.grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], ]
        assignment.grid = solution.grid
        assignment.empty_slots = solution.empty_slots
        assignment.random_position = solution.random_position
        assignment.add_random_number = solution.add_random_number

        assignment.find_identifier = solution.find_identifier
        assignment.update_grid = solution.update_grid

        assignment.add_random_number_at = solution.add_random_number_at
        assignment.merge = solution.merge

        positions = [(0, 3), (1, 3), (2, 3), (3, 3), ]

        map(lambda position: assignment.add_random_number_at(board, *position), positions)

        assignment.animate_movement = solution.animate_movement
        assignment.move = solution.move

        assignment.move_all_left(board)

        results = filter(lambda position: assignment.grid[position[0]][position[1] - 3] == 0, positions)
        if not results:
            score += 4
        else:
            score += (score_total - len(results))
            print "Grid is {} and positions tested were {} hence not all positions were moved correctly left".format(
                assignment.grid, positions)

        return (score / score_total) * 5
    except Exception as e:
        print e.message
        return (score / score_total) * 5
    except SyntaxError as e:
        print e.message
        return (score / score_total) * 5


def grade_number_13(assignment):
    """
    Test the functionality of the student's move_all function
    :param assignment: The student's assignment
    :return: The grade out of 3
    """

    if not hasattr(assignment, "move_all"):
        print "Submission does not contain a global move_all function"
        return 0

    score = 0.
    score_total = 16

    try:
        # Inject correct answers for previous questions from the solution
        solution.grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], ]
        assignment.grid = solution.grid
        assignment.empty_slots = solution.empty_slots
        assignment.random_position = solution.random_position
        assignment.add_random_number = solution.add_random_number
        assignment.merge = solution.merge

        assignment.find_identifier = solution.find_identifier
        assignment.update_grid = solution.update_grid

        assignment.add_random_number_at = solution.add_random_number_at
        assignment.animate_movement = solution.animate_movement
        assignment.move = solution.move

        assignment.move_all_right = solution.move_all_right
        assignment.move_all_left = solution.move_all_left
        assignment.move_all_down = solution.move_all_down
        assignment.move_all_up = solution.move_all_up

        right_event = MockEvent("Right")
        left_event = MockEvent("Left")
        up_event = MockEvent("Up")
        down_event = MockEvent("Down")

        # Begin down test
        board.numbers = {}
        solution.grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], ]

        positions = [(0, 0), (0, 1), (0, 2), (0, 3), ]
        print board.numbers
        map(lambda position: assignment.add_random_number_at(board, *position), positions)
        print board.numbers
        assignment.move_all(board, down_event)

        results = filter(lambda position: assignment.grid[position[0] + 3][position[1]] == 0, positions)
        if not results:
            score += 4
        else:
            print "Grid is {} and positions tested were {} hence not all positions were moved correctly Down".format(
                assignment.grid, positions)

        # Begin up test
        map(lambda key: gui.remove_number(board, key),
            map(lambda position: assignment.find_identifier(board, *position), positions))
        board.numbers = {}
        solution.grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], ]

        positions = [(3, 0), (3, 1), (3, 2), (3, 3), ]

        map(lambda position: assignment.add_random_number_at(board, *position), positions)
        print board.numbers
        assignment.move_all(board, up_event)

        results = filter(lambda position: assignment.grid[position[0] - 3][position[1]] == 0, positions)
        if not results:
            score += 4
        else:
            print "Grid is {} and positions tested were {} hence not all positions were moved correctly up".format(
                assignment.grid, positions)

        map(lambda key: gui.remove_number(board, key),
            map(lambda position: assignment.find_identifier(board, *position), positions))

        board.numbers = {}
        solution.grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], ]

        print "Grid:{}".format(assignment.grid)
        # begin right test
        positions = [(0, 0), (1, 0), (2, 0), (3, 0), ]

        map(lambda position: assignment.add_random_number_at(board, *position), positions)
        print board.numbers
        assignment.move_all(board, right_event)
        results = filter(lambda position: assignment.grid[position[0]][position[1] + 3] == 0, positions)
        if not results:
            print "here"
            score += 4
        else:
            print "Grid is {} and positions tested were {} hence not all positions were moved correctly Right".format(
                assignment.grid, positions)

        map(lambda key: gui.remove_number(board, key),
            map(lambda position: assignment.find_identifier(board, *position), positions))

        board.numbers = {}
        solution.grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], ]

        # begin left test
        positions = [(0, 3), (1, 3), (2, 3), (3, 3), ]

        map(lambda position: assignment.add_random_number_at(board, *position), positions)

        assignment.move_all(board, left_event)

        results = filter(lambda position: assignment.grid[position[0]][position[1] - 3] == 0, positions)
        if not results:
            print "here"
            score += 4
        else:
            print "Grid is {} and positions tested were {} hence not all positions were moved correctly left".format(
                assignment.grid, positions)
        return (score / score_total) * 3
    except Exception as e:
        print e.message
        return (score / score_total) * 3
    except SyntaxError as e:
        print e.message
        return (score / score_total) * 3


def grade_number_14(assignment):
    """
    Test the functionality of the student's keyboard_callback function
    :param assignment: The student's assignment
    :return: The grade out of 7
    """

    if not hasattr(assignment, "keyboard_callback"):
        print "Submission does not contain a global keyboard_callback function"
        return 0

    score = 0.
    score_total = 12

    try:
        # Inject correct answers for previous questions from the solution
        solution.grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], ]
        assignment.grid = solution.grid
        assignment.empty_slots = solution.empty_slots
        assignment.random_position = solution.random_position
        assignment.add_random_number = solution.add_random_number

        assignment.find_identifier = solution.find_identifier
        assignment.update_grid = solution.update_grid

        assignment.add_random_number_at = solution.add_random_number_at
        assignment.animate_movement = solution.animate_movement
        assignment.move = solution.move
        assignment.merge = solution.merge

        assignment.move_all_right = solution.move_all_right
        assignment.move_all_left = solution.move_all_left
        assignment.move_all_down = solution.move_all_down
        assignment.move_all_up = solution.move_all_up
        assignment.move_all = solution.move_all

        up_event = MockEvent("Up")
        down_event = MockEvent("Down")

        # Begin down test
        positions = [(0, 0), (0, 1), (0, 2), (0, 3), ]

        map(lambda position: assignment.add_random_number_at(board, *position), positions)

        assignment.keyboard_callback(down_event, frame, board)

        results = filter(lambda position: assignment.grid[position[0] + 3][position[1]] == 0, positions)
        if not results:
            score += 2
        else:
            print "Grid is {} and positions tested were {} hence not all positions were moved correctly Down".format(
                assignment.grid, positions)

        if len(board.numbers) == 5:
            score += 5

        map(lambda key: gui.remove_number(board, key),
            map(lambda position: assignment.find_identifier(board, *position), positions))

        board.numbers = {}
        solution.grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], ]

        # Begin new number addition control test
        positions = [(0, 0), (0, 1), (0, 2), (0, 3), ]

        map(lambda position: assignment.add_random_number_at(board, *position), positions)

        assignment.keyboard_callback(up_event, frame, board)

        results = filter(lambda position: assignment.grid[position[0] + 3][position[1]] == 0, positions)
        if not results:
            score += 2
        else:
            print "Grid is {} and positions tested were {} hence not all positions were moved correctly Down".format(
                assignment.grid, positions)

        if len(board.numbers) == 4:
            score += 5

        return (score / score_total) * 5
    except Exception as e:
        print e.message
        return (score / score_total) * 5
    except SyntaxError as e:
        print e.message
        return (score / score_total) * 5


def grade_number_15(assignment):
    """
    Test the functionality of the student's move_all function
    :param assignment: The student's assignment
    :return: The grade out of 5
    """

    if not hasattr(assignment, "move_all"):
        print "Submission does not contain a global move_all function"
        return 0

    score = 0.
    score_total = 4

    try:
        pass
        return (score / score_total) * 5
    except Exception as e:
        print e.message
        return (score / score_total) * 5
    except SyntaxError as e:
        print e.message
        return (score / score_total) * 5


def grade_number_16(assignment):
    """
    Test the functionality of the student's move_all function
    :param assignment: The student's assignment
    :return: The grade out of 5
    """

    if not hasattr(assignment, "move_all"):
        print "Submission does not contain a global move_all function"
        return 0

    score = 0.
    score_total = 4

    try:
        pass
        return (score / score_total) * 5
    except Exception as e:
        print e.message
        return (score / score_total) * 5
    except SyntaxError as e:
        print e.message
        return (score / score_total) * 5


def grade_number_17(assignment):
    """
    Test the functionality of the student's move_all function
    :param assignment: The student's assignment
    :return: The grade out of 5
    """

    if not hasattr(assignment, "move_all"):
        print "Submission does not contain a global move_all function"
        return 0

    score = 0.
    score_total = 4

    try:
        pass
        return (score / score_total) * 5
    except Exception as e:
        print e.message
        return (score / score_total) * 5
    except SyntaxError as e:
        print e.message
        return (score / score_total) * 5


def grade_number_18(assignment):
    """
    Test the functionality of the student's move_all function
    :param assignment: The student's assignment
    :return: The grade out of 5
    """

    if not hasattr(assignment, "move_all"):
        print "Submission does not contain a global move_all function"
        return 0

    score = 0.
    score_total = 4

    try:
        pass
        return (score / score_total) * 5
    except Exception as e:
        print e.message
        return (score / score_total) * 5
    except SyntaxError as e:
        print e.message
        return (score / score_total) * 5


def grade_number_19(assignment):
    """
    Test the functionality of the student's move_all function
    :param assignment: The student's assignment
    :return: The grade out of 5
    """

    if not hasattr(assignment, "move_all"):
        print "Submission does not contain a global move_all function"
        return 0

    score = 0.
    score_total = 4

    try:
        pass
        return (score / score_total) * 5
    except Exception as e:
        print e.message
        return (score / score_total) * 5
    except SyntaxError as e:
        print e.message
        return (score / score_total) * 5


def grade_number_20(assignment):
    """
    Test the functionality of the student's move_all function
    :param assignment: The student's assignment
    :return: The grade out of 5
    """

    if not hasattr(assignment, "move_all"):
        print "Submission does not contain a global move_all function"
        return 0

    score = 0.
    score_total = 4

    try:
        pass
        return (score / score_total) * 5
    except Exception as e:
        print e.message
        return (score / score_total) * 5
    except SyntaxError as e:
        print e.message
        return (score / score_total) * 5


def grade_number_21(assignment):
    """
    Test the functionality of the student's move_all function
    :param assignment: The student's assignment
    :return: The grade out of 5
    """

    if not hasattr(assignment, "move_all"):
        print "Submission does not contain a global move_all function"
        return 0

    score = 0.
    score_total = 4

    try:
        pass
        return (score / score_total) * 5
    except Exception as e:
        print e.message
        return (score / score_total) * 5
    except SyntaxError as e:
        print e.message
        return (score / score_total) * 5


if __name__ == "__main__":

    assignments = sys.argv[1:]

    count = 0
    for assign in assignments:
        total = 0
        print "\n\nAssignment {}\n".format(count)
        print "\n" + assign + "\n"

        student_assignment = load_source('comp1127', assign)

        print "Problem 1: {}/1".format(grade_number_1(assignment=student_assignment))

        student_assignment = load_source('comp1127', assign)

        print "Problem 2: {}/2".format(grade_number_2(assignment=student_assignment))

        student_assignment = load_source('comp1127', assign)

        print "Problem 3: {}/1".format(grade_number_3(assignment=student_assignment))

        student_assignment = load_source('comp1127', assign)

        print "Problem 4: {}/3".format(grade_number_4(assignment=student_assignment))

        student_assignment = load_source('comp1127', assign)

        print "Problem 5: {}/2".format(grade_number_5(assignment=student_assignment))

        student_assignment = load_source('comp1127', assign)

        print "Problem 6: {}/7".format(grade_number_6(assignment=student_assignment))

        student_assignment = load_source('comp1127', assign)

        print "Problem 7: {}/12".format(grade_number_7(assignment=student_assignment))
        #
        # student_assignment = load_source('comp1127', assign)
        #
        # print "Problem 8: {}/6".format(str(grade_number_8(assignment=student_assignment)))

        student_assignment = load_source('comp1127', assign)

        print "Problem 9: {}/5".format(grade_number_9(assignment=student_assignment))

        student_assignment = load_source('comp1127', assign)

        print "Problem 10: {}/5".format(grade_number_10(assignment=student_assignment))

        student_assignment = load_source('comp1127', assign)

        print "Problem 11: {}/5".format(grade_number_11(assignment=student_assignment))

        student_assignment = load_source('comp1127', assign)

        print "Problem 12: {}/5".format(grade_number_12(assignment=student_assignment))

        student_assignment = load_source('comp1127', assign)

        print "Problem 13: {}/3".format(grade_number_13(assignment=student_assignment))

        student_assignment = load_source('comp1127', assign)

        print "Problem 14: {}/3".format(grade_number_14(assignment=student_assignment))

        count += 1
