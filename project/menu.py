import pygame
import keyboard
import random
from tkinter import messagebox
def runmenu():
  DARKORANGE = (250,150,100)

  pygame.init()
  menus_stack = ["screen"]
  def hi():
      print("hi")
  def show():
      messagebox.showinfo("info","hi user, this is my firstly game,btw do u like sun and my grass? okay so now ima explain you what is this game. so this sandbox game, where you spawn likee oblects and can make them roll or even break them so you can do anything. //creator: Atlantic Game Dev, Head Dev--samsoncat19//")




  info = keyboard.add_hotkey("i",show)
  screen = pygame.display.set_mode((800,600))
  settting = pygame.display.set_mode((800,600))
  running = True
  pygame.display.set_caption("physical sky breaker vA.01")

  def draw_set():
      screen.fill((200,200,200))
      day = pygame.Rect(193,82,100,50)
      night = pygame.Rect(93,82,100,50)
      back = pygame.Rect(0,0,80,80)
      pygame.draw.rect(screen,(240,20,10),back)
      font = pygame.font.SysFont(None,165)
      text = font.render("x",True,(250,250,250))
      screen.blit(text,(9,-20))
      pygame.draw.rect(screen,(100,150,200),night)
      pygame.draw.rect(screen,(20,20,80),day)
      font = pygame.font.SysFont(None,40)
      text = font.render("Menu modes",True,(250,250,250))
      screen.blit(text,(105,28))
      font = pygame.font.SysFont(None,40)
      text = font.render("Night",True,(20,20,80))
      screen.blit(text,(105,90))
      font = pygame.font.SysFont(None,40)
      text = font.render("Day",True,(250,250,80))
      screen.blit(text,(220,90))

    
      return{"back": back, "night": night, "day": day}
  def draw_screen():
      pygame.draw.ellipse(screen,DARKORANGE,(75,25,100,100))
      pygame.draw.ellipse(screen, (235,135,85),(85,35,80,80))
      pygame.draw.rect(screen, (10,100,10),(0,550,1000,80))
      pygame.draw.rect(screen, (50,150,50),(0,500,1000,60))
      pygame.draw.rect(screen, (25,125,25),(0,525,1000,50))
      pygame.draw.ellipse(screen,(50,150,50),(350,490,150,25))
      pygame.draw.ellipse(screen,(50,150,50),(300,480,150,23))
      pygame.draw.ellipse(screen,(50,150,50),(230,490,100,20))
      pygame.draw.ellipse(screen,(50,150,50),(40,490,100,30))
      pygame.draw.ellipse(screen,(50,150,50),(710,490,100,20))
      pygame.draw.ellipse(screen,(50,150,50),(-40,480,130,40))
      pygame.draw.ellipse(screen,(50,150,50),(750,485,130,30))
      pygame.draw.ellipse(screen,(50,150,50),(570,485,70,30))
      pygame.draw.ellipse(screen,(50,150,50),(580,490,80,20))
      
pygame.draw.circle
(screen,(240,240,255),(610,100),50)
      
pygame.draw.circle
(screen,(240,240,255),(490,100),50)
      
pygame.draw.circle
(screen,(240,240,255),(570,90),80)
      
pygame.draw.circle
(screen,(240,240,255),(715,100),45)
      
pygame.draw.circle
(screen,(240,240,255),(590,100),45)
      
