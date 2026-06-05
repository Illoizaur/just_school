import pygame
import random

def generate_forest(screen_width, ground_y, count=15):
    forest = []
    for _ in range(count):
        trunk_x = random.randint(20, screen_width - 60)
        
        trunk_width = random.randint(12, 20)
        trunk_height = random.randint(60, 140)
        
        trunk_y = ground_y - trunk_height
        
        foliage_radius = random.randint(35, 55)
        foliage_x = trunk_x + (trunk_width // 2)
        foliage_y = trunk_y
        
        green_color = (random.randint(30, 60), random.randint(120, 180), random.randint(30, 60))
        brown_color = (random.randint(120, 150), random.randint(70, 90), random.randint(20, 40))
        
        forest.append({
            "trunk_rect": (trunk_x, trunk_y, trunk_width, trunk_height),
            "foliage_pos": (foliage_x, foliage_y),
            "foliage_radius": foliage_radius,
            "green_color": green_color,
            "brown_color": brown_color
        })
        
    forest.sort(key=lambda d: d["trunk_rect"][1])
    return forest

def rungame():
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Sandbox Game - Procedural Forest")
    clock = pygame.time.Clock()

    ground_y = 550
    
    forest = generate_forest(screen_width, ground_y, count=18)

    player_size = 40
    player_x = 400
    player_y = ground_y - player_size # Ставимо на землю відразу

    velocity_x = 0
    velocity_y = 0
    acceleration = 0.6
    friction = 0.85
    gravity = 0.5
    jump_power = -12

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            velocity_x -= acceleration
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            velocity_x += acceleration

        is_on_ground = (player_y >= ground_y - player_size)
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and is_on_ground:
            velocity_y = jump_power

        velocity_y += gravity
        velocity_x *= friction

        player_x += velocity_x
        player_y += velocity_y

        if player_x < 0:
            player_x = 0
            velocity_x = 0
        elif player_x > screen_width - player_size:
            player_x = screen_width - player_size
            velocity_x = 0

        if player_y < 0:
            player_y = 0
            velocity_y = 0
        elif player_y > ground_y - player_size:
            player_y = ground_y - player_size
            velocity_y = 0

        screen.fill((135, 180, 220)) 

        for tree in forest:
            pygame.draw.rect(screen, tree["brown_color"], tree["trunk_rect"])
            pygame.draw.circle(screen, tree["green_color"], tree["foliage_pos"], tree["foliage_radius"])
            highlight_color = (min(tree["green_color"][0] + 20, 255), min(tree["green_color"][1] + 20, 255), tree["green_color"][2])
            pygame.draw.circle(screen, highlight_color, (tree["foliage_pos"][0] - 5, tree["foliage_pos"][1] - 5), int(tree["foliage_radius"] * 0.8))

        pygame.draw.rect(screen, (34, 139, 34), (0, ground_y, screen_width, screen_height - ground_y))

        pygame.draw.rect(screen, (0, 120, 255), (int(player_x), int(player_y), player_size, player_size))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()