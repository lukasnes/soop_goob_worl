from csv import reader
from settings import tile_size
import pygame

def import_csv(path):
    terrain_map = []
    with open(path) as map:
        level = reader(map,delimiter = ',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map

def import_tiles(path):
    surface = pygame.image.load(path).convert_alpha()
    tiles_x = int(surface.get_width() / tile_size)
    tiles_y = int(surface.get_height() / tile_size)
    
    cut_tiles = []
    for row in range(tiles_y):
        for col in range(tiles_x):
            x = col * tile_size
            y = row * tile_size
            new_surf = pygame.Surface((tile_size,tile_size))
            new_surf.blit(surface,(0,0),pygame.Rect(x,y,tile_size,tile_size))
            cut_tiles.append(new_surf)
            
    return cut_tiles