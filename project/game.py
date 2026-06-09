import pygame
import random
import math

# --- КОНСТАНТИ ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 20  
FPS = 60

WORLD_COLS = 3000  
WORLD_ROWS = 250   

BIOME_SIZE = 300  

# --- КОЛЬОРИ БІОМІВ ТА РІДИН ---
SKY_BLUE = (135, 180, 220)
PLAYER_BLUE = (0, 120, 255)
WATER_BLUE = (30, 85, 230, 180)
ENEMY_PURPLE = (150, 50, 220) # Колір нашого моба

# Фонова стіна (печери)
WALL_DIRT = (70, 40, 15)
WALL_STONE = (55, 55, 55)
WALL_DUNGEON = (45, 45, 60)

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

# Печери та данжі
STONE_GRAY = (90, 90, 90)
MOSS_GREEN = (50, 150, 60)     
DUNGEON_BRICK = (100, 100, 130) 
WOOD_PLATFORM = (140, 90, 40)   

# Руди (Ores)
ORE_COPPER = (184, 115, 51)
ORE_IRON = (165, 150, 140)
ORE_GOLD = (255, 215, 0)
ORE_AMETHYST = (155, 40, 235)

# --- ДАНІ ПРЕДМЕТІВ ДЛЯ ІНВЕНТАРЮ ---
BLOCK_ITEMS = {
    1: {"name": "Grass", "color": (34, 139, 34)},
    2: {"name": "Dirt", "color": (139, 69, 19)},
    3: {"name": "Stone", "color": (90, 90, 90)},
    5: {"name": "Moss Stone", "color": (50, 150, 60)},
    6: {"name": "Copper", "color": (184, 115, 51)},
    7: {"name": "Iron", "color": (165, 150, 140)},
    8: {"name": "Gold", "color": (255, 215, 0)},
    9: {"name": "Amethyst", "color": (155, 40, 235)},
    10: {"name": "Dungeon Brick", "color": (100, 100, 130)},
    11: {"name": "Wood Platform", "color": (140, 90, 40)}
}


