import pygame
import random
import math

# --- Constants ---
WINDOW_SIZE = (400, 450)
GRID_SIZE = 4
TILE_SIZE = 100
HEADER_HEIGHT = 50
FPS = 60
ANIMATION_SPEED = 0.2  # Vitesse d'animation (0.1 = lent, 0.5 = rapide)

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

# --- Animation Classes ---
class AnimatedTile:
    def __init__(self, value, start_row, start_col, end_row, end_col):
        self.value = value
        self.start_row = start_row
        self.start_col = start_col
        self.end_row = end_row
        self.end_col = end_col
        self.current_row = start_row
        self.current_col = start_col
        self.progress = 0.0
        self.is_new = False
        self.merged = False
    
    def update(self, dt):
        if self.progress < 1.0:
            self.progress = min(1.0, self.progress + ANIMATION_SPEED)
            # Utilisation d'une fonction d'easing pour une animation plus fluide
            eased_progress = self.ease_out_cubic(self.progress)
            self.current_row = self.start_row + (self.end_row - self.start_row) * eased_progress
            self.current_col = self.start_col + (self.end_col - self.start_col) * eased_progress
    
    def ease_out_cubic(self, t):
        return 1 - pow(1 - t, 3)
    
    def is_finished(self):
        return self.progress >= 1.0

class AnimationManager:
    def __init__(self):
        self.animated_tiles = []
        self.is_animating = False
    
    def start_animation(self, old_grid, new_grid, direction):
        self.animated_tiles.clear()
        self.is_animating = True
        
        # Créer une copie pour travailler
        working_grid = [row[:] for row in old_grid]
        
        # Simuler le mouvement pour tracer les trajectoires
        if direction == "left":
            self._trace_horizontal_movement(working_grid, new_grid, False)
        elif direction == "right":
            self._trace_horizontal_movement(working_grid, new_grid, True)
        elif direction == "up":
            self._trace_vertical_movement(working_grid, new_grid, False)
        elif direction == "down":
            self._trace_vertical_movement(working_grid, new_grid, True)
    
    def _trace_horizontal_movement(self, old_grid, new_grid, reverse):
        for i in range(GRID_SIZE):
            if reverse:
                old_row = old_grid[i][::-1]
                new_row = new_grid[i][::-1]
            else:
                old_row = old_grid[i][:]
                new_row = new_grid[i][:]
            
            # Trouver les tuiles non nulles dans l'ancienne rangée
            old_tiles = [(j, old_row[j]) for j in range(GRID_SIZE) if old_row[j] != 0]
            new_tiles = [(j, new_row[j]) for j in range(GRID_SIZE) if new_row[j] != 0]
            
            # Mapper les mouvements
            for old_idx, (old_j, old_value) in enumerate(old_tiles):
                if old_idx < len(new_tiles):
                    new_j, new_value = new_tiles[old_idx]
                    
                    # Calculer les vraies positions
                    if reverse:
                        real_old_j = GRID_SIZE - 1 - old_j
                        real_new_j = GRID_SIZE - 1 - new_j
                    else:
                        real_old_j = old_j
                        real_new_j = new_j
                    
                    if real_old_j != real_new_j:
                        tile = AnimatedTile(old_value, i, real_old_j, i, real_new_j)
                        self.animated_tiles.append(tile)
    
    def _trace_vertical_movement(self, old_grid, new_grid, reverse):
        for j in range(GRID_SIZE):
            if reverse:
                old_col = [old_grid[GRID_SIZE-1-i][j] for i in range(GRID_SIZE)]
                new_col = [new_grid[GRID_SIZE-1-i][j] for i in range(GRID_SIZE)]
            else:
                old_col = [old_grid[i][j] for i in range(GRID_SIZE)]
                new_col = [new_grid[i][j] for i in range(GRID_SIZE)]
            
            # Trouver les tuiles non nulles dans l'ancienne colonne
            old_tiles = [(i, old_col[i]) for i in range(GRID_SIZE) if old_col[i] != 0]
            new_tiles = [(i, new_col[i]) for i in range(GRID_SIZE) if new_col[i] != 0]
            
            # Mapper les mouvements
            for old_idx, (old_i, old_value) in enumerate(old_tiles):
                if old_idx < len(new_tiles):
                    new_i, new_value = new_tiles[old_idx]
                    
                    # Calculer les vraies positions
                    if reverse:
                        real_old_i = GRID_SIZE - 1 - old_i
                        real_new_i = GRID_SIZE - 1 - new_i
                    else:
                        real_old_i = old_i
                        real_new_i = new_i
                    
                    if real_old_i != real_new_i:
                        tile = AnimatedTile(old_value, real_old_i, j, real_new_i, j)
                        self.animated_tiles.append(tile)
    
    def update(self, dt):
        if not self.is_animating:
            return
        
        for tile in self.animated_tiles:
            tile.update(dt)
        
        # Vérifier si toutes les animations sont terminées
        if all(tile.is_finished() for tile in self.animated_tiles):
            self.is_animating = False
            self.animated_tiles.clear()
    
    def draw_animated_tiles(self, screen):
        font = pygame.font.SysFont(None, 48)
        for tile in self.animated_tiles:
            color = COLORS.get(tile.value, (60, 58, 50))
            x = tile.current_col * TILE_SIZE
            y = tile.current_row * TILE_SIZE + HEADER_HEIGHT
            rect = (x, y, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, color, rect)
            
            if tile.value:
                text = font.render(str(tile.value), True, (0, 0, 0))
                text_rect = text.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
                screen.blit(text, text_rect)

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
    animation_manager = AnimationManager()
    return grid, 0, animation_manager

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
    old_grid = [row[:] for row in grid]  # Copie de l'ancienne grille
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
    return moved, score, old_grid, "left"

