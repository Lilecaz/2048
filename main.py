import pygame
import random

# --- Constants ---
WINDOW_SIZE = (400, 450)
GRID_SIZE = 4
TILE_SIZE = 100
HEADER_HEIGHT = 50
FPS = 60

COLORS = {
    0: (200, 200, 200),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}

# --- Game Initialization ---
def init_game():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("2048 Celil")
    return screen

def start_new_game():
    grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    add_random_tile(grid)
    add_random_tile(grid)
    return grid, 0

# --- Grid and Tile Operations ---
def add_random_tile(grid):
    empty = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if grid[i][j] == 0]
    if empty:
        i, j = random.choice(empty)
        grid[i][j] = 2 if random.random() < 0.9 else 4

def transpose(grid):
    return [list(row) for row in zip(*grid)]

def can_move(grid):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j] == 0:
                return True
            if j < GRID_SIZE - 1 and grid[i][j] == grid[i][j + 1]:
                return True
            if i < GRID_SIZE - 1 and grid[i][j] == grid[i + 1][j]:
                return True
    return False

# --- Move Operations ---
def move_left(grid, score):
    moved = False
    for i in range(GRID_SIZE):
        tiles = [v for v in grid[i] if v != 0]
        merged = []
        j = 0
        while j < len(tiles):
            if j + 1 < len(tiles) and tiles[j] == tiles[j + 1]:
                new_value = tiles[j] * 2
                merged.append(new_value)
                score += new_value
                j += 2
                moved = True
            else:
                merged.append(tiles[j])
                j += 1
        merged += [0] * (GRID_SIZE - len(merged))
        if merged != grid[i]:
            moved = True
        grid[i] = merged
    return moved, score

def move_right(grid, score):
    for i in range(GRID_SIZE):
        grid[i].reverse()
    moved, score = move_left(grid, score)
    for i in range(GRID_SIZE):
        grid[i].reverse()
    return moved, score

def move_up(grid, score):
    grid[:] = transpose(grid)
    moved, score = move_left(grid, score)
    grid[:] = transpose(grid)
    return moved, score

def move_down(grid, score):
    grid[:] = transpose(grid)
    moved, score = move_right(grid, score)
    grid[:] = transpose(grid)
    return moved, score

# --- Drawing Functions ---
def draw_header(screen, score, best_score):
    font = pygame.font.SysFont(None, 36)
    pygame.draw.rect(screen, (150, 140, 130), (0, 0, WINDOW_SIZE[0], HEADER_HEIGHT))
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    best_text = font.render(f"Best: {best_score}", True, (255, 255, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(best_text, (250, 10))

def draw_tiles(screen, grid):
    font = pygame.font.SysFont(None, 48)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            value = grid[i][j]
            color = COLORS.get(value, (60, 58, 50))
            rect = (j * TILE_SIZE, i * TILE_SIZE + HEADER_HEIGHT, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, color, rect)
            if value:
                text = font.render(str(value), True, (0, 0, 0))
                text_rect = text.get_rect(center=(j * TILE_SIZE + TILE_SIZE // 2, i * TILE_SIZE + HEADER_HEIGHT + TILE_SIZE // 2))
                screen.blit(text, text_rect)

def draw_game_over(screen):
    overlay = pygame.Surface((WINDOW_SIZE[0], WINDOW_SIZE[1] - HEADER_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, HEADER_HEIGHT))
    over_font = pygame.font.SysFont(None, 64)
    msg = over_font.render("Game Over!", True, (255, 255, 255))
    msg_rect = msg.get_rect(center=(WINDOW_SIZE[0] // 2, HEADER_HEIGHT + 150))
    screen.blit(msg, msg_rect)
    regame_font = pygame.font.SysFont(None, 36)
    regame_msg = regame_font.render("Press R to restart", True, (255, 255, 255))
    regame_rect = regame_msg.get_rect(center=(WINDOW_SIZE[0] // 2, HEADER_HEIGHT + 220))
    quit_msg = regame_font.render("Press Q to quit", True, (255, 255, 255))
    quit_rect = quit_msg.get_rect(center=(WINDOW_SIZE[0] // 2, HEADER_HEIGHT + 260))
    screen.blit(regame_msg, regame_rect)
    screen.blit(quit_msg, quit_rect)

def draw_grid(screen, grid, score, best_score, game_over=False):
    draw_header(screen, score, best_score)
    draw_tiles(screen, grid)
    if game_over:
        draw_game_over(screen)

# --- Main Game Loop ---
def main():
    screen = init_game()
    clock = pygame.time.Clock()
    best_score = 0
    grid, score = start_new_game()
    running = True
    game_over = False

    while running:
        moved = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif not game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    moved, score = move_left(grid, score)
                elif event.key == pygame.K_RIGHT:
                    moved, score = move_right(grid, score)
                elif event.key == pygame.K_UP:
                    moved, score = move_up(grid, score)
                elif event.key == pygame.K_DOWN:
                    moved, score = move_down(grid, score)
            elif game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    grid, score = start_new_game()
                    game_over = False
                elif event.key == pygame.K_q:
                    running = False

        if moved:
            add_random_tile(grid)
            if score > best_score:
                best_score = score

        screen.fill((187, 173, 160))
        draw_grid(screen, grid, score, best_score, game_over)
        pygame.display.flip()

        if not game_over and not can_move(grid):
            game_over = True
            if score > best_score:
                best_score = score

        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
