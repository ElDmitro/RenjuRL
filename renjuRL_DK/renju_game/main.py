from renjuRL_DK.renju_game.brains.GameManager import GameManager
from renjuRL_DK.renju_game.console_ui.source import ConsoleInterface


interface = ConsoleInterface()
gm = GameManager('easy', interface)
gm.start_new_game(False)
