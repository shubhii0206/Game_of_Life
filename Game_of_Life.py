import pygame
import random
from time import sleep
pygame.init()
screen = pygame.display.set_mode((500, 500))
ALIVE, DEAD = "1", "0"
BLACK = (0, 0, 0)
PINK = (255, 0, 126)
colour_names = ["RED","PINK", "BLUE", "GREEN"]
WHITE = (255, 255, 255)
screen.fill(WHITE)
dimensions = [(255, 0, 0), (255, 0, 126), (0, 132, 255), (122, 255,0)]
COLOUR = dict(zip(colour_names, dimensions))


def generate_block(x, y, color):
    block_size = 20
    x *= block_size*3
    y *= block_size*3

    pygame.draw.rect(screen, color, (x,y,block_size*3,block_size*3),0)
def make_random_grid(row: int, column: int):
    
    random_grid = []
    
    for rows in range(row):
        columns = ""
        
        for cell in range(column):
            
            columns += random.choice([ALIVE, DEAD])
        random_grid.append(columns)
        
    return random_grid

def sentinel_grid(original_list): 
    size = len(original_list[0])
    infinite_grid = ["0" + row + "0" for row in original_list]

    infinite_grid.append((len(infinite_grid[0]) ) * "0")
    infinite_grid.append((len(infinite_grid[0])) * "0")


    infinite_grid.insert(0, (size + 2) * "0")
    infinite_grid.insert(1, (size + 2) * "0")
    return infinite_grid



def count_alive_neighbour_cells(row_number, col_number, infinite_grid):
    return infinite_grid[row_number - 1][col_number - 1: col_number + 2].count("1") + infinite_grid[row_number][
                                                                                      col_number - 1: col_number + 2].count(
        "1") + infinite_grid[row_number + 1][col_number - 1: col_number + 2].count("1")


def new_cell_status(cell, row_number, column_number, infinite_grid):
    if cell == ALIVE:
        alive_neighbour_cells = count_alive_neighbour_cells(row_number, column_number, infinite_grid) - 1
        if alive_neighbour_cells < 2 or alive_neighbour_cells > 3:
            cell = "0"
        if alive_neighbour_cells == 2 or alive_neighbour_cells == 3:
            cell = "1"
    if cell == DEAD:
        cell = ALIVE if count_alive_neighbour_cells(row_number, column_number, infinite_grid) == 3 else DEAD      
    return cell

def add_dead_row_on_left(grid):
    for  row in grid:
        row = DEAD + row
    return grid    
def add_dead_row_on_right(grid):
    for  row in grid:
        row += DEAD        
    return grid

def add_dead_row_on_top(grid):

    grid.insert(0, DEAD*len(grid[0]))      
    return grid

def add_dead_row_at_bottom(grid):

    grid.append(DEAD*len(grid[0]) )     
    return grid

def game_of_life_continues(original_list):
    infinite_grid = sentinel_grid(original_list)
    new_row = ""
    new_grid = []
    add, add1,add_row_at_bottom,add_row_on_top = 0, 0, 0, 0
    last_column_number = len(original_list[0])
    for row_number, infinite_row in enumerate(infinite_grid[1: -1], start=1):

        for col_number, cell in enumerate(infinite_row[1:-1], start=1):
            cell == new_cell_status(cell, row_number, col_number, infinite_grid)
            new_row += cell
            if row_number == 1and ALIVE in new_row:
                add_row_on_top = 1
            if row_number == last_column_number and ALIVE in new_row:
                add_row_at_bottom = 1    
                
            if col_number == 1 and cell == ALIVE: 
                add = 1
            if col_number == last_column_number and cell == ALIVE:
                add1 = 1
        
        new_grid.append(new_row)
        new_row = ""
        
        if add == 1:
            add_dead_row_on_left(new_grid)
        if add1 == 1:
            add_dead_row_on_right(new_grid)
        if  add_row_on_top ==1:
            add_dead_row_on_top(new_grid)
        if add_row_at_bottom == 1:
            add_dead_row_at_bottom(new_grid)
            
        

    return new_grid


def main(rows, columns):
    grid =  make_random_grid(rows,columns)
    running = True
    new_row = ""
    new_grid = []
    while running:
        random_colour = COLOUR[random.choice(colour_names)]
        for row_number in range(rows):

            for column_number in range(columns):
                cell = grid[row_number][column_number]
                color = random_colour if cell == ALIVE else WHITE
                generate_block(row_number, column_number, color)
        grid = game_of_life_continues(grid)      
                    
        pygame.display.flip()
        sleep(0.5)
    
                

if __name__ == "__main__" :
    main(8,8)
                
