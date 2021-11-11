import random
import pygame

class Square:
    def __init__(self, x:int, y:int, colour:list=(random.randint(0,255),0,random.randint(0,255))):#rgb?
        self.x = x
        self.y = y
        self.image = None
        self.blue = colour[2]
        self.red = colour[0]
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

