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

current_generation = 0 # Generation counter

class Square:
    def __init__(self, x:int, y:int, colour:tuple=(random.randint(0,255),0,random.randint(0,255))):#rgb?
        self.x = x
        self.y = y
        self.image = None
        self.colour = colour
        
    def draw(self,window):
        pygame.draw.rect(surface = window, color = self.colour, rect = (self.x,self.y, 100,100))

    def change_colour(self,new_colour:tuple()):
        self.colour = new_colour


class Bacteria:
    def __init__(self, x:int, y:int, colour:tuple=(0,0,255), max_energy = 100,current_energy=50, max_speed=10, current_speed = 10, vision_range = 150 ):
        self.x = x
        self.y = y
        self.colour = colour
        self.time = 0
        self.alive = True

        self.max_energy = max_energy
        self.current_energy = current_energy
        self.max_speed = max_speed
        self.current_speed = current_speed

        self.vision_range = vision_range
        self.affinity_to_eat_red = 1
        self.affinity_to_eat_blue = 0
        self.hunger = self.max_energy - self.current_energy #does this need to be in a function?

        self.rl_sensor = None
        self.tb_sensor = None

    def draw(self,window):
        pygame.draw.circle(surface = window, color = self.colour, center = (self.x,self.y), radius =30)
        self.rl_sensor = pygame.draw.line(surface=window, color = (0,255,0), start_pos=(self.x -100,self.y), end_pos=(self.x +100, self.y))
        self.tb_sensor = pygame.draw.line(surface=window, color = (0,255,0), start_pos=(self.x,self.y+100), end_pos=(self.x , self.y -100))

    def eat(self):
        if self.current_energy <= self.max_energy - 10:
            self.current_energy += 10
        pass

    def radiate(self):
        self.current_energy -= self.calculate_radiation(self.current_speed)
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

    def see (self):
        right_x = math.floor(self.rl_sensor.right /100) 
        right_y = math.floor(self.rl_sensor.top /100) 
        right_colour = self.get_colour_from_tile(right_x,right_y)

        left_x = math.floor(self.rl_sensor.left /100) 
        left_y = math.floor(self.rl_sensor.top /100) 
        left_colour = self.get_colour_from_tile(left_x,left_y)

        top_x = math.floor(self.tb_sensor.right /100) 
        top_y = math.floor(self.tb_sensor.top /100) 
        top_colour = self.get_colour_from_tile(top_x,top_y)

        bottom_x = math.floor(self.tb_sensor.right /100) 
        bottom_y = math.floor(self.tb_sensor.bottom /100) 
        bottom_colour = self.get_colour_from_tile(bottom_x,bottom_y)

        print (right_colour, left_colour, top_colour, bottom_colour)
    def get_colour_from_tile(self,x,y):
        return grid_array[x,y].colour

    def mitosis(self):
        pass

    def die(self):
        print("gg")
        bac_population.pop()

    def calculate_radiation(self,current_speed):
        radiation_amount = 0.1 + current_speed/4
        return radiation_amount

def create_grids( grid_array:np.array, size = 100):
    print("creating grids")
    
    for x in range(0, WIDTH, size): 
        for y in range(0, HEIGHT, size):
            grid_array = np.append(grid_array,Square(x=x,y=y, colour=(random.randint(0,255),0,random.randint(0,255) )) )
    return grid_array


            
def statistics(bacteria):
        text_1 = FONT.render(f'Energy:{str(round(bacteria.current_energy,1))}', True, (0, 255, 0)) 
        text_2 = FONT.render(f'Population:{str(len(bac_population))}', True, (0, 255, 0)) 

        WIN.blit(text_1, (50, 50))
        WIN.blit(text_2, (50, 100))



def main():
    run = True
    FPS = 60
    clock = pygame.time.Clock()
    # Empty Collections For Nets and bac population
    global nets
    nets = []
    global bac_population
    bac_population =  []
    global grid_array
    grid_array = np.array([])
    

    bacteria = Bacteria(x=150, y=250)
    bac_population.append(bacteria)
    grid_array = create_grids(grid_array).reshape(10,10)

    #first_tile = grid_array[0,0]
    three_two_tile = grid_array[1,3]
    three_two_tile.change_colour((0,0,0))

    def redraw_window():
        WIN.blit(BG,(0,0))
        #tile.draw(WIN)
        for row in grid_array:
            for tile in row:
                tile.draw(WIN)
        for bac in bac_population:
            bac.draw(WIN)
            statistics(bac)

        pygame.display.update()
        

    while run:
        clock.tick(FPS)
        for bac in bac_population:
            bac.eat()
            bac.radiate()
            #bac.move(direction="right")
            
        redraw_window()
        bac.see()

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
