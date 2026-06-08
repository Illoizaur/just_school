# Перед головним циклом ініціалізуємо шрифт:
font = pygame.font.SysFont("Arial", 12, bold=True)

# Наприкінці секції малювання (перед pygame.display.flip()):
slot_size = 40
slot_margin = 5
start_x = 10
start_y = 10

for i in range(slots):
    # Координати кожного квадрата комірки
    slot_x = start_x + i * (slot_size + slot_margin)
    slot_rect = pygame.Rect(slot_x, start_y, slot_size, slot_size)
    
    # Світло-сірий фон для звичайних слотів, білий — для активного
    slot_color = (200, 200, 200) if i == active_slot else (60, 60, 60)
    border_color = (255, 255, 255) if i == active_slot else (30, 30, 30)
    border_width = 3 if i == active_slot else 2
    
    # Малюємо фон слота
    pygame.draw.rect(screen, slot_color, slot_rect)
    pygame.draw.rect(screen, border_color, slot_rect, border_width)
    
    # Малюємо іконку предмета всередині слота, якщо він не порожній (id != 0)
    item_data = inventory[i]
    if item_data["id"] != 0:
        item_info = BLOCK_ITEMS[item_data["id"]]
        # Малюємо міні-блок всередині слота
        item_rect = pygame.Rect(slot_x + 8, start_y + 8, slot_size - 16, slot_size - 16)
        pygame.draw.rect(screen, item_info["color"], item_rect)
        pygame.draw.rect(screen, (0, 0, 0), item_rect, 1)
        
        # Виводимо текст із кількістю блоків
        text_surf = font.render(str(item_data["count"]), True, (255, 255, 255))
        screen.blit(text_surf, (slot_x + 4, start_y + slot_size - 16))