import pygame
import math
from queue import PriorityQueue

width = 800
window = pygame.display.set_mode((width, width))
pygame.display.set_caption("A* Path Finding Algorithm")

# Colors   
Closed = (255, 0, 0)
Open = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
white = (255, 255, 255)
Barrier = (0, 0, 0)
Path = (128, 0, 128)
Start = (255, 165 ,0)
GREY = (128, 128, 128)
End = (64, 224, 208)

class Tile:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.width = width
        self.total_rows = total_rows
        self.x = row * width
        self.y = col * width
        self.color = white
        self.neighbors = []
    
    def getPos(self):
        return self.row, self.col
    
    def getState(self):
        return self.color
    
    def checkState(self, state):
        return self.color == state
    
    def updateState(self, state):
        self.color = state

    def reset(self):
        self.color = white
    
    def draw(self , window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))
    
    def updateNeighbors(self, grid):
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].checkState(Barrier):
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].checkState(Barrier):
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].checkState(Barrier):
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].checkState(Barrier):
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False
    
def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1-x2) + abs(y1-y2)


def algorithm(draw, grid, start, end):

    count = 0
    openSet = PriorityQueue()
    openSet.put((0, count, start))

    prevTile = {}

    gScore = {tile: float("inf") for row in grid for tile in row}
    gScore[start] = 0

    fScore = {tile: float("inf") for row in grid for tile in row}
    fScore[start] = distance(start.getPos(), end.getPos())

    openSetHash = {start}

    while not openSet.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        cureentTile = openSet.get()[2]
        openSetHash.remove(cureentTile)

        if cureentTile == end:
            return True
        
        for neighbor in cureentTile.neighbors:
            tempGScore = gScore[cureentTile] + 1

            if tempGScore < gScore[neighbor]:

                prevTile[neighbor] = cureentTile

                gScore[neighbor] = tempGScore
                fScore[neighbor] = tempGScore + distance(neighbor.getPos(), end.getPos())

                if neighbor not in openSetHash:
                    count += 1

                    openSet.put((fScore[neighbor], count, neighbor))

                    openSetHash.add(neighbor)

                    neighbor.updateState(Open)
        
        draw()
        
        if cureentTile != start:
            cureentTile.updateState(Closed)
    
    return False


def makeGrid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            tile = Tile(i, j, gap, rows)
            grid[i].append(tile)
    return grid
    
def drawGrid(window, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(window, GREY, (0, i*gap), (width, i*gap))
        for j in range(rows):
            pygame.draw.line(window, GREY, (j*gap, 0), (j*gap, width))


def draw(window, grid, rows, width):
    window.fill(white)
    for row in grid:
        for tile in row:
            tile.draw(window)
    drawGrid(window, rows, width)
    pygame.display.update()

def getClickedPos(pos, rows, width):
    gap = width // rows
    y , x = pos
    row = y // gap
    col = x // gap
    return row , col

def main(window, width):
    ROWS = 50
    grid = makeGrid(ROWS, width)

    start = None
    end = None
    
    run = True
    started = False

    while run:
        draw(window, grid, ROWS, width)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row , col = getClickedPos(pos, ROWS, width)

                tile = grid[row][col]

                if not start and tile != end:
                    start = tile
                    start.updateState(Start)
                
                elif not end and tile != start:
                    end = tile
                    end.updateState(End)

                elif tile != start and tile != end:
                    tile.updateState(Barrier)
            
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row , col = getClickedPos(pos, ROWS, width)
                tile = grid[row][col]
                tile.reset()
                if tile == start:
                    start = None
                elif tile == end:
                    end = None
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    for row in grid:
                        for tile in row:
                            tile.updateNeighbors(grid)
                    
                    algorithm(lambda: draw(window, grid, ROWS, width), grid, start, end)

    pygame.quit()
main(window, width)
    