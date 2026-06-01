import pygame
import sys

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TILE_SIZE = 40  

SKY_BLUE = (135, 206, 235)
DIRT_COLOR = (139, 69, 19)
GRASS_COLOR = (34, 139, 34)
PLAYER_COLOR = (255, 105, 180)
GRID_COLOR = (100, 149, 237)


class World:
    def __init__(self):
        self.grid = []
        for row in range(15):
            grid_row = []
            for col in range(20):
                if row < 10:
                    grid_row.append(0)  
                elif row == 10:
                    grid_row.append(1)  
                else:
                    grid_row.append(2)  
            self.grid.append(grid_row)

    def draw(self, screen):
        for row_idx, row in enumerate(self.grid):
            for col_idx, tile in enumerate(row):
                if tile > 0:
                    x = col_idx * TILE_SIZE
                    y = row_idx * TILE_SIZE
                    rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    
                    color = GRASS_COLOR if tile == 1 else DIRT_COLOR
                    pygame.draw.rect(screen, color, rect)
                    pygame.draw.rect(screen, (0, 0, 0), rect, 1)


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 50) 
        self.vel_y = 0
        self.is_on_ground = False
        self.speed = 5

    def handle_movement(self, world_grid):
        keys = pygame.key.get_pressed()
        dx = 0

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = self.speed

        if (keys[pygame.K_SPACE] or keys[pygame.K_w]) and self.is_on_ground:
            self.vel_y = -12
            self.is_on_ground = False

        self.vel_y += 0.6
        if self.vel_y > 10:
            self.vel_y = 10
        dy = self.vel_y

        self.rect.x += dx
        self.check_collision(world_grid, dx, 0)
        
        self.rect.y += dy
        self.check_collision(world_grid, 0, dy)

    def check_collision(self, world_grid, dx, dy):
        for row_idx, row in enumerate(world_grid):
            for col_idx, tile in enumerate(row):
                if tile > 0: 
                    tile_rect = pygame.Rect(col_idx * TILE_SIZE, row_idx * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    
                    if self.rect.colliderect(tile_rect):
                        if dx > 0: self.rect.right = tile_rect.left
                        if dx < 0: self.rect.left = tile_rect.right
                        
                        if dy > 0: 
                            self.rect.bottom = tile_rect.top
                            self.vel_y = 0
                            self.is_on_ground = True
                        if dy < 0: 
                            self.rect.top = tile_rect.bottom
                            self.vel_y = 0

    def draw(self, screen):
        pygame.draw.rect(screen, PLAYER_COLOR, self.rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Мій клон Террарії (Етап 4)")
    clock = pygame.time.Clock()

    world = World()
    player = Player(100, 200)

    running = True
    while running:
        clock.tick(FPS)
        screen.fill(SKY_BLUE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                grid_col = mouse_x // TILE_SIZE
                grid_row = mouse_y // TILE_SIZE

                if 0 <= grid_col < 20 and 0 <= grid_row < 15:
                    
                    if event.button == 1:
                        world.grid[grid_row][grid_col] = 0
                        
                    elif event.button == 3:
                        new_tile_rect = pygame.Rect(grid_col * TILE_SIZE, grid_row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        
                        if world.grid[grid_row][grid_col] == 0 and not player.rect.colliderect(new_tile_rect):
                            world.grid[grid_row][grid_col] = 2

        player.handle_movement(world.grid)

        world.draw(screen)
        player.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()