import random
import sys
import pygame

# Спробуємо імпортувати шум Перліна для гарної генерації
try:
    from noise import pnoise1
    HAS_NOISE = True
except ImportError:
    HAS_NOISE = False
    print(
        "Порада: встановіть бібліотеку noise (pip install noise) для кращої генерації!"
    )

# --- НАЛАШТУВАННЯ ГРИ ---
WIDTH, HEIGHT = 1920, 1080
TILE_SIZE = 16  # Розмір одного блоку в пікселях
FPS = 60

# Кількість блоків у світі
WORLD_WIDTH = 150
WORLD_HEIGHT = 80

# Кольори блоків (Тільки лісовий біом)
SKY_COLOR = (135, 206, 235)
DIRT_COLOR = (139, 69, 19)
GRASS_COLOR = (34, 139, 34)
STONE_COLOR = (128, 128, 128)
WATER_COLOR = (0, 0, 255, 150)  # Напівпрозора вода
WOOD_COLOR = (101, 67, 33)
LEAVES_COLOR = (0, 100, 0)

# Ідентифікатори блоків
AIR = 0
DIRT = 1
GRASS = 2
STONE = 3
WATER = 4
WOOD = 5
LEAVES = 6


# --- ПРОЦЕДУРНА ГЕНЕРАЦІЯ ---
def generate_world():
    # Створюємо порожню матрицю світу [y][x]
    world = [[AIR for _ in range(WORLD_WIDTH)] for _ in range(WORLD_HEIGHT)]

    # Базова лінія поверхні (середина екрану)
    base_floor = WORLD_HEIGHT // 2

    # 1. Генерація рельєфу (земля, трава, камінь)
    for x in range(WORLD_WIDTH):
        if HAS_NOISE:
            # Шум Перліна для плавних пагорбів
            noise_val = pnoise1(x * 0.05, octaves=2)
            height_offset = int(noise_val * 12)
        else:
            # Спрощений варіант, якщо немає бібліотеки noise
            import math

            height_offset = int(math.sin(x * 0.1) * 5 + math.cos(x * 0.05) * 3)

        surface_y = base_floor + height_offset

        for y in range(WORLD_HEIGHT):
            if y < surface_y:
                world[y][x] = AIR
            elif y == surface_y:
                world[y][x] = GRASS
            elif y < surface_y + 5:  # 5 блоків під травою — земля
                world[y][x] = DIRT
            else:
                world[y][x] = STONE  # Все що глибше — камінь

    # 2. Генерація водойм (озер)
    # Шукаємо випадкові "низини" для заповнення водою
    num_lakes = random.randint(0, 3)
    for _ in range(num_lakes):
        lake_center_x = random.randint(10, WORLD_WIDTH - 10)
        lake_depth = random.randint(1, 10)
        lake_radius = random.randint(3, 20)

        # Знаходимо рівень трави в центрі озера, щоб знати, де вода
        surface_y = base_floor
        for y in range(WORLD_HEIGHT):
            if world[y][lake_center_x] in [GRASS, DIRT]:
                surface_y = y
                break

        # Вирізаємо заглиблення під озеро і заливаємо водою
        for x in range(lake_center_x - lake_radius, lake_center_x + lake_radius):
            if 0 <= x < WORLD_WIDTH:
                # Робимо округлу форму дна
                dist_to_center = abs(x - lake_center_x)
                current_depth = int(
                    lake_depth * (1 - (dist_to_center / lake_radius) ** 2)
                )

                for d in range(current_depth):
                    target_y = surface_y + d
                    if target_y < WORLD_HEIGHT:
                        # Заливаємо водою, якщо це повітря або верхні шари землі
                        if d == 0:
                            world[target_y][x] = WATER
                        else:
                            # Робимо дно озера з бруду, а не з трави
                            world[target_y][x] = WATER
                        # Робимо під водою бруд замість повітря
                        if (
                            target_y + 1 < WORLD_HEIGHT
                            and world[target_y + 1][x] == AIR
                        ):
                            world[target_y + 1][x] = DIRT

    # 3. Генерація дерев
    for x in range(2, WORLD_WIDTH - 2):
        # Перевіряємо, чи тут росте трава і чи немає поруч води
        has_grass = False
        surface_y = 0
        for y in range(WORLD_HEIGHT):
            if world[y][x] == GRASS:
                has_grass = True
                surface_y = y
                break
            elif world[y][x] == WATER:
                break  # На воді дерева не ростуть

        if has_grass:
            # Шанс спавну дерева (наприклад, 15%)
            # Також перевіряємо, щоб дерева не росли впритул одне до одного
            if random.random() < 0.15:
                # Перевірка сусідніх блоків на наявність інших стовбурів
                is_space_free = True
                for check_x in range(x - 2, x + 3):
                    if 0 <= check_x < WORLD_WIDTH:
                        if world[surface_y - 1][check_x] == WOOD:
                            is_space_free = False

                if is_space_free:
                    tree_height = random.randint(4, 7)
                    # Ростимо стовбур вгору (заміняючи повітря)
                    for h in range(1, tree_height + 1):
                        if surface_y - h >= 0:
                            world[surface_y - h][x] = WOOD

                    # Створюємо листя (крону) на верхівці
                    top_y = surface_y - tree_height
                    for leaf_y in range(top_y - 2, top_y + 1):
                        for leaf_x in range(x - 2, x + 3):
                            if 0 <= leaf_x < WORLD_WIDTH and 0 <= leaf_y < WORLD_HEIGHT:
                                # Не ставимо листя туди, де вже є стовбур
                                if world[leaf_y][leaf_x] == AIR:
                                    # Робимо крону трохи округлою
                                    if not (
                                        (
                                            leaf_y == top_y - 2
                                            and (
                                                leaf_x == x - 2 or leaf_x == x + 2
                                            )
                                        )
                                    ):
                                        world[leaf_y][leaf_x] = LEAVES

    return world


