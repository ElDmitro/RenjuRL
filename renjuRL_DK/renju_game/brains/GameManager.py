from renjuRL_DK.renju_game.brains.BoardManager import BoardManager
from renjuRL_DK.renju_game.brains.BoardManager import PLAYERS


class GameManager:
    __current_bm = None
    __interface = None

    def __init__(self, bot_difficulty, interface):
        assert bot_difficulty in ['easy', 'medium', 'professional'], "Incorrect opponent difficulty"

        self.__bot_difficulty = bot_difficulty
        self.__interface = interface

    def start_new_game(self, user_first=True):
        if self.__current_bm is not None:
            raise AssertionError(57, "Current game is not finished")

        self.__current_bm = BoardManager()
        self.__interface.update_board(self.__current_bm.get_board_status())

        user_id, opponent_id = PLAYERS[1], PLAYERS[0]
        if user_first:
            user_id, opponent_id = PLAYERS[0], PLAYERS[1]

        while True:
            if self.__make_turn(user_id, self.__interface.get_command):
                break

        self.__destroy_gm()

    def __make_turn(self, uid, get_command):
        command = get_command()

        if command['code'] is None:
            self.__interface.show_message("\nIncorrect command")
            return False

        if command['code'] == 'move':
            if len(command['args']) != 2:
                self.__interface.show_message("Incompatible arguments number")
                return False

            x, y = command['args']
            try:
                move_code = self.__current_bm.make_move(uid, (x, y))
            except Exception as ex:
                self.__interface.show_message(ex.args[1])
                return False

            self.__interface.update_board(self.__current_bm.get_board_status())
            if move_code is None:
                return False

            self.__interface.update_board(self.__get_win_board(move_code))
            self.__interface.show_message("{} player WIN!".format(uid))
            return True

        if command['code'] == 'pass':
            try:
                move_code = self.__current_bm.make_pass(uid)
            except Exception as ex:
                self.__interface.show_message(ex.args[1])
                return False

            if move_code is not None:
                self.__interface.show_message("DRAW!\n")
                return True
            return False

        if command['code'] == 'finish':
            if self.__interface.close_thm():
                return True

            return False

        if command['code'] == 'show':
            self.__interface.update_board(self.__current_bm.get_board_status())
            return False

        self.__interface.show_message("\nIncorrect command")
        return False

    def __get_win_board(self, move_code):
        pl, x, y, x_v, y_v = move_code
        board = self.__current_bm.get_board_status()
        for i in range(5):
            board[x + x_v * i, y + y_v * i] = 9

        return board

    def __destroy_gm(self):
        self.__current_bm = None
