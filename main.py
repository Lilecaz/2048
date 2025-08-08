import pygame
import random

def init_game():
    pygame.init()
    screen = pygame.display.set_mode((400, 450))
    pygame.display.set_caption("2048 Celil")
    return screen

def add_random_tile(grid):
    empty = [(i, j) for i in range(4) for j in range(4) if grid[i][j] == 0]
    if empty:
        i, j = random.choice(empty)
        grid[i][j] = 2 if random.random() < 0.9 else 4

def draw_grid(screen, grid, score):
    font = pygame.font.SysFont(None, 48)
    score_font = pygame.font.SysFont(None, 36)

    # Couleurs
    colors = {
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

    pygame.draw.rect(screen, (150, 140, 130), (0, 0, 400, 50))
    score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))


    for i in range(4):
        for j in range(4):
            value = grid[i][j]
            color = colors.get(value, (60, 58, 50))
            pygame.draw.rect(screen, color, (j * 100, i * 100 + 50, 100, 100))
            if value:
                text = font.render(str(value), True, (0, 0, 0))
                rect = text.get_rect(center=(j * 100 + 50, i * 100 + 100))
                screen.blit(text, rect)

def move_left(grid, score):
    moved = False
    for i in range(4):
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
        merged += [0] * (4 - len(merged))
        if merged != grid[i]:
            moved = True
        grid[i] = merged
    return moved, score

def move_right(grid, score):
    for i in range(4):
        grid[i] = grid[i][::-1]
    moved, score = move_left(grid, score)
    for i in range(4):
        grid[i] = grid[i][::-1]
    return moved, score

def transpose(grid):
    return [list(row) for row in zip(*grid)]

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

def can_move(grid):
    for i in range(4):
        for j in range(4):
            if grid[i][j] == 0:
                return True
            if j < 3 and grid[i][j] == grid[i][j+1]:
                return True
            if i < 3 and grid[i][j] == grid[i+1][j]:
                return True
    return False

def main():
    screen = init_game()
    grid = [[0]*4 for _ in range(4)]
    add_random_tile(grid)
    add_random_tile(grid)
    clock = pygame.time.Clock()
    running = True
    score = 0

    while running:
        moved = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    moved, score = move_left(grid, score)
                elif event.key == pygame.K_RIGHT:
                    moved, score = move_right(grid, score)
                elif event.key == pygame.K_UP:
                    moved, score = move_up(grid, score)
                elif event.key == pygame.K_DOWN:
                    moved, score = move_down(grid, score)
        if moved:
            add_random_tile(grid)
        screen.fill((187, 173, 160))
        draw_grid(screen, grid, score)
        pygame.display.flip()
        if not can_move(grid):
            pygame.time.wait(1000)
            running = False
        clock.tick(60)

    print("Game Over! Final Score:", score)
    pygame.quit()

if __name__ == "__main__":
    main()
