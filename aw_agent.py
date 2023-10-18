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

class MoveWeightAgent:

    def calc_best_turn(self, game_state):
        legal_moves = game_state.get_all_legal_moves()
        print(f"legal: {legal_moves}")
        if len(legal_moves) == 0:
            return GameState.END_TURN
        
        moves = game_state.get_binned_plausible_moves()

        base_heur = heuristic(game_state)
        
        scored_bins = []
        end_bins = {}
        # calculate heuristic improvement for each plausible move and sort
        for bin in moves:
            scored_moves = []
            for move in bin:
                new_state = game_state.clone()
                new_state.move(move)
                score = heuristic(new_state) - base_heur
                scored_moves.append([move,score,0]) #0 for base harm that it does to other bins

                #populate end_bins
                (endR,endC) = (move[2],move[3])
                if (endR,endC) not in end_bins:
                    end_bins[(endR,endC)] = []
                end_bins[(endR,endC)].append(move)


            scored_moves = sorted(scored_moves, key=lambda x: x[1], reverse=True)
            scored_bins.append(scored_moves)


        print(f"scored_bins: {scored_bins}")

        # for each bin, calculate the move that has the highest improvement relative to cuts it makes in other bins highest score
        # stochastically update random bins, focus on top bins later in search
        # define exclusive relationship, necessary relationship, and possible relationship (backtracking)
        
        iters = 100

        for i in range(iters):
            bin = random.choice(scored_bins)
            ind = random.randint(0,len(bin)-1)
            move = bin[ind]
            moveRCs = move[0]

            # pentalty = highest drop in top due to end, - highest rise due to possible
            highest_drop = 0
            highest_rise = 0
            for bin_i in scored_bins:

                if bin_i is not bin:
                    top_move = bin_i[0]
                    if top_move[0][2] == moveRCs[2] and top_move[0][3] == moveRCs[3]:
                        next_move = bin_i[1]
                        for move_i in bin_i:
                            if move_i in legal_moves:
                                next_move = move_i
                                break
                        drop = top_move[1] - next_move[1]
                        if drop > highest_drop:
                            highest_drop = drop

                    # if move allows for top bin move to be played
                    if top_move[0][2] == moveRCs[0] and top_move[0][3] == moveRCs[1] and (moveRCs[0],moveRCs[1]) != (moveRCs[2],moveRCs[3]):
                        next_move = bin_i[1]
                        for move_i in bin_i:
                            if move_i in legal_moves:
                                next_move = move_i
                                break
                        rise = top_move[1] - next_move[1]
                        if rise > highest_rise:
                            highest_rise = drop
            move[2] = (highest_rise - highest_drop)*.75

            # rerank move
            if ind != 0:
                next_up = bin[ind-1]
                if move[1]+move[2] > next_up[1]+next_up[2]:
                    bin[ind-1] = move
                    bin[ind] = next_move

        # if the top move for any bin is now legal, take it
        best_difference = -1
        best_move = -1

        for bin in scored_bins:
            top_move = bin[0]
            top_moveRCs = top_move[0]
            if top_moveRCs in legal_moves:
                next_move = bin[len(bin)-1]
                for move_i in bin:
                    if move_i in legal_moves:
                        next_move = move_i
                        break
                diff = (top_move[1]+top_move[2])-(next_move[1]+next_move[2])
                if diff > best_difference:
                    best_difference = diff
                    best_move = top_moveRCs

        if best_move != -1:
            return best_move

        #otherwise, start backtracking

        #for now, pick random bin and get first legal
        bin = random.choice(scored_bins)
        for move in bin:
            if move in legal_moves:
                return move
            
        return "this shouldn't be possible"
    
    def get_next_move(self, game_state):
        return self.calc_best_turn(game_state)
    


#things to do
#play moves that are obviously good first
#assign values to possible moves that aren't legal yet

1