pygame.draw.circle
(screen,(240,240,255),(650,90),70)
      starbut = pygame.Rect(315,220,150,60)
      setbut = pygame.Rect(315,280,150,60)
      tutbut = pygame.Rect(315,340,150,60)
      pygame.draw.rect(screen,(120,170,220),starbut)
      font = pygame.font.SysFont(None,40)
      text = font.render("Start",True,(220,220,220))
      screen.blit(text,(345,238))
      pygame.draw.rect(screen,(120,170,220),setbut)
      font = pygame.font.SysFont(None,35)
      text = font.render("Settings",True,(220,220,220))
      screen.blit(text,(327,298))
      pygame.draw.rect(screen,(120,170,220),tutbut)
      font = pygame.font.SysFont(None,35)
      text = font.render("Tutorial",True,(220,220,220))
      screen.blit(text,(330,358))
      font = pygame.font.SysFont(None,20)
      text = font.render(" vA.01 Alpha",True,(220,220,220))
      screen.blit(text,(0,580))
      pygame.draw.ellipse(screen,(150,80,30),(600,390,15,120))
      pygame.draw.ellipse(screen,(50,150,50),(559,490,90,20))
      pygame.draw.ellipse(screen,(65,165,65),(580,320,90,80))
      pygame.draw.ellipse(screen,(60,160,60),(550,320,90,80))
      pygame.draw.ellipse(screen,(50,150,50),(540,350,80,65))
      pygame.draw.ellipse(screen,(55,155,55),(565,335,80,65))
      pygame.draw.ellipse(screen,(50,150,50),(600,340,80,70))
      pygame.draw.ellipse(screen,(45,145,45),(570,355,85,60))
      return{"starbut": starbut, "tutbut": tutbut, "setbut": setbut}
  def draw_calamity():
     return "game"
    # back = pygame.Rect(0,0,80,80)
    # pygame.draw.rect(screen,(240,20,10),back)
    # font = pygame.font.SysFont(None,165)
    # text = font.render("x",True,(250,250,250))
    # screen.blit(text,(9,-20)) #game here \/
    # return{"back":back}


  def draw_gamech():
     calamity = pygame.Rect(200,200,300,300)
     back = pygame.Rect(0,0,80,80)
     pygame.draw.rect(screen,(240,20,10),back)
     pygame.draw.rect(screen,(20,20,210),calamity)
     font = pygame.font.SysFont(None,165)
     text = font.render("x",True,(250,250,250))
     screen.blit(text,(9,-20))
     return{"back": back,"calamity": calamity}
  def draw_nightscreen():
      pygame.draw.rect(screen,(250,250,250),(300,90,5,5))
      pygame.draw.rect(screen,(250,250,250),(200,20,5,5))
      pygame.draw.rect(screen,(250,250,250),(350,20,5,5))
      pygame.draw.rect(screen,(250,250,250),(400,100,5,5))
      pygame.draw.rect(screen,(250,250,250),(750,20,5,5))
      pygame.draw.rect(screen,(250,250,250),(50,40,5,5))
      pygame.draw.rect(screen,(250,250,250),(180,100,5,5))
      pygame.draw.rect(screen,(250,250,250),(20,100,5,5))
      pygame.draw.rect(screen,(250,250,250),(770,90,5,5))
      pygame.draw.rect(screen,(250,250,250),(650,10,5,5))
      pygame.draw.rect(screen,(250,250,250),(450,30,5,5))
      pygame.draw.ellipse(screen,(170,170,170),(75,25,100,100))
      pygame.draw.ellipse(screen, (190,190,190),(85,35,80,80))
      pygame.draw.rect(screen, (10,100,10),(0,550,1000,80))
      pygame.draw.rect(screen, (50,150,50),(0,500,1000,60))
      pygame.draw.rect(screen, (25,125,25),(0,525,1000,50))
      pygame.draw.ellipse(screen,(50,150,50),(350,490,150,25))
      pygame.draw.ellipse(screen,(50,150,50),(300,480,150,23))
      pygame.draw.ellipse(screen,(50,150,50),(230,490,100,20))
      pygame.draw.ellipse(screen,(50,150,50),(40,490,100,30))
      pygame.draw.ellipse(screen,(50,150,50),(710,490,100,20))
      pygame.draw.ellipse(screen,(50,150,50),(-40,480,130,40))
      pygame.draw.ellipse(screen,(50,150,50),(750,485,130,30))
      pygame.draw.ellipse(screen,(50,150,50),(570,485,70,30))
      pygame.draw.ellipse(screen,(50,150,50),(580,490,80,20))
      
pygame.draw.circle
(screen,(140,140,155),(610,100),50)
      
pygame.draw.circle
(screen,(140,140,155),(490,100),50)
      
pygame.draw.circle
(screen,(140,140,155),(570,90),80)
      
