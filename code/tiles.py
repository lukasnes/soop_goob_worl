import pygame
from support import import_folder

class Tile(pygame.sprite.Sprite):
    def __init__(self,size,x,y):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.rect = self.image.get_rect(topleft = (x,y))
        
    def update(self,shift):
        self.rect.x += shift
        
class StaticTile(Tile):
    def __init__(self,size,x,y,surface):
        super().__init__(size,x,y)
        self.image = surface

class StumpTile(StaticTile):
    def __init__(self,size,x,y):
        super().__init__(size,x,y,pygame.image.load('../PixelArt/stump/stump_tiles.png').convert_alpha())

class AnimeTile(Tile):
    def __init__(self,size,x,y,path):
        super().__init__(size,x,y)
        self.frames=import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        
    def anime(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        
    def update(self,shift):
        self.anime()
        self.rect.x += shift
        
class Coin(AnimeTile):
    def __init__(self, size, x, y, path, type):
        super().__init__(size, x, y, path)
        center_x = x + int(size / 2)
        center_y = y + int(size / 2)
        self.type = type
        self.rect = self.image.get_rect(center = (center_x,center_y))
    
    def __repr__(self):
        return f"<Pickup type={self.type}>"