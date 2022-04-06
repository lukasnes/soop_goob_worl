import pygame, sys
from settings import *
from ui import UI
from level import Level
from overworld import Overworld
from communicator import Communicator

class Game:
    status = 'overworld'
    def __init__(self):
        
        #game attributes
        self.max_level = 0
        self.max_health = 100
        self.curr_health = 45
        self.bacon_amt = 0
        self.egg = False
        
        #overworld creation
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
        Game.status = 'overworld'
        
    def create_lvl(self,current_lvl):
        start_time = pygame.time.get_ticks()
        self.bacon_amt = 0
        self.level = Level(current_lvl,screen,self.create_overworld,self.create_end_of_lvl,start_time,self.get_bacon,self.get_egg)
        self.ui = UI(screen,current_lvl)
        self.status = 'level'
        Game.status = 'level'
        
    def create_end_of_lvl(self,current_lvl,new_max,start_time,bacon_amt,egg):
        end_time = pygame.time.get_ticks()
        self.lvl_end = Communicator(current_lvl,screen,self.create_overworld,new_max,start_time,end_time,bacon_amt,egg)
        self.status = 'lvl-end'
        Game.status = 'lvl-end'
        
    def get_bacon(self,amount):
        self.bacon_amt += amount
        
    def get_egg(self):
        self.egg = True
        
    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        elif self.status == 'level':
            self.level.run()
            self.ui.create_UI(self.curr_health,self.max_health,self.bacon_amt,self.egg)
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
                
        if Communicator.username_active:
            if event.type == pygame.KEYDOWN and Game.status == 'lvl-end':
                if event.key == pygame.K_BACKSPACE:
                    Communicator.user_text = Communicator.user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    Communicator.username_active = False
                elif len(Communicator.user_text) <= 20:
                    Communicator.user_text += f'{event.unicode}'
                
        if Communicator.pass_active:
            if event.type == pygame.KEYDOWN and Game.status == 'lvl-end':
                if event.key == pygame.K_BACKSPACE:
                    Communicator.password_text = Communicator.password_text[:-1]
                elif event.key == pygame.K_RETURN:
                    Communicator.pass_active = False
                elif len(Communicator.password_text) <= 20:
                    Communicator.password_text += f'{event.unicode}'
            
    screen.fill('#acc18a')
    game.run()
    
    pygame.display.update()
    clock.tick(60)