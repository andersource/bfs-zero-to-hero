##############################################################################
#
#                    BFS zero-to-hero part 3:   water jugs
#                    -------------------------------------
#
##############################################################################
##############################################################################

from enum import Enum


class Action(Enum):
    """
    Possible actions to take (emptying jugs, filling them etc.)
    """
    EMPTY_1 = 1
    EMPTY_2 = 2
    FILL_1 = 3
    FILL_2 = 4
    POUR_1_TO_2 = 5
    POUR_2_TO_1 = 6


def apply_action(jug1, jug2, curr_jugs, action):
    """
    Return state after applying action to some state of jugs
    :param jug1: Maximum capacity of jug 1
    :param jug2: Maximum capacity of jug 2
    :param curr_jugs: int tuple (j1, j2) of current amounts in the two jugs
    :param action: Action to apply
    :return: int tuple (j1, j2) of amounts in the two jugs after applying `action`
    """
    curr_buck1, curr_buck2 = curr_jugs
    match action:
        case Action.FILL_1:
            curr_buck1 = jug1
        case Action.FILL_2:
            curr_buck2 = jug2
        case Action.EMPTY_1:
            curr_buck1 = 0
        case Action.EMPTY_2:
            curr_buck2 = 0
        case Action.POUR_1_TO_2:
            pour_amount = min(curr_buck1, jug2 - curr_buck2)
            curr_buck1 -= pour_amount
            curr_buck2 += pour_amount
        case Action.POUR_2_TO_1:
            pour_amount = min(curr_buck2, jug1 - curr_buck1)
            curr_buck1 += pour_amount
            curr_buck2 -= pour_amount

    return curr_buck1, curr_buck2


def plan(jug1, jug2, goal):
    # Params:
    #   jug 1 (int):    Maximum capacity in jug 1
    #   jug 2 (int):    Maximum capacity in jug 2
    #   goal (int):     Desired water amount
    #
    # Return value:     List of <Action>s to be taken to obtain
    #                   the desired amount in any of the jugs
    raise NotImplementedError()


##############################################################################
########################    behind-the-scenes code    ########################
##############################################################################
def run_test_case(jug1, jug2, goal, possible=True, verbose=True):
    if verbose:
        print(f"Running test case: jug 1 capacity = {jug1}, jug 2 capacity = {jug2}, goal = {goal}")
    actions = plan(jug1, jug2, goal)
    if not possible:
        assert actions is None, "Case shouldn't be possible -- return `None`"
        if verbose:
            print("Case not possible, `None` returned")
            print("\n\n")

        return

    if actions is None:
        raise Exception("Case is possible -- return list of <Action>s")

    jugs = (0, 0)
    for action in actions:
        if verbose:
            print(f"Current state: {jugs}, taking action: {action}")

        jugs = apply_action(jug1, jug2, jugs, action)

    if verbose:
        print(f"Current state: {jugs}")
        print("\n\n")

    assert goal in jugs, f"Goal ({goal}) not in jugs ({jugs[0]}, {jugs[1]}) after plan execution"


def main(verbose=True):
    run_test_case(3, 5, 4, verbose=verbose)
    run_test_case(5, 7, 6, verbose=verbose)
    run_test_case(4, 6, 3, possible=False, verbose=verbose)

    print("All test cases passed!")


if __name__ == "__main__":
    main()
