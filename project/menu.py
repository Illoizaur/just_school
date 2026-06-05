import pygame.font  # Ламаємо циклічний імпорт
import pygame
import random
from tkinter import messagebox

pygame.font.init()

def runmenu():
    DARKORANGE = (250, 150, 100)
    pygame.init()
    
    font_40 = pygame.font.Font(None, 40)
    font_35 = pygame.font.Font(None, 35)
    font_20 = pygame.font.Font(None, 20)
    font_165 = pygame.font.Font(None, 165)

    menus_stack = ["screen"]
    start_game = False  # Прапорець для запуску гри
    
    def show():
        messagebox.showinfo("info", "hi user, this is my firstly game,btw do u like sun and my grass? okay so now ima explain you what is this game. so this sandbox game, where you spawn likee oblects and can make them roll or even break them so you can do anything. //creator: Atlantic Game Dev, Head Dev--samsoncat19//")

    screen = pygame.display.set_mode((800, 600))
    running = True
    pygame.display.set_caption("physical sky breaker vA.01")

    def draw_set():
        screen.fill((200, 200, 200))
        day = pygame.Rect(193, 82, 100, 50)
        night = pygame.Rect(93, 82, 100, 50)
        back = pygame.Rect(0, 0, 80, 80)
        pygame.draw.rect(screen, (240, 20, 10), back)
        
        if font_165:
            text = font_165.render("x", True, (250, 250, 250))
            screen.blit(text, (9, -20))
            
        pygame.draw.rect(screen, (100, 150, 200), night)
        pygame.draw.rect(screen, (20, 20, 80), day)
        
        if font_40:
            text = font_40.render("Menu modes", True, (250, 250, 250))
            screen.blit(text, (105, 28))
            text = font_40.render("Night", True, (20, 20, 80))
            screen.blit(text, (105, 90))
            text = font_40.render("Day", True, (250, 250, 80))
            screen.blit(text, (220, 90))

        return {"back": back, "night": night, "day": day}

    def draw_screen():
        pygame.draw.ellipse(screen, DARKORANGE, (75, 25, 100, 100))
        pygame.draw.ellipse(screen, (235, 135, 85), (85, 35, 80, 80))
        pygame.draw.rect(screen, (10, 100, 10), (0, 550, 1000, 80))
        pygame.draw.rect(screen, (50, 150, 50), (0, 500, 1000, 60))
        pygame.draw.rect(screen, (25, 125, 25), (0, 525, 1000, 50))
        pygame.draw.ellipse(screen, (50, 150, 50), (350, 490, 150, 25))
        pygame.draw.ellipse(screen, (50, 150, 50), (300, 480, 150, 23))
        pygame.draw.ellipse(screen, (50, 150, 50), (230, 490, 100, 20))
        pygame.draw.ellipse(screen, (50, 150, 50), (40, 490, 100, 30))
        pygame.draw.ellipse(screen, (50, 150, 50), (710, 490, 100, 20))
        pygame.draw.ellipse(screen, (50, 150, 50), (-40, 480, 130, 40))
        pygame.draw.ellipse(screen, (50, 150, 50), (750, 485, 130, 30))
        pygame.draw.ellipse(screen, (50, 150, 50), (570, 485, 70, 30))
        pygame.draw.ellipse(screen, (50, 150, 50), (580, 490, 80, 20))
        
        pygame.draw.circle(screen, (240, 240, 255), (610, 100), 50)
        pygame.draw.circle(screen, (240, 240, 255), (490, 100), 50)
        pygame.draw.circle(screen, (240, 240, 255), (570, 90), 80)
        pygame.draw.circle(screen, (240, 240, 255), (715, 100), 45)
        pygame.draw.circle(screen, (240, 240, 255), (590, 100), 45)
        pygame.draw.circle(screen, (240, 240, 255), (650, 90), 70)
        
        pygame.draw.ellipse(screen, (150, 80, 30), (600, 390, 15, 120))
        pygame.draw.ellipse(screen, (50, 150, 50), (559, 490, 90, 20))
        pygame.draw.ellipse(screen, (65, 165, 65), (580, 320, 90, 80))
        pygame.draw.ellipse(screen, (60, 160, 60), (550, 320, 90, 80))
        pygame.draw.ellipse(screen, (50, 150, 50), (540, 350, 80, 65))
        pygame.draw.ellipse(screen, (55, 155, 55), (565, 335, 80, 65))
        pygame.draw.ellipse(screen, (50, 150, 50), (600, 340, 80, 70))
        pygame.draw.ellipse(screen, (45, 145, 45), (570, 355, 85, 60))

        starbut = pygame.Rect(315, 220, 150, 60)
        setbut = pygame.Rect(315, 280, 150, 60)
        tutbut = pygame.Rect(315, 340, 150, 60)
        
        pygame.draw.rect(screen, (120, 170, 220), starbut)
        if font_40:
            text = font_40.render("Start", True, (220, 220, 220))
            screen.blit(text, (345, 238))
            
        pygame.draw.rect(screen, (120, 170, 220), setbut)
        if font_35:
            text = font_35.render("Settings", True, (220, 220, 220))
            screen.blit(text, (327, 298))
            
        pygame.draw.rect(screen, (120, 170, 220), tutbut)
        if font_35:
            text = font_35.render("Tutorial", True, (220, 220, 220))
            screen.blit(text, (330, 358))
            
        if font_20:
            text = font_20.render(" vA.01 Alpha", True, (220, 220, 220))
            screen.blit(text, (0, 580))
            
        return {"starbut": starbut, "tutbut": tutbut, "setbut": setbut}

    def draw_calamity():
        back = pygame.Rect(0, 0, 80, 80)
        pygame.draw.rect(screen, (240, 20, 10), back)
        if font_165:
            text = font_165.render("x", True, (250, 250, 250))
            screen.blit(text, (9, -20))
        return {"back": back}

    def draw_gamech():
        calamity = pygame.Rect(200, 200, 300, 300)
        back = pygame.Rect(0, 0, 80, 80)
        pygame.draw.rect(screen, (240, 20, 10), back)
        pygame.draw.rect(screen, (20, 20, 210), calamity)
        if font_165:
            text = font_165.render("x", True, (250, 250, 250))
            screen.blit(text, (9, -20))
        return {"back": back, "calamity": calamity}

    def draw_nightscreen():
        for pos in [(300,90), (200,20), (350,20), (400,100), (750,20), (50,40), (180,100), (20,100), (770,90), (650,10), (450,30)]:
            pygame.draw.rect(screen, (250, 250, 250), (pos[0], pos[1], 5, 5))
            
        pygame.draw.ellipse(screen, (170, 170, 170), (75, 25, 100, 100))
        pygame.draw.ellipse(screen, (190, 190, 190), (85, 35, 80, 80))
        pygame.draw.rect(screen, (10, 100, 10), (0, 550, 1000, 80))
        pygame.draw.rect(screen, (50, 150, 50), (0, 500, 1000, 60))
        pygame.draw.rect(screen, (25, 125, 25), (0, 525, 1000, 50))
        pygame.draw.ellipse(screen, (50, 150, 50), (350, 490, 150, 25))
        pygame.draw.ellipse(screen, (50, 150, 50), (300, 480, 150, 23))
        pygame.draw.ellipse(screen, (50, 150, 50), (230, 490, 100, 20))
        pygame.draw.ellipse(screen, (50, 150, 50), (40, 490, 100, 30))
        pygame.draw.ellipse(screen, (50, 150, 50), (710, 490, 100, 20))
        pygame.draw.ellipse(screen, (50, 150, 50), (-40, 480, 130, 40))
        pygame.draw.ellipse(screen, (50, 150, 50), (750, 485, 130, 30))
        pygame.draw.ellipse(screen, (50, 150, 50), (570, 485, 70, 30))
        pygame.draw.ellipse(screen, (50, 150, 50), (580, 490, 80, 20))
        
        pygame.draw.circle(screen, (140, 140, 155), (610, 100), 50)
        pygame.draw.circle(screen, (140, 140, 155), (490, 100), 50)
        pygame.draw.circle(screen, (140, 140, 155), (570, 90), 80)
        pygame.draw.circle(screen, (140, 140, 155), (715, 100), 45)
        pygame.draw.circle(screen, (140, 140, 155), (590, 100), 45)
        pygame.draw.circle(screen, (140, 140, 155), (650, 90), 70)
        
        pygame.draw.ellipse(screen, (150, 80, 30), (600, 390, 15, 120))
        pygame.draw.ellipse(screen, (50, 150, 50), (559, 490, 90, 20))
        pygame.draw.ellipse(screen, (65, 165, 65), (580, 320, 90, 80))
        pygame.draw.ellipse(screen, (60, 160, 60), (550, 320, 90, 80))
        pygame.draw.ellipse(screen, (50, 150, 50), (540, 350, 80, 65))
        pygame.draw.ellipse(screen, (55, 155, 55), (565, 335, 80, 65))
        pygame.draw.ellipse(screen, (50, 150, 50), (600, 340, 80, 70))
        pygame.draw.ellipse(screen, (45, 145, 45), (570, 355, 85, 60))
        
        starbut = pygame.Rect(315, 220, 150, 60)
        setbut = pygame.Rect(315, 280, 150, 60)
        tutbut = pygame.Rect(315, 340, 150, 60)
        
        pygame.draw.rect(screen, (120, 170, 220), starbut)
        if font_40:
            text = font_40.render("Start", True, (220, 220, 220))
            screen.blit(text, (345, 238))
            
        pygame.draw.rect(screen, (120, 170, 220), setbut)
        if font_35:
            text = font_35.render("Settings", True, (220, 220, 220))
            screen.blit(text, (327, 298))
            
        pygame.draw.rect(screen, (120, 170, 220), tutbut)
        if font_35:
            text = font_35.render("Tutorial", True, (220, 220, 220))
            screen.blit(text, (330, 358))
            
        if font_20:
            text = font_20.render("vA.01 Alpha", True, (220, 220, 220))
            screen.blit(text, (0, 580))
        
        return {"starbut": starbut, "tutbut": tutbut, "setbut": setbut}

    while running:
        buttons = {}
        current = menus_stack[-1]

        if current == "screen":
            screen.fill((120, 170, 220))
            buttons = draw_screen()
        elif current == "setting":
            screen.fill((100, 100, 100))
            buttons = draw_set()
        elif current == "nightscreen":
            screen.fill((35, 35, 60))
            buttons = draw_nightscreen()
        elif current == "gamech":
            screen.fill((50, 100, 150))
            buttons = draw_gamech()
        elif current == "calamity":
            screen.fill((50, 100, 200))
            buttons = draw_calamity()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    show()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for name, rect in buttons.items():
                    if rect.collidepoint(event.pos):
                        if name == "starbut":
                            start_game = True  # Сигнал для запуску гри
                            running = False     # Виходимо з циклу меню
                        elif name == "setbut":
                            menus_stack.append("setting")
                        elif name == "tutbut":
                            show()
                        elif name == "back":
                            if len(menus_stack) > 1:
                                menus_stack.pop()
                        elif name == "night":
                            if len(menus_stack) > 1: menus_stack.pop()
                            menus_stack.append("nightscreen")
                        elif name == "day":
                            if len(menus_stack) > 1: menus_stack.pop()
                            menus_stack.append("screen")
                        elif name == "calamity":
                            menus_stack.append("calamity")

        pygame.display.flip()
    
    pygame.quit()
    return start_game # Повертаємо True або False для main.py

if __name__ == "__main__":
    runmenu()