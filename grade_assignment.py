import imp
import gui

try:
    solution = imp.load_source('students', 'solution.py')
    frame, board = gui.setup()
except Exception:
    raise Exception("Error setting up program to grade")


def grade_number_1(assignment):
    """
    Checks to see if the grid is the 4 dimensional list of lists globally
    :param assignment: The student's assignment
    :return: The grade out of 1
    """
    if hasattr(assignment, "grid"):
        if assignment.grid == [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], ]:
            return 1
    return 0


def grade_number_2(assignment):
    """
    Tests the functionality of the student's empty_slot() function
    :param assignment: The student's assignment
    :return: The grade out of 2
    """

    if not hasattr(assignment, "empty_slots"):
        return 0

    score = 0.
    score_total = 5

    try:
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


def grade_number_3(assignment):
    """
    Test the functionality of the students random_position function
    :param assignment: The student's assignment
    :return: The grade out of 1
    """

    if not hasattr(assignment, "random_position"):
        return 0

    score = 0.
    score_total = 3

    try:
        from copy import deepcopy

        # Inject correct answers for previous questions from the solution
        assignment.grid = deepcopy(solution.grid)
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
        solution.grid = deepcopy(assignment.grid)
        empty_slot = assignment.random_position()
        if empty_slot == (2, 3):
            score += 1
        else:
            print "random_position() returned {} instead of {} when grid is {}".format(empty_slot, "(2,3)",
                                                                                       assignment.grid)

        assignment.grid = [[0, 2, 2, 0], [2, 2, 2, 2], [2, 2, 2, 2], [2, 2, 2, 2], ]
        solution.grid = deepcopy(assignment.grid)

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


def grade_number_4(assignment):
    """
    Tests the functionality of the student's add_random_number function
    :param assignment: The student's assignment
    :return: The grade out of 3
    """

    if not hasattr(assignment, "add_random_number"):
        return 0

    score = 0.
    score_total = 5

    try:
        from copy import deepcopy

        # Inject correct answers for previous questions from the solution
        assignment.grid = deepcopy(solution.grid)
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
            print "Both positions for the numbers were equal"

        assignment.grid = deepcopy(solution.grid)
        if (assignment.grid[new_position1[0]][new_position1[1]] == 2 or assignment.grid[new_position1[0]][
            new_position1[1]] == 4) and (
                        assignment.grid[new_position2[0]][new_position2[1]] == 2 or assignment.grid[new_position2[0]][
                    new_position2[1]] == 2):
            score += 1
        else:
            print "Grid does not contain either a 2 or a 4 for positions {} and {}".format(new_position1, new_position2)

        if len(board.numbers) == 2:
            score += 2

        return (score / score_total) * 3
    except Exception as e:
        print e.message
        return (score / score_total) * 3


def grade_number_5(assignment):
    """
    Test the functionality of the student's find_identifier function
    :param assignment: The student's assignment
    :return: The grade out of 2
    """
    if not hasattr(assignment, "find_identifier"):
        return 0

    score = 0.
    score_total = 3

    try:
        from copy import deepcopy

        # Inject correct answers for previous questions from the solution
        assignment.grid = deepcopy(solution.grid)
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


def grade_number_6(assignment):
    """
    Test the functionality of the student's update_grid function
    :param assignment: The student's assignment
    :return: The grade out of 7
    """

    if not hasattr(assignment, "update_grid"):
        return 0

    score = 0.
    score_total = 5

    try:
        from copy import deepcopy

        # Inject correct answers for previous questions from the solution
        assignment.grid = deepcopy(solution.grid)
        assignment.empty_slots = solution.empty_slots
        assignment.random_position = solution.random_position
        assignment.add_random_number = solution.add_random_number

        new_position1 = assignment.add_random_number(board)
        new_position2 = assignment.add_random_number(board)

        assignment.find_identifier = solution.find_identifier
        return (score / score_total) * 7
    except Exception as e:
        print e.message
        return (score / score_total) * 7


def grade_number_7(assignment):
    """
    Test the functionality of the student's update_grid function
    :param assignment: The student's assignment
    :return: The grade out of 7
    """

    if not hasattr(assignment, "update_grid"):
        return 0

    score = 0.
    score_total = 5

    try:
        pass
        return (score / score_total) * 7
    except Exception as e:
        print e.message
        return (score / score_total) * 7


def grade_number_8(assignment):
    """
    Test the functionality of the student's update_grid function
    :param assignment: The student's assignment
    :return: The grade out of 7
    """

    if not hasattr(assignment, "update_grid"):
        return 0

    score = 0.
    score_total = 5

    try:
        pass
        return (score / score_total) * 7
    except Exception as e:
        print e.message
        return (score / score_total) * 7


def grade_number_9(assignment):
    """
    Test the functionality of the student's update_grid function
    :param assignment: The student's assignment
    :return: The grade out of 7
    """

    if not hasattr(assignment, "update_grid"):
        return 0

    score = 0.
    score_total = 5

    try:
        pass
        return (score / score_total) * 7
    except Exception as e:
        print e.message
        return (score / score_total) * 7


if __name__ == "__main__":
    import sys
    import gui

    assignments = sys.argv[1:]

    total = 0
    print assignments[0]

    student_assignment = imp.load_source('students', assignments[0])

    print "Problem 1: {}".format(grade_number_1(assignment=student_assignment))

    student_assignment = imp.load_source('students', assignments[0])

    print "Problem 2: {}".format(grade_number_2(assignment=student_assignment))

    student_assignment = imp.load_source('students', assignments[0])

    print "Problem 3: {}".format(grade_number_3(assignment=student_assignment))

    student_assignment = imp.load_source('students', assignments[0])

    print "Problem 4: {}".format(grade_number_4(assignment=student_assignment))

    student_assignment = imp.load_source('students', assignments[0])

    print "Problem 5: {}".format(grade_number_5(assignment=student_assignment))

    student_assignment = imp.load_source('students', assignments[0])

    print "Problem 6: {}".format(grade_number_6(assignment=student_assignment))
