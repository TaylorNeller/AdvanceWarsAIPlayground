from aw_game import AWGame
from aw_agent import *
from gui import Gui

state = AWGame.map1

gui = Gui(state)
game = AWGame(HumanAgent(gui), GreedyAgent(), state, gui)
game.run()