pygame.draw.circle
(screen,(140,140,155),(715,100),45)
      
pygame.draw.circle
(screen,(140,140,155),(590,100),45)
      
pygame.draw.circle
(screen,(140,140,155),(650,90),70)
      starbut = pygame.Rect(315,220,150,60)
      setbut = pygame.Rect(315,280,150,60)
      tutbut = pygame.Rect(315,340,150,60)
      pygame.draw.rect(screen,(120,170,220),starbut)
      font = pygame.font.SysFont(None,40)
      text = font.render("Start",True,(220,220,220))
      screen.blit(text,(345,238))
      pygame.draw.rect(screen,(120,170,220),setbut)
      font = pygame.font.SysFont(None,35)
      text = font.render("Settings",True,(220,220,220))
      screen.blit(text,(327,298))
      pygame.draw.rect(screen,(120,170,220),tutbut)
      font = pygame.font.SysFont(None,35)
      text = font.render("Tutorial",True,(220,220,220))
      screen.blit(text,(330,358))
      font = pygame.font.SysFont(None,20)
      text = font.render("vA.01 Alpha",True,(220,220,220))
      screen.blit(text,(0,580))
      pygame.draw.ellipse(screen,(150,80,30),(600,390,15,120))
      pygame.draw.ellipse(screen,(50,150,50),(559,490,90,20))
      pygame.draw.ellipse(screen,(65,165,65),(580,320,90,80))
      pygame.draw.ellipse(screen,(60,160,60),(550,320,90,80))
      pygame.draw.ellipse(screen,(50,150,50),(540,350,80,65))
      pygame.draw.ellipse(screen,(55,155,55),(565,335,80,65))
      pygame.draw.ellipse(screen,(50,150,50),(600,340,80,70))
      pygame.draw.ellipse(screen,(45,145,45),(570,355,85,60))
      return{"starbut": starbut, "tutbut": tutbut, "setbut": setbut}
      
        



  prev_menu = None
  while running:
      screen.fill((120,170,220))
      buttons = {}
      current = menus_stack[-1]
      # if not current == prev_menu:
      #     pygame.mixer.music.stop()
      #     if current == "screen":
      #        pygame.mixer.music.load("musics/01_overworld_day.ogg")
      #        
pygame.mixer.music.play
(-1)
      #     if current == "nightscreen":
      #        pygame.mixer.music.load("musics/03_Night.ogg")
      #        
pygame.mixer.music.play
(-1)
      #     if current == "setting":
      #        pygame.mixer.music.load("musics/024_Plantera.ogg")
      #        
pygame.mixer.music.play
(-1)
        #  prev_menu = current
      if current == "screen":
          screen.fill((120,170,220))
          buttons = draw_screen()
      if current == "setting":
          screen.fill((100,100,100))
          buttons = draw_set()
      if current == "nightscreen":
        screen.fill((35,35,60))
        buttons = draw_nightscreen()
      if current == "gamech":
        screen.fill((50,100,150))
        buttons = draw_gamech()
      if current == "calamity":
        screen.fill((50,100,200))
        buttons = draw_calamity()
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
            running = False
          if event.type == pygame.MOUSEBUTTONDOWN:
              for name,rect in buttons.items():
                  if rect.collidepoint(event.pos):
                    if name == "starbut":
                      menus_stack.append("gamech")
                    if name == "setbut":
                      menus_stack.append("setting")
                    if name ==  "tutbut":
                      messagebox.showinfo("info","hi user, this is my firstly game,btw do u like sun and my grass? okay so now ima explain you what is this game. so this sandbox game, where you spawn likee oblects and can make them roll or even break them so you can do anything. //creator: Atlantic Game Dev, Head Dev--samsoncat19//")
                    if name =="back":
                      menus_stack.pop()
                    if name =="night":
                      menus_stack.pop()
                      menus_stack.append("nightscreen")
                    if name =="day":
                      menus_stack.pop()
                      menus_stack.append("screen")
                    if name =="calamity":
                      menus_stack.append("calamity")
                      
                    
      
      
      
      
      pygame.display.flip() 