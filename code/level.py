import pygame
from support import import_csv, import_tiles
from settings import tile_size, screen_height, screen_width
from enemy import Enemy
from tiles import Tile, StaticTile, AnimeTile, Coin, StumpTile
from decoration import Sky, Void, Clouds
from player import Player
from particles import ParticleEffect
from game_data import levels

class Level:
    def __init__(self,current_level,surface,create_overworld,create_end_of_lvl,start_time,get_bacon,get_egg):
        #screen setup
        self.display_surface = surface
        self.world_shift = 0
        
        #overworld & lvl end
        self.start_time = start_time
        self.create_overworld = create_overworld
        self.create_end_of_lvl = create_end_of_lvl
        self.current_level = current_level
        level_data = levels[self.current_level]
        self.new_max_lvl = level_data['unlock']
        
        #particle effects
        self.particle_sprite = pygame.sprite.GroupSingle()
        self.player_on_gound = False
        
        #player setup
        player_layout = import_csv(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)
        
        #user interface
        self.get_bacon = get_bacon
        self.get_egg = get_egg
        self.bacon_amt = 0
        self.egg = False
        
        #terrain setup
        terrain_layout = import_csv(level_data['terrain'])
        self.terrain_sprites = self.create_tiles(terrain_layout,'terrain')
        
        #stump setup
        stump_layout = import_csv(level_data['stump'])
        self.stump_sprites = self.create_tiles(stump_layout,'stump')
        
        #foliage setup
        tree_layout = import_csv(level_data['trees'])
        self.tree_sprites = self.create_tiles(tree_layout,'tree')
        brush_layout = import_csv(level_data['brush'])
        self.brush_sprites = self.create_tiles(brush_layout,'brush')
        
        #coin setup
        coin_layout = import_csv(level_data['coins'])
        self.coin_sprites = self.create_tiles(coin_layout,'coins')
        
        #enemy setup
        enemy_layout = import_csv(level_data['enemies'])
        self.enemy_sprites = self.create_tiles(enemy_layout,'enemy')
        
        #constraint setup
        constraint_layout = import_csv(level_data['constraints'])
        self.constraint_sprites = self.create_tiles(constraint_layout,'constraint')
        
        #sky setup
        self.sky = Sky(9)
        level_width = len(terrain_layout[0]) * tile_size
        self.clouds = Clouds(600,level_width,30)
        self.void = Void(screen_height - 50,level_width)
        
        
    def create_tiles(self,layout,type):
        sprites = pygame.sprite.Group()
        path = f'../PixelArt/{type}/{type}_tiles.png'

        
        for row_index,row in enumerate(layout):
            for col_index,val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size
                    
                    if type in ['tree','terrain','brush']:
                        tile_list = import_tiles(path)
                        tile = tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,tile)
                    if type == 'stump':
                        tile_list = import_tiles(path)
                        tile = tile_list[int(val)]
                        sprite = StumpTile(tile_size,x,y)
                    if type == 'coins':
                        tile_list = import_tiles(path)
                        tile = tile_list[int(val)]
                        if int(val) == 0:
                            sprite = Coin(tile_size,x,y,'../PixelArt/coins/bacon','bacon')
                        if int(val) == 1:
                            sprite = Coin(tile_size,x,y,'../PixelArt/coins/egg','egg')
                    if type == 'enemy':
                        tile_list = import_tiles(path)
                        tile = tile_list[int(val)]
                        sprite = Enemy(tile_size,x,y,Enemy.enemy_type[int(val)])
                        
                    if type == 'constraint':
                        sprite = Tile(tile_size,x,y)
       
                    sprites.add(sprite)
        return sprites
    
    def player_setup(self,layout):
        for row_index,row in enumerate(layout):
            for col_index,val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '0':
                    sprite = Player((x,y),self.display_surface,self.create_jump_particles)
                    self.player.add(sprite)
                if val == '1':
                    sprite = AnimeTile(tile_size,x,y,"../PixelArt/goal")
                    self.goal.add(sprite)
    
    def create_jump_particles(self,pos):
        pos -= pygame.math.Vector2(0,10)
        jump_particle_sprite = ParticleEffect(pos,'jump')
        self.particle_sprite.add(jump_particle_sprite)
    
    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False
            
    def create_land_particles(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.particle_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(0,10)
            else:
                offset = pygame.math.Vector2(0,10)
            fall_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset,'land')
            self.particle_sprite.add(fall_particle)
    
    def enemy_turn(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy,self.constraint_sprites,False):
                enemy.rev()    
    
    #Scrolling the screen when the player hits the left or right quarter
    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        #If the player hits the left quarter, and is still moving
        if player_x < (screen_width / 5) * 2 and direction_x < 0:
            #Turn off player speed, and move the screen instead
            self.world_shift = 5
            player.speed = 0
        #If the player hits right quarter, and is still moving
        elif player_x > (screen_width / 5) * 3 and direction_x > 0:
            #Turn off player speed, and move the screen instead
            self.world_shift = -5
            player.speed = 0
        else:
            #Otherwise, if the player is not at the screen edges, don't move the world, just move the player
            self.world_shift = 0
            player.speed = 5
      
    #Horizontal tile collision
    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        
        collidables = self.terrain_sprites.sprites() + self.stump_sprites.sprites()

        for sprite in collidables:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right
        
        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    #Vertical tile collision
    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        collidables = self.terrain_sprites.sprites() + self.stump_sprites.sprites()
        
        for sprite in collidables:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                    player.jump_counter = 0
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
                    
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False
        
    def death(self):
        if self.player.sprite.rect.top > screen_height:
            self.create_overworld(self.current_level,0)
    
    def win(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_BACKSPACE]:
            self.create_end_of_lvl(self.current_level,self.new_max_lvl,self.start_time,self.bacon_amt,self.egg)
        
        if pygame.sprite.spritecollide(self.player.sprite,self.goal,False):
            self.create_end_of_lvl(self.current_level,self.new_max_lvl,self.start_time,self.bacon_amt,self.egg)
    
    def bacon_n_eggs_acquired(self):
        collided_pickups = pygame.sprite.spritecollide(self.player.sprite,self.coin_sprites,True)
        for pickup in collided_pickups:
            if pickup.type == 'bacon':
                self.get_bacon(1)
                self.bacon_amt += 1
            if pickup.type == 'egg':
                self.get_egg()
                self.egg = True
        
    def run(self):
        #run the entire level
        
        #A sky in the sky
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface,self.world_shift)
        
        #Let there be trees
        self.tree_sprites.draw(self.display_surface)
        self.tree_sprites.update(self.world_shift)
        
        #And the earth shook with great force and lifted the mountains
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)
        
        
        #And upon the earth began to grow strange things, of purple and brown
        self.brush_sprites.update(self.world_shift)
        self.brush_sprites.draw(self.display_surface)
        
        #These strange things withered and died, leaving husks of their former selves
        self.stump_sprites.update(self.world_shift)
        self.stump_sprites.draw(self.display_surface)
        
        #Whence the eggs came, they do not know, but they do know they came before the chicken
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)
        
        #And where there are eggs, and bacon, there are the goobers.
        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_turn()
        self.enemy_sprites.draw(self.display_surface)
        
        #particle effects
        self.particle_sprite.update(self.world_shift)
        self.particle_sprite.draw(self.display_surface)
        
        #player sprites
        self.player.update()
        self.horizontal_movement_collision()
        
        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.create_land_particles()
        
        self.scroll_x()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)
        
        self.death()
        self.win()
        
        self.bacon_n_eggs_acquired()
        
        #And the water nourished the world
        self.void.draw(self.display_surface,self.world_shift)