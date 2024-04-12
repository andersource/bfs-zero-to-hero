##############################################################################
#
#               BFS zero-to-hero part 4:   escape from the fort
#               -----------------------------------------------
#
##############################################################################
##############################################################################

from enum import Enum
from copy import deepcopy


class Character(Enum):
    """
    Characters in puzzle (including the weight)
    """
    WEIGHT = 25
    AMELIA = 50
    OLIVIA = 75
    LUCAS = 125


class Action(Enum):
    """
    Possible actions to take (loading / unloading the pulley, lowering it)
    """
    LOWER_PULLEY = 1
    LOAD_UP = 2
    UNLOAD_UP = 3
    LOAD_DOWN = 4
    UNLOAD_DOWN = 5


class State:
    """
    Object representing puzzle state in a given moment
    """
    def __init__(self):
        """
        Fresh puzzle state
        """
        self.up = set(Character)
        self.down = set()
        self.pulley_end1 = set()
        self.pulley_end2 = set()
        self.pulley_end1_up = True

    def apply(self, action, character):
        """
        Attempt to apply action in current puzzle state.
        In-place, raises AssertionError / ValueError if action isn't possible.
        :param action: Action to perform
        :param character: Character to perform action with, should be `None` if lowering pulley
        """
        if action == Action.LOWER_PULLEY and character is not None:
            raise ValueError("Lowering pulley doesn't involve a character")
        if action != Action.LOWER_PULLEY and character is None:
            raise ValueError("Any action other than lowering pulley involves a character")

        match action:
            case Action.LOWER_PULLEY:
                weight_diff = sum(x.value for x in self.pulley_end1) - sum(x.value for x in self.pulley_end2)
                if not self.pulley_end1_up:
                    weight_diff *= -1

                assert weight_diff == 25, "Can only lower pulley if weight difference is 25 kg"
                self.pulley_end1_up = not self.pulley_end1_up
            case Action.LOAD_UP:
                assert character in self.up, f"{character} not available for loading up"
                if character == Character.WEIGHT and len(self.up) == 1:
                    raise ValueError("No one available to load weight up")

                self.up.remove(character)
                pulley_end = self.pulley_end1 if self.pulley_end1_up else self.pulley_end2
                pulley_end.add(character)
            case Action.LOAD_DOWN:
                assert character in self.down, f"{character} not available for loading down"
                if character == Character.WEIGHT and len(self.down) == 1:
                    raise ValueError("No one available to load weight down")

                self.down.remove(character)
                pulley_end = self.pulley_end2 if self.pulley_end1_up else self.pulley_end1
                pulley_end.add(character)
            case Action.UNLOAD_UP:
                pulley_end = self.pulley_end1 if self.pulley_end1_up else self.pulley_end2
                assert character in pulley_end, f"{character} not available for unloading up"
                if character == Character.WEIGHT and len(self.up) == 0:
                    raise ValueError("No one available to unload weight up")

                pulley_end.remove(character)
                self.up.add(character)
            case Action.UNLOAD_DOWN:
                pulley_end = self.pulley_end2 if self.pulley_end1_up else self.pulley_end1
                assert character in pulley_end, f"{character} not available for unloading down"
                if character == Character.WEIGHT and len(self.down) == 0:
                    raise ValueError("No one available to unload weight down")

                pulley_end.remove(character)
                self.down.add(character)

    def __str__(self):
        """
        :return: String representation of puzzle state
        """
        up = sorted(tuple(self.up), key=lambda x: x.value)
        down = sorted(tuple(self.down), key=lambda x: x.value)
        pulley_end1 = sorted(tuple(self.pulley_end1), key=lambda x: x.value)
        pulley_end2 = sorted(tuple(self.pulley_end2), key=lambda x: x.value)
        return  (f"Up: {up}, down: {down}, pulley end 1: {pulley_end1},"
                 f" pulley end 2: {pulley_end2}, pulley end 1 up? {self.pulley_end1_up}")


def find_solution():
    # Return value:     List of (Action, Character) tuples to solve the puzzle
    raise NotImplementedError()


##############################################################################
########################    behind-the-scenes code    ########################
##############################################################################
def main():
    curr_state = State()

    for action, character in find_solution():
        print(f"{curr_state}, action: {(action, character)}")
        curr_state.apply(action, character)

    print(curr_state)
    if {Character.OLIVIA, Character.AMELIA, Character.LUCAS}.issubset(curr_state.down):
        print("Fort escaped, well done!")


if __name__ == "__main__":
    main()
