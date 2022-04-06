import pygame
from game_data import levels

class Node(pygame.sprite.Sprite):
    def __init__(self,pos,locked,speed):
        super().__init__()
        self.image = pygame.Surface((100,80))
        if not locked:
            self.image.fill('red')
        else:
            self.image.fill('black')
        self.rect = self.image.get_rect(center = pos)
        
        self.detect = pygame.Rect(self.rect.centerx - (speed/2), self.rect.centery - (speed/2), speed, speed)

class P_Icon(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.pos = pos
        self.image = pygame.Surface((20,20))
        self.image.fill('blue')
        self.rect = self.image.get_rect(center = pos)
    
    def update(self):
        self.rect.center = self.pos

class Overworld:
    def __init__(self,start_level,max_level,surface,create_lvl):
        
        #setup
        self.display_surface = surface
        self.max_level = max_level
        self.current_level = start_level
        self.create_lvl = create_lvl
        
        #movement
        self.moving = False
        self.move_dir = pygame.math.Vector2(0,0)
        self.speed = 8
        
        #sprites
        self.setup_nodes()
        self.setup_icon()
        
    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()
        for i,nodes in enumerate(levels.values()):
            if i <= self.max_level:
                node_sprite = Node(nodes['node_pos'],False,self.speed)
            else:
                node_sprite = Node(nodes['node_pos'],True,self.speed)
            self.nodes.add(node_sprite)
            
    def draw_paths(self):
        points = [node['node_pos'] for i,node in enumerate(levels.values()) if i <= self.max_level]
        pygame.draw.lines(self.display_surface,'purple',False,points,6)
        
    def setup_icon(self):
        self.icon = pygame.sprite.GroupSingle()
        icon_sprite = P_Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)
        
    def input(self):
        keys = pygame.key.get_pressed()
        
        if not self.moving:
            if keys[pygame.K_RIGHT] and self.current_level < self.max_level:
                self.move_dir = self.get_movement(True)
                self.current_level += 1
                self.moving = True
            elif keys[pygame.K_LEFT] and self.current_level > 0:
                self.move_dir = self.get_movement(False)
                self.current_level -= 1
                self.moving = True
            elif keys[pygame.K_SPACE]:
                self.create_lvl(self.current_level)
            
    def get_movement(self,forward):
        start = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)
        
        if forward:
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level + 1].rect.center)
        else:
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level - 1].rect.center)
        
        return (end - start).normalize()
    
    def update_icon(self):
        if self.moving and self.move_dir:
            self.icon.sprite.pos += self.move_dir * self.speed
            target = self.nodes.sprites()[self.current_level]
            if target.detect.collidepoint(self.icon.sprite.pos):
                self.moving = False
                self.move_dir = pygame.math.Vector2((0,0))

        
    def run(self):
        self.input()
        self.update_icon()
        self.icon.update()
        if self.max_level > 0:
            self.draw_paths()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)