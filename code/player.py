import pygame
import requests
from support import import_folder
#This file creates our player, including their speed, animations, and gravity, as well as our client input data.
url = 'http://localhost:5000'


class Player(pygame.sprite.Sprite):
    #Creating our player image
    def __init__(self,pos,surface,create_jump_particles):
        super().__init__()
        self.import_char_assets()
        self.frame_index = 0
        self.animation_speed = 0.2
        self.jump_counter = 0
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)

        #particle effects
        self.import_particle_effect()
        self.particle_frame_index = 0
        self.particle_animation_speed = 0.2
        self.display_surface = surface
        self.create_jump_particles = create_jump_particles
        
        #player movement
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 5
        self.gravity = 0.8
        self.jump_speed = -20
        
        #player status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

    #Importing image data for animations
    def import_char_assets(self):
        char_path = '../PixelArt/player/Doggo/'
        self.animations = {
            'idle':[],
            'run':[],
            'jump':[],
            'fall':[]
        }

        for animation in self.animations.keys():
            full_path = char_path + animation
            self.animations[animation] = import_folder(full_path)
    
    def import_particle_effect(self):
        self.run_effect = import_folder('../PixelArt/player/Particles/run')
        
    #animate the frames
    def animate(self):
        animation = self.animations[self.status]
        
        #loop over frame index
        self.frame_index += self.animation_speed
        if self.status == 'idle':
            if self.frame_index >= len(animation):
                self.frame_index = 0
        elif self.status == 'run':
            if self.frame_index >= len(animation):
                self.frame_index = 0
        elif self.status == 'jump' or 'fall':
            self.animation_speed = 0.1
            if self.frame_index >= len(animation):
                self.frame_index = (len(animation) - 1)
        
        #flip the image depending on the facing direction
        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image,True,False)
            self.image = flipped_image
        
        #make sure that changes in rectangle size don't affect player collision
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)
        else:
            self.rect = self.image.get_rect(center = self.rect.center)
            
    def animate_particle(self):
        if self.status == 'run' and self.on_ground:
            self.particle_frame_index += self.particle_animation_speed
            if self.particle_frame_index >= len(self.run_effect):
                self.particle_frame_index = 0
            
            particle_effect = self.run_effect[int(self.particle_frame_index)]
            
            if self.facing_right:
                pos = self.rect.bottomleft - pygame.math.Vector2(10,18)
                self.display_surface.blit(particle_effect,pos)
            
            if not self.facing_right:
                pos = self.rect.bottomright - pygame.math.Vector2(10,18)
                flipped_particles = pygame.transform.flip(particle_effect,True,False)
                self.display_surface.blit(flipped_particles,pos)

    #Receiving client input data
    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0
        
        #Player may only jump if they are not already moving vertically
        if keys[pygame.K_SPACE] and self.status == 'fall' and self.jump_counter == 0:
            self.jump()
            self.create_jump_particles(self.rect.midbottom)
            self.jump_counter += 1
        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()
            self.create_jump_particles(self.rect.midbottom)
            # goober_web = requests.get(url)
            # print(goober_web.text)
            
                   
    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0 and self.on_ground:
                self.status = 'run'
            else:
                self.status = 'idle'
    #Player gravity based on vertical direction
    #Gravity is constant, and can only be stopped by tile collision
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    #If jump, then player vertical direction = player jump speed
    def jump(self):
        self.direction.y = self.jump_speed

    #Updating the player position based on input data
    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.animate_particle()