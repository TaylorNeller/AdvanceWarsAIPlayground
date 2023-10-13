import pygame
from state import GameState
from unit import Unit
import os


class Gui:

    def __init__(self, state):
        self.game_state = state
    
        # Constants
        self.CELL_SIZE = 80
        self.GRID_ROWS = state.rows
        self.GRID_COLS = state.cols
        self.TOP_PADDING = 60
        self.SCREEN_WIDTH = self.GRID_COLS * self.CELL_SIZE
        self.SCREEN_HEIGHT = self.GRID_ROWS * self.CELL_SIZE + self.TOP_PADDING

        # Create game screen
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Advance Wars Sandbox")
        pygame.font.init()

        self.selected_unit_coords = None  # To track if a unit is currently selected
        self.current_move = None
        self.chosen_move = None
        self.possible_moves = []

        self.HP_DISPLAY_SIZE = self.CELL_SIZE // 2.2

        self.END_TURN_BUTTON_RECT = pygame.Rect(self.SCREEN_WIDTH - 150, 10, 140, 40)
    
        # Load sprites
        asset_path = 'assets/'
        def load_scaled_image(path):
            image = pygame.image.load(path)
            return pygame.transform.scale(image, (self.CELL_SIZE, self.CELL_SIZE))

        self.SPRITES = {
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
                    self.SPRITES[key] = pygame.image.load(os.path.join(asset_path, f"{key}.png"))
                    self.SPRITES[key] = pygame.transform.scale(self.SPRITES[key], (self.CELL_SIZE, self.CELL_SIZE))

        # Load HP sprites
        for i in range(1, 10):
            self.SPRITES[f"hp{i}"] = pygame.image.load(os.path.join(asset_path, f"hp{i}.png"))
            self.SPRITES[f"hp{i}"] = pygame.transform.scale(self.SPRITES[f"hp{i}"], (self.CELL_SIZE, self.CELL_SIZE))



    def draw_end_turn_button(self):
        pygame.draw.rect(self.screen, (255, 0, 0), self.END_TURN_BUTTON_RECT)
        font = pygame.font.SysFont('arial', 36)
        text = font.render('End Turn', True, (255, 255, 255))
        self.screen.blit(text, (self.SCREEN_WIDTH - 130, 15))

    def draw_grid(self):
        for row in range(self.GRID_ROWS):
            for col in range(self.GRID_COLS):
                x, y = col * self.CELL_SIZE, row * self.CELL_SIZE + self.TOP_PADDING
                
                # Draw terrain
                terrain_type = self.game_state.get_terrain(row, col)
                self.screen.blit(self.SPRITES['terrain'][terrain_type], (x, y))
                
                # Draw unit
                unit = self.game_state.get_unit(row, col)
                if self.current_move:
                    # If unit moved to this square   
                    if not unit and self.current_move[2] == row and self.current_move[3] == col:
                        unit = self.game_state.get_unit(self.current_move[0], self.current_move[1])
                    # If unit has moved away from this square
                    elif self.current_move[0] == row and self.current_move[1] == col and (self.current_move[2] != row or self.current_move[3] != col):
                        unit = None
                if unit:
                    unit_sprite = self.SPRITES[f"{unit.get_army_str()}{unit.get_unit_type_str()}{2 if unit.is_exhausted() else 1}"]
                    self.screen.blit(unit_sprite, (x, y))

                    if 0 < unit.get_hp() < 91:
                        hp_sprite = pygame.transform.scale(self.SPRITES[f"hp{unit.get_visible_hp()}"], (self.HP_DISPLAY_SIZE, self.HP_DISPLAY_SIZE))
                        self.screen.blit(hp_sprite, (x + self.CELL_SIZE - self.HP_DISPLAY_SIZE, y + self.CELL_SIZE - self.HP_DISPLAY_SIZE))


                # Highlight possible moves
                for move in self.possible_moves:
                    endr, endc = 0,0
                    if (self.current_move):
                        endr, endc = move[4:6]
                    else:
                        endr, endc = move[2:4]
                    if (row, col) == (endr, endc):
                        pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(x, y, self.CELL_SIZE, self.CELL_SIZE), 2)
        self.draw_end_turn_button()

      
    def handle_click(self, x, y):
        col, row = x // self.CELL_SIZE, (y-self.TOP_PADDING) // self.CELL_SIZE

        # Check if the "End Turn" button is clicked
        if self.END_TURN_BUTTON_RECT.collidepoint(x, y):
            self.chosen_move = GameState.END_TURN
            return

        if self.selected_unit_coords:
            # If a unit is selected, check if the clicked cell is a possible move
            for move in self.possible_moves:
                # Check for movement
                if move[2] == row and move[3] == col:
                    # Check for possible actions after the move
                    possible_actions = [m for m in self.possible_moves if m[2] == row and m[3] == col]
                    if len(possible_actions) > 1 and not self.current_move:
                        self.selected_unit_coords = (row, col)  # Keep the unit selected
                        self.possible_moves = possible_actions  # Update possible moves to attacks
                        self.current_move = move
                        return  # Do not deselect the unit yet
                    else:
                        # If no possible attacks, exhaust the unit
                        self.end_move(move)
                        return

                # Check for ranged attack
                elif (move[2],move[3]) == self.selected_unit_coords and move[4] == row and move[5] == col:
                    # Attack the target unit
                    self.end_move(move)
                    return

            # If clicked cell is neither a move nor an attack, or if the unit itself is clicked after moving
            if (row, col) == self.selected_unit_coords or not self.possible_moves:
                unit = self.game_state.get_unit(*self.selected_unit_coords)
                end_move(self.current_move)

        else:
            # If no unit is selected, select the unit in the clicked cell (if present)
            unit = self.game_state.get_unit(row, col)
            if unit and not unit.exhausted and unit.army == self.game_state.current_army:
                self.selected_unit_coords = (row, col)
                self.possible_moves = self.game_state.get_legal_moves(row, col)

    def end_move(self, move):
        # self.game_state.move(move)
        self.current_move = None
        self.selected_unit_coords = None
        self.possible_moves = []
        self.chosen_move = move

    def quit(self):
        pygame.quit()

    def display(self):
        self.screen.fill((255, 255, 255))  # Clear screen
        self.draw_grid()
        pygame.display.flip()

    def get_chosen_move(self):
        running = True
        while running:
            self.display()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.chosen_move = GameState.RESIGN
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    self.handle_click(x, y)
                    if (self.chosen_move is not None):
                        running = False

        move = self.chosen_move
        self.chosen_move = None
        return move
    
    def set_state(self, state):
        self.game_state = state
        self.display()
