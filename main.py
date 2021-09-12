import pygame
import os
import numpy as np
import time
import random
pygame.font.init()

#https://github.com/codewmax/NEAT-ChromeDinosaur/blob/master/main.py

#Config
WIDTH, HEIGHT = 1000, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.Font('freesansbold.ttf', 20)
pygame.display.set_caption("Bacteria sim")

#Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))


population = []
class Square:
    def __init__(self, x:int, y:int, colour:tuple=(random.randint(0,255),0,random.randint(0,255))):#rgb?
        self.x = x
        self.y = y
        self.image = None
        self.colour = colour
        
    def draw(self,window):
        pygame.draw.rect(surface = window, color = self.colour, rect = (self.x,self.y, 99,99))

    def change_colour(self,new_colour:tuple()):
        self.colour = new_colour


class Bacteria:
    def __init__(self, x:int, y:int, colour:tuple=(0,0,255), max_energy = 100,current_energy=50, max_speed=10, current_speed = 10, vision_range = 150 ):
        self.x = x
        self.y = y
        self.colour = colour
        self.max_energy = max_energy
        self.current_energy = current_energy
        self.max_speed = max_speed
        self.current_speed = current_speed
        self.vision_range = vision_range
        self.affinity_to_eat_red = 1
        self.affinity_to_eat_blue = 0
        self.hunger = self.max_energy - self.current_energy #does this need to be in a function?


    def draw(self,window):
        pygame.draw.circle(surface = window, color = self.colour, center = (self.x,self.y), radius =30)
    
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
            if self.y <= WIDTH-40:
                self.y +=self.max_speed

    def mitosis(self):
        pass

    def die(self):
        print("gg")
        population.pop()

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
        text_2 = FONT.render(f'Population:{str(len(population))}', True, (0, 255, 0)) 

        WIN.blit(text_1, (50, 50))
        WIN.blit(text_2, (50, 100))



def main():
    run = True
    FPS = 60
    clock = pygame.time.Clock()
    grid_array = np.array([])
    

    bacteria = Bacteria(x=200, y=200)
    population.append(bacteria)
    print(len(population))
    grid_array = create_grids(grid_array).reshape(10,10)

    #first_tile = grid_array[0,0]
    second_tile = grid_array[1,0]
    second_tile.change_colour((0,0,0))

    def redraw_window():
        WIN.blit(BG,(0,0))
        #tile.draw(WIN)
        for row in grid_array:
            for tile in row:
                tile.draw(WIN)
        for bac in population:
            bac.draw(WIN)
            statistics(bac)

        pygame.display.update()
        

    while run:
        clock.tick(FPS)
        for bac in population:
            bac.eat()
            bac.radiate()
            bac.move()
        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False


main()
