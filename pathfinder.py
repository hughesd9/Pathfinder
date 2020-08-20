import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Cubes:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row*width
        self.y = col*width
        self.color = WHITE
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows

    def get_postion(self):
        return self.row, self.col

    def is_closed(self): #i.e not looking at this cube anymore
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbour(self, grid):
        pass

    def __lt__(self, other): #compare cubes to each other
        return False

def h(p1, p2): #heuristic function using point 1 and point 2 using Manhatten distance
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            cube = Cubes(i, j, gap, rows)
            grid[i].append(cube)

    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i*gap), (width, i*gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for cube in row:
            cube.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_position(pos, rows, width):
    gap = width // rows
    x, y = pos

    col = x // gap
    row = y // gap

    return col, row

def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    started = False
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if started:
                continue
            if pygame.mouse.get_pressed()[0]: #if the left mouse button is pressed, first click = start, second click = end, rest = black barriers
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, ROWS, width)
                cube = grid[row][col]
                if not start and cube != end: #can't put start and end in same position
                    start = cube
                    start.make_start()
                elif not end and cube != start:
                    end = cube
                    end.make_end()
                elif cube != end and cube != start:
                    cube.make_barrier()
            elif pygame.mouse.get_pressed()[2]: #if the right mouse button is pressed reset the colour of the cube
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, ROWS, width)
                cube = grid[row][col]
                cube.reset()
                if cube == start:
                    start = None
                elif cube == end:
                    end = None
    pygame.quit()

main(WIN, WIDTH)