# --- ГОЛОВНА ФУНКЦІЯ ГРИ ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Terraria Clone - Procedural Forest")
    clock = pygame.time.Clock()

    # Генеруємо світ
    world_matrix = generate_world()

    # Зсув камери (для можливості перегляду світу)
    camera_x = 0
    camera_y = 0
    scroll_speed = 5

    running = True
    while running:
        clock.tick(FPS)

        # 1. Обробка подій та керування камерою
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Перегенерація світу на Пробіл
                    world_matrix = generate_world()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            camera_x -= scroll_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            camera_x += scroll_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            camera_y -= scroll_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            camera_y += scroll_speed

        # Обмеження камери, щоб не вилітати за межі світу
        camera_x = max(
            0, min(camera_x, WORLD_WIDTH * TILE_SIZE - WIDTH)
        )
        camera_y = max(
            0, min(camera_y, WORLD_HEIGHT * TILE_SIZE - HEIGHT)
        )

        # 2. Рендеринг (Малювання)
        screen.fill(SKY_COLOR)  # Небо на задньому плані

        # Обчислюємо які блоки видимі на екрані (оптимізація)
        start_x = camera_x // TILE_SIZE
        end_x = (camera_x + WIDTH) // TILE_SIZE + 1
        start_y = camera_y // TILE_SIZE
        end_y = (camera_y + HEIGHT) // TILE_SIZE + 1

        # Малюємо блоки
        for y in range(start_y, min(end_y, WORLD_HEIGHT)):
            for x in range(start_x, min(end_x, WORLD_WIDTH)):
                block = world_matrix[y][x]
                if block == AIR:
                    continue

                # Координати на екрані з урахуванням камери
                rect = pygame.Rect(
                    x * TILE_SIZE - camera_x,
                    y * TILE_SIZE - camera_y,
                    TILE_SIZE,
                    TILE_SIZE,
                )

                if block == GRASS:
                    pygame.draw.rect(screen, GRASS_COLOR, rect)
                elif block == DIRT:
                    pygame.draw.rect(screen, DIRT_COLOR, rect)
                elif block == STONE:
                    pygame.draw.rect(screen, STONE_COLOR, rect)
                elif block == WOOD:
                    pygame.draw.rect(screen, WOOD_COLOR, rect)
                elif block == LEAVES:
                    pygame.draw.rect(screen, LEAVES_COLOR, rect)
                elif block == WATER:
                    # Для води використовуємо спеціальну поверхню з альфа-каналом (прозорість)
                    water_surface = pygame.Surface(
                        (TILE_SIZE, TILE_SIZE), pygame.SRCALPHA
                    )
                    water_surface.fill(WATER_COLOR)
                    screen.blit(water_surface, (rect.x, rect.y))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()