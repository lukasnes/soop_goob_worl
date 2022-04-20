import pygame
from data.code.game_data import levels
import requests
from data.code.settings import screen_height, screen_width
from data.code.support import create_time
from data.code.ui import UI
import math

class Communicator(): 
    user_text = ''
    username_active = False
    
    password_text = ''
    pass_active = False
    
    lvl_names = {
        0:"Lolligagging through Liz Land",
        1:"Hopping Turtle Mountain",
        2:"Raiding the Pride",
        3:"Caverns of the Wise",
        4:"Jump, Monke! Jump!",
        5:"Ralta's Respite",
        6:"Steve",
        7:"Pincer Cape"}

    def __init__(self,current_lvl,screen,create_overworld,new_max,start_time,end_time,bacon_amt,egg):
        
        self.display_surface = screen
        
        self.create_overworld = create_overworld
        
        self.current_lvl = current_lvl
        self.new_max = new_max
        self.start_time = start_time
        self.end_time = end_time
        self.score = ''
        self.score_num = 0
        self.bacon_amt = bacon_amt
        self.total_bacon = UI.lvl_bacon_max[current_lvl]
        self.egg = egg
        
        self.font = pygame.font.Font('./data/PixelArt/Font/Pixeltype.ttf', 50)
        self.text_error = ''
        self.white = "#f7ebe8"
        self.neon = "#59f8e8"
        self.blue = "#6883ba"
        self.navy = "#104f55"
        self.black = "#2e1f27"
    
    def input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_RCTRL]:
            self.create_overworld(self.current_lvl,self.new_max)
    
    def display_score(self):
        score_box = pygame.Surface(((screen_width/2),(((screen_height/5)*3)-20)))
        score_box.fill(self.blue)
        score_box_rect = score_box.get_rect(topleft = (0,0))
        score_box_title = self.font.render('Your stats:',True,self.neon)
        
        self.score_num = self.end_time - self.start_time
        self.score = create_time(self.start_time,self.end_time)
        score_text = self.font.render(self.score,True,self.neon)
        score_label = self.font.render('Level Time:',True,self.neon)
        
         
        bacon = pygame.image.load('./data/PixelArt/coins/bacon/bacon1.png')
        bacon_text = self.font.render('{}/{}'.format(self.bacon_amt,self.total_bacon),True,self.neon)
        bacon_label = self.font.render('Bacon Collected:',True,self.neon)

        
        if self.egg:
            egg = pygame.image.load('./data/PixelArt/ui/egg2.png')
        else:
            egg = pygame.image.load('./data/PixelArt/ui/egg1.png')
        egg_label = self.font.render('Void Egg Collected:',True,self.neon)
        
        self.display_surface.blit(score_box,score_box_rect)
        pygame.draw.rect(self.display_surface,self.navy,score_box_rect,8)
        self.display_surface.blit(score_box_title,(score_box_rect.x + 200,score_box_rect.y + 30))  
        self.display_surface.blit(score_text,(score_box_rect.x + 200,score_box_rect.y + 125))
        self.display_surface.blit(score_label,(score_box_rect.x + 30,score_box_rect.y + 125))
        self.display_surface.blit(bacon_text,(score_box_rect.x + 350,score_box_rect.y + 200))
        self.display_surface.blit(bacon_label,(score_box_rect.x + 30,score_box_rect.y + 200))
        self.display_surface.blit(bacon,(score_box_rect.x + 300,score_box_rect.y + 195))
        self.display_surface.blit(egg,(score_box_rect.x + 350,score_box_rect.y + 250))
        self.display_surface.blit(egg_label,(score_box_rect.x + 30,score_box_rect.y + 275))
        
    def display_goob_web(self):
        web_box = pygame.Surface(((screen_width/2),(((screen_height/5)*3)-20)))
        web_box.fill(self.navy)
        web_box_rect = web_box.get_rect(topright = (screen_width,0))
        web_box_text_1 = self.font.render("Don't have an account? That's okay!",True,self.neon)
        web_box_text_2 = self.font.render("Go to goober-web.herokuapp.com",True,self.neon)
        web_box_text_3 = self.font.render("to create an account and compare",True,self.neon)
        web_box_text_4 = self.font.render("your score to other players!",True,self.neon)
        
        self.display_surface.blit(web_box,web_box_rect)
        pygame.draw.rect(self.display_surface,self.black,web_box_rect,8)
        self.display_surface.blit(web_box_text_1,(web_box_rect.x + 40, web_box_rect.y + 100))
        self.display_surface.blit(web_box_text_2,(web_box_rect.x + 40, web_box_rect.y + 175))
        self.display_surface.blit(web_box_text_3,(web_box_rect.x + 40, web_box_rect.y + 250))
        self.display_surface.blit(web_box_text_4,(web_box_rect.x + 40, web_box_rect.y + 325))
        
    def display_input_box(self):
        input_box = pygame.Surface(((screen_width/2),(screen_height/3)))
        input_box.fill(self.blue)
        input_box_rect = input_box.get_rect(bottomleft = (0,screen_height))
        
        input_box_label = self.font.render("Enter your Goober Web information!",True,self.neon)
        
        self.display_surface.blit(input_box,input_box_rect)
        pygame.draw.rect(self.display_surface,self.black,input_box_rect,8)
        self.display_surface.blit(input_box_label,(50,(screen_height - 230)))
    
    def display_username_field(self):
        text = self.font.render(Communicator.user_text,True,self.neon)
        
        input_rect = pygame.Rect(260,(screen_height - 160),140,48)
        input_rect.w = max(150,text.get_width() + 10)
        input_surf = pygame.Surface((input_rect.w - 8,40))
        input_color = self.black
        
        username_label = self.font.render("Username",True,self.neon)
        
        color_active = self.white
        color_passive = self.navy
        color = color_passive
        
        if Communicator.username_active:
            color = color_active
        else:
            color = color_passive
        input_surf.fill(color)
        
        mouse = pygame.mouse.get_pressed()
        if mouse[0]:
            if input_rect.collidepoint(pygame.mouse.get_pos()):
                Communicator.pass_active = False
                Communicator.username_active = True

        pygame.draw.rect(self.display_surface,input_color,input_rect,4)
        self.display_surface.blit(input_surf,(input_rect.x + 4, input_rect.y + 4))
        self.display_surface.blit(text,(input_rect.x + 5,input_rect.y + 10))
        self.display_surface.blit(username_label,(100,(screen_height - 150)))
    
    def display_password_field(self):
        text = self.font.render(Communicator.password_text,True,self.neon)
        
        input_rect = pygame.Rect(260,(screen_height - 90),140,48)
        input_rect.w = max(150,text.get_width() + 10)
        input_surf = pygame.Surface((input_rect.w - 8,40))
        input_color = self.black
        
        password_label = self.font.render("Password",True,self.neon)
        
        color_active = self.white
        color_passive = self.navy
        color = color_passive
        
        if Communicator.pass_active:
            color = color_active
        else:
            color = color_passive
        input_surf.fill(color)
        
        mouse = pygame.mouse.get_pressed()
        if mouse[0]:
            if input_rect.collidepoint(pygame.mouse.get_pos()):
                Communicator.username_active = False
                Communicator.pass_active = True

        pygame.draw.rect(self.display_surface,input_color,input_rect,4)
        self.display_surface.blit(input_surf,(input_rect.x + 4, input_rect.y + 4))
        self.display_surface.blit(text,(input_rect.x + 5,input_rect.y + 10))
        self.display_surface.blit(password_label,(100,(screen_height - 80)))
    
    def display_send_data_box(self):
        next_lvl_box = pygame.Surface(((screen_width/2),(screen_height/3)))
        next_lvl_box.fill(self.navy)
        next_lvl_rect = next_lvl_box.get_rect(bottomright = (screen_width,screen_height))
        
        self.display_surface.blit(next_lvl_box,next_lvl_rect)
        pygame.draw.rect(self.display_surface,self.black,next_lvl_rect,8)
        
    def skip_to_overworld(self):
        skip_label = self.font.render("Return to the game.",True,self.neon)
        skip_btn = pygame.Surface((((screen_width/2)-30),60))
        skip_btn.fill(self.blue)
        btn_rect = skip_btn.get_rect(topleft = (((screen_width/2)+15),(((screen_height/3)*2)+150)))
        
        mouse = pygame.mouse.get_pressed()
        if mouse[0]:
            if btn_rect.collidepoint(pygame.mouse.get_pos()):
                self.create_overworld(self.current_lvl,self.new_max)
                
        self.display_surface.blit(skip_btn,btn_rect)
        pygame.draw.rect(self.display_surface,self.black,btn_rect,3)
        self.display_surface.blit(skip_label,(btn_rect.x + 10,btn_rect.y + 15))
    
    def send_data(self):
        send_data_label = self.font.render("Send your level data to the Goober Web!",True,self.neon)
        send_data_btn = pygame.Surface((((screen_width/2)-30),60))
        send_data_btn.fill(self.blue)
        btn_rect = send_data_btn.get_rect(topleft = (((screen_width/2)+15),(((screen_height/3)*2)+50)))
        
        data = {
            "username":Communicator.user_text,
            "password":Communicator.password_text,
            "lvl":self.current_lvl,
            "max_lvl":self.new_max,
            "lvl_time":self.score_num,
            'lvl_name':Communicator.lvl_names[self.current_lvl],
            'bacon_amt':self.bacon_amt,
            'egg':self.egg}
        
        if Communicator.user_text != '' and Communicator.password_text != '':
            mouse = pygame.mouse.get_pressed()
            if mouse[0]:
                if btn_rect.collidepoint(pygame.mouse.get_pos()):
                    successful_request = requests.post('https://goober-web.herokuapp.com/goober_data',data=data)
                    if successful_request.text == "True":
                       self.create_overworld(self.current_lvl,self.new_max)
                    else:
                        self.text_error = successful_request.text
        else:
            self.text_error = "You must enter a username and password in order to send your Goober Data."
        
        self.display_surface.blit(send_data_btn,btn_rect)
        pygame.draw.rect(self.display_surface,self.black,btn_rect,3)
        self.display_surface.blit(send_data_label,(btn_rect.x + 10,btn_rect.y + 15))
    
    def return_to_overworld(self):
        pass
    
    def error_text(self,text):
        error_text = self.font.render(text,True,self.neon)
        error_surf = pygame.Surface(((screen_width - 20),70))
        error_surf.fill(self.black)
        error_rect = error_surf.get_rect(bottomleft = (10,(((screen_height/3)*2))))
            
        self.display_surface.blit(error_surf,error_rect)
        pygame.draw.rect(self.display_surface,self.white,error_rect,3)
        self.display_surface.blit(error_text,(50,(((screen_height/3)*2)-50)))
     
    def run(self):
        self.input()
        self.display_input_box()
        self.display_send_data_box()
        self.display_username_field()
        self.display_password_field()
        self.send_data()
        self.skip_to_overworld()
        self.error_text(self.text_error)
        self.display_score()
        self.display_goob_web()