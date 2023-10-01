##############################################################################
#
#                    BFS zero-to-hero part 2:   snake challenge
#                    ------------------------------------------
#
##############################################################################
##############################################################################

N_CELLS = 32  # Number of cells per row / column in the arena grid
DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def find_directions(snake, food_pos):
    # Params:
    #   snake:      list of (int, int), denoting (row, column) positions
    #               of snake cells, with index 0 representing the tail and the
    #               last element representing the head
    #   food_pos:   (int, int) tuple denoting the (row, column) position of
    #               the snake's tasty snack
    #
    # Return value:     list of integers denoting the direction indices
    #                   (referring to the DIRECTION const list) for each step
    #                   to be taken by the snake's head until arriving at
    #                   food_pos
    raise NotImplementedError()


##############################################################################
########################    behind-the-scenes code    ########################
##############################################################################
import random
import pygame


FPS = 60
W, H = 1200, 720
ARENA_SIZE = 600
SNAKE_COLOR = '#2978A0'
FOOD_COLOR = '#315659'


def main():
    pygame.init()
    clock = pygame.time.Clock()

    pygame.display.set_caption('Snake solver')
    window_surface = pygame.display.set_mode((W, H))

    arena_start_x = W // 2 - ARENA_SIZE // 2
    arena_start_y = H // 2 - ARENA_SIZE // 2
    cell_size = ARENA_SIZE / N_CELLS

    background = pygame.Surface((W, H))
    background.fill(pygame.Color('#C6E0FF'))
    pygame.draw.rect(background, '#BCAB79',
                     (arena_start_x, arena_start_y, ARENA_SIZE, ARENA_SIZE))

    snake = [(N_CELLS // 2, N_CELLS // 2 - 2), (N_CELLS // 2, N_CELLS // 2 - 1), (N_CELLS // 2, N_CELLS // 2)]
    eaten = False

    food_row, food_col = gen_food_pos(snake)
    dirs = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise KeyboardInterrupt()

        window_surface.blit(background, (0, 0))
        for cell_row, cell_col in snake:
            cell_x = arena_start_x + round(cell_col * cell_size)
            cell_y = arena_start_y + round(cell_row * cell_size)
            pygame.draw.rect(window_surface, SNAKE_COLOR, (cell_x, cell_y, round(cell_size), round(cell_size)))

        food_x = arena_start_x + round(cell_size * food_col)
        food_y = arena_start_y + round(cell_size * food_row)
        pygame.draw.rect(window_surface, FOOD_COLOR, (food_x, food_y, round(cell_size), round(cell_size)))

        pygame.display.update()
        clock.tick(FPS)

        if eaten:
            snake.insert(0, (0, 0))
            eaten = False

        for i in range(len(snake) - 1):
            snake[i] = snake[i + 1]

        if len(dirs) == 0:
            dirs = find_directions(snake, (food_row, food_col))

        if len(dirs) == 0:
            exit('Empty direction queue')

        dir_idx = dirs.pop(0)

        snake[-1] = (snake[-1][0] + DIRECTIONS[dir_idx][0], snake[-1][1] + DIRECTIONS[dir_idx][1])
        if (snake[-1][0] < 0
                or snake[-1][1] < 0
                or snake[-1][0] >= N_CELLS
                or snake[-1][1] >= N_CELLS
                or snake[-1] in snake[:-1]):
            exit('Fatal crash')

        if (food_row, food_col) == snake[-1]:
            eaten = True
            food_row, food_col = gen_food_pos(snake)


def gen_food_pos(snake):
    food_row, food_col = snake[0]
    while (food_row, food_col) in snake:
        food_row = random.randint(0, N_CELLS - 1)
        food_col = random.randint(0, N_CELLS - 1)

    return food_row, food_col


if __name__ == '__main__':
    main()

