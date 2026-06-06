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
WATER_BLUE = (30, 85, 230, 180)  # Напівпрозора вода для краси

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


# --- 2. ГЕНЕРАЦІЯ СВІТУ (З озерами та підземними водами) ---
def generate_world(cols_count):
    heights = []
    block_grid = {}  
    wall_grid = {}   
    water_grid = {}  # Окрема сітка для води
    
    seed1 = random.uniform(0, 1000)
    seed2 = random.uniform(0, 1000)
    cave_seeds = [random.uniform(0, 500) for _ in range(4)]
    
    # 1. Рахуємо рельєф поверхні з плавними переходами
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

    # Спочатку створюємо центри підземних озер (кишень)
    underground_lakes = []
    for _ in range(cols_count // 60):
        lc = random.randint(100, cols_count - 100)
        lr = random.randint(80, WORLD_ROWS - 40)
        if not (200 <= lc <= 400):  # Подалі від спавну
            underground_lakes.append((lc, lr, random.randint(8, 15), random.randint(4, 7)))

    # 2. Заповнюємо підземелля блоками та базовими печерами
    for col in range(cols_count):
        final_height = heights[col]
        is_spawn_zone = (230 <= col <= 370)

        for row in range(final_height, WORLD_ROWS):
            depth = row - final_height
            is_cave = False
            
            if not is_spawn_zone and depth >= 20:
                n1 = math.sin(col * 0.08 + cave_seeds[0]) * math.cos(row * 0.12 + cave_seeds[1])
                n2 = math.sin(row * 0.07 + cave_seeds[2]) * math.cos(col * 0.15 + cave_seeds[3])
                if -0.21 < (n1 + n2) < 0.21:
                    is_cave = True

            b_type = 1 if row == final_height else (2 if row < final_height + 10 else 3)
            w_type = 1 if row < final_height + 10 else 2  

            if not is_cave:
                block_grid[(col, row)] = b_type
            else:
                wall_grid[(col, row)] = w_type

    # 3. Вирізаємо красиві входи ("хробаки")
    entrance_cols = []
    next_ent = 140
    while next_ent < cols_count - 140:
        if not (210 <= next_ent <= 390):
            entrance_cols.append(next_ent)
        next_ent += random.randint(180, 280)

    for start_col in entrance_cols:
        cur_x, cur_y = float(start_col), float(heights[start_col])
        angle = random.choice([math.radians(35), math.radians(145)]) 
        tunnel_length = random.randint(45, 75)
        
        for step in range(tunnel_length):
            radius = 3.5 + math.sin(step * 0.3) * 1.0
            min_c = max(0, int(cur_x - radius - 1))
            max_c = min(cols_count, int(cur_x + radius + 1))
            min_r = max(0, int(cur_y - radius - 1))
            max_r = min(WORLD_ROWS, int(cur_y + radius + 1))
            
            for cx in range(min_c, max_c):
                for cy in range(min_r, max_r):
                    if (cx - cur_x)**2 + (cy - cur_y)**2 <= radius**2:
                        if (cx, cy) in block_grid:
                            w_t = 1 if cy < heights[cx] + 10 else 2
                            del block_grid[(cx, cy)]
                            wall_grid[(cx, cy)] = w_t

            cur_x += math.cos(angle) * 1.2
            cur_y += math.sin(angle) * 0.9
            angle += random.uniform(-0.1, 0.1)

    # 4. Створення ПІДЗЕМНИХ озер (заповнення каверн водою)
    for (lc, lr, rad_x, rad_y) in underground_lakes:
        for cx in range(lc - rad_x, lc + rad_x + 1):
            for cy in range(lr - rad_y, lr + rad_y + 1):
                if 0 <= cx < cols_count and 0 <= cy < WORLD_ROWS:
                    # Еліптична форму каверни
                    if ((cx - lc) / rad_x)**2 + ((cy - lr) / rad_y)**2 <= 1.0:
                        # Завжди прибираємо блоки, створюючи грот
                        if (cx, cy) in block_grid:
                            del block_grid[(cx, cy)]
                        wall_grid[(cx, cy)] = 2
                        # Нижню половину гроту заливаємо водою
                        if cy >= lr - int(rad_y * 0.2):
                            water_grid[(cx, cy)] = 4

    # 5. Створення НАЗЕМНИХ озер (у заглибленнях лісового біому)
    # Шукаємо локальні низини та заповнюємо їх водою, якщо вони занадто низько
    for col in range(10, cols_count - 10):
        if get_biome_at(col) == "forest" and not (250 <= col <= 350):
            # Якщо рівень землі нижчий за певну позначку (наприклад, 48), це може бути озеро
            lake_level = 47
            if heights[col] > lake_level:
                for row in range(lake_level, heights[col] + 1):
                    # Прибираємо верхні блоки трави/землі під воду
                    if (col, row) in block_grid:
                        del block_grid[(col, row)]
                    water_grid[(col, row)] = 4
                    wall_grid[(col, row)] = 1

    # 6. Оновлення трави на нових схилах та стиках
    for col in range(cols_count):
        for row in range(heights[col], WORLD_ROWS):
            if (col, row) in block_grid:
                if (col, row - 1) not in block_grid and (col, row - 1) not in water_grid:
                    block_grid[(col, row)] = 1  
                break
                    
    return heights, block_grid, wall_grid, water_grid


# --- 3. ГЕНЕРАЦІЯ ОБ'ЄКТІВ ---
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
        
        # Дерева не ростуть під водою
        if actual_surface_y != -1 and block_grid.get((col, actual_surface_y)) == 1:
            if (col, actual_surface_y - 1) in water_grid:
                continue

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


# Перевірка: чи знаходиться гравець у воді
def check_in_water(player_rect, water_grid):
    start_x = int(player_rect.left // TILE_SIZE)
    end_x = int((player_rect.right // TILE_SIZE) + 1)
    start_y = int(player_rect.top // TILE_SIZE)
    end_y = int((player_rect.bottom // TILE_SIZE) + 1)

    for tx in range(start_x, end_x):
        for ty in range(start_y, end_y):
            if (tx, ty) in water_grid:
                w_rect = pygame.Rect(tx * TILE_SIZE, ty * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if player_rect.colliderect(w_rect):
                    return True
    return False


def rungame():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Terraria Engine: Lakes & Underwater Caves")
    clock = pygame.time.Clock()

    world_heights, block_grid, wall_grid, water_grid = generate_world(WORLD_COLS)
    world_objects = generate_world_objects(WORLD_COLS, world_heights, block_grid, water_grid)

    # Персонаж
    player_w = 24
    player_h = 38
    spawn_col = 300
    
    p_x = spawn_col * TILE_SIZE + 2
    p_y = (world_heights[spawn_col] - 4) * TILE_SIZE
    player_rect = pygame.Rect(p_x, p_y, player_w, player_h)

    velocity_x = 0
    velocity_y = 0
    acceleration = 5
    friction = 0.80
    
    # Фізичні константи
    gravity_air = 0.4
    gravity_water = 0.12  # Знижена гравітація у воді (спливна сила)
    jump_power_air = -9.5
    jump_power_water = -3.5 # Плавні поштовхи вгору під час плавання

    is_on_ground = False
    is_touching_wall_left = False
    is_touching_wall_right = False

    camera_x = player_rect.x - SCREEN_WIDTH // 2
    camera_y = player_rect.y - SCREEN_HEIGHT // 2

    # Створюємо окрему поверхню для рендерингу напівпрозорої води
    water_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    water_surface.fill(WATER_BLUE)

    running = True
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Перевіряємо середовище, де знаходиться гравець
        is_in_water = check_in_water(player_rect, water_grid)

        # Керування
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: velocity_x -= acceleration
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: velocity_x += acceleration

        velocity_x *= friction
        
        # Налаштування фізики під середовище
        current_gravity = gravity_water if is_in_water else gravity_air
        
        is_sliding = (is_touching_wall_left or is_touching_wall_right) and not is_on_ground and velocity_y > 0 and not is_in_water
        if is_sliding:
            velocity_y += current_gravity * 0.25  
            if velocity_y > 2.0: velocity_y = 2.0
        else:
            velocity_y += current_gravity
            max_fall_speed = 4.0 if is_in_water else 12.0
            if velocity_y > max_fall_speed: velocity_y = max_fall_speed

        is_touching_wall_left = False
        is_touching_wall_right = False

        # Рух та колізії X
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

        # Рух та колізії Y
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

        # Механіка стрибків / Стрибків від стіни / Плавання
        jump_pressed = keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]
        if jump_pressed:
            if is_in_water:
                # Плавання: багаторазові легкі поштовхи вгору у воді
                velocity_y = jump_power_water
            elif is_on_ground:
                velocity_y = jump_power_air
                is_on_ground = False
            elif is_touching_wall_left and not is_on_ground:
                velocity_y = jump_power_air * 0.95
                velocity_x = 6.5  
                is_touching_wall_left = False
            elif is_touching_wall_right and not is_on_ground:
                velocity_y = jump_power_air * 0.95
                velocity_x = -6.5 
                is_touching_wall_right = False

        if player_rect.bottom > WORLD_ROWS * TILE_SIZE:
            current_col = int(player_rect.x // TILE_SIZE)
            player_rect.y = (world_heights[current_col] - 4) * TILE_SIZE
            velocity_y = 0

        # Камера
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

        int_cam_x, int_cam_y = int(camera_x), int(camera_y)

        # Рендеринг блоків, стін та води
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
                    pygame.draw.rect(screen, (0, 0, 0), rect, 1)  
                else:
                    # Якщо блоку немає — малюємо задній фон (стіну)
                    wall_type = wall_grid.get((col, row), 0)
                    if wall_type == 1: pygame.draw.rect(screen, WALL_DIRT, rect)
                    elif wall_type == 2: pygame.draw.rect(screen, WALL_STONE, rect)
                    
                    # Якщо в цій точці є вода — накладаємо її поверх задньої стіни
                    if (col, row) in water_grid:
                        screen.blit(water_surface, rect)

        # Малювання об'єктів (дерева/катуси)
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

        # Малювання гравця
        player_screen_x = player_rect.x - int_cam_x
        player_screen_y = player_rect.y - int_cam_y
        pygame.draw.rect(screen, PLAYER_BLUE, (player_screen_x, player_screen_y, player_w, player_h))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    rungame()