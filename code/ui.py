import pygame
from settings import screen_height, screen_width

class UI:
    lvl_bacon_max = {
        0:36,
        1:24,
        2:23,
        3:12,
        4:33,
        5:12,
        6:57,
        7:44}
    def __init__(self,screen,curr_lvl):
        
        #setup
        self.screen = screen
        self.colors = {
            'black':'#2e1f27',
            'navy':'#104f55',
            'blue':'#6883ba',
            'neon':'#59f8e8',
            'white':'#f7ebe8'}
        self.font = pygame.font.Font('../PixelArt/Font/Pixeltype.ttf',50)
        self.lvl = curr_lvl
        
        #health
        self.health_bar = pygame.image.load('../PixelArt/ui/health_bar.png')
        self.bar_top = 50
        self.bar_left = 80
        self.bar_max_w = 89
        self.bar_h = 4
        
        #bacon
        self.bacon = pygame.image.load('../PixelArt/ui/bacon.png')
            
        #egg
        self.egg = pygame.image.load('../PixelArt/ui/egg1.png')
        
    def create_UI(self,curr_health,max_health,bacon_amt,egg_collected):
        self.UI_box()
        self.show_health(curr_health,max_health)
        self.show_bacon(bacon_amt)
        self.show_egg(egg_collected)
        
    def show_health(self,current,full):
        self.screen.blit(self.health_bar,(20,20))
        hp_ratio = current / full
        curr_bar_width = self.bar_max_w * hp_ratio
        health_bar = pygame.Rect(self.bar_left,self.bar_top,curr_bar_width,self.bar_h)
        pygame.draw.rect(self.screen,self.colors['neon'],health_bar)
    
    def show_bacon(self,amount):
        bacon_text = self.font.render(f"{amount}/{UI.lvl_bacon_max[self.lvl]}",True,self.colors['neon'])
        
        self.screen.blit(self.bacon,(50,100))
        self.screen.blit(bacon_text,(115,105))
    
    def show_egg(self,collected):
        if collected:
            self.egg = pygame.image.load('../PixelArt/ui/egg2.png')
        else:
            self.egg = pygame.image.load('../PixelArt/ui/egg1.png')
        self.screen.blit(self.egg,(60,145))
    
    def UI_box(self):
        box_rect = pygame.Rect(0,0,(screen_width/5),(screen_height/3)-30)
             
        # self.screen.blit(box,box_rect)
        pygame.draw.rect(self.screen,self.colors['blue'],box_rect,0,0,0,100,100,100)
        pygame.draw.rect(self.screen,self.colors['black'],box_rect,5,0,0,100,100,100)