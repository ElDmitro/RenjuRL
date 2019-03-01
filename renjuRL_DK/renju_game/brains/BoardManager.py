import numpy as np

# --GAME CONSTANTS--

# First - black, second - white
PLAYERS = [1, -1]
# Board shape
B_SHAPE = (15, 15)
# Board grid
GRID_X, GRID_Y = np.meshgrid(np.arange(B_SHAPE[0]), np.arange(B_SHAPE[1]))
# Chips in a row to win
WNT_CHIP_IN_ROW = 5
# Winning chip sequence in a board
WIN_PL_COMBS ={PLAYERS[0]: np.array([PLAYERS[0]] * WNT_CHIP_IN_ROW),
               PLAYERS[1]: np.array([PLAYERS[1]] * WNT_CHIP_IN_ROW)}


class BoardManager:

    def __init__(self):
        self.__next_player = PLAYERS[0]
        self.__board = np.zeros(B_SHAPE, dtype=np.int8)
        self.__step = 0
        self.__is_pass = 0

    @staticmethod
    def __get_diag_mx(a):
        return [np.diagonal(a, i) for i in range(B_SHAPE[1] - 1, -B_SHAPE[0], -1)]

    @staticmethod
    def __extend2nparray(a):
        return [list(arr) + [0] * (B_SHAPE[0] - len(arr)) for arr in a]

    @staticmethod
    def __clear_board(board, length, x, y, v_x, v_y):
        for i in range(length):
            board[x + v_x * i, y + v_y * i] = 0

    @staticmethod
    def __rolling_window(a, window):
        shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
        strides = a.strides + (a.strides[-1],)
        return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)

    @staticmethod
    def __get_win_roll_wds(pl, board):
        grid_combs_horizon = BoardManager.__rolling_window(board, WNT_CHIP_IN_ROW)
        mask = np.all(grid_combs_horizon == WIN_PL_COMBS[pl], axis=2)
        return np.where(mask)

    @staticmethod
    def __find_pattern(board, patt):
        grid_combs_horizon = BoardManager.__rolling_window(board, len(patt))
        mask = np.all(grid_combs_horizon == patt, axis=2)
        return np.where(mask)

    def __check_win_combinations(self):
        for pl in PLAYERS:
            X, Y = BoardManager.__get_win_roll_wds(pl, self.__board)
            if len(X) > 0:
                return pl, X[0], Y[0], 0, 1

            X, Y = BoardManager.__get_win_roll_wds(pl, self.__board.T)
            if len(X) > 0:
                return pl, Y[0], X[0], 1, 0

            main_diag_mx = self.__get_diag_mx(self.__board)
            main_diag_mx = np.array(self.__extend2nparray(main_diag_mx))
            X, Y = BoardManager.__get_win_roll_wds(pl, main_diag_mx)
            if len(X) > 0:
                X = 14 - X[0]
                Y = Y[0]

                if X < 0:
                    tmp = -X
                    X = Y
                    Y = tmp

                return pl, X, Y, 1, 1

            main_diag_mx = self.__get_diag_mx(np.fliplr(self.__board))
            main_diag_mx = np.array(self.__extend2nparray(main_diag_mx))
            X, Y = BoardManager.__get_win_roll_wds(pl, main_diag_mx)
            if len(X) > 0:
                x = 14 - X[0]
                y = 14 - Y[0]

                if x < 0:
                    y = 14 + x
                    x = Y[0]

                    y -= Y[0]
                else:
                    x += Y[0]

                return pl, x, y, 1, -1

            return None

    # TODO: after debug need correction
    def __get_next_player(self, x):
        return x

    def get_board_status(self):
        """
        Function return a copy of current board grid

        :return: numpy.array with shape B_SHAPE
                copy of a current board grid
        """
        return self.__board.copy()

    def make_pass(self, player):
        """
        Function making a pass on a next step

        Parameters
        ----------
        :param player: int (value from PLAYER constant)
                    Represent id of making pass player
        :return: None
        """
        if player not in PLAYERS:
            raise Exception(2, "Incorrect players number.\nPlayers list: {}, {}".format(PLAYERS[0], PLAYERS[1]))

        if self.__next_player != player:
            raise Exception(0, "It's not {} player turn".format(player))

        if self.__is_pass:
            return 0, 0, 0, 0, 0

        self.__is_pass = 1
        self.__next_player = self.__get_next_player(self.__next_player)

        return None

    def make_move(self, player, cell):
        """
        Function making a move on a next step

        Parameters
        ----------
        :param player: int (value from PLAYER constant)
                    Represent number of making move player

        :param cell: tuple(int, int)
                Board cell coardinates in a format: (vertical, horizontal)
                Board grows down-right
                Cell coordinates are limited by rectangle with vertices (0, 0) x B_SHAPE

        :return: None or tuple
                Game status (nobody win or return winning combination position)
                None - nobody win
                tuple  - winning combination description

                tuple has format: (player id, x cell coord, y cell coord, vector from top-left chip to the end)
        """
        if player not in PLAYERS:
            raise Exception(2, "Incorrect players number.\nPlayers list: {}, {}".format(PLAYERS[0], PLAYERS[1]))

        if self.__next_player != player:
            raise Exception(0, "It's not {} player turn".format(player))

        if cell[0] < 0 or cell[0] >= B_SHAPE[0]:
            raise Exception(1, "Incorrect move")
        if cell[1] < 0 or cell[1] >= B_SHAPE[1]:
            raise Exception(1, "Incorrect move")

        if self.__board[cell] != 0:
            raise Exception(3, "This cell is used")

        self.__board[cell] = player

        self.__next_player = self.__get_next_player(self.__next_player)
        self.__is_pass = 0

        return self.__check_win_combinations()




