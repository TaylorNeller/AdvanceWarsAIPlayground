import numpy as np
from unit import Unit

class GameState:
    
    # Define the terrain types as class-level constants
    ROAD, PLAIN, FOREST = range(3)
    
    # Update in the GameState class
    TERRAIN_MAPPING = {
        'road': 0,
        'plain': 1,
        'forest': 2,
        'city': 3,
        'mountain': 4,
        'river': 5
    }
    TERRAIN_MOVE_COSTS = {
        'inf': [1, 1, 1, 1, 2, 2],
        'mech': [1, 1, 1, 1, 1, 1],
        'wheel': [1, 2, 3, 1, float('inf'), float('inf')],
        'tread': [1, 1, 2, 1, float('inf'), float('inf')]
    } 

    TERRAIN_MATRIX = [
        TERRAIN_MOVE_COSTS['inf'],
        TERRAIN_MOVE_COSTS['mech'],
        TERRAIN_MOVE_COSTS['wheel'],
        TERRAIN_MOVE_COSTS['tread'],
        TERRAIN_MOVE_COSTS['tread'],
    ]

    REVERSE_TERRAIN_MAPPING = {value: key for key, value in TERRAIN_MAPPING.items()}

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.searched = None
        
        # Initialize terrain matrix with default terrain (e.g., 'road'). You can adjust this.
        self.terrain_matrix = np.full((rows, cols), self.ROAD, dtype=np.uint8)
        
        # Initialize unit matrix with None, indicating no units.
        self.unit_matrix = np.full((rows, cols), None, dtype=object)
        
        # List to store all active units for efficient iteration
        self.active_units = []

    def add_unit(self, unit, row, col):
        """Adds a unit to the specified location."""
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            raise ValueError(f"Invalid location: ({row}, {col})")
        
        if self.unit_matrix[row][col] is not None:
            raise ValueError(f"Cell ({row}, {col}) is already occupied.")
        
        self.unit_matrix[row][col] = unit
        self.active_units.append(unit)

    def remove_unit(self, row, col):
        """Removes the unit from the specified location."""
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            raise ValueError(f"Invalid location: ({row}, {col})")
        
        unit = self.unit_matrix[row][col]
        if unit is None:
            raise ValueError(f"No unit at location: ({row}, {col})")
        
        self.unit_matrix[row][col] = None
        self.active_units.remove(unit)

    def set_terrain(self, terrain_type, row, col):
        """Sets the terrain type for the specified location."""
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            raise ValueError(f"Invalid location: ({row}, {col})")
        if terrain_type not in self.TERRAIN_MAPPING:
            raise ValueError(f"Invalid terrain type: {terrain_type}")
        
        self.terrain_matrix[row][col] = self.TERRAIN_MAPPING[terrain_type]

    def get_terrain(self, row, col):
        """Returns the terrain type at the specified location."""
        return self.REVERSE_TERRAIN_MAPPING[self.terrain_matrix[row][col]]

    def get_unit(self, row, col):
        """Returns the unit at the specified location, or None if no unit is present."""
        return self.unit_matrix[row][col]

    def can_attack(self, attacker_coords, attacker_new_coords, defender_coords):
        """
        Determine if the attacking unit can attack the defender based on their positions.
        """
        
        attacker = self.get_unit(*attacker_coords)
        defender = self.get_unit(*defender_coords)
        
        # If the attacker or defender does not exist, return False
        if not attacker or not defender:
            return False

        # Check for artillery
        if attacker.unit_type == Unit.ARTILLERY:
            # Artillery shouldn't have moved to attack
            if attacker_coords != attacker_new_coords:
                return False
            # Check if the defender is within the artillery's attack range (2-3 cells away)
            dr = abs(attacker_new_coords[0] - defender_coords[0])
            dc = abs(attacker_new_coords[1] - defender_coords[1])
            if (dr <= 3 and dc <= 3) and (dr >= 2 or dc >= 2):
                return True
            return False

        # Other units (for now) can always attack if adjacent
        dr = abs(attacker_new_coords[0] - defender_coords[0])
        dc = abs(attacker_new_coords[1] - defender_coords[1])
        return dr <= 1 and dc <= 1

    def get_possible_attacks(self, start_row, start_col, end_row, end_col):
        unit = self.get_unit(end_row, end_col)
        if not unit:
            return []
        
        attacks = []
        # Define possible directions for attack
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        for dr, dc in directions:
            new_r, new_c = end_row + dr, end_col + dc

            if 0 <= new_r < self.rows and 0 <= new_c < self.cols:
                target = self.get_unit(new_r, new_c)
                if target and target.army != unit.army and self.can_attack((start_row, start_col), (end_row, end_col), (new_r, new_c)):
                    attacks.append((start_row, start_col, end_row, end_col, new_r, new_c))
                    
        return attacks

    def get_possible_moves(self, row, col):
        unit = self.get_unit(row, col)
        if not unit:
            return []

        visited = set()  # To keep track of visited cells
        moves = []

        # Define possible directions for movement or attack
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        # Use BFS for movement exploration
        queue = [(row, col, unit.get_movement_amount())]

        while queue:
            r, c, remaining_movement = queue.pop(0)

            # If we've moved to this position, update the moves list
            if (r, c) != (row, col):
                moves.append((row, col, r, c, None, None))

            for dr, dc in directions:
                new_r, new_c = r + dr, c + dc

                if (0 <= new_r < self.rows and 0 <= new_c < self.cols) and (new_r, new_c) not in visited:
                    terrain = self.get_terrain(new_r, new_c)
                    move_cost = GameState.TERRAIN_MOVE_COSTS[unit.get_move_type()][GameState.TERRAIN_MAPPING[terrain]]
                    
                    if remaining_movement - move_cost >= 0:
                        target = self.get_unit(new_r, new_c)
                        if not target:
                            queue.append((new_r, new_c, remaining_movement - move_cost))
                        elif target.army != unit.army and self.can_attack((row, col), (r, c), (new_r, new_c)):
                            moves.append((row, col, r, c, new_r, new_c))

            visited.add((r, c))
            # moves.extend(self.get_possible_attacks(row, col, r, c))

        return moves
    
    def can_traverse(self, unit, row, col):
        if GameState.TERRAIN_MATRIX[unit.get_unit_type()][self.terrain_matrix[row][col]] > 20:
            return False
        unit2 = self.unit_matrix[row][col]
        return not (unit2 and unit2.army != unit.army)
    
    def can_end(self, unit, row, col):
        if not self.can_traverse(self, unit, row, col):
            return False
        return not self.unit_matrix[row][col]
    
    def get_all_possible_moves(self):
        moves = []
        for r in range(self.rows):
            for c in range(self.cols):
                unit = self.get_unit(r, c)
                if unit and not unit.is_exhausted:
                    self.searched = np.full((self.rows, self.cols), -1)
                    new_moves = self.move_search(r, c, r, c, unit.get_movement_amount())
                    moves.extend(new_moves)
        return moves
    
    def get_legal_moves(self, row, col):
        self.searched = np.full((self.rows, self.cols), -1)
        return self.move_search(row, col, row, col, self.unit_matrix[row][col].get_movement_amount())
    
    def can_end(self, unit, row, col):
        unit2 = self.unit_matrix[row][col]
        return not unit2 or unit2 == unit

    def move_search(self, oriR, oriC, row, col, dist):
        moves = []
        unit = self.get_unit(oriR,oriC)

        if self.searched[row][col] < dist:
            if self.searched[row][col] == -1 and self.can_end(unit,row,col): # if unit can end on row, col
                moves.append((oriR, oriC, row, col, None, None))
                for dr, dc in unit.get_attack_squares(): #search attacks
                    newR = row + dr
                    newC = col + dc
                    if self.can_attack((oriR,oriC),(row, col,),(newR, newC)):
                        moves.append((oriR, oriC, row, col, newR, newC))
            self.searched[row][col] = dist
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]: # search new moves
                newR = row + dr
                newC = col + dc
                if self.can_traverse(unit, newR, newC) and dist > 0:
                    moves.extend(self.move_search(oriR, oriC, newR, newC, dist-1))
        return moves