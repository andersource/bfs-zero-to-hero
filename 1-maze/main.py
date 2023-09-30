##############################################################################
#
#                    BFS zero-to-hero part 1:   maze challenge
#                    -----------------------------------------
#
##############################################################################
##############################################################################

def find_path(maze, start_pos, end_pos):
    # Params:
    #   maze:       nested list of booleans, where each row represents a row
    #               in the maze, and each bool denotes whether the corresponding
    #               cell is free (True) or occupied by a wall (False)
    #   start_pos:  (int, int) tuple denoting the initial (row, column) position
    #               of the player
    #   end_pos:    (int, int) tuple denoting the objective (row, column)
    #               position
    #
    # Return value:     list of (int, int) tuples denoting (row, column)
    #                   positions of the shortest path, starting with
    #                   start_pos and ending in end_pos
    raise NotImplementedError()


##############################################################################
########################    behind-the-scenes code    ########################
##############################################################################
from glob import glob
import pygame


FPS = 30
W, H = 1200, 720
MAX_MAZE_WIDTH = 1100
MAX_MAZE_HEIGHT = 640
COLORS = {
    True: '#EED7C5',
    False: '#B36A5E'
}
END_COLOR = '#0000FF'
PLAYER_COLOR = '#00FF00'


def validate_path(maze, start_pos, path):
    if len(path) < 2:
        exit('Empty path')
    if path[0] != start_pos:
        exit('Path needs to start at initial position')
    prev_pos = start_pos
    for i in range(1, len(path)):
        pos = path[i]
        if not maze[pos[0]][pos[1]]:
            exit('Path passes through wall')
        if abs(pos[0] - prev_pos[0]) + abs(pos[1] - prev_pos[1]) > 1:
            exit('Consecutive path positions must be adjacent')

        prev_pos = pos


def run_test_case(window_surface, clock, testcase_path):
    with open(testcase_path, 'r') as f:
        txt_maze = list(filter(None, f.read().split('\n')))

    maze = [[cell in (' ', '!', '@') for cell in row] for row in txt_maze]
    start_pos = find_loc_in_maze(txt_maze, '@')
    end_pos = find_loc_in_maze(txt_maze, '!')
    maze_width = len(maze[0])
    maze_height = len(maze)

    path = find_path(maze, start_pos, end_pos)
    validate_path(maze, start_pos, path)

    cell_size = min(MAX_MAZE_WIDTH // len(maze[0]), MAX_MAZE_HEIGHT // len(maze))
    maze_start_x = W // 2 - cell_size * maze_width / 2
    maze_start_y = H // 2 - cell_size * maze_height / 2
    background = pygame.Surface((W, H))
    background.fill(pygame.Color('#EEE2DF'))
    for row_idx, row in enumerate(maze):
        for col_idx, cell in enumerate(row):
            cell_x = maze_start_x + col_idx * cell_size
            cell_y = maze_start_y + row_idx * cell_size
            pygame.draw.rect(background, COLORS[cell], (cell_x, cell_y, cell_size, cell_size))

    end_x = maze_start_x + cell_size * end_pos[1]
    end_y = maze_start_y + cell_size * end_pos[0]
    start_x = maze_start_x + cell_size * start_pos[1]
    start_y = maze_start_y + cell_size * start_pos[0]
    pygame.draw.rect(background, END_COLOR, (end_x, end_y, cell_size, cell_size))
    pygame.draw.rect(background, PLAYER_COLOR, (start_x, start_y, cell_size, cell_size))

    window_surface.blit(background, (0, 0))
    pygame.display.update()
    clock.tick(.5)

    for cell_pos in path:
        cell_x = maze_start_x + cell_size * cell_pos[1]
        cell_y = maze_start_y + cell_size * cell_pos[0]
        pygame.draw.rect(background, PLAYER_COLOR, (cell_x, cell_y, cell_size, cell_size))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise KeyboardInterrupt()

        window_surface.blit(background, (0, 0))

        pygame.display.update()
        clock.tick(FPS)

    clock.tick(.5)


def find_loc_in_maze(txt_maze, ch):
    return [
        (row_idx, col_idx)
        for row_idx, row in enumerate(txt_maze)
        for col_idx, cell in enumerate(row)
        if cell == ch
    ][0]


def main():
    pygame.init()
    clock = pygame.time.Clock()

    pygame.display.set_caption('Maze solver')
    window_surface = pygame.display.set_mode((W, H))

    for testcase_path in sorted(glob('mazes/*.txt')):
        run_test_case(window_surface, clock, testcase_path)


if __name__ == '__main__':
    main()
