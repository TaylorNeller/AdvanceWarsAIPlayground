from game import *
import math

def get_next_greedy(game):
    legalMoves = game.get_legal_moves()
    bestMoves = []
    bestScore = -9999
    for move in legalMoves:
        if move[4] is not None:
            score = get_greedy_score(game,move)
            if score > bestScore:
                bestMoves = [move]
                bestScore = score
            elif score == bestScore:
                bestMoves.append(move)
    if bestMoves:
        return bestMoves[-1]
    else:
        bestMove = None
        get_center(game)
        for move in legalMoves:
            score = get_dist_score(game,move)
            if score > bestScore:
                bestMove = move
                bestScore = score
    return bestMove

def get_greedy_score(game,move):
    copy = game.clone()
    copy.make_move(move)
    return copy.heuristic()

# center moves towards opponent
def get_center(game):
    Rs = []
    Cs = []
    weights = []
    for r in range(game.rows):
        for c in range(game.cols):
            unit = game.map[r][c]
            if unit != None and unit.team == 1-game.turn:
                Rs.append(r)
                Cs.append(c)
                weights.append(unit.hp / 10)
    n = len(weights)
    center = [0,0]
    for i in range(n):
        center[0] += Rs[i]*weights[i]/n
        center[1] += Cs[i]*weights[i]/n
    return center

def get_dist_score(game,move):
    center = get_center(game)
    return -math.sqrt((move[2]-center[0])**2 + (move[3]-center[1])**2)

def takeGreedyTurn(game):
    move = get_next_greedy(game)
    while (move):
        game.make_move(move)
        move = get_next_greedy(game)
    game.end_turn()


def get_move_order(game,steps):
    state = game.clone()
    orderedMoves = []
    move = get_next_greedy(state)

    # generate initial ordered list of moves (use greedy)
    while move:
        orderedMoves.append(move)
        state.make_move(move)
        move = get_next_greedy(state)
    state.end_turn()

    bestMoveSet = list(orderedMoves)
    bestScore = state.deep_heuristic(1,1,takeGreedyTurn)
    currMoveSet = list(orderedMoves)
    currScore = bestScore
    epsilon = 0.1

    for i in range(steps):
        # step: pop random move + dependents
        orderedMoves = list(currMoveSet)
        popNum = random.randint(0, len(orderedMoves) - 1)
        j = len(orderedMoves) - 1
        while j > popNum:
            if orderedMoves[j][2] == orderedMoves[popNum][0] and orderedMoves[j][3] == orderedMoves[popNum][1] or \
                (orderedMoves[popNum][4] is not None and orderedMoves[j][2] == orderedMoves[popNum][4] and orderedMoves[j][3] == orderedMoves[popNum][5]):
                orderedMoves.pop(j)
            j -= 1
        orderedMoves.pop(popNum)

        state = game.clone()

        for j in range(len(orderedMoves)):
            if orderedMoves[j][4] and state[orderedMoves[j][4]][orderedMoves[j][5]]:
                orderedMoves[j][4] = None
                # orderedMoves[j][5] = None
            state.make_move(orderedMoves[j])

    # for each popped, move to random location
        move = get_next_random(state)
        while move is not None:
            orderedMoves.append(move)
            state.make_move(move)
            move = get_next_random(state)
        state.end_turn()

        # evaluate if it is better, if it is, keep it
        newScore = state.deep_heuristic(1,1,takeGreedyTurn)

        if newScore >= currScore or random.random() < epsilon:
            currMoveSet = list(orderedMoves)
            currScore = newScore
            if newScore >= bestScore:
                bestMoveSet = list(orderedMoves)
                bestScore = newScore

    return bestMoveSet

def get_next_random(game):
    legalMoves = game.get_legal_moves()
    return None if len(legalMoves) == 0 else legalMoves[random.randint(0, len(legalMoves)-1)]




