import os
import sys
import random
import math
import time
import numpy as np
import pygame
from square import Square
from generations import Generation, Species
from utils import *

pygame.font.init()

#https://github.com/codewmax/NEAT-ChromeDinosaur/blob/master/main.py
#https://github.com/NeuralNine/ai-car-simulation/blob/master/newcar.py

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
        self.center_tile_pos = self.get_tile_position([self.x,self.y])

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
            center_tile = self.get_tile(self.center_tile_pos)
            self.current_energy += center_tile.eat_me(red = 5)
            if self.current_energy > 90:
                self.mitosis(self.x,self.y)

    def radiate(self):
        radiation_amount = self.calculate_radiation(self.current_speed)
        self.current_energy -= radiation_amount
        center_tile = self.get_tile(self.center_tile_pos)
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
        self.center_tile_pos = self.get_tile_position([self.x,self.y])
        #self.update_current_tile()

    def see (self):
        center_colour = self.get_colour_from_tile(self.get_tile_position([self.x,self.y]))
        right_colour = self.get_colour_from_tile(self.get_tile_position([self.rl_sensor.right,self.rl_sensor.top]))
        left_colour = self.get_colour_from_tile(self.get_tile_position([self.rl_sensor.left,self.rl_sensor.top]))
        top_colour = self.get_colour_from_tile(self.get_tile_position([self.tb_sensor.right,self.tb_sensor.top]))
        bottom_colour = self.get_colour_from_tile(self.get_tile_position([self.tb_sensor.right,self.tb_sensor.bottom]))
        return [top_colour, left_colour, center_colour, bottom_colour, right_colour]
        #print ( center_colour)
    
    def get_data(self):
        input_list=[] #would dict make more sense?
        colour_list = self.see()
        for colour in colour_list:
            input_list.append(colour[0]) #red
            input_list.append(colour[2]) #blue
        input_list.append(self.hunger)
        #print(input_list)
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

    def get_colour_from_tile(self,xy:list):
        try:
             return grid_array[xy[0],xy[1]].colour
        except IndexError:
            if xy == [10,10]:
                return grid_array[xy[0]-1,xy[1]].colour
            elif xy[0] > 9:
                return grid_array[xy[0]-1,xy[1]-1].colour
            else:
                return grid_array[xy[0],xy[1]-1].colour
    
    def get_tile(self,xy:list):
        try:
             return grid_array[xy[0],xy[1]]
        except IndexError:
            if xy[0] > 9:
                return grid_array[xy[0]-1,xy[1]]
            else:
                return grid_array[xy[0],xy[1]-1]

    def get_tile_position (self,xy:list):
        arr_x = math.floor(xy[0] /100) 
        arr_y = math.floor(xy[1] /100)
        return [arr_x,arr_y]


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
        gg_dict[time_spent_alive + 15] =  [x,y]


    def calculate_radiation(self,current_speed):
        radiation_amount = 0.1 + current_speed/10
        return radiation_amount


def run_simulation(net,gen_counter):
    run = True
    FPS = 60
    
    # Empty Collections For Nets and bac population
    global bac_population, grid_array,max_population,current_population,gg_dict,time_spent_alive
    bac_population =  []
    grid_array = np.array([])
    max_population=0
    time_spent_alive=0
    gg_dict = {}

    #setup
    pygame.init()
    clock = pygame.time.Clock()
    grid_array = create_grids(grid_array, WIDTH,HEIGHT).reshape(10,10)
    total_food_start = total_food_in_grids(grid_array)

    bac_population.append(Bacteria(x=random.randint(50,950), y=random.randint(50,950)))
    current_population = len(bac_population)

    #print(f"Population created. size={len(nets)},{len(bac_population)}")
    
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
            if key == time_spent_alive:
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
                print(X)
                command= (net.spit_output(X))
                bac.update(command)

            else:
                pass
        total_food_end = total_food_in_grids(grid_array) 

        current_population = calculate_population(bac_population)
        if current_population>0:
            time_spent_alive+=1
            if current_population>max_population:
                max_population = current_population

        if current_population<=0:
            total_food_end = total_food_in_grids(grid_array)        
            #print(f"max_pop= {max_population} ; fitness = {round(calculate_fitness_function(max_population,time_spent_alive, 1-total_food_end/total_food_start))} ; alive_for:  {time_spent_alive}, start_food = {total_food_start}, end_food ={total_food_end}")

            time.sleep(1)
            run=False
        
        redraw_window()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
        
def main_loop(number_of_generations=2):
    global gen_counter,top_performers
    gen_counter = 0
    top_performers = []

    while number_of_generations >= gen_counter: 
        current_generation = Generation(gen_counter,top_performers)
        neural_net_list = current_generation.neural_net_list
        for net in neural_net_list:
            run_simulation(net,gen_counter)
        
        number_of_generations +=1
        #compare fitness
        #get top performers
        #log smth?



if __name__ == "__main__":

    main_loop()

