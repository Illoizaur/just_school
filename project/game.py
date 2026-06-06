import pygame
import random
import math

# --- КОНСТАНТИ ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 20  
FPS = 60

WORLD_COLS = 3000  
WORLD_ROWS = 250   # Трохи збільшено глибину для довших тунелів

BIOME_SIZE = 300  

# --- КОЛЬОРИ БІОМІВ ---
SKY_BLUE = (135, 180, 220)
PLAYER_BLUE = (0, 120, 255)

# Фонова стіна (печери)
WALL_DIRT = (70, 40, 15)
WALL_STONE = (55, 55, 55)

# Ліс
GRASS_GREEN = (34, 139, 34)
DIRT_BROWN = (139, 69, 19)
LEAVES_GREEN = (40, 150, 40)
TRUNK_BROWN = (100, 60, 20)

# Тундра
SNOW_WHITE = (240, 245, 250)
ICE_BLUE = (115, 195, 225)
NEEDLES_DARKG = (20, 80, 40)

# Пустеля
SAND_YELLOW = (235, 200, 100)
SAND_DARK = (210, 170, 70)
CACTUS_GREEN = (50, 180, 70)

# Печери
STONE_GRAY = (90, 90, 90)


# --- 1. КАРТА БІОМІВ ---
def generate_biome_map(cols_count, biome_size):
    total_biomes = (cols_count // biome_size) + 1
    biome_map = []
    
    current_biome = random.choice(["tundra", "forest", "desert"])
    biome_map.append(current_biome)
    
    for _ in range(1, total_biomes):
        if current_biome in ["tundra", "desert"]:
            current_biome = "forest"
        else:
            current_biome = random.choice(["tundra", "forest", "desert"])
        biome_map.append(current_biome)
        
    spawn_biome_idx = 300 // biome_size
    if spawn_biome_idx < len(biome_map):
        biome_map[spawn_biome_idx] = "forest"
    return biome_map

BIOME_MAP = generate_biome_map(WORLD_COLS, BIOME_SIZE)

def get_biome_at(col):
    biome_idx = col // BIOME_SIZE
    if biome_idx >= len(BIOME_MAP): biome_idx = len(BIOME_MAP) - 1
    return BIOME_MAP[biome_idx]


# --- 2. ГЕНЕРАЦІЯ СВІТУ (Плавні біоми + тунельні входи) ---
def generate_world(cols_count):
    heights = []
    block_grid = {}  
    wall_grid = {}   
    
    seed1 = random.uniform(0, 1000)
    seed2 = random.uniform(0, 1000)
    cave_seeds = [random.uniform(0, 500) for _ in range(4)]
    
    # --- ЕТАП 1: ГЕНЕРАЦІЯ ПЛАВНОЇ ПОВЕРХНІ (Без стрімчаків) ---
    # Спочатку рахуємо параметри для кожної колонки окремо
    raw_heights = []
    for col in range(cols_count):
        biome = get_biome_at(col)
        if biome == "tundra":
            base_y, amp = 55, 3.0
        elif biome == "forest":
            base_y, amp = 45, 5.0
        else:
            base_y, amp = 35, 7.0
        raw_heights.append((base_y, amp))
    
    # Згладжуємо параметри за допомогою змінного вікна (Moving Average), щоб прибрати сходинки
    smooth_window = 40 
    for col in range(cols_count):
        sum_base = 0
        sum_amp = 0
        count = 0
        for i in range(col - smooth_window, col + smooth_window):
            if 0 <= i < cols_count:
                sum_base += raw_heights[i][0]
                sum_amp += raw_heights[i][1]
                count += 1
        
        avg_base = sum_base / count
        avg_amp = sum_amp / count
        
        # Накладаємо хвилі шуму на вже ідеально згладжену основу
        noise = math.sin(col * 0.03 + seed1) * avg_amp + math.cos(col * 0.09 + seed2) * (avg_amp * 0.4)
        final_height = int(avg_base + noise)
        if final_height < 15: final_height = 15
        heights.append(final_height)

    # --- ЕТАП 2: ЗАПОВНЕННЯ ТАНГЕНЦІАЛЬНИМИ БЛОКАМИ ---
    for col in range(cols_count):
        final_height = heights[col]
        is_spawn_zone = (230 <= col <= 370)

        for row in range(final_height, WORLD_ROWS):
            depth = row - final_height
            is_cave = False
            
            # Генерація глибоких печер (не ближче 20 блоків до поверхні і за межами спавну)
            if not is_spawn_zone and depth >= 20:
                n1 = math.sin(col * 0.08 + cave_seeds[0]) * math.cos(row * 0.12 + cave_seeds[1])
                n2 = math.sin(row * 0.07 + cave_seeds[2]) * math.cos(col * 0.15 + cave_seeds[3])
                if -0.21 < (n1 + n2) < 0.21:
                    is_cave = True

            # Базові шари землі
            b_type = 1 if row == final_height else (2 if row < final_height + 10 else 3)
            w_type = 1 if row < final_height + 10 else 2  

            if not is_cave:
                block_grid[(col, row)] = b_type
            else:
                wall_grid[(col, row)] = w_type

    # --- ЕТАП 3: СТВОРЕННЯ КРАСИВИХ ВХОДІВ ("ЧЕРВ'ЯЧНІ ТУНЕЛІ") ---
    # Замість дірок ми пускаємо "хробаків руйнування", які вигризають похилі тунелі з поверхні
    entrance_cols = []
    next_ent = 140
    while next_ent < cols_count - 140:
        if not (210 <= next_ent <= 390): # ігноруємо спавн
            entrance_cols.append(next_ent)
        next_ent += random.randint(180, 280)

    for start_col in entrance_cols:
        # Стартова точка хробака на реальній поверхні землі
        cur_x = float(start_col)
        cur_y = float(heights[start_col])
        
        # Випадковий похилий напрямок спуску (ліворуч або праворуч під кутом)
        angle = random.choice([math.radians(35), math.radians(145)]) 
        
        tunnel_length = random.randint(45, 75)
        for step in range(tunnel_length):
            # Радіус тунелю трохи змінюється, імітуючи природні звуження/розширення
            radius = 3.5 + math.sin(step * 0.3) * 1.0
            
            # Вирізаємо коло навколо поточної голови хробака
            min_c = max(0, int(cur_x - radius - 1))
            max_c = min(cols_count, int(cur_x + radius + 1))
            min_r = max(0, int(cur_y - radius - 1))
            max_r = min(WORLD_ROWS, int(cur_y + radius + 1))
            
            for cx in range(min_c, max_c):
                for cy in range(min_r, max_r):
                    if (cx - cur_x)**2 + (cy - cur_y)**2 <= radius**2:
                        # Стираємо блок, створюючи прохід, і заповнюємо фон стіною
                        if (cx, cy) in block_grid:
                            w_t = 1 if cy < heights[cx] + 10 else 2
                            del block_grid[(cx, cy)]
                            wall_grid[(cx, cy)] = w_t

            # Рухаємо хробака вперед за вектором напрямку
            cur_x += math.cos(angle) * 1.2
            cur_y += math.sin(angle) * 0.9  # плавно вниз
            
            # Злегка викривляємо траєкторію, щоб тунель звивався
            angle += random.uniform(-0.1, 0.1)

    # --- ЕТАП 4: ОНОВЛЕННЯ ТРАВИ НА НОВИХ СХИЛАХ ---
    for col in range(cols_count):
        for row in range(heights[col], WORLD_ROWS):
            if (col, row) in block_grid:
                if (col, row - 1) not in block_grid:
                    block_grid[(col, row)] = 1  # робимо блок верхнім шаром
                break
                    
    return heights, block_grid, wall_grid


# --- 3. ГЕНЕРАЦІЯ ОБ'ЄКТІВ ---
def generate_world_objects(cols_count, world_heights, block_grid):
    objects = []
    min_distance = 8  
    last_obj_col = -min_distance 
    
    for col in range(5, cols_count - 5):
        actual_surface_y = -1
        for row in range(world_heights[col], WORLD_ROWS):
            if (col, row) in block_grid:
                actual_surface_y = row
                break
        
        if actual_surface_y != -1 and block_grid.get((col, actual_surface_y)) == 1:
            if col - last_obj_col >= min_distance and (col, actual_surface_y - 1) not in block_grid:
                biome = get_biome_at(col)
                
                if biome == "tundra" and random.random() < 0.08:
                    height = random.randint(5, 8)
                    objects.append({"type": "pine", "tile_x": col, "tile_y": actual_surface_y - height, "height": height})
                    last_obj_col = col
                elif biome == "forest" and random.random() < 0.14:
                    height = random.randint(5, 9)
                    objects.append({"type": "normal_tree", "tile_x": col, "tile_y": actual_surface_y - height, "height": height, "foliage_radius": random.randint(2, 3)})
                    last_obj_col = col
                elif biome == "desert" and random.random() < 0.10:
                    height = random.randint(3, 6)
                    objects.append({"type": "cactus", "tile_x": col, "tile_y": actual_surface_y - height, "height": height, "has_branches": random.choice([True, False])})
                    last_obj_col = col
                    
    return objects


# --- 4. ПЕРЕВІРКА КОЛІЗІЙ ---
def get_colliding_blocks(player_rect, block_grid):
    colliders = []
    start_x = int(player_rect.left // TILE_SIZE)
    end_x = int((player_rect.right // TILE_SIZE) + 1)
    start_y = int(player_rect.top // TILE_SIZE)
    end_y = int((player_rect.bottom // TILE_SIZE) + 1)

    for tx in range(start_x, end_x):
        for ty in range(start_y, end_y):
            if (tx, ty) in block_grid:
                block_rect = pygame.Rect(tx * TILE_SIZE, ty * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if player_rect.colliderect(block_rect):
                    colliders.append(block_rect)
    return colliders


def rungame():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Terraria Engine: Perfect Lerp Biomes & Worm Cave Entrances")
    clock = pygame.time.Clock()

    world_heights, block_grid, wall_grid = generate_world(WORLD_COLS)
    world_objects = generate_world_objects(WORLD_COLS, world_heights, block_grid)

    # Гравець
    player_w = 24
    player_h = 38
    spawn_col = 300
    
    p_x = spawn_col * TILE_SIZE + 2
    p_y = (world_heights[spawn_col] - 3) * TILE_SIZE
    player_rect = pygame.Rect(p_x, p_y, player_w, player_h)

    velocity_x = 0
    velocity_y = 0
    acceleration = 5
    friction = 0.80
    gravity = 0.4
    jump_power = -9.5
    
    is_on_ground = False
    is_touching_wall_left = False
    is_touching_wall_right = False

    camera_x = player_rect.x - SCREEN_WIDTH // 2
    camera_y = player_rect.y - SCREEN_HEIGHT // 2

    running = True
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: velocity_x -= acceleration
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: velocity_x += acceleration

        velocity_x *= friction
        
        is_sliding = (is_touching_wall_left or is_touching_wall_right) and not is_on_ground and velocity_y > 0
        if is_sliding:
            velocity_y += gravity * 0.25  
            if velocity_y > 2.0: velocity_y = 2.0
        else:
            velocity_y += gravity
            if velocity_y > 12: velocity_y = 12

        is_touching_wall_left = False
        is_touching_wall_right = False

        # Рух та колізії по X
        player_rect.x += int(round(velocity_x))
        if player_rect.left < 0: player_rect.left = 0
        if player_rect.right > WORLD_COLS * TILE_SIZE: player_rect.right = WORLD_COLS * TILE_SIZE

        hits = get_colliding_blocks(player_rect, block_grid)
        for block in hits:
            if velocity_x > 0:  
                player_rect.right = block.left
                velocity_x = 0
                is_touching_wall_right = True
            elif velocity_x < 0:  
                player_rect.left = block.right
                velocity_x = 0
                is_touching_wall_left = True

        test_rect_left = player_rect.copy()
        test_rect_left.x -= 2
        if get_colliding_blocks(test_rect_left, block_grid): is_touching_wall_left = True

        test_rect_right = player_rect.copy()
        test_rect_right.x += 2
        if get_colliding_blocks(test_rect_right, block_grid): is_touching_wall_right = True

        # Рух та колізії по Y
        player_rect.y += int(round(velocity_y))
        is_on_ground = False
        
        hits = get_colliding_blocks(player_rect, block_grid)
        for block in hits:
            if velocity_y > 0:  
                player_rect.bottom = block.top
                velocity_y = 0
                is_on_ground = True
            elif velocity_y < 0:  
                player_rect.top = block.bottom
                velocity_y = 0

        # Стрибки та Wall Jump
        jump_pressed = keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]
        if jump_pressed:
            if is_on_ground:
                velocity_y = jump_power
                is_on_ground = False
            elif is_touching_wall_left and not is_on_ground:
                velocity_y = jump_power * 0.95
                velocity_x = 6.5  
                is_touching_wall_left = False
            elif is_touching_wall_right and not is_on_ground:
                velocity_y = jump_power * 0.95
                velocity_x = -6.5 
                is_touching_wall_right = False

        if player_rect.bottom > WORLD_ROWS * TILE_SIZE:
            current_col = int(player_rect.x // TILE_SIZE)
            player_rect.y = (world_heights[current_col] - 4) * TILE_SIZE
            velocity_y = 0

        # Плавна камера
        target_camera_x = player_rect.centerx - SCREEN_WIDTH // 2
        camera_x += (target_camera_x - camera_x) * 0.1  
        camera_x = max(0, min(camera_x, WORLD_COLS * TILE_SIZE - SCREEN_WIDTH))

        target_camera_y = player_rect.centery - SCREEN_HEIGHT // 2
        camera_y += (target_camera_y - camera_y) * 0.1  
        camera_y = max(0, min(camera_y, WORLD_ROWS * TILE_SIZE - SCREEN_HEIGHT))

        # --- РЕНДЕРИНГ ---
        screen.fill(SKY_BLUE)

        start_col = max(0, int(camera_x // TILE_SIZE))
        end_col = min(WORLD_COLS, start_col + (SCREEN_WIDTH // TILE_SIZE) + 2)
        start_row = max(0, int(camera_y // TILE_SIZE))
        end_row = min(WORLD_ROWS, start_row + (SCREEN_HEIGHT // TILE_SIZE) + 2)

        int_cam_x = int(camera_x)
        int_cam_y = int(camera_y)

        for col in range(start_col, end_col):
            biome = get_biome_at(col)
            if biome == "tundra": c1, c2 = SNOW_WHITE, ICE_BLUE
            elif biome == "forest": c1, c2 = GRASS_GREEN, DIRT_BROWN
            else: c1, c2 = SAND_YELLOW, SAND_DARK

            for row in range(start_row, end_row):
                block_type = block_grid.get((col, row), 0)
                rect = pygame.Rect(col * TILE_SIZE - int_cam_x, row * TILE_SIZE - int_cam_y, TILE_SIZE, TILE_SIZE)
                
                if block_type != 0:
                    if block_type == 1: pygame.draw.rect(screen, c1, rect)
                    elif block_type == 2: pygame.draw.rect(screen, c2, rect)
                    elif block_type == 3: pygame.draw.rect(screen, STONE_GRAY, rect)
                    pygame.draw.rect(screen, (0, 0, 0), rect, 1)  
                else:
                    wall_type = wall_grid.get((col, row), 0)
                    if wall_type == 1: pygame.draw.rect(screen, WALL_DIRT, rect)
                    elif wall_type == 2: pygame.draw.rect(screen, WALL_STONE, rect)

        # Малювання об'єктів
        for obj in world_objects:
            obj_screen_x = obj["tile_x"] * TILE_SIZE - int_cam_x
            if -100 < obj_screen_x < SCREEN_WIDTH + 100:
                if obj["type"] == "normal_tree":
                    for h in range(obj["height"]):
                        rect = pygame.Rect(obj_screen_x, (obj["tile_y"] + h) * TILE_SIZE - int_cam_y, TILE_SIZE, TILE_SIZE)
                        pygame.draw.rect(screen, TRUNK_BROWN, rect)
                    cx, cy = obj["tile_x"], obj["tile_y"]
                    r = obj["foliage_radius"]
                    for nx in range(cx - r, cx + r + 1):
                        for ny in range(cy - r, cy + r):
                            if (nx - cx)**2 + (ny - cy)**2 <= r**2:
                                l_rect = pygame.Rect(nx * TILE_SIZE - int_cam_x, ny * TILE_SIZE - int_cam_y, TILE_SIZE, TILE_SIZE)
                                pygame.draw.rect(screen, LEAVES_GREEN, l_rect)
                elif obj["type"] == "pine":
                    for h in range(obj["height"]):
                        rect = pygame.Rect(obj_screen_x, (obj["tile_y"] + h) * TILE_SIZE - int_cam_y, TILE_SIZE, TILE_SIZE)
                        pygame.draw.rect(screen, TRUNK_BROWN, rect)
                    for h in range(obj["height"] - 2):
                        layer_y = obj["tile_y"] + h
                        width_factor = 2 if h > 2 else 1
                        for dw in range(-width_factor, width_factor + 1):
                            l_rect = pygame.Rect((obj["tile_x"] + dw) * TILE_SIZE - int_cam_x, layer_y * TILE_SIZE - int_cam_y, TILE_SIZE, TILE_SIZE)
                            pygame.draw.rect(screen, NEEDLES_DARKG, l_rect)
                elif obj["type"] == "cactus":
                    for h in range(obj["height"]):
                        rect = pygame.Rect(obj_screen_x, (obj["tile_y"] + h) * TILE_SIZE - int_cam_y, TILE_SIZE, TILE_SIZE)
                        pygame.draw.rect(screen, CACTUS_GREEN, rect)
                    if obj["has_branches"] and obj["height"] > 4:
                        left_y = obj["tile_y"] + 2
                        pygame.draw.rect(screen, CACTUS_GREEN, (obj_screen_x - TILE_SIZE, left_y * TILE_SIZE - int_cam_y, TILE_SIZE, TILE_SIZE))
                        pygame.draw.rect(screen, CACTUS_GREEN, (obj_screen_x - TILE_SIZE, (left_y - 1) * TILE_SIZE - int_cam_y, TILE_SIZE, TILE_SIZE))
                        right_y = obj["tile_y"] + 3
                        pygame.draw.rect(screen, CACTUS_GREEN, (obj_screen_x + TILE_SIZE, right_y * TILE_SIZE - int_cam_y, TILE_SIZE, TILE_SIZE))
                        pygame.draw.rect(screen, CACTUS_GREEN, (obj_screen_x + TILE_SIZE, (right_y - 1) * TILE_SIZE - int_cam_y, TILE_SIZE, TILE_SIZE))

        # Малювання гравця
        player_screen_x = player_rect.x - int_cam_x
        player_screen_y = player_rect.y - int_cam_y
        pygame.draw.rect(screen, PLAYER_BLUE, (player_screen_x, player_screen_y, player_w, player_h))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    rungame()