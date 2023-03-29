from game import *
import math

def getNextGreedy(game):
    legalMoves = game.getLegalMoves()
    bestMoves = []
    bestScore = -9999
    for move in legalMoves:
        if move[4] is not None:
            score = getGreedyScore(game,move)
            if score > bestScore:
                bestMoves = [move]
                bestScore = score
        elif score == bestScore:
            bestMoves.append(move)
    if bestMoves:
        return bestMoves[-1]
    else:
        bestMove = None
        getCenter(game)
        for move in legalMoves:
            score = getDistScore(game,move)
            if score > bestScore:
                bestMove = move
                bestScore = score
    return bestMove

def getGreedyScore(game,move):
    copy = game.clone()
    copy.make_move(move)
    return copy.heuristic()

def getCenter(game):
    Rs = []
    Cs = []
    weights = []
    for r in range(game.rows):
        for c in range(game.cols):
            unit = game.map[r][c]
            if unit != None and unit.team == 1-game.player:
                Rs.append(r)
                Cs.append(c)
                weights.append(unit.hp / 10)
    n = len(weights)
    center = [0,0]
    for i in range(n):
        center[0] += Rs[i]*weights[i]/n
        center[1] += Cs[i]*weights[i]/n
    return center

def getDistScore(game,move):
    center = getCenter(game.turn)
    return -math.sqrt((move[2]-center[0])**2 + (move[3]-center[1])**2)
