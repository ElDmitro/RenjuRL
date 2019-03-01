import numpy as np

winning_patterns = [
    (4, [1, 1, 1, 1]),
    (3, [1, 1, 1])
]


class BoardManager:
    __step = 0
    __B_SHAPE = (15, 15)
    __grid_X, __grid_Y = np.meshgrid(np.arange(__B_SHAPE[0]), np.arange(__B_SHAPE[1]))
    __winning_number_chip_in_row = 5
    __players = [1, -1]
    __winning_players_comb ={__players[0]: np.array([__players[0]] * __winning_number_chip_in_row),
                             __players[1]: np.array([__players[1]] * __winning_number_chip_in_row)}

    def __get_next_player(self, x):
        return x

    def get_players_list(self):
        return self.__players.copy()

    def __get_diag_mx(self, a):
        return [np.diagonal(a, i) for i in range(self.__B_SHAPE[1] - 1, -self.__B_SHAPE[0], -1)]

    def __extend2nparray(self, a):
        return [list(arr) + [0] * (self.__B_SHAPE[0] - len(arr)) for arr in a]

    def __init__(self):
        self.__next_player = self.__players[0]
        self.__board = np.zeros(self.__B_SHAPE, dtype=np.int8)
        self.__step = 0
        self.__is_pass = 0

    def make_pass(self, player):
        if player not in self.__players:
            raise Exception(2, "Incorrect players number.\nPlayers list: {}, {}".format(self.__players[0], self.__players[1]))

        if self.__next_player != player:
            raise Exception(0, "It's not {} player turn".format(player))

#        if self.__step < 5:
#            raise Exception(0, "You have no chances to pass")

        if self.__is_pass:
            return 0, 0, 0, 0, 0

        self.__is_pass = 1
        self.__next_player = self.__get_next_player(self.__next_player)

        return None

    def make_move(self, player, cell):
        if player not in self.__players:
            raise Exception(2, "Incorrect players number.\nPlayers list: {}, {}".format(self.__players[0], self.__players[1]))

        if self.__next_player != player:
            raise Exception(0, "It's not {} player turn".format(player))

        if cell[0] < 0 or cell[0] >= self.__B_SHAPE[0]:
            raise Exception(1, "Incorrect move")
        if cell[1] < 0 or cell[1] >= self.__B_SHAPE[1]:
            raise Exception(1, "Incorrect move")

        if self.__board[cell] != 0:
            raise Exception(3, "This cell is used")

        self.__check_prefab_tabu(player, cell)

        self.__board[cell] = player
        if self.__check_tabu():
            return -1, 0, 0, 0, 0

        self.__next_player = self.__get_next_player(self.__next_player)
        self.__is_pass = 0
        self.__step += 1
        return self.__check_combinations()

    def get_board_status(self):
        return self.__board.copy()

    def __find_pattern(self, board, patt):
        grid_combs_horizon = self.__rolling_window(board, len(patt))
        mask = np.all(grid_combs_horizon == patt, axis=2)
        return np.where(mask)

    def __clear_board(self, board, len, x, y, v_x, v_y):
        for i in range(len):
            board[x + v_x * i, y + v_y * i] = 0

        return board

    def __check_tabu(self):
        board = self.__board.copy()

        board[board != self.__players[0]] = 0
        board_h = board.copy()
        board_v = board.copy()
        board_d = board.copy()
        board_sd = board.copy()

        fork_count = [0, 0]
        for wp_len, patt in winning_patterns:
            X, Y = self.__find_pattern(board_h, patt)
            if len(X) > 0:
                # TODO: check is this pattern open
                fork_count[abs(3 - wp_len)] += len(X)
                board_h = self.__clear_board(board_h, len(patt), X[0], Y[0], 0, 1)

            X, Y = self.__find_pattern(board_v.T, patt)
            if len(X) > 0:
                # TODO
                fork_count[abs(3 - wp_len)] += len(X)
                board_v = self.__clear_board(board_v, len(patt), X[0], X[0], 1, 0)

            main_diag_mx = self.__get_diag_mx(board_d)
            main_diag_mx = np.array(self.__extend2nparray(main_diag_mx))
            # TODO: from here
            X, Y = self.__find_pattern(main_diag_mx, patt)
            # TODO: Do it for all
            if len(X) > 0:
                if X <= 14:
                    y = 14 - X[0]
                    x = 0

                    y += Y[0]
                    x += Y[0]
                else:
                    x = X[0] - 14
                    y = 0

                    y += Y[0]
                    x += Y[0]

                # TODO
                fork_count[abs(3 - wp_len)] += len(X)
                board_d = self.__clear_board(board_d, len(patt), x, y, 1, 1)

            main_diag_mx = self.__get_diag_mx(np.fliplr(board_sd))
            main_diag_mx = np.array(self.__extend2nparray(main_diag_mx))
            X, Y = self.__find_pattern(main_diag_mx, patt)
            if len(X) > 0:
                # TODO: Correct index process.
                if X[0] <= 14:
                    x = 

                # TODO
                fork_count[abs(3 - wp_len)] += len(X)
                board_sd = self.__clear_board(board_sd, len(patt), x, y, 1, -1)

        return np.any(np.array(fork_count) > 1)

    def __check_prefab_tabu(self, player, cell):
        if self.__step == 0 and cell != (7, 7):
            raise Exception(1, "Go to center!")

#        if self.__step < 3 and (cell[0] < 6 or cell[0] > 8 or cell[1] < 6 or cell[1] > 8):
#            raise Exception(1, 'Go to 3x3 square')

#        if self.__step < 6 and (cell[0] < 4 or cell[0] > 10 or cell[1] < 4 or cell[1] > 10):
#            raise Exception(1, 'Go to 5x5 square')

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

                    y -= Y[0]
                else:
                    x += Y[0]

                return pl, x, y, 1, -1

            return None
