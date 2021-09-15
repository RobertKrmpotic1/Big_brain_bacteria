import os
import sys
import random
import math
import time
import numpy as np
import pygame
import neat

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



class Square:
    def __init__(self, x:int, y:int, colour:list=(random.randint(0,255),0,random.randint(0,255))):#rgb?
        self.x = x
        self.y = y
        self.image = None
        self.blue = random.randint(0,255)
        self.red = random.randint(0,255)
        self.colour = colour
        
    def draw(self,window):
        pygame.draw.rect(surface = window, color = tuple(self.get_colour(self.red, self.blue)), rect = (self.x,self.y, 100,100))

    def get_colour (self, red:int,blue:int):
        red_c = min(255,red)
        blue_c = min (255,blue) 
        self.colour = [red_c,0,blue_c]
        return [red_c,0,blue_c]

    def eat_me(self,red=0, blue=0):
        if red > 0:
            if self.red > red:
                self.red -= red
                return red
            else:
                max_enr = self.red
                self.red = 0
                return max_enr
        elif blue > 0:
            if self.blue > blue:
                self.blue -= blue
                return blue
            else:
                max_enr = self.blue
                self.blue = 0
                return max_enr


class Bacteria:
    def __init__(self, x:int, y:int, colour:tuple=(0,155,255), max_energy = 100,current_energy=50, max_speed=10, current_speed = 10, vision_range = 150 ):
        self.x = x
        self.y = y
        self.colour = colour
        self.time = 0
        self.alive = True
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
        if self.current_energy <= self.max_energy - 10:
            center_tile = self.get_tile(self.center_tile_pos)
            self.current_energy += center_tile.eat_me(red = 20)
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
        self.center_tile_pos = self.get_tile_position([self.x,self.y])
        #self.update_current_tile()

    def see (self):
        center_colour = self.get_colour_from_tile(self.get_tile_position([self.x,self.y]))
        right_colour = self.get_colour_from_tile(self.get_tile_position([self.rl_sensor.right,self.rl_sensor.top]))
        left_colour = self.get_colour_from_tile(self.get_tile_position([self.rl_sensor.left,self.rl_sensor.top]))
        top_colour = self.get_colour_from_tile(self.get_tile_position([self.tb_sensor.right,self.tb_sensor.top]))
        bottom_colour = self.get_colour_from_tile(self.get_tile_position([self.tb_sensor.right,self.tb_sensor.bottom]))

        print ( center_colour)

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
        #
        self.hunger = self.max_energy - self.current_energy

    def get_colour_from_tile(self,xy:list):
        print(xy)
        try:
             return grid_array[xy[0],xy[1]].colour
        except IndexError:
            if xy[0] > 9:
                print("if")
                return grid_array[xy[0]-1,xy[1]].colour
            elif xy == [10,10]:
                print("elif")
                return grid_array[xy[0]-1,xy[1]-1].colour
            else:
                print("elif")
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
        new_bacteria = Bacteria(min(x + 100,1000), (min(y + 100,1000)))
        bac_population.append(new_bacteria)

    def die(self):
        
        self.say_gg(self.x,self.y)
        #this needs to be changed to 
        index = (bac_population.index(self))
        bac_population.pop(index)
        
    def say_gg(self,x,y):
        gg_dict[time_spent_alive + 15] =  [x,y]


    def calculate_radiation(self,current_speed):
        radiation_amount = 0.1 + current_speed/10
        return radiation_amount

def create_grids( grid_array:np.array, size = 100):
    print("creating grids")
    
    for x in range(0, WIDTH, size): 
        for y in range(0, HEIGHT, size):
            grid_array = np.append(grid_array,Square(x=x,y=y, colour=[random.randint(150,255),0,random.randint(0,255) ]) )
    return grid_array
            
def statistics(bacteria):
        text_1 = FONT.render(f'{str(int(round(bacteria.current_energy,0)))}', True, (0, 255, 0)) 
        text_2 = FONT.render(f'Population:{str(len(bac_population))}', True, (0, 255, 0)) 

        WIN.blit(text_1, (bacteria.x, bacteria.y))
        WIN.blit(text_2, (50, 100))



def main():
    

    run = True
    FPS = 60
    
    # Empty Collections For Nets and bac population
    global nets, bac_population, grid_array,current_generation,max_population,gg_dict,time_spent_alive 
    nets = []
    bac_population =  []
    grid_array = np.array([])
    current_generation = 0 # Generation counter
    max_population=0
    time_spent_alive=0
    gg_dict = {}
    #setup
    pygame.init()
    clock = pygame.time.Clock()
    bacteria = Bacteria(x=150, y=250)
    bac_population.append(bacteria)
    grid_array = create_grids(grid_array).reshape(10,10)
    #PLAYSOUNDEVENT = pygame.USEREVENT + 1
    #pygame.time.set_timer(PLAYSOUNDEVENT, 65)
    

    #draw on screen
    def redraw_window():
        WIN.blit(BG,(0,0))
        #tile.draw(WIN)
        for row in grid_array:
            for tile in row:
                tile.draw(WIN)
        for bac in bac_population:
            bac.draw()
            statistics(bac)
        check_gg()

        pygame.display.update()
    
    def check_gg():

        delete_list = []
        for key,value in gg_dict.items():
            print(key,value)
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
        for bac in bac_population:
            list1 =  [ "eat","move_down", "move_left", "move_right", "eat", "eat", "eat", "eat", "eat"]
            #bac.update(command="eat")
            bac.update(command= list1[random.randint(0,8)])
        
        if len(bac_population)>0:
            time_spent_alive+=1
            if len(bac_population)>max_population:
                max_population = len(bac_population)
        
        redraw_window()
        
        #if pygame.event.get(PLAYSOUNDEVENT): # check event queue contains PLAYSOUNDEVENT 
        #    print("troll")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
        
if __name__ == "__main__":
        # Load Config
    config_path = "./config.txt"
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_path)

    # Create Population And Add Reporters
    net_population = neat.Population(config)
    net_population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    net_population.add_reporter(stats)
    main()
