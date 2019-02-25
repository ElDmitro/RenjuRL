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
        self.__interface.update_board(self.__current_bm.get_board_status())
        while True:
            self.__interface.show_message("\nYour turn $:", end=' ')
            command = self.__interface.get_command()

            if command['code'] is None:
                self.__interface.show_message("\nIncorrect command")
                continue

            if command['code'] == 'move':
                try:
                    x, y = command['args']

                    x = ord(x) - ord('a')
                    y = 15 - int(y, 16)

                    x ^= y
                    y ^= x
                    x ^= y
                except:
                    self.__interface.show_message("Too few arguments")
                    continue

                try:
                    move_code = self.__current_bm.make_move(1, (x, y))
                except Exception as ex:
                    self.__interface.show_message(ex.args[1])
                    continue

                self.__interface.update_board(self.__current_bm.get_board_status())
                if move_code is None:
                    continue

                # REFACTOR TODO
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
                    self.__interface.close_thm()
                    break
                continue

            if command['code'] == 'show':
                self.__interface.update_board(self.__current_bm.get_board_status())
                continue

            if command['code'] == 'pass':
                try:
                    move_code = self.__current_bm.make_pass(1)
                except Exception as ex:
                    self.__interface.show_message(ex.args[1])
                    continue

                if move_code is not None:
                    self.__interface.show_message("DRAW!\n")
                    break
                continue

            self.__interface.show_message("\nIncorrect command")
            continue

    def finish_current_game(self):
        self.__current_bm = None

    def __destroy_gm(self):
        pass
