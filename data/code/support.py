from csv import reader
from data.code.settings import tile_size
import pygame
from os import walk
import math

def import_folder(path):
    surf_list = []
    
    for _,__,files in walk(path):
        for image in files:
            full_path = path + '/' + image
            surf = pygame.image.load(full_path).convert_alpha()
            surf_list.append(surf)
            
    return surf_list

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
            new_surf = pygame.Surface((tile_size,tile_size),flags = pygame.SRCALPHA)
            new_surf.blit(surface,(0,0),pygame.Rect(x,y,tile_size,tile_size))
            cut_tiles.append(new_surf)
            
    return cut_tiles

def create_time(start_time,end_time):
    time_num = end_time - start_time
    minute_score = math.trunc((time_num / 1000) / 60)
    second_score = math.trunc((time_num / 1000) % 60)
    millisecond_score = math.trunc((time_num % 1000) % 60)
    
    if second_score < 10 and millisecond_score < 10:
        score = f"{minute_score}: 0{second_score}: 0{millisecond_score}"
    elif second_score < 10:
        score = f"{minute_score}: 0{second_score}: {millisecond_score}"
    elif millisecond_score < 10:
        score = f"{minute_score}: {second_score}: 0{millisecond_score}"
    else:
        score = f"{minute_score}: {second_score}: {millisecond_score}"
    
    return score