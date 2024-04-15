##############################################################################
#
#                   BFS zero-to-hero part 5:   15 puzzle
#                   ------------------------------------
#
##############################################################################
##############################################################################

from enum import Enum
from copy import deepcopy


class Direction(Enum):
    """
    Directions on the board
    """
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


def solved(board):
    """
    Check whether the desired board configuration has been achieved
    :param board: Board to check
    :return: True if board is solved, otherwise False
    """
    return sum(board, [])[:-1] == list(range(1, 16))


def apply_action(board, direction):
    """
    Applies action on board, i.e. "moves" the empty square in the direction specified.
    Creates a new copy of the board.
    :param board: Board to apply action to
    :param direction: Direction to move empty square
    :return: New board
    """
    empty_row, empty_col = find_empty_pos(board)
    drow, dcol = direction.value
    new_row = empty_row + drow
    new_col = empty_col + dcol
    new_board = deepcopy(board)
    if 0 <= new_row < len(board) and 0 <= new_col < len(board[0]):
        new_board[empty_row][empty_col] = board[new_row][new_col]
        new_board[new_row][new_col] = 0

    return new_board


def find_empty_pos(board):
    """
    Finds position (row, col) of empty square in board
    :param board: Board to examine
    :return: (row, col) tuple of empty square position
    """
    return [(row, col)
            for row in range(len(board)) for col in range(len(board[0]))
            if board[row][col] == 0][0]


def find_instructions(board):
    # Params:
    #   board:          Nested list describing current board state. List of list of ints,
    #                   each number denotes itself except 0 which denotes the empty square.
    #
    # Return value:     List of <Direction>s to move the empty square in order to solve the puzzle.
    #                   Note that we're treating the empty square as if it's moving around, even
    #                   though in practice it's other squares that are moving onto the empty one.
    #
    raise NotImplementedError()


##############################################################################
########################    behind-the-scenes code    ########################
##############################################################################
import pygame
import json
import os


FPS = 40
ACTION_FRAMES = 10
W, H = 1200, 720
BOARD_SIZE = 600
SQUARE_COLORS = [
    [72, 35, 116],
    [69, 54, 129],
    [63, 71, 136],
    [56, 87, 140],
    [49, 102, 141],
    [43, 116, 142],
    [37, 130, 142],
    [32, 144, 140],
    [30, 157, 136],
    [37, 171, 129],
    [54, 184, 119],
    [81, 196, 104],
    [114, 207, 85],
    [149, 215, 63],
    [189, 222, 38]
]
TEXT_COLOR = BACKGROUND_COLOR = (222, 220, 230)
MARGIN = 3


def run_test_case(filename):
    with open(filename, 'r') as f:
        board = json.load(f)

    instructions = find_instructions(board)

    pygame.init()
    pygame.font.init()
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 112)

    board_start_x = W // 2 - BOARD_SIZE // 2
    board_start_y = H // 2 - BOARD_SIZE // 2
    square_size = BOARD_SIZE / len(board)

    pygame.display.set_caption("15 puzzle")
    window_surface = pygame.display.set_mode((W, H))

    background = pygame.Surface((W, H))
    background.fill(pygame.Color(BACKGROUND_COLOR))

    is_running = True

    delay = FPS * 2
    phase = 0
    curr_action = moving_row = moving_col = None
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

        window_surface.blit(background, (0, 0))
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] == 0:
                    continue

                col_offset = row_offset = 0
                if moving_row == row and moving_col == col:
                    row_offset = -curr_action.value[0] * phase / ACTION_FRAMES
                    col_offset = -curr_action.value[1] * phase / ACTION_FRAMES

                square_x = board_start_x + (col + col_offset) * square_size + MARGIN
                square_y = board_start_y + (row + row_offset) * square_size + MARGIN

                pygame.draw.rect(window_surface, SQUARE_COLORS[board[row][col] - 1],
                                 (square_x, square_y, round(square_size - 2 * MARGIN), round(square_size - 2 * MARGIN)))
                num = font.render(str(board[row][col]), True, TEXT_COLOR)
                text_x = round(square_x + (square_size - 2 * MARGIN) / 2 - num.get_width() / 2)
                text_y = round(square_y + (square_size - 2 * MARGIN) / 2 - num.get_height() / 2)
                window_surface.blit(num, (text_x, text_y))

        pygame.display.update()

        if delay > 0 or (len(instructions) == 0 and curr_action is None):
            delay -= 1

        if delay == 0 and (len(instructions) > 0 or curr_action is not None):
            if curr_action is None:
                curr_action = instructions.pop(0)
                empty_row, empty_col = find_empty_pos(board)
                moving_row = empty_row + curr_action.value[0]
                moving_col = empty_col + curr_action.value[1]

            if phase == ACTION_FRAMES - 1:
                board = apply_action(board, curr_action)
                phase = 0
                curr_action = None
            else:
                phase += 1

        if delay == -FPS * 2:
            is_running = False

        clock.tick(FPS)


def main():
    for i in range(1, 4):
        print(f"Solving {i}...")
        run_test_case(os.path.join("boards", f"{i}.json"))


if __name__ == '__main__':
    main()
