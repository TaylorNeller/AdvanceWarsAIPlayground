from state import GameState
from aw_agent import *
from unit import Unit
import time

class AWGame:

    map1 = GameState(5,8)
    map1.add_unit(Unit(Unit.INFANTRY, Unit.ORANGE_STAR), 1, 3)  # Add an Orange Star infantry at (2, 2)
    map1.add_unit(Unit(Unit.MECH, Unit.ORANGE_STAR), 2, 4)  # Add an Orange Star infantry at (2, 2)
    map1.add_unit(Unit(Unit.RECON, Unit.ORANGE_STAR), 2, 3)  # Add an Orange Star infantry at (2, 2)
    map1.add_unit(Unit(Unit.ARTILLERY, Unit.ORANGE_STAR), 2, 7)  # Add an Orange Star infantry at (2, 2)
    map1.add_unit(Unit(Unit.TANK, Unit.ORANGE_STAR), 1, 6)  # Add an Orange Star infantry at (2, 2)

    map1.add_unit(Unit(Unit.INFANTRY, Unit.BLUE_MOON), 0, 5)  # Add a Blue Moon infantry at (5, 5)
    map1.add_unit(Unit(Unit.TANK, Unit.BLUE_MOON), 0, 6)  # Add a Blue Moon infantry at (5, 5)



    def __init__(self, player1, player2, state=map1, gui=None):
        self.players = [player1, player2]
        self.gui = gui
        self.state = state

    def run(self):
        game_over = False
        # turn loop
        while not game_over:
            # get move loop
            curr_army = self.state.current_army
            move = None
            while move != GameState.END_TURN:

                if self.gui:
                    self.gui.set_state(self.state)
                    self.gui.display()

                # print(self.players[curr_army])
                move = self.players[curr_army].get_next_move(self.state.clone())
                if move == GameState.RESIGN:
                    game_over = True
                    break
                print(move)
                self.state.move(move)

                if not isinstance(self.players[curr_army], HumanAgent):
                    time.sleep(.5)
