import random
import numpy as np
from square import Square

def create_grids( grid_array:np.array,WIDTH, HEIGHT, size = 100  ):    
    for x in range(0, WIDTH, size): 
        for y in range(0, HEIGHT, size):
            grid_array = np.append(grid_array,Square(x=x,y=y, colour=[random.randint(100,255),0,random.randint(0,255) ]) )
    np.save("grid_array0.npy",grid_array)
    return grid_array
            
def statistics(bacteria, WIN, FONT):
    text_1 = FONT.render(f'{str(int(round(bacteria.current_energy,0)))}', True, (0, 255, 0)) 
    WIN.blit(text_1, (bacteria.x, bacteria.y))
    pass
        
def total_food_in_grids(grid_array):
    total_food =0
    for tile in grid_array.flat:
        total_food +=tile.red
    return total_food 

def calculate_fitness_function(max_population, perc_eaten):
    return (max_population) * (perc_eaten*perc_eaten)

def calculate_population(bac_population):
    pop = 0
    for bac in bac_population:
        if bac.is_alive:
            pop +=1
    return pop