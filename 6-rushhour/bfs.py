##############################################################################
#
#                   BFS zero-to-hero part 6:   Rush hour
#                   ------------------------------------
#
##############################################################################
##############################################################################

from enum import Enum


CELLS = 6


class Direction(Enum):
    """
    Directions on the board
    """
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


class Orientation(Enum):
    """
    Vehicle orientation
    """
    HORIZONTAL = (0, 1)
    VERTICAL = (1, 0)


def find_instructions(board):
    # Params:
    #   board:          List of dictionaries describing current board state. Each dict is of the form:
    #                   {
    #                       "cell": [[2, 1], [2, 2]]   # Positions occupied by vehicle ([y, x])
    #                       "color": [143, 114, 164]   # Vehicle color ([r, g, b])
    #                       "orientation": <Orientation.HORIZONTAL>  # Vehicle orientation
    #                   }
    #                   The player's car is the reddest of them all :)
    #
    # Return value:     List of tuples of (vehicle_index, <Direction>) to move the vehicles
    #                   in order to solve the puzzle.
    #
    raise NotImplementedError()
