from os import stat
import pygame, sys
from communicator import Communicator
from settings import *
from overworld import Overworld
from level import Level

class Game:
    def __init__(self):
        self.max_level = 0
        self.overworld = Overworld(0,
                                   self.max_level,
                                   screen,
                                   self.create_lvl)
        self.status = 'overworld'
        
    def create_overworld(self,current_lvl,new_max):
        if new_max > self.max_level:
            self.max_level = new_max
        self.overworld = Overworld(current_lvl,
                                   self.max_level,
                                   screen,
                                   self.create_lvl)
        self.status = 'overworld'
        
    def create_lvl(self,current_lvl):
        start_time = pygame.time.get_ticks()
        self.level = Level(current_lvl,screen,self.create_overworld,self.create_end_of_lvl,start_time)
        self.status = 'level'
        
    def create_end_of_lvl(self,current_lvl,new_max,start_time):
        end_time = pygame.time.get_ticks()
        self.lvl_end = Communicator(current_lvl,screen,self.create_overworld,new_max,start_time,end_time)
        self.status = 'lvl-end'
        
    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        elif self.status == 'level':
            self.level.run()
        elif self.status == 'lvl-end':
            self.lvl_end.run()

#Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    screen.fill('grey')
    game.run()
    
    pygame.display.update()
    clock.tick(60)