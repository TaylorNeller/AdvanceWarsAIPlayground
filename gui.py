import pygame
from state import GameState
from unit import Unit
import os

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
CELL_SIZE = 80
GRID_SIZE = 10

# Load sprites
asset_path = 'assets/'
def load_scaled_image(path):
    image = pygame.image.load(path)
    return pygame.transform.scale(image, (CELL_SIZE, CELL_SIZE))

SPRITES = {
    'terrain': {
        'road': load_scaled_image(asset_path + 'road.png'),
        # Add other terrain sprites here...
    },
    'unit': {
        # Load each combination of army, unit type, and exhaustion state
        (Unit.ORANGE_STAR, Unit.INFANTRY, False): load_scaled_image(asset_path + 'OSInfantry1.png'),
        (Unit.ORANGE_STAR, Unit.INFANTRY, True): load_scaled_image(asset_path + 'OSInfantry2.png'),
        (Unit.BLUE_MOON, Unit.INFANTRY, False): load_scaled_image(asset_path + 'BMInfantry1.png'),
        (Unit.BLUE_MOON, Unit.INFANTRY, True): load_scaled_image(asset_path + 'BMInfantry2.png'),
        # ... Load other unit sprites in a similar way...
    }
}

# SPRITES = {}
for faction in ['OS', 'BM']:
    for unit_type in ['Infantry', 'Mech', 'Recon', 'Artillery', 'Tank']:
        for exhaust in ['1', '2']:
            key = f"{faction}{unit_type}{exhaust}"
            SPRITES[key] = pygame.image.load(os.path.join(asset_path, f"{key}.png"))
            SPRITES[key] = pygame.transform.scale(SPRITES[key], (CELL_SIZE, CELL_SIZE))

# Load HP sprites
HP_SPRITES = {}
for i in range(1, 10):
    HP_SPRITES[i] = pygame.image.load(os.path.join(asset_path, f"hp{i}.png"))
    HP_SPRITES[i] = pygame.transform.scale(HP_SPRITES[i], (CELL_SIZE, CELL_SIZE))



# Create game state
game_state = GameState(GRID_SIZE, GRID_SIZE)
# Add some test units for both Orange Star and Blue Moon
os_infantry = Unit(Unit.INFANTRY, Unit.ORANGE_STAR)
bm_infantry = Unit(Unit.INFANTRY, Unit.BLUE_MOON)

game_state.add_unit(os_infantry, 2, 2)  # Add an Orange Star infantry at (2, 2)
game_state.add_unit(bm_infantry, 5, 5)  # Add a Blue Moon infantry at (5, 5)


# Create game screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Advance Wars Sandbox")

selected_unit_coords = None  # To track if a unit is currently selected
action_check = False
possible_moves = []

HP_DISPLAY_SIZE = CELL_SIZE // 2.2

def draw_grid():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x, y = col * CELL_SIZE, row * CELL_SIZE
            
            # Draw terrain
            terrain_type = game_state.get_terrain(row, col)
            screen.blit(SPRITES['terrain'][terrain_type], (x, y))
            
            # Draw unit
            unit = game_state.get_unit(row, col)
            if unit:
                unit_sprite = SPRITES[f"{unit.get_army_str()}{unit.get_unit_type_str()}{2 if unit.is_exhasted() else 1}"]
                screen.blit(unit_sprite, (x, y))

                if unit.get_hp() < 91:
                    hp_sprite = pygame.transform.scale(HP_SPRITES[unit.get_visible_hp()], (HP_DISPLAY_SIZE, HP_DISPLAY_SIZE))
                    screen.blit(hp_sprite, (x + CELL_SIZE - HP_DISPLAY_SIZE, y + CELL_SIZE - HP_DISPLAY_SIZE))


            # Highlight possible moves
            for move in possible_moves:
                endr, endc = 0,0
                if (action_check):
                    endr, endc = move[4:6]
                else:
                    endr, endc = move[2:4]
                if (row, col) == (endr, endc):
                    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(x, y, CELL_SIZE, CELL_SIZE), 2)

def handle_click(x, y):
    global selected_unit_coords, possible_moves, action_check
    col, row = x // CELL_SIZE, y // CELL_SIZE


    if selected_unit_coords:
        # If a unit is selected, check if the clicked cell is a possible move
        for move in possible_moves:
            # Check for movement
            if move[2] == row and move[3] == col:
                # Move unit in the game state
                unit = game_state.get_unit(*selected_unit_coords)
                game_state.remove_unit(*selected_unit_coords)
                game_state.add_unit(unit, row, col)
                
                # Check for possible actions after the move
                possible_actions = [m for m in possible_moves if m[2] == row and m[3] == col]
                if len(possible_actions) > 1 and action_check is False:
                    selected_unit_coords = (row, col)  # Keep the unit selected
                    possible_moves = possible_actions  # Update possible moves to attacks
                    action_check = True
                    return  # Do not deselect the unit yet
                else:
                    # If no possible attacks, exhaust the unit
                    end_move(unit)
                    return

            # Check for attack
            elif move[4] == row and move[5] == col:
                # Attack the target unit
                attacker = game_state.get_unit(*selected_unit_coords)
                defender = game_state.get_unit(row, col)
                attacker.attack(defender, 0)  # Using 0 as placeholder for terrain defense bonus, adjust as needed
                # If either are destroyed, remove from game state
                if defender.hp <= 0:
                    game_state.remove_unit(row, col)
                if attacker.hp <= 0:
                    game_state.remove_unit(move[0], move[1])
                # Exhaust the attacker
                end_move(attacker)
                return

        # If clicked cell is neither a move nor an attack, or if the unit itself is clicked after moving
        if (row, col) == selected_unit_coords or not possible_moves:
            unit = game_state.get_unit(*selected_unit_coords)
            end_move(unit)

    else:
        # If no unit is selected, select the unit in the clicked cell (if present)
        unit = game_state.get_unit(row, col)
        if unit and not unit.exhausted:
            selected_unit_coords = (row, col)
            possible_moves = game_state.get_legal_moves(row, col)

def end_move(unit):
    global possible_moves, selected_unit_coords, action_check
    if (unit):
        unit.mark_exhausted()
    selected_unit_coords = None
    possible_moves = []
    action_check = False

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            handle_click(x, y)

    screen.fill((255, 255, 255))  # Clear screen
    draw_grid()
    pygame.display.flip()

pygame.quit()
