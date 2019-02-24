from .BoardManager import BoardManager
from ..console_ui.source import ConsoleInterface


class InterfaceAbstract:
    def __init__(self, **kwargs):
        pass

    def update_board(self, board):
        pass

    def show_message(self, line, end):
        pass

    def get_command(self):
        pass


class GameManager:
    __current_bm = None
    __interface = None

    def __init__(self, bot_difficulty='medium', interface='console', **kwargs):
        assert interface in ['console', 'gui'], "Incorrect interface label"
        assert bot_difficulty in ['easy', 'medium', 'professional'], "Incorrect opponent difficulty"

        self.__bot_difficulty = bot_difficulty
        if interface == 'console':
            self.__interface = ConsoleInterface(kwargs)
        #else:
        #    self.__interface = GInterface(kwargs)

    def start_new_game(self):
        if self.__current_bm is not None:
            raise Exception("nn_bm", "Current game is not finished")

        self.__current_bm = BoardManager()
        while True:
            self.__interface.show_message("Your turn $:", end=' ')
            command = self.__interface.get_command()

            if command['code'] is None:
                self.__interface.show_message("\nIncorrect command")
                continue

            if command['code'] == 'move':
                x, y = command['args']
                self.__current_bm.make_move(1, x, y)
                self.__interface.update_board(self.__current_bm.get_board_status())

            if command['code'] == 'finish':
                self.__interface.show_message("Are you sure? [y/n]:", end='')
                if input() == 'y':
                    break
                continue

            if command['code'] == 'show':
                self.__interface.update_board(self.__current_bm.get_board_status())

    def finish_current_game(self):
        self.__current_bm = None

    def __destroy_gm(self):
        pass
