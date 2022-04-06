import pygame
from tiles import AnimeTile
from random import randint

class Enemy(AnimeTile):
    enemy_type = {
        0:'crab',
        1:'lion',
        2:'lizard',
        3:'monke',
        5:'cyclops',
        6:'flow',
        7:'monk',
        8:'turt'}
    enemy_speed = {
        'crab': (0,0),
        'lion': (8,10),
        'lizard': (1,3),
        'monke': (4,8),
        'cyclops': (1,10),
        'flow': (0,0),
        'monk': (6,8),
        'turt': (2,4)}
    def __init__(self,size,x,y,type):
        super().__init__(size,x,y,f"../PixelArt/enemy/{type}")
        self.rect.y += size - self.image.get_height()
        self.rect.x += size - (self.image.get_width()*1.5)
        
        self.type = type
        self.speed = randint(*Enemy.enemy_speed[type])
        
    def move(self):
        self.rect.x += self.speed
        
    def rev_img(self):
        if self.speed < 0:
            self.image = pygame.transform.flip(self.image,True,False)
            
    def rev(self):
        self.speed *= -1
        
    def update(self, shift):
        self.rect.x += shift
        self.anime()
        self.move()
        self.rev_img()