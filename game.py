import copy

melee = ((-1,0),(0,1),(1,0),(0,-1))

class Game:
    def __init__(self, map, turn):
        self.map = map
        self.rows = len(map)
        self.cols = len(map[0])
        self.turn = turn
    
    def get_legal_moves(self):
        moves = []
        for r in range(self.rows):
            for c in range(self.cols):
                unit = self.map[r][c]
                if unit and unit.team == self.turn and not unit.is_exhausted:
                    self.searched = [[-1] * self.cols for _ in range(self.rows)]
                    new_moves = self.search(r, c, r, c, unit.move, unit.attack_squares)
                    moves.extend(new_moves)
        return moves
    
    def search(self, ori_r, ori_c, row, col, dist, atk_squares):
        moves = []
        if self.searched[row][col] < dist:
            # attacks
            if self.searched[row][col] == -1 and self.can_end(ori_r, ori_c, row, col):
                moves.append([ori_r, ori_c, row, col, None, None])
                
                is_there = True
                ob = None
                if not (ori_r == row and ori_c == col):
                    is_there = False
                    ob = copy.deepcopy(self.map[row][col])
                    self.set_unit(row, col, self.map[ori_r][ori_c])
                for i in range(len(atk_squares)):
                    new_r = row + atk_squares[i][0]
                    new_c = col + atk_squares[i][1]
                    if self.is_targetable(row, col, new_r, new_c):
                        moves.append([ori_r, ori_c, row, col, new_r, new_c])
                if not is_there:
                    self.map[row][col] = ob
            
            self.searched[row][col] = dist
            # other moves
            for i in range(len(melee)):
                new_r = row + melee[i][0]
                new_c = col + melee[i][1]
                if self.is_accessable(new_r, new_c, self.map[ori_r][ori_c]) and dist > 0:
                    new_moves = self.search(ori_r, ori_c, new_r, new_c, dist-1, atk_squares)
                    moves.extend(new_moves)
        return moves
    
    def make_move(self, move):
        self.set_unit(move[2], move[3], self.map[move[0]][move[1]])
        if not (move[0] == move[2] and move[1] == move[3]):
            self.map[move[0]][move[1]] = None
        self.map[move[2]][move[3]].is_exhausted = True
        if move[4] is not None:
            self.attack(move[2], move[3], move[4], move[5])

    def can_end(self, fromR, fromC, toR, toC):
        # basically checks if a unit is trying to end on an illegal square
        if fromR == toR and fromC == toC:
            return True
        else:
            unit2 = self.map[toR][toC]
            return unit2 is None

    def set_unit(self, r, c, unit):
        self.map[r][c] = copy.deepcopy(unit)

    def is_accessable(self, row, col, unit):
        # is the square in bounds and can the unit traverse it
        if unit is None:
            return True
        if not (0 <= row < self.rows and 0 <= col < self.cols):
           return False
        if self.map[row][col]:
            return self.map[row][col].team == unit.team
        return True

    def is_targetable(self, attackerR, attackerC, defenderR, defenderC):
        # returns if the first row/col can attack the second row/col
        attackList = self.valid_attacks( attackerR, attackerC)
        for attack in attackList:
            if attack[0] == defenderR and attack[1] == defenderC:
                return True
        return False

    def valid_attacks(self, row, col):
        validList = []
        unit = self.map[row][col]
        for i in range(len(unit.attack_squares)):
            newR = row + unit.attack_squares[i][0]
            newC = col + unit.attack_squares[i][1]
            if newR >= 0 and newR < self.rows and newC >= 0 and newC < self.cols:
                target = self.map[newR][newC]
                if target and unit.team != target.team:
                    validList.append([newR, newC])
        return validList


    def is_game_over(self):
        # Returns True if the game is over in the given state, False otherwise
        pass
    
    def heuristic(self):
        score = 0
        for r in range(self.rows):
            for c in range(self.cols):
                unit = self.map[r][c]
                if unit:
                    score += unit.value * unit.hp / 10 * (1 if unit.team == self.turn else -1)
        return score



    
    def get_map(self):
        return self.map

    def clone(self):
        return Game(copy.deepcopy(self.map))  # create new Game instance with a deep copy of the map





class Unit:
    def __init__(self, id, team, hp, move, value, is_exhausted, attack_squares):
        self.id = id
        self.team = team
        self.hp = hp
        self.move = move
        self.value = value
        self.is_exhausted = is_exhausted
        self.attack_squares = attack_squares


class Infantry(Unit):
    def __init__(self, team=0, hp=10, is_exhausted=False):
        super().__init__(0, team, hp, 3, 1, is_exhausted, [(0, 1), (1, 0), (0, -1), (-1, 0)])


class Mech(Unit):
    def __init__(self, team=0, hp=10, is_exhausted=False):
        super().__init__(1, team, hp, 2, 3, is_exhausted, [(0, 1), (1, 0), (0, -1), (-1, 0)])

class Recon(Unit):
    def __init__(self, team=0, hp=10, is_exhausted=False):
        super().__init__(2, team, hp, 8, 4, is_exhausted, [(0, 1), (1, 0), (0, -1), (-1, 0)])

class Tank(Unit):
    def __init__(self, team=0, hp=10, is_exhausted=False):
        super().__init__(3, team, hp, 6, 7, is_exhausted, [(0, 1), (1, 0), (0, -1), (-1, 0)])


ranged = [(-3, 0), (-2, -1), (-2, 0), (-2, 1), (-1, -2), (-1, -1), (-1, 1), (-1, 2), (0, -3), (0, -2), (0, 2), (0, 3), (1, -2), (1, -1), (1, 1), (1, 2), (2, -1), (2, 0), (2, 1), (3, 0)]

class Artillery(Unit):
    def __init__(self, team=0, hp=10, is_exhausted=False):
        super().__init__(4, team, hp, 5, 6, is_exhausted, ranged)
