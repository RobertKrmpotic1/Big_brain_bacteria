import random
import math
import numpy as np
from square import Square

def create_grids( grid_array:np.array,WIDTH, HEIGHT, size = 100  ):    
    for x in range(0, WIDTH, size): 
        for y in range(0, HEIGHT, size):
            grid_array = np.append(grid_array,Square(x=x,y=y, colour=[random.randint(100,255),0,random.randint(0,255) ]) )
    np.save("grid_array0.npy",grid_array)
    return grid_array
            
def get_colour_from_tile(xy:list, grid_array):
    try:
         return grid_array[xy[0],xy[1]].colour
    except IndexError:
        if xy == [10,10]:
            return grid_array[xy[0]-1,xy[1]].colour
        elif xy[0] > 9:
            return grid_array[xy[0]-1,xy[1]-1].colour
        else:
            return grid_array[xy[0],xy[1]-1].colour
def get_tile(xy:list, grid_array):
    try:
         return grid_array[xy[0],xy[1]]
    except IndexError:
        if xy[0] > 9:
            return grid_array[xy[0]-1,xy[1]]
        else:
            return grid_array[xy[0],xy[1]-1]

def get_tile_position (xy:list):
    arr_x = math.floor(xy[0] /100) 
    arr_y = math.floor(xy[1] /100)
    return [arr_x,arr_y]


def statistics(bacteria, WIN, FONT):
    text_1 = FONT.render(f'{str(int(round(bacteria.current_energy,0)))}', True, (0, 255, 0)) 
    WIN.blit(text_1, (bacteria.x, bacteria.y))
    pass
        
def total_food_in_grids(grid_array):
    total_food =0
    for tile in grid_array.flat:
        total_food +=tile.red
    return total_food 

def calculate_fitness_function(max_population, total_food_end, total_food_start):
    percent_eaten = 1 - (total_food_end/total_food_start)
    return round(max_population + 200 * (percent_eaten**2), 5)

def calculate_population(bac_population):
    pop = 0
    for bac in bac_population:
        if bac.is_alive:
            pop +=1
    return pop