def move_right(grid, score):
    old_grid = [row[:] for row in grid]  # Copie de l'ancienne grille
    for i in range(GRID_SIZE):
        grid[i].reverse()
    moved, score, _, _ = move_left(grid, score)
    for i in range(GRID_SIZE):
        grid[i].reverse()
    return moved, score, old_grid, "right"

def move_up(grid, score):
    old_grid = [row[:] for row in grid]  # Copie de l'ancienne grille
    grid[:] = transpose(grid)
    moved, score, _, _ = move_left(grid, score)
    grid[:] = transpose(grid)
    return moved, score, old_grid, "up"

def move_down(grid, score):
    old_grid = [row[:] for row in grid]  # Copie de l'ancienne grille
    grid[:] = transpose(grid)
    moved, score, _, _ = move_right(grid, score)
    grid[:] = transpose(grid)
    return moved, score, old_grid, "down"

# --- Drawing Functions ---
def draw_header(screen, score, best_score):
    font = pygame.font.SysFont(None, 36)
    pygame.draw.rect(screen, (150, 140, 130), (0, 0, WINDOW_SIZE[0], HEADER_HEIGHT))
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    best_text = font.render(f"Best: {best_score}", True, (255, 255, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(best_text, (250, 10))

def draw_tiles(screen, grid, animation_manager=None):
    font = pygame.font.SysFont(None, 48)
    
    # Dessiner d'abord le fond de la grille
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            rect = (j * TILE_SIZE, i * TILE_SIZE + HEADER_HEIGHT, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, COLORS[0], rect)
    
    # Si il y a une animation, dessiner les tuiles animées
    if animation_manager and animation_manager.is_animating:
        animation_manager.draw_animated_tiles(screen)
    else:
        # Dessiner les tuiles statiques
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                value = grid[i][j]
                if value != 0:
                    color = COLORS.get(value, (60, 58, 50))
                    rect = (j * TILE_SIZE, i * TILE_SIZE + HEADER_HEIGHT, TILE_SIZE, TILE_SIZE)
                    pygame.draw.rect(screen, color, rect)
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

def draw_grid(screen, grid, score, best_score, animation_manager=None, game_over=False):
    draw_header(screen, score, best_score)
    draw_tiles(screen, grid, animation_manager)
    if game_over:
        draw_game_over(screen)

# --- Main Game Loop ---
def main():
    screen = init_game()
    clock = pygame.time.Clock()
    best_score = 0
    grid, score, animation_manager = start_new_game()
    running = True
    game_over = False
    pending_new_tile = False  # Variable pour se souvenir qu'on doit ajouter une tuile

    while running:
        dt = clock.tick(FPS) / 1000.0  # Delta time en secondes
        moved = False
        old_grid = None
        direction = None
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif not game_over and not animation_manager.is_animating and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    moved, score, old_grid, direction = move_left(grid, score)
                elif event.key == pygame.K_RIGHT:
                    moved, score, old_grid, direction = move_right(grid, score)
                elif event.key == pygame.K_UP:
                    moved, score, old_grid, direction = move_up(grid, score)
                elif event.key == pygame.K_DOWN:
                    moved, score, old_grid, direction = move_down(grid, score)
            elif game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    grid, score, animation_manager = start_new_game()
                    game_over = False
                    pending_new_tile = False
                elif event.key == pygame.K_q:
                    running = False

        # Démarrer l'animation si un mouvement a eu lieu
        if moved and old_grid and direction:
            animation_manager.start_animation(old_grid, grid, direction)
            pending_new_tile = True  # Marquer qu'on doit ajouter une tuile après l'animation

        # Mettre à jour les animations
        animation_manager.update(dt)

        # Ajouter une nouvelle tuile seulement quand l'animation est terminée
        if pending_new_tile and not animation_manager.is_animating:
            add_random_tile(grid)
            pending_new_tile = False
            if score > best_score:
                best_score = score

        screen.fill((187, 173, 160))
        draw_grid(screen, grid, score, best_score, animation_manager, game_over)
        pygame.display.flip()

        if not game_over and not can_move(grid) and not animation_manager.is_animating:
            game_over = True
            if score > best_score:
                best_score = score

    pygame.quit()

if __name__ == "__main__":
    main()
