##############################################################################
##################    BFS zero-to-hero part 6: Rush hour    ##################
##########################    Run from this file    ##########################
##############################################################################


def main():
    pygame.init()
    clock = pygame.time.Clock()

    pygame.display.set_caption('Rushhour solver')
    window_surface = pygame.display.set_mode((W, H))

    run_challenge(window_surface, clock, 1)
    run_challenge(window_surface, clock, 2)
    # run_challenge(window_surface, clock, 3)  # Could take a (relatively) long time to solve
    run_challenge(window_surface, clock, 4)


##############################################################################
########################    behind-the-scenes code    ########################
##############################################################################
import json
import pygame
from copy import deepcopy
from bfs import find_instructions, Orientation, Direction, CELLS


W, H = 600, 600
BACKGROUND_COLOR = '#cccccc'
LINE_COLOR = '#666666'
LINE_WIDTH = 4
FPS = 30
TRANSITION_FRAMES = FPS // 4
CELL_SIZE = W / CELLS


def preprocess(board_state):
    for car in board_state:
        car['orientation'] = (
            Orientation.HORIZONTAL if car['cells'][0][0] == car['cells'][1][0] else Orientation.VERTICAL
        )

    return board_state


def test_instruction(board, instruction):
    try:
        car = board[instruction[0]]
        orient = Orientation.HORIZONTAL if car['cells'][0][0] == car['cells'][1][0] else Orientation.VERTICAL
        if orient.value[0] * instruction[1].value[0] + orient.value[1] * instruction[1].value[1] == 0:
            return False

        board = deepcopy(board)
        apply_instruction(board, instruction)

        all_cells = list(map(tuple, sum([car['cells'] for car in board], [])))

        return (
                len(all_cells) == len(set(all_cells))
                and min([min(c) for c in all_cells]) >= 0
                and max([max(c) for c in all_cells]) < CELLS
        )
    except:
        return False


def test_win(board):
    redcar = sorted(
        [(car, car['color'][0] / max(car['color'][1:])) for car in board], key=lambda x: x[1],
        reverse=True
    )[0][0]

    return set(list(map(tuple, redcar['cells']))) == {(2, 4), (2, 5)}


def apply_instruction(board, instruction):
    for idx, car in enumerate(board):
        if idx != instruction[0]:
            continue

        direction = instruction[1]
        car['cells'] = [(cy + direction.value[0], cx + direction.value[1]) for cy, cx in car['cells']]


def run_challenge(window_surface, clock, idx):
    with open(f'challenges/{idx}.json', 'r') as f:
        board_state = preprocess(json.load(f))

    instructions = find_instructions(board_state)

    background = pygame.Surface((W, H))
    background.fill(pygame.Color(BACKGROUND_COLOR))

    for i in range(CELLS + 1):
        pygame.draw.line(background, pygame.Color(LINE_COLOR),
                         (0, i * (H - LINE_WIDTH) / CELLS + LINE_WIDTH // 3),
                         (W, i * (H - LINE_WIDTH) / CELLS + LINE_WIDTH // 3),
                         LINE_WIDTH)

        pygame.draw.line(background, pygame.Color(LINE_COLOR),
                         (i * (W - LINE_WIDTH) / CELLS + LINE_WIDTH // 3, 0),
                         (i * (W - LINE_WIDTH) / CELLS + LINE_WIDTH // 3, H),
                         LINE_WIDTH)

    is_running = True
    curr_instruction = None
    transition_idx = 0
    final_delay = int(.5 * FPS)

    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

        window_surface.blit(background, (0, 0))
        for idx, car in enumerate(board_state):
            car_color = pygame.Color(tuple(car['color']))
            x_offset = 0
            y_offset = 0
            if curr_instruction is not None and idx == curr_instruction[0]:
                x_offset = transition_idx / TRANSITION_FRAMES * CELL_SIZE * curr_instruction[1].value[1]
                y_offset = transition_idx / TRANSITION_FRAMES * CELL_SIZE * curr_instruction[1].value[0]
            for cell_y, cell_x in car['cells']:
                pygame.draw.rect(window_surface, car_color, (
                    (cell_x * W / CELLS + x_offset, cell_y * H / CELLS + y_offset), (W / CELLS, H / CELLS)
                ))

        pygame.draw.rect(window_surface, pygame.Color('#ff0000'), (
            (4 * W / CELLS, 2 * H / CELLS), ((W - 5) * 2 / CELLS, H / CELLS)
        ), 2)

        pygame.display.update()

        clock.tick(FPS)

        if curr_instruction is not None:
            if transition_idx + 1 == TRANSITION_FRAMES:
                apply_instruction(board_state, curr_instruction)
                curr_instruction = None
            else:
                transition_idx += 1

        if curr_instruction is None and len(instructions) > 0:
            curr_instruction = instructions.pop(0)
            if not test_instruction(board_state, curr_instruction):
                is_running = False
                print("Illegal instruction!")
            transition_idx = 0

        if curr_instruction is None:
            if final_delay == 0:
                is_running = False
                if test_win(board_state):
                    print("You won!")
                else:
                    print("You lost!")
            else:
                final_delay -= 1


if __name__ == '__main__':
    main()
