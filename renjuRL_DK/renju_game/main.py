from renjuRL_DK.renju_game.brains.GameManager import GameManager
from renjuRL_DK.renju_game.console_ui.source import ConsoleInterface

first = False
if input("Do you want to be the first? [y/n]") == 'y':
    first = True
interface = ConsoleInterface()
gm = GameManager('easy', interface)
gm.start_new_game(first)
