from renjuRL_DK.renju_game.brains.BoardManager import BoardManager
from renjuRL_DK.renju_game.console_ui.source import ConsoleInterface


class GameManager:
    __current_bm = None
    __interface = None

    def __init__(self, bot_difficulty='medium', interface='console', **kwargs):
        assert interface in ['console', 'gui'], "Incorrect interface label"
        assert bot_difficulty in ['easy', 'medium', 'professional'], "Incorrect opponent difficulty"

        self.__bot_difficulty = bot_difficulty
        if interface == 'console':
            self.__interface = ConsoleInterface(**kwargs)
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
                x, y = [int(x, 16) for x in command['args']]
                move_code = self.__current_bm.make_move(1, (x, y))
                self.__interface.update_board(self.__current_bm.get_board_status())
                if move_code is None:
                    continue

                pl, x, y, x_v, y_v = move_code
                board = self.__current_bm.get_board_status()
                for i in range(5):
                    board[x + x_v * i, y + y_v * i] = 9
                self.__interface.update_board(board)
                self.__interface.show_message("{} player WIN!".format(pl))
                break


            if command['code'] == 'finish':
                self.__interface.show_message("Are you sure? [y/n]:", end='')
                if input() == 'y':
                    break
                continue

            if command['code'] == 'show':
                self.__interface.update_board(self.__current_bm.get_board_status())
                continue

            self.__interface.show_message("\nIncorrect command")
            continue

    def finish_current_game(self):
        self.__current_bm = None

    def __destroy_gm(self):
        pass
