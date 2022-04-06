from tiles import AnimeTile, StaticTile
from support import import_folder
from settings import vertical_tiles, tile_size, screen_width
from random import choice, randint
import pygame

class Sky():
    
    def __init__(self,horizon,style = 'level'):
        self.top = pygame.image.load('../PixelArt/sky/sky_top.png')
        self.mid = pygame.image.load('../PixelArt/sky/sky_mid.png')
        self.bot = pygame.image.load('../PixelArt/sky/sky_bot.png')
        self.horizon = horizon
        
        #stretch
        self.top = pygame.transform.scale(self.top,(screen_width,tile_size))
        self.mid = pygame.transform.scale(self.mid,(screen_width,tile_size))
        self.bot = pygame.transform.scale(self.bot,(screen_width,tile_size))
        
        self.style = style
        if self.style == 'overworld':
            clouds = import_folder('../PixelArt/overworld/decorations/clouds')
            self.clouds = []
            
            for cloud in [choice(clouds) for image in range(20)]:
                x = randint(0,screen_width)
                y = randint(0,(self.horizon * tile_size))
                cloud_rect = cloud.get_rect(midbottom = (x,y))
                self.clouds.append((cloud,cloud_rect))
        
    def draw(self,surface):
        for row in range(vertical_tiles):
            y = row * tile_size
            if row < self.horizon:
                surface.blit(self.top,(0,y))
            elif row == self.horizon:
                surface.blit(self.mid,(0,y))
            else:
                surface.blit(self.bot,(0,y))
            
            if self.style == 'overworld':
                for cloud in self.clouds:
                    surface.blit(cloud[0],cloud[1])
    
class Void:
    def __init__(self,top,level_width):
        void_start = -screen_width
        void_width = 64
        tile_x = int((level_width + screen_width) / void_width)
        self.void_sprites = pygame.sprite.Group()
        
        for tile in range(tile_x):
            x = tile * void_width + void_start
            y = top
            sprite = AnimeTile(void_width,x,y,"../PixelArt/void")
            self.void_sprites.add(sprite)
            
    def draw(self,surface,shift):
        self.void_sprites.update(shift)
        self.void_sprites.draw(surface)
        
class Clouds:
    def __init__(self,horizon,level_width,count):
        clouds = import_folder('../PixelArt/clouds')
        min_x = -screen_width
        max_x = level_width + screen_width
        min_y = 0
        max_y = horizon
        self.cloud_sprites = pygame.sprite.Group()
        
        for cloud in range(count):
            cloud = choice(clouds)
            x = randint(min_x,max_x)
            y = randint(min_y,max_y)
            sprite = StaticTile(0,x,y,cloud)
            self.cloud_sprites.add(sprite)
            
    def draw(self,surface,shift):
        self.cloud_sprites.update(shift)
        self.cloud_sprites.draw(surface)