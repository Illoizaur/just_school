import pygame
import random

# --- КОНСТАНТИ ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 20  
FPS = 60

WORLD_COLS = 300
WORLD_ROWS = SCREEN_HEIGHT // TILE_SIZE

# Кольори
SKY_BLUE = (135, 180, 220)
GRASS_GREEN = (34, 139, 34)
DIRT_BROWN = (139, 69, 19)
LEAVES_GREEN = (40, 150, 40)
TRUNK_BROWN = (100, 60, 20)
PLAYER_BLUE = (0, 120, 255)


# 1. ПЛАВНА ГЕНЕРАЦІЯ РЕЛЬЄФУ
def generate_world_heights(cols_count):
    heights = []
    current_height = 20  
    
    trend = 0        
    trend_steps = 0  
    
    for col in range(cols_count):
        if trend_steps <= 0:
            trend = random.choice([-1, 0, 1])
            trend_steps = random.randint(3, 7) 
            
        current_height += trend
        trend_steps -= 1
        
        if current_height < 14: 
            current_height = 14
            trend = 1 
        if current_height > 25: 
            current_height = 25
            trend = -1 
            
        heights.append(current_height)
    return heights


# 2. ВИПРАВЛЕНА ГЕНЕРАЦІЯ ДЕРЕВ (Строго 1 блок, без злипання крон)
def generate_forest(cols_count, world_heights):
    forest = []
    min_distance = 8  # Збільшили відстань, щоб листя не перетикалося
    last_tree_col = -min_distance 
    
    for col in range(5, cols_count - 5):
        if col - last_tree_col >= min_distance:
            
            if random.random() < 0.15:  # Шанс появи
                trunk_width = 1         # ВИПРАВЛЕНО: Дерева тепер завжди стрункі (в 1 блок)
                trunk_height = random.randint(5, 9)   # Висота дерева
                foliage_radius = random.randint(2, 3) # Радіус листя
                
                ground_tile_y = world_heights[col]
                
                forest.append({
                    "tile_x": col,
                    "tile_y": ground_tile_y - trunk_height,
                    "width": trunk_width,
                    "height": trunk_height,
                    "foliage_radius": foliage_radius
                })
                
                last_tree_col = col # Наступне дерево буде дуже нескоро
                
    return forest


def rungame():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Terraria Smooth Procedural Engine vA.03")
    clock = pygame.time.Clock()

    world_heights = generate_world_heights(WORLD_COLS)
    forest = generate_forest(WORLD_COLS, world_heights)

    # Гравець
    player_w = 30
    player_h = 40
    player_x = 400
    
    start_tile_x = int((player_x + player_w // 2) // TILE_SIZE)
    player_y = world_heights[start_tile_x] * TILE_SIZE - player_h

    velocity_x = 0
    velocity_y = 0
    acceleration = 0.6
    friction = 0.85
    gravity = 0.5
    jump_power = -11

    camera_x = 0

    running = True
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Керування
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            velocity_x -= acceleration
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            velocity_x += acceleration

        velocity_x *= friction
        player_x += velocity_x

        if player_x < 0: player_x = 0
        if player_x > WORLD_COLS * TILE_SIZE - player_w: 
            player_x = WORLD_COLS * TILE_SIZE - player_w

        # Колізія
        center_tile_x = int((player_x + player_w // 2) // TILE_SIZE)
        if center_tile_x >= WORLD_COLS: center_tile_x = WORLD_COLS - 1

        current_ground_y = world_heights[center_tile_x] * TILE_SIZE
        is_on_ground = (player_y >= current_ground_y - player_h)

        if (keys[pygame.K_UP] or keys[pygame.K_w]) and is_on_ground:
            velocity_y = jump_power
            is_on_ground = False

        if not is_on_ground:
            velocity_y += gravity
        else:
            if velocity_y > 0:
                velocity_y = 0
                player_y = current_ground_y - player_h

        player_y += velocity_y

        if player_y > current_ground_y - player_h:
            player_y = current_ground_y - player_h
            velocity_y = 0

        # Камера
        target_camera_x = player_x - SCREEN_WIDTH // 2
        camera_x += (target_camera_x - camera_x) * 0.1  

        if camera_x < 0: camera_x = 0
        if camera_x > WORLD_COLS * TILE_SIZE - SCREEN_WIDTH:
            camera_x = WORLD_COLS * TILE_SIZE - SCREEN_WIDTH

        # Малювання
        screen.fill(SKY_BLUE)

        start_col = max(0, int(camera_x // TILE_SIZE))
        end_col = min(WORLD_COLS, start_col + (SCREEN_WIDTH // TILE_SIZE) + 2)

        # Земля
        for col in range(start_col, end_col):
            ground_top = world_heights[col]
            for row in range(ground_top, WORLD_ROWS):
                rect = pygame.Rect(col * TILE_SIZE - int(camera_x), row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if row == ground_top:
                    pygame.draw.rect(screen, GRASS_GREEN, rect)
                else:
                    pygame.draw.rect(screen, DIRT_BROWN, rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)

        # Дерева
        for tree in forest:
            tree_screen_x = tree["tile_x"] * TILE_SIZE - int(camera_x)
            if -100 < tree_screen_x < SCREEN_WIDTH + 100:
                # Стовбур (теж спрощений до 1 циклу по висоті)
                for h in range(tree["height"]):
                    trunk_rect = pygame.Rect(
                        tree["tile_x"] * TILE_SIZE - int(camera_x), 
                        (tree["tile_y"] + h) * TILE_SIZE, 
                        TILE_SIZE, TILE_SIZE
                    )
                    pygame.draw.rect(screen, TRUNK_BROWN, trunk_rect)
                
                # Крона
                foliage_center_x = tree["tile_x"]
                foliage_center_y = tree["tile_y"]
                r = tree["foliage_radius"]
                for nx in range(foliage_center_x - r, foliage_center_x + r + 1):
                    for ny in range(foliage_center_y - r, foliage_center_y + r):
                        if (nx - foliage_center_x)**2 + (ny - foliage_center_y)**2 <= r**2:
                            leaves_rect = pygame.Rect(
                                nx * TILE_SIZE - int(camera_x), 
                                ny * TILE_SIZE, 
                                TILE_SIZE, TILE_SIZE
                            )
                            pygame.draw.rect(screen, LEAVES_GREEN, leaves_rect)

        # Гравець
        player_screen_x = int(player_x - camera_x)
        pygame.draw.rect(screen, PLAYER_BLUE, (player_screen_x, int(player_y), player_w, player_h))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    rungame()