# --- КАРТА БІОМІВ ---
def generate_biome_map(cols_count, biome_size):
    total_biomes = (cols_count // biome_size) + 1
    biome_map = []
    current_biome = random.choice(["tundra", "forest", "desert"])
    biome_map.append(current_biome)
    for _ in range(1, total_biomes):
        if current_biome in ["tundra", "desert"]: current_biome = "forest"
        else: current_biome = random.choice(["tundra", "forest", "desert"])
        biome_map.append(current_biome)
    spawn_biome_idx = 300 // biome_size
    if spawn_biome_idx < len(biome_map): biome_map[spawn_biome_idx] = "forest"
    return biome_map

BIOME_MAP = generate_biome_map(WORLD_COLS, BIOME_SIZE)

def get_biome_at(col):
    biome_idx = col // BIOME_SIZE
    if biome_idx >= len(BIOME_MAP): biome_idx = len(BIOME_MAP) - 1
    return BIOME_MAP[biome_idx]


# --- ГЕНЕРАЦІЯ СВІТУ ---
def generate_world(cols_count):
    heights = []
    block_grid = {}  
    wall_grid = {}   
    water_grid = {}  
    
    seed1 = random.uniform(0, 1000)
    seed2 = random.uniform(0, 1000)
    
    cave_seeds = [random.uniform(0, 2000) for _ in range(8)]
    ore_seeds = [random.uniform(0, 1000) for _ in range(4)]
    
    # 1. Рельєф
    raw_heights = []
    for col in range(cols_count):
        biome = get_biome_at(col)
        if biome == "tundra": base_y, amp = 55, 3.0
        elif biome == "forest": base_y, amp = 45, 5.0
        else: base_y, amp = 35, 7.0
        raw_heights.append((base_y, amp))
    
    smooth_window = 40 
    for col in range(cols_count):
        sum_base, sum_amp, count = 0, 0, 0
        for i in range(col - smooth_window, col + smooth_window):
            if 0 <= i < cols_count:
                sum_base += raw_heights[i][0]
                sum_amp += raw_heights[i][1]
                count += 1
        avg_base = sum_base / count
        avg_amp = sum_amp / count
        
        noise = math.sin(col * 0.03 + seed1) * avg_amp + math.cos(col * 0.09 + seed2) * (avg_amp * 0.4)
        final_height = int(avg_base + noise)
        if final_height < 15: final_height = 15
        heights.append(final_height)

    # 2. Заповнення шарів
    for col in range(cols_count):
        final_height = heights[col]
        is_spawn_zone = (230 <= col <= 370)

        for row in range(final_height, WORLD_ROWS):
            depth = row - final_height
            is_cave = False
            
            # Реалістичні печери
            if not is_spawn_zone and depth >= 20:
                n1 = math.sin(col * 0.06 + cave_seeds[0]) * math.cos(row * 0.09 + cave_seeds[1])
                n2 = math.sin(row * 0.05 + cave_seeds[2]) * math.cos(col * 0.11 + cave_seeds[3])
                
                detail_n1 = math.sin(col * 0.22 + cave_seeds[4]) * math.cos(row * 0.31 + cave_seeds[5])
                detail_n2 = math.sin(row * 0.18 + cave_seeds[6]) * math.cos(col * 0.27 + cave_seeds[7])
                
                total_cave_noise = (n1 + n2) * 0.75 + (detail_n1 + detail_n2) * 0.25
                
                if -0.17 < total_cave_noise < 0.17:
                    is_cave = True

            if row < final_height + 10:
                b_type = 1 if row == final_height else 2  
                w_type = 1
            else:
                b_type = 3  
                w_type = 2

            # Руди (рідкісні великі поклади)
            if b_type == 3 and not is_cave:
                if row < 130:
                    if math.sin(col * 0.24 + ore_seeds[0]) * math.cos(row * 0.24 + ore_seeds[1]) > 0.94: b_type = 6 
                    elif math.sin(col * 0.22 + ore_seeds[2]) * math.cos(row * 0.22 + seed1) > 0.95: b_type = 7 
                else:
                    if math.sin(col * 0.26 + ore_seeds[1]) * math.cos(row * 0.26 + ore_seeds[3]) > 0.96: b_type = 8 
                    elif math.sin(col * 0.28 + seed2) * math.cos(row * 0.28 + ore_seeds[0]) > 0.97: b_type = 9 

            if not is_cave:
                block_grid[(col, row)] = b_type
            else:
                wall_grid[(col, row)] = w_type

    # 3. Тунелі
    entrance_cols = []
    next_ent = 140
    while next_ent < cols_count - 140:
        if not (210 <= next_ent <= 390): entrance_cols.append(next_ent)
        next_ent += random.randint(180, 280)

    for start_col in entrance_cols:
        cur_x, cur_y = float(start_col), float(heights[start_col])
        angle = random.choice([math.radians(35), math.radians(145)]) 
        tunnel_length = random.randint(50, 80)
        
        for step in range(tunnel_length):
            radius = 3.2 + math.sin(step * 0.3) * 0.8
            for cx in range(max(0, int(cur_x - radius - 1)), min(cols_count, int(cur_x + radius + 1))):
                for cy in range(max(0, int(cur_y - radius - 1)), min(WORLD_ROWS, int(cur_y + radius + 1))):
                    if (cx - cur_x)**2 + (cy - cur_y)**2 <= radius**2:
                        if (cx, cy) in block_grid:
                            w_t = 1 if cy < heights[cx] + 10 else 2
                            del block_grid[(cx, cy)]
                            wall_grid[(cx, cy)] = w_t
            cur_x += math.cos(angle) * 1.2
            cur_y += math.sin(angle) * 0.9
            angle += random.uniform(-0.1, 0.1)

    # 4. Підземні озера
    for _ in range(cols_count // 70):
        lc = random.randint(100, cols_count - 100)
        lr = random.randint(100, WORLD_ROWS - 50)
        if not (200 <= lc <= 400):
            rad_x, rad_y = random.randint(10, 16), random.randint(5, 8)
            for cx in range(lc - rad_x, lc + rad_x + 1):
                for cy in range(lr - rad_y, lr + rad_y + 1):
                    if 0 <= cx < cols_count and 0 <= cy < WORLD_ROWS:
                        if ((cx - lc) / rad_x)**2 + ((cy - lr) / rad_y)**2 <= 1.0:
                            if (cx, cy) in block_grid: del block_grid[(cx, cy)]
                            wall_grid[(cx, cy)] = 2
                            if cy >= lr - int(rad_y * 0.1): water_grid[(cx, cy)] = 4

    # 5. Наземні озера
    for col in range(10, cols_count - 10):
        if get_biome_at(col) == "forest" and not (250 <= col <= 350):
            lake_level = 47
            if heights[col] > lake_level:
                for row in range(lake_level, heights[col] + 1):
                    if (col, row) in block_grid: del block_grid[(col, row)]
                    water_grid[(col, row)] = 4
                    wall_grid[(col, row)] = 1

    # 6. Мох на поверхні каменю
    for col in range(cols_count):
        for row in range(95, WORLD_ROWS - 1):
            if block_grid.get((col, row)) == 3:  
                above_is_empty = (col, row - 1) not in block_grid
                if above_is_empty:
                    if random.random() < 0.65:
                        block_grid[(col, row)] = 5  

    # 7. Данжі
    for _ in range(cols_count // 120):
        room_w, room_h = random.randint(14, 22), random.randint(8, 12)
        rx, ry = random.randint(100, cols_count - 100), random.randint(110, WORLD_ROWS - 40)
        if (200 <= rx <= 400): continue 
        
        for cx in range(rx, rx + room_w):
            for cy in range(ry, ry + room_h):
                if 0 <= cx < cols_count and 0 <= cy < WORLD_ROWS:
                    if cx == rx or cx == rx + room_w - 1 or cy == ry or cy == ry + room_h - 1:
                        block_grid[(cx, cy)] = 10 
                        if (cx, cy) in water_grid: del water_grid[(cx, cy)]
                    else:
                        if (cx, cy) in block_grid: del block_grid[(cx, cy)]
                        if (cx, cy) in water_grid: del water_grid[(cx, cy)]
                        wall_grid[(cx, cy)] = 3 
                        if cy == ry + room_h - 4 and (rx + 3 <= cx <= rx + room_w - 4):
                            block_grid[(cx, cy)] = 11 

    # 8. Вирівнювання探трави
    for col in range(cols_count):
        for row in range(heights[col], WORLD_ROWS):
            if (col, row) in block_grid:
                if (col, row - 1) not in block_grid and (col, row - 1) not in water_grid:
                    if block_grid[(col, row)] in [1, 2, 3]:
                        block_grid[(col, row)] = 1  
                break
                    
    return heights, block_grid, wall_grid, water_grid


# --- ГЕНЕРАЦІЯ ОБ'ЄКТІВ ---
def generate_world_objects(cols_count, world_heights, block_grid, water_grid):
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
            if (col, actual_surface_y - 1) in water_grid: continue
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
                    objects.append({"type": "cactus", "tile_x": col, "tile_y": actual_surface_y - height, "height": height})
                    last_obj_col = col
    return objects


def get_colliding_blocks(player_rect, block_grid):
    colliders = []
    start_x = player_rect.left // TILE_SIZE
    end_x = (player_rect.right // TILE_SIZE) + 1
    start_y = player_rect.top // TILE_SIZE
    end_y = (player_rect.bottom // TILE_SIZE) + 1
    for tx in range(start_x, end_x):
        for ty in range(start_y, end_y):
            if (tx, ty) in block_grid:
                block_rect = pygame.Rect(tx * TILE_SIZE, ty * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if player_rect.colliderect(block_rect):
                    colliders.append(block_rect)
    return colliders


def check_in_water(player_rect, water_grid):
    start_x = player_rect.left // TILE_SIZE
    end_x = (player_rect.right // TILE_SIZE) + 1
    start_y = player_rect.top // TILE_SIZE
    end_y = (player_rect.bottom // TILE_SIZE) + 1
    for tx in range(start_x, end_x):
        for ty in range(start_y, end_y):
            if (tx, ty) in water_grid:
                if player_rect.colliderect(pygame.Rect(tx * TILE_SIZE, ty * TILE_SIZE, TILE_SIZE, TILE_SIZE)): return True
    return False


def rungame():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Terraria Engine: Angry Purple Slime Added!")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Arial", 12, bold=True)
    HOTBAR_SLOTS = 10
    inventory = [{"id": 0, "count": 0} for _ in range(HOTBAR_SLOTS)]
    active_slot = 0

    world_heights, block_grid, wall_grid, water_grid = generate_world(WORLD_COLS)
    world_objects = generate_world_objects(WORLD_COLS, world_heights, block_grid, water_grid)

    # Налаштування гравця
    player_w, player_h = 24, 38
    spawn_col = 300
    p_x = spawn_col * TILE_SIZE + 2
    p_y = (world_heights[spawn_col] - 4) * TILE_SIZE
    player_rect = pygame.Rect(p_x, p_y, player_w, player_h)

    velocity_x, velocity_y = 0, 0
    acceleration, friction = 0.5, 0.80  
    gravity_air, gravity_water = 0.4, 0.12
    jump_power_air, jump_power_water = -9.5, -3.5

    is_on_ground = False
    is_touching_wall_left = False
    is_touching_wall_right = False

    # --- НАЛАШТУВАННЯ МОБА (ФІОЛЕТОВЕ КОЛО) ---
    enemy_radius = 10
    # Спавним ворога на 10 блоків правіше від гравця на поверхні
    enemy_tile_x = spawn_col + 10
    enemy_x = enemy_tile_x * TILE_SIZE
    enemy_y = (world_heights[enemy_tile_x] - 2) * TILE_SIZE
    # Створюємо квадратний Rect для прорахунку фізики колізій коліщатка
    enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_radius * 2, enemy_radius * 2)
    
    enemy_vel_x = 0
    enemy_vel_y = 0
    enemy_speed = 1.1
    enemy_wander_timer = 0
    enemy_dir = 1 # 1 - вправо, -1 - вліво

    camera_x = player_rect.x - SCREEN_WIDTH // 2
    camera_y = player_rect.y - SCREEN_HEIGHT // 2

    water_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    water_surface.fill(WATER_BLUE)

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False

            # Перемикання слотів
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:    
                    active_slot = (active_slot - 1) % HOTBAR_SLOTS
                elif event.button == 5:  
                    active_slot = (active_slot + 1) % HOTBAR_SLOTS

            if event.type == pygame.KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_9:
                    active_slot = event.key - pygame.K_1
                elif event.key == pygame.K_0:
                    active_slot = 9

        is_in_water = check_in_water(player_rect, water_grid)

        # --- КЕРУВАННЯ ГРАВЦЕМ ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: velocity_x -= acceleration
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: velocity_x += acceleration
        velocity_x *= friction
        
        current_gravity = gravity_water if is_in_water else gravity_air
        is_sliding = (is_touching_wall_left or is_touching_wall_right) and not is_on_ground and velocity_y > 0 and not is_in_water
        if is_sliding:
            velocity_y += current_gravity * 0.25  
            if velocity_y > 2.0: velocity_y = 2.0
        else:
            velocity_y += current_gravity
            max_fall = 4.0 if is_in_water else 12.0
            if velocity_y > max_fall: velocity_y = max_fall

        is_touching_wall_left = is_touching_wall_right = False

        # Рух гравця X
        player_rect.x += int(round(velocity_x))
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

        test_left = player_rect.copy(); test_left.x -= 2
        if get_colliding_blocks(test_left, block_grid): is_touching_wall_left = True
        test_right = player_rect.copy(); test_right.x += 2
        if get_colliding_blocks(test_right, block_grid): is_touching_wall_right = True

        # Рух гравця Y
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

        # Стрибки гравця
        if keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]:
            if is_in_water: velocity_y = jump_power_water
            elif is_on_ground:
                velocity_y = jump_power_air
                is_on_ground = False
            elif is_touching_wall_left and not is_on_ground:
                velocity_y = jump_power_air * 0.95; velocity_x = 6.5; is_touching_wall_left = False
            elif is_touching_wall_right and not is_on_ground:
                velocity_y = jump_power_air * 0.95; velocity_x = -6.5; is_touching_wall_right = False


        # --- ФІЗИКА ТА ШІ АГРЕСИВНОГО МОБА ---
        # Гравітація моба
        enemy_vel_y += gravity_air
        if enemy_vel_y > 10.0: enemy_vel_y = 10.0

        # Обчислення ШІ: відстань до гравця
        dist_to_player = math.sqrt((player_rect.centerx - enemy_rect.centerx)**2 + (player_rect.centery - enemy_rect.centery)**2)
        
        if dist_to_player < 240: # Агро-режим (якщо гравець ближче ніж 12 блоків)
            if player_rect.centerx < enemy_rect.centerx:
                enemy_vel_x = -enemy_speed
            else:
                enemy_vel_x = enemy_speed
        else: # Вільне вештання (патрулювання)
            enemy_wander_timer -= 1
            if enemy_wander_timer <= 0:
                enemy_dir = random.choice([1, -1, 0]) # Зміна напрямку або зупинка
                enemy_wander_timer = random.randint(40, 120)
            enemy_vel_x = enemy_dir * (enemy_speed * 0.6)

        # Рух моба по X та колізії
        enemy_rect.x += int(round(enemy_vel_x))
        enemy_hits_x = get_colliding_blocks(enemy_rect, block_grid)
        
        # Якщо врізався в блок по горизонталі — намагається стрибнути!
        if enemy_hits_x:
            for block in enemy_hits_x:
                if enemy_vel_x > 0: enemy_rect.right = block.left
                elif enemy_vel_x < 0: enemy_rect.left = block.right
            # Стрибок моба вгору
            enemy_vel_y = -6.5 

        # Рух моба по Y та колізії
        enemy_rect.y += int(round(enemy_vel_y))
        enemy_hits_y = get_colliding_blocks(enemy_rect, block_grid)
        for block in enemy_hits_y:
            if enemy_vel_y > 0:
                enemy_rect.bottom = block.top
                enemy_vel_y = 0
            elif enemy_vel_y < 0:
                enemy_rect.top = block.bottom
                enemy_vel_y = 0


        # --- МИША: КОПАННЯ ТА БУДІВНИЦТВО ---
        mouse_pressed = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        
        world_mouse_x = mouse_pos[0] + camera_x
        world_mouse_y = mouse_pos[1] + camera_y
        
        target_col = int(world_mouse_x // TILE_SIZE)
        target_row = int(world_mouse_y // TILE_SIZE)
        
        player_tile_x = player_rect.centerx // TILE_SIZE
        player_tile_y = player_rect.centery // TILE_SIZE
        
        distance = math.sqrt((target_col - player_tile_x)**2 + (target_row - player_tile_y)**2)

        if distance <= 5 and 0 <= target_col < WORLD_COLS and 0 <= target_row < WORLD_ROWS:
            # КОПАННЯ
            if mouse_pressed[0]: 
                if (target_col, target_row) in block_grid:
                    broken_block_type = block_grid[(target_col, target_row)]
                    
                    if broken_block_type in BLOCK_ITEMS:
                        added = False
                        for slot in inventory:
                            if slot["id"] == broken_block_type:
                                slot["count"] += 1
                                added = True
                                break
                        if not added:
                            for slot in inventory:
                                if slot["id"] == 0:
                                    slot["id"] = broken_block_type
                                    slot["count"] = 1
                                    added = True
                                    break
                    
                    surface_y = world_heights[target_col]
                    if target_row >= surface_y:
                        if (target_col, target_row) not in wall_grid:
                            if target_row < surface_y + 10: wall_grid[(target_col, target_row)] = 1  
                            else: wall_grid[(target_col, target_row)] = 2  
                    else:
                        if (target_col, target_row) in wall_grid: del wall_grid[(target_col, target_row)]
                    
                    del block_grid[(target_col, target_row)]

            # БУДІВНИЦТВО
            elif mouse_pressed[2]: 
                active_item = inventory[active_slot]
                if active_item["id"] != 0 and active_item["count"] > 0:
                    if (target_col, target_row) not in block_grid:
                        placed_block_rect = pygame.Rect(target_col * TILE_SIZE, target_row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        if not player_rect.colliderect(placed_block_rect):
                            block_grid[(target_col, target_row)] = active_item["id"]
                            if (target_col, target_row) in water_grid: del water_grid[(target_col, target_row)]
                            active_item["count"] -= 1
                            if active_item["count"] <= 0:
                                active_item["id"] = 0
                                active_item["count"] = 0

        # Динамічна камера
        camera_x += ((player_rect.centerx - SCREEN_WIDTH // 2) - camera_x) * 0.1  
        camera_x = max(0, min(camera_x, WORLD_COLS * TILE_SIZE - SCREEN_WIDTH))
        camera_y += ((player_rect.centery - SCREEN_HEIGHT // 2) - camera_y) * 0.1  
        camera_y = max(0, min(camera_y, WORLD_ROWS * TILE_SIZE - SCREEN_HEIGHT))

        # --- МАЛЮВАННЯ СВІТУ ---
        screen.fill(SKY_BLUE)
        start_col = max(0, int(camera_x // TILE_SIZE))
        end_col = min(WORLD_COLS, start_col + (SCREEN_WIDTH // TILE_SIZE) + 2)
        start_row = max(0, int(camera_y // TILE_SIZE))
        end_row = min(WORLD_ROWS, start_row + (SCREEN_HEIGHT // TILE_SIZE) + 2)
        int_cam_x, int_cam_y = int(camera_x), int(camera_y)

        for col in range(start_col, end_col):
            biome = get_biome_at(col)
            if biome == "tundra": c1, c2 = SNOW_WHITE, ICE_BLUE
            elif biome == "forest": c1, c2 = GRASS_GREEN, DIRT_BROWN
            else: c1, c2 = SAND_YELLOW, SAND_DARK

            for row in range(start_row, end_row):
                rect = pygame.Rect(col * TILE_SIZE - int_cam_x, row * TILE_SIZE - int_cam_y, TILE_SIZE, TILE_SIZE)
                block_type = block_grid.get((col, row), 0)
                
                if block_type != 0:
                    if block_type == 1: pygame.draw.rect(screen, c1, rect)
                    elif block_type == 2: pygame.draw.rect(screen, c2, rect)
                    elif block_type == 3: pygame.draw.rect(screen, STONE_GRAY, rect)
                    elif block_type == 5: pygame.draw.rect(screen, MOSS_GREEN, rect)
                    elif block_type == 6: pygame.draw.rect(screen, ORE_COPPER, rect)
                    elif block_type == 7: pygame.draw.rect(screen, ORE_IRON, rect)
                    elif block_type == 8: pygame.draw.rect(screen, ORE_GOLD, rect)
                    elif block_type == 9: pygame.draw.rect(screen, ORE_AMETHYST, rect)
                    elif block_type == 10: pygame.draw.rect(screen, DUNGEON_BRICK, rect)
                    elif block_type == 11: pygame.draw.rect(screen, WOOD_PLATFORM, rect)
                    pygame.draw.rect(screen, (0, 0, 0), rect, 1)  
                else:
                    wall_type = wall_grid.get((col, row), 0)
                    if wall_type == 1: pygame.draw.rect(screen, WALL_DIRT, rect)
                    elif wall_type == 2: pygame.draw.rect(screen, WALL_STONE, rect)
                    elif wall_type == 3: pygame.draw.rect(screen, WALL_DUNGEON, rect)
                    if (col, row) in water_grid: screen.blit(water_surface, rect)

        # Об'єкти світу (дерева)
        for obj in world_objects:
            obj_screen_x = obj["tile_x"] * TILE_SIZE - int_cam_x
            if -100 < obj_screen_x < SCREEN_WIDTH + 100:
                if obj["type"] in ["normal_tree", "pine"]:
                    for h in range(obj["height"]):
                        pygame.draw.rect(screen, TRUNK_BROWN, pygame.Rect(obj_screen_x, (obj["tile_y"] + h) * TILE_SIZE - int_cam_y, TILE_SIZE, TILE_SIZE))
                    cx, cy, r = obj["tile_x"], obj["tile_y"], obj.get("foliage_radius", 2)
                    foliage_color = LEAVES_GREEN if obj["type"] == "normal_tree" else (20, 80, 40)
                    for nx in range(cx - r, cx + r + 1):
                        for ny in range(cy - r, cy + r + 1):
                            if (nx - cx)**2 + (ny - cy)**2 <= r**2:
                                pygame.draw.rect(screen, foliage_color, pygame.Rect(nx * TILE_SIZE - int_cam_x, ny * TILE_SIZE - int_cam_y, TILE_SIZE, TILE_SIZE))
                elif obj["type"] == "cactus":
                    for h in range(obj["height"]):
                        pygame.draw.rect(screen, CACTUS_GREEN, pygame.Rect(obj_screen_x, (obj["tile_y"] + h) * TILE_SIZE - int_cam_y, TILE_SIZE, TILE_SIZE))

        # --- МАЛЮВАННЯ МОБА ---
        # Віднімаємо координати камери, щоб моб залишався прив'язаним до світу
        pygame.draw.circle(screen, ENEMY_PURPLE, (enemy_rect.centerx - int_cam_x, enemy_rect.centery - int_cam_y), enemy_radius)

        # Малювання гравця
        pygame.draw.rect(screen, PLAYER_BLUE, (player_rect.x - int_cam_x, player_rect.y - int_cam_y, player_w, player_h))
        
        # --- МАЛЮВАННЯ ІНВЕНТАРЮ ---
        slot_size = 40
        slot_margin = 5
        start_x = 10
        start_y = 10

        for i in range(HOTBAR_SLOTS):
            slot_x = start_x + i * (slot_size + slot_margin)
            slot_rect = pygame.Rect(slot_x, start_y, slot_size, slot_size)
            
            slot_color = (180, 180, 180) if i == active_slot else (60, 60, 60)
            border_color = (255, 255, 255) if i == active_slot else (30, 30, 30)
            border_width = 3 if i == active_slot else 2
            
            pygame.draw.rect(screen, slot_color, slot_rect)
            pygame.draw.rect(screen, border_color, slot_rect, border_width)
            
            item_data = inventory[i]
            if item_data["id"] != 0:
                item_info = BLOCK_ITEMS[item_data["id"]]
                item_rect = pygame.Rect(slot_x + 8, start_y + 8, slot_size - 16, slot_size - 16)
                pygame.draw.rect(screen, item_info["color"], item_rect)
                pygame.draw.rect(screen, (0, 0, 0), item_rect, 1)
                
                text_surf = font.render(str(item_data["count"]), True, (255, 255, 255))
                screen.blit(text_surf, (slot_x + 4, start_y + slot_size - 16))
        
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    rungame()