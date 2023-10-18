from aw_game import AWGame
from aw_agent import *
from gui import Gui

state = AWGame.map2

gui = Gui(state)
game = AWGame(HumanAgent(gui), MoveWeightAgent(), state, gui)
game.run()