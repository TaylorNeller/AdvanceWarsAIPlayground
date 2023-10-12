import numpy as np
import math
    
class Unit:
    # Define the unit types and armies as class-level constants for memory efficiency and easy referencing
    INFANTRY, MECH, RECON, ARTILLERY, TANK = range(5)
    ORANGE_STAR, BLUE_MOON = range(2)

    UNIT_TYPES = ["Infantry","Mech","Recon","Artillery","Tank"]
    ARMY_NAMES = ["OS","BM"]

    BASE_DAMAGE = {
        INFANTRY: {INFANTRY: 55, MECH: 45, RECON: 12, ARTILLERY: 15, TANK: 5},
        MECH: {INFANTRY: 65, MECH: 55, RECON: 35, ARTILLERY: 70, TANK: 55},
        RECON: {INFANTRY: 70, MECH: 65, RECON: 35, ARTILLERY: 60, TANK: 6},
        ARTILLERY: {INFANTRY: 90, MECH: 85, RECON: 80, ARTILLERY: 70, TANK: 50},
        TANK: {INFANTRY: 75, MECH: 70, RECON: 85, ARTILLERY: 105, TANK: 55}
    }

    MOVE_AMOUNTS = [3, 2, 8, 6, 5]
    MOVE_TYPES = ['inf', 'mech', 'wheel','tread', 'tread']

    
    melee = [[-1, 0], [0, 1], [1, 0], [0, -1]]
    art = []
    for r in range(-3, 4):  # Python's range is exclusive of the upper bound
        for c in range(-3, 4):
            dist = (r**2 + c**2)**0.5  # Python's power operator is **
            if dist > 1 and dist <= 3 and not (abs(r) == 2 and abs(c) == 2):
                art.append([r, c])

    ATTACK_SQUARES = [melee,melee,melee,art,melee]

    def __init__(self, unit_type, army):
        self.unit_type = unit_type
        self.army = army
        self.hp = 100  # Assuming a default of 100. Adjust as needed.
        self.exhausted = False  # Units start as not exhausted
    

    def get_unit_type(self):
        """Returns the string representation of the unit type."""
        return self.unit_type
    
    def get_unit_type_str(self):
        return Unit.UNIT_TYPES[self.get_unit_type()]

    def get_army(self):
        """Returns the string representation of the army."""
        return self.army
    
    def get_army_str(self):
        return Unit.ARMY_NAMES[self.get_army()]
    
    def get_movement_amount(self):
        return Unit.MOVE_AMOUNTS[self.unit_type]
    
    def get_attack_squares(self):
        return Unit.ATTACK_SQUARES[self.unit_type]

    def get_move_type(self):
        return Unit.MOVE_TYPES[self.unit_type]

    def take_damage(self, damage):
        """Reduce the unit's HP by the given damage amount."""
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def heal(self, amount):
        """Increase the unit's HP by the given amount, up to the max."""
        self.hp += amount
        if self.hp > 100:
            self.hp = 100
    
    def get_hp(self):
        return self.hp
    
    def get_visible_hp(self):
        return math.ceil(self.hp / 10)
        
    def is_exhasted(self):
        return self.exhausted

    def mark_exhausted(self):
        """Mark the unit as exhausted."""
        self.exhausted = True

    def reset_exhaustion(self):
        """Reset the unit's exhaustion status for the next turn."""
        self.exhausted = False

    def __repr__(self):
        return f"{self.get_army_str().capitalize()} {self.get_unit_type_str().capitalize()} (HP: {self.hp})"

    def calculate_damage(self, defender, terrain_defense_bonus):
        """
        Calculate the damage this unit would deal to the defender using the provided formula.
        
        Parameters:
        - defender: The defending unit.
        - terrain_defense_bonus: Defense stars of the terrain the defender is on.
        
        Returns:
        - damage: The calculated damage as a percentage.
        """
        # Extract values directly for speed
        B = Unit.BASE_DAMAGE[self.unit_type][defender.unit_type]
        L = np.random.randint(0, 10)  # Using numpy for efficient random generation
        HPA = self.get_visible_hp()
        DV = 100
        DTR = terrain_defense_bonus
        HPD = defender.get_visible_hp()

        # Calculate final damage using the formula
        damage_percentage = (B + L) * HPA / 10 * (200 - (DV + DTR * HPD)) / 100
        
        return damage_percentage


    def can_counterattack(self, attacker):
        """
        Determine if this unit can counterattack the attacker.
        Artillery units cannot counterattack, but others can if they are attacked from an adjacent cell.
        """
        # Artillery units cannot counterattack
        if self.unit_type == Unit.ARTILLERY:
            return False
        
        # For now, other units can always counterattack. Update this based on actual game mechanics.
        return True

    def attack(self, defender, terrain_defense_bonus):
        """
        This unit attacks the defender. If the defender survives and can counterattack,
        it will deal damage back to this unit.

        Parameters:
        - defender: The defending unit.
        - terrain_defense_bonus: Defense stars of the terrain the defender is on.
        """
        # Attacker deals damage to defender
        damage_percentage = self.calculate_damage(defender, terrain_defense_bonus)
        print(damage_percentage)
        defender.take_damage(damage_percentage)

        # If defender survives and can counterattack, it deals damage back to the attacker
        if defender.hp > 0 and defender.can_counterattack(self):
            counter_damage_percentage = defender.calculate_damage(self, terrain_defense_bonus)
            self.take_damage(counter_damage_percentage)

        # Mark attacker as exhausted
        self.exhausted = True

        # Return True if defender is destroyed, otherwise False
        return defender.hp <= 0