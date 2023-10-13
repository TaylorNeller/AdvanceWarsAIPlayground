from state import GameState
import random
import numpy as np

def heuristic(game_state):
    coeffs = [.01,1]
    gold_values = [0,0]
    for unit in game_state.active_units:
        gold_values[unit.army] += unit.get_value() / unit.get_visible_hp()
    
    return (gold_values[0]-gold_values[1])*coeffs[0]

class RandomAgent:

    def get_next_move(game_state):
        moves = game_state.get_all_legal_moves()
        if len(moves) == 0:
            return GameState.END_TURN
        move = random.choice(moves)
        return move
    

class HumanAgent:

    def __init__(self, gui):
        self.gui = gui
    
    def get_next_move(self, game_state):
        self.gui.set_state(game_state)
        return self.gui.get_chosen_move()
    

class GreedyAgent:

    def __init__(self):
        self.scored_moves = []
        self.turn = 0

    def calc_next_move(self, game_state):
        moves = game_state.get_all_legal_moves()
        if len(moves) == 0:
            return GameState.END_TURN
        
        if (self.turn != game_state.turn):
            self.turn = game_state.turn
            self.scored_moves = []
                
            for move in moves:
                new_state = game_state.clone()
                new_state.move(move)
                score = heuristic(new_state)
                self.scored_moves.append((move,score))
        
            self.scored_moves = sorted(self.scored_moves, key=lambda x: x[1], reverse=True)

        return self.scored_moves[0][0]
    
    def get_next_move(self, game_state):
        move = self.calc_next_move(game_state)
        #remove illegal moves
        self.scored_moves = [elem for elem in self.scored_moves if not (elem[0][0] == move[0] and elem[0][1] == move[1] or elem[0][2] == move[2] and elem[0][3] == move[3])]
        if move == GameState.END_TURN:
            moves = game_state.get_all_legal_moves()
            if len(moves) > 0:
                self.turn = -1
                return self.get_next_move(game_state)
            return move
        return move
