import pygame
import random

# Ініціалізація Pygame
pygame.init()

# Налаштування екрана
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Trainer")

# Кольори
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Початкові координати фігури
x, y = random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)
RADIUS = 30

# Змінні для таймера
last_move_time = 0
MOVE_INTERVAL = 1000 # Інтервал у мілісекундах

# Основний цикл гри
running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False


        # Записуємо в змінну поточний час
        current_time = pygame.time.get_ticks()

        # Переміщуємо фігуру у випадкове місце щосекунди
    if current_time - last_move_time>= MOVE_INTERVAL:

        x, y = random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)
        last_move_time = current_time

# Очищаємо екран і малюємо нову фігурку
screen.fill(WHITE)
pygame.draw.circle(screen, RED, (x, y), RADIUS)
pygame.display.flip() # Оновлюємо екран

pygame.quit()