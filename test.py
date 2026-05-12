import pygame
import random

WIDTH, HEIGHT = 800, 600
TILE_SIZE = 32
FPS = 60

SKY_BLUE = (135, 206, 235)
DIRT = (155, 118, 83)
GRASS = (34, 139, 34)
PLAYER_COLOR = (255, 0, 0)

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TILE_SIZE * 0.8, TILE_SIZE * 1.5)
        self.vel_y = 0
        self.speed = 5
        self.jump_power = -12

    def update(self, tiles):
        dx, dy = 0, 0
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_a]: dx -= self.speed
        if keys[pygame.K_d]: dx += self.speed
        
        self.vel_y += 0.8
        if self.vel_y > 10: self.vel_y = 10
        dy += self.vel_y

        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False

        self.on_ground = False
        for tile in tiles:
            if tile.colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                dx = 0
            if tile.colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                if self.vel_y < 0:
                    dy = tile.bottom - self.rect.top
                    self.vel_y = 0
                elif self.vel_y >= 0:
                    dy = tile.top - self.rect.bottom
                    self.vel_y = 0
                    self.on_ground = True

        self.rect.x += dx
        self.rect.y += dy

def create_world():
    world = []
    for x in range(0, WIDTH, TILE_SIZE):
        ground_level = HEIGHT // 2 + random.randint(0, 2) * TILE_SIZE
        for y in range(ground_level, HEIGHT, TILE_SIZE):
            color = GRASS if y == ground_level else DIRT
            world.append({'rect': pygame.Rect(x, y, TILE_SIZE, TILE_SIZE), 'color': color})
    return world

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    
    world_data = create_world()
    player = Player(WIDTH // 2, 100)

    running = True
    while running:
        screen.fill(SKY_BLUE)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    world_data = [t for t in world_data if not t['rect'].collidepoint(mouse_pos)]
                if event.button == 3:
                    grid_x = (mouse_pos[0] // TILE_SIZE) * TILE_SIZE
                    grid_y = (mouse_pos[1] // TILE_SIZE) * TILE_SIZE
                    new_tile = {'rect': pygame.Rect(grid_x, grid_y, TILE_SIZE, TILE_SIZE), 'color': DIRT}
                    world_data.append(new_tile)

        tiles = [t['rect'] for t in world_data]
        player.update(tiles)

        for tile in world_data:
            pygame.draw.rect(screen, tile['color'], tile['rect'])
            pygame.draw.rect(screen, (0,0,0), tile['rect'], 1) # Контур

        pygame.draw.rect(screen, PLAYER_COLOR, player.rect)
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()