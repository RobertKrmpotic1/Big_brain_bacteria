import os
import sys
from pathlib import Path
import random
import math
import time
import copy
import numpy as np
import pygame
import pickle
from square import Square
from generations import Generation, Species
from utils import *

pygame.font.init()

#Config
WIDTH, HEIGHT = 1000, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.Font('freesansbold.ttf', 20)
pygame.display.set_caption("Bacteria sim")

#Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))

class Bacteria():
    def __init__(self, x:int, y:int, colour:tuple=(0,155,255), max_energy = 100,current_energy=50, max_speed=10, current_speed = 0, vision_range = 150 ):
        self.x = x
        self.y = y
        self.colour = colour
        self.time = 0
        self.is_alive = True
        self.center_tile_pos = get_tile_position([self.x,self.y])

        self.max_energy = max_energy
        self.current_energy = current_energy
        self.max_speed = max_speed
        self.current_speed = current_speed

        self.vision_range = vision_range
        self.affinity_to_eat_red = 1
        self.affinity_to_eat_blue = 0
        self.hunger = self.max_energy - self.current_energy #does this need to be in a function?

        self.rl_sensor = pygame.draw.line(surface=WIN, color = (0,255,0), start_pos=(self.x -100,self.y), end_pos=(self.x +100, self.y))
        self.tb_sensor = pygame.draw.line(surface=WIN, color = (0,255,0), start_pos=(self.x,self.y+100), end_pos=(self.x , self.y -100))
    def draw(self):
        pygame.draw.circle(surface = WIN, color = self.colour, center = (self.x,self.y), radius =30)
        self.rl_sensor = pygame.draw.line(surface=WIN, color = (0,255,0), start_pos=(self.x -100,self.y), end_pos=(self.x +100, self.y))
        self.tb_sensor = pygame.draw.line(surface=WIN, color = (0,255,0), start_pos=(self.x,self.y+100), end_pos=(self.x , self.y -100))

    def eat(self):
        self.current_speed = 0
        if self.current_energy <= self.max_energy - 5:
            center_tile = get_tile(self.center_tile_pos,grid_array)
            self.current_energy += center_tile.eat_me(red = 5)
            if self.current_energy > 90:
                self.mitosis(self.x,self.y)

    def radiate(self):
        radiation_amount = self.calculate_radiation(self.current_speed)
        self.current_energy -= radiation_amount
        center_tile = get_tile(self.center_tile_pos,grid_array)
        center_tile.blue += radiation_amount
        if self.current_energy <= 0:
            self.die()
    
    def move(self, direction="down"):
        if direction == "down":
            if self.y <= HEIGHT-40:
                self.y +=self.max_speed
        elif direction == "up":
            if self.y >= 40:
                self.y -=self.max_speed
        elif direction == "right":
            if self.x <= WIDTH-40:
                self.x +=self.max_speed
        elif direction == "left":
            if self.x >= 40:
                self.x -=self.max_speed
        self.current_speed = self.max_speed
        self.center_tile_pos = get_tile_position([self.x,self.y])
        #self.update_current_tile()

    def see (self):
        center_colour = get_colour_from_tile(get_tile_position([self.x,self.y]),grid_array)
        right_colour = get_colour_from_tile(get_tile_position([self.rl_sensor.right,self.rl_sensor.top]),grid_array)
        left_colour = get_colour_from_tile(get_tile_position([self.rl_sensor.left,self.rl_sensor.top]),grid_array)
        top_colour = get_colour_from_tile(get_tile_position([self.tb_sensor.right,self.tb_sensor.top]),grid_array)
        bottom_colour = get_colour_from_tile(get_tile_position([self.tb_sensor.right,self.tb_sensor.bottom]),grid_array)
        return [top_colour, left_colour, center_colour, bottom_colour, right_colour]
    
    def get_data(self):
        input_list=[] #would dict make more sense?
        colour_list = self.see()
        for colour in colour_list:
            input_list.append(colour[0]) #red
            input_list.append(colour[2]) #blue
        input_list.append(self.hunger)
        return input_list

    def update(self, command):
        #look around
        self.see()
        #follow output command
        if command == "move_up":
            self.move(direction="up")
        elif command == "move_down":
            self.move(direction="down")
        elif command == "move_left":
            self.move(direction="left")
        elif command == "move_right":
            self.move(direction="right")
        elif command == "eat":
            self.eat()
        #radiate energy
        self.radiate()
        self.hunger = self.max_energy - self.current_energy

    def mitosis(self,x,y):
        new_x, new_y = self.get_new_spawnpoint(x,y)
        new_bacteria = Bacteria(new_x, new_y, current_energy=self.current_energy/2)
        self.current_energy = self.current_energy/2
        bac_population.append(new_bacteria)

    def get_new_spawnpoint(self,x,y):
        rand_int_x = random.randint(-60,60)
        rand_int_y = random.randint(-60,60)
        new_x = x + rand_int_x
        new_y = y + rand_int_y
        if new_x > 1000 or new_x<0:
            new_x = new_x - 2*rand_int_x
        if new_y > 1000 or new_y<0:
            new_y = new_y - 2*rand_int_y
        return new_x, new_y

    def die(self):
        self.say_gg(self.x,self.y)
        self.is_alive = False
        #index = (bac_population.index(self))
        #bac_population.pop(index)
        
    def say_gg(self,x,y):
        gg_dict[time_passed + 15] =  [x,y]


    def calculate_radiation(self,current_speed):
        radiation_amount = 0.5 + current_speed/10
        return radiation_amount


