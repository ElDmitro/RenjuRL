import numpy as np


class BoardManager:
    __B_SHAPE = (15, 15)
    __grid_X, __grid_Y = np.meshgrid(np.arange(__B_SHAPE[0]), np.arange(__B_SHAPE[1]))
    __winning_number_chip_in_row = 5
    __players = [1, -1]
    __winning_players_comb ={__players[0]: np.array([__players[0]] * __winning_number_chip_in_row),
                             __players[1]: np.array([__players[1]] * __winning_number_chip_in_row)}

    def __get_diag_mx(self, a):
        return [np.diagonal(a, i) for i in range(self.__B_SHAPE[1] - 1, -self.__B_SHAPE[0], -1)]

    def __extend2nparray(self, a):
        return [list(arr) + [0] * (self.__B_SHAPE[0] - len(arr)) for arr in a]

    def __init__(self):
        self.__next_player = self.__players[0]
        self.__board = np.zeros(self.__B_SHAPE, dtype=np.int8)

    def make_move(self, player, cell):
        assert self.__next_player == player, "It's not {} player turn".format(player)
        assert player in self.__players, "Incorrect players number"

        self.__board[cell] = player
        return self.__check_combinations()

    def get_board_status(self):
        return self.__board.copy()

    def __rolling_window(self, a, window):
        shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
        strides = a.strides + (a.strides[-1],)
        return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)

    def __check_combination(self, pl, board):
        grid_combs_horizon = self.__rolling_window(board, self.__winning_number_chip_in_row)
        mask = np.all(grid_combs_horizon == self.__winning_players_comb[pl], axis=2)
        return np.where(mask)

    def __check_combinations(self):
        for pl in self.__players:
            X, Y = self.__check_combination(pl, self.__board)
            if len(X) > 0:
                return pl, X[0], Y[0], 0, 1

            X, Y = self.__check_combination(pl, self.__board.T)
            if len(X) > 0:
                return pl, Y[0], X[0], 1, 0

            main_diag_mx = self.__get_diag_mx(self.__board)
            main_diag_mx = np.array(self.__extend2nparray(main_diag_mx))
            X, Y = self.__check_combination(pl, main_diag_mx)
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
            X, Y = self.__check_combination(pl, main_diag_mx)
            if len(X) > 0:
                x = 14 - X[0]
                y = 14 - Y[0]

                if x < 0:
                    y = 14 + x
                    x = Y[0]

                return pl, x, y, 1, -1

            return None
