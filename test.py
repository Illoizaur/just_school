import pygame
import random

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
    
target_radius = 30
target_pos = (random.randint(target_radius, 800 - target_radius), random.randint(target_radius, 600 - target_radius))
    
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if (mouse_pos[0] - target_pos[0]) ** 2 + (mouse_pos[1] - target_pos[1]) ** 2 <= target_radius ** 2:
                print("Hit!")
                target_pos = (random.randint(target_radius, 800 - target_radius), random.randint(target_radius, 600 - target_radius))
        
    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (255, 0, 0), target_pos, target_radius)
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()