def run_simulation(net,gen_counter, grid_array):
    run = True
    FPS = 60
    global bac_population,max_population,current_population,gg_dict,time_passed
    bac_population =  []
    max_population=0
    time_passed=0
    gg_dict = {}

    #setup
    pygame.init()
    clock = pygame.time.Clock()
    total_food_start = total_food_in_grids(grid_array)
    bac_population.append(Bacteria(x=random.randint(50,950), y=random.randint(50,950)))
    current_population = len(bac_population)
    #draw on screen
    def redraw_window():
        WIN.blit(BG,(0,0))
        #tile.draw(WIN)
        for row in grid_array:
            for tile in row:
                tile.draw(WIN)
        for bac in bac_population:
            if bac.is_alive:
                bac.draw()
                statistics(bac,WIN, FONT)
        text_2 = FONT.render(f'Population:{current_population}', True, (0, 255, 0)) 
        text_3 = FONT.render(f'Generation:{gen_counter}', True, (0, 255, 0)) 
        WIN.blit(text_2, (50, 100))
        WIN.blit(text_3, (50, 150))
        check_gg()

        pygame.display.update()
    
    def check_gg():
        delete_list = []
        for key,value in gg_dict.items():
            if key == time_passed:
                delete_list.append(key)
            else:
                gg_text = FONT.render('gg', True, (0, 255, 0)) 
                WIN.blit(gg_text, (value[0], value[1]))
        if len(delete_list)>0:
            for gg_key in delete_list:
                del gg_dict[gg_key]


    #Every tick
    while run:
        clock.tick(FPS)
        #there should be 1 brain (1 memeber in net) and it should just keep making decisions
        for bac in bac_population:
            if bac.is_alive:
                X =bac.get_data()
                command= (net.spit_output(X))
                bac.update(command)

            else:
                pass
        total_food_end = total_food_in_grids(grid_array) 

        current_population = calculate_population(bac_population)
        if current_population>0:
            time_passed+=1
            if current_population>max_population:
                max_population = current_population

        if current_population<=0:
            total_food_end = total_food_in_grids(grid_array)        
            fitness = calculate_fitness_function(max_population, total_food_end, total_food_start)
            time.sleep(1)
            run=False
            return fitness

        if time_passed >= 1800:
            total_food_end = total_food_in_grids(grid_array) 
            fitness = calculate_fitness_function(max_population, total_food_end, total_food_start)
            time.sleep(1)
            run=False
            return fitness
        
        redraw_window()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False

def save_logs(gen_counter, dictionary, location):
    Path(f"logs/{location}").mkdir(exist_ok=True)
    with open(f'logs/{location}/gen_{gen_counter}.pickle', 'wb') as handle:
        pickle.dump(dictionary, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
def main_loop(number_of_generations=2):
    global gen_counter,top_performers
    gen_counter = 1
    top_performers = []
    while number_of_generations >= gen_counter: 
        #create generation
        current_generation = Generation(gen_counter,top_performers)
        neural_net_dict = current_generation.neural_net_dict

        #create grid for the generation which will be used for each species
        grid_array_ref = np.array([])
        grid_array_ref = create_grids(grid_array_ref, WIDTH,HEIGHT).reshape(10,10)

        fitness_dict={}
        #for brain of each species
        for key in neural_net_dict:
            global grid_array
            grid_array = copy.deepcopy(grid_array_ref)
            net_fitness = run_simulation(neural_net_dict[key],gen_counter, grid_array)
            neural_net_dict[key].set_fitness(net_fitness)
            fitness_dict[key] = net_fitness
        top_performers_int = sorted(fitness_dict, key=fitness_dict.get, reverse=True)[:8]
        top_performers = []

        save_logs(gen_counter, fitness_dict, "stats")
        
        print(f"Generation: {gen_counter}  Avg fitness: {np.array(list(fitness_dict.values())).mean()}, Max fitness: {np.array(list(fitness_dict.values())).max()}")

        for val in top_performers_int:
            top_performers.append(neural_net_dict[val].brain)

        if gen_counter % 5 == 0:
            weights_list = []
            for brain in top_performers:
                weights_list.append(brain.weights)
            save_logs(gen_counter, weights_list, "model_weights")

        gen_counter +=1

if __name__ == "__main__":

    main_loop(300)

