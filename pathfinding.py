import pygame
import math
from queue import PriorityQueue

WIDTH = 500
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Pathfinding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUIOSE = (64, 224, 208)

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.colour = WHITE
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows
        self.g_score = float("inf")
        self.f_score = float("inf")
    
    def get_pos(self):
        return self.row, self.col
    
    def is_closed(self):
        return self.colour == RED
    
    def is_open(self):
        return self.colour == GREEN
    
    def is_barrier(self):
        return self.colour == BLACK
    
    def is_start(self):
        return self.colour == ORANGE
    
    def is_end(self):
        return self.colour == TURQUIOSE
    
    def reset(self):
        self.colour = WHITE

    def make_closed(self):
        self.colour = RED

    def make_open(self):
        self.colour = GREEN

    def make_barrier(self):
        self.colour = BLACK

    def make_start(self):
        self.colour = ORANGE

    def make_end(self):
        self.colour = TURQUIOSE

    def make_path(self):
        self.colour = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
        self.neighbours = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # down
            self.neighbours.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # up
            self.neighbours.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # right
            self.neighbours.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # left
            self.neighbours.append(grid[self.row][self.col - 1])

        # diagonals
        if self.row < self.total_rows - 1 and self.col > 0 and not grid[self.row + 1][self.col-1].is_barrier() and not (grid[self.row + 1][self.col].is_barrier() or grid[self.row][self.col - 1].is_barrier()): # left - down
            self.neighbours.append(grid[self.row + 1][self.col-1])

        if self.row > 0 and self.col > 0 and not grid[self.row - 1][self.col - 1].is_barrier() and not (grid[self.row - 1][self.col].is_barrier() or grid[self.row][self.col - 1].is_barrier()): # left-up
            self.neighbours.append(grid[self.row - 1][self.col - 1])

        if self.col < self.total_rows - 1 and self.row < self.total_rows - 1 and not grid[self.row+1][self.col + 1].is_barrier() and not (grid[self.row + 1][self.col].is_barrier() or grid[self.row][self.col + 1].is_barrier()): # right - down
            self.neighbours.append(grid[self.row+1][self.col + 1])
        
        if self.col < self.total_rows - 1 and self.row > 0 and not grid[self.row-1][self.col + 1].is_barrier() and not (grid[self.row - 1][self.col].is_barrier() or grid[self.row][self.col + 1].is_barrier()): # right - up
            self.neighbours.append(grid[self.row-1][self.col + 1])
        

    def __lt__(self, other):
        return False
    
def h(p1, p2):
    #using manhattan distance
    x1, y1 = p1
    x2, y2 = p2

    disX = abs(x1 - x2)
    disY = abs(y1 - y2)

    if disX > disY:
        return (14 * disY) + (10 * (disX - disY))
    return (14 * disX) + (10 * (disY - disX))

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def algorithm(draw, start, end):
    open_set = PriorityQueue()
    open_set.put((0, 0, start))
    came_from = {}

    start.g_score = 0
    start.f_score = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[2]
        open_set_hash.remove(current)
        
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True
        
        for neighbour in current.neighbours:
            temp_g_score = current.g_score + 1

            if temp_g_score < neighbour.g_score:
                came_from[neighbour] = current
                neighbour.g_score = temp_g_score
                neighbour.f_score = temp_g_score + h(neighbour.get_pos(), end.get_pos())

                if neighbour not in open_set_hash:
                    open_set.put((neighbour.f_score, neighbour.g_score, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()
    
        draw()

        if current != start:
            current.make_closed()

    return False

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (i * gap, 0), (i * gap, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)
    
    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_position(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap

    return row, col

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
            if pygame.mouse.get_pressed()[0]: # left mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, ROWS, width)
                node = grid[row][col]

                if not start and node != end:
                    start = node
                    start.make_start()

                elif not end and node != start:
                    end = node
                    end.make_end()

                elif node != start and node != end:
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[2]: # right mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                if node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)
                    
                    algorithm(lambda: draw(win, grid, ROWS, width), start, end)
            
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
    pygame.quit()

main(WIN, WIDTH)