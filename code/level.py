import pygame
from support import import_csv, import_tiles
from settings import tile_size
from tiles import Tile, StaticTile

class Level:
    def __init__(self,level_data,surface):
        #screen setup
        self.display_surface = surface
        self.world_shift = -2
        
        #terrain setup
        terrain_layout = import_csv(level_data['terrain'])
        self.terrain_sprites = self.create_tiles(terrain_layout,'terrain')
        #foliage setup
        tree_layout = import_csv(level_data['trees'])
        brush_layout = import_csv(level_data['brush'])
        self.tree_sprites = self.create_tiles(tree_layout,'tree')
        self.brush_sprites = self.create_tiles(brush_layout,'brush')
        
    def create_tiles(self,layout,type):
        sprites = pygame.sprite.Group()
        path = f'../PixelArt/{type}/{type}_tiles.png'

        
        for row_index,row in enumerate(layout):
            for col_index,val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size
                    
                    if type == 'terrain' or 'tree' or 'brush':
                        tile_list = import_tiles(path)
                        tile = tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,tile)
                        sprites.add(sprite)
        
        return sprites
        
    def run(self):
        #run the entire level
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift)
        self.tree_sprites.draw(self.display_surface)
        self.tree_sprites.update(self.world_shift)
        self.brush_sprites.draw(self.display_surface)
        self.brush_sprites.update(self.world_shift)