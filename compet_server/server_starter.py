import logging
import os
import sys

import numpy as np
import keras
import warnings

warnings.simplefilter("ignore")
X_RANGE = range(15, 0, -1)
X_RANGE = [str(x) for x in X_RANGE]
X_MAPPING = dict(zip(X_RANGE, range(len(X_RANGE))))
#
Y_RANGE = list("abcdefghjklmnop")
Y_MAPPING = dict(zip(Y_RANGE, range(len(Y_RANGE))))

PLAYERS = [1, -1]

movement_encoder_x = dict(zip(range(len(X_RANGE)), X_RANGE))
movement_encoder_y = dict(zip(range(len(Y_RANGE)), Y_RANGE))

CHECKPOINT_PATH = 'model_weights'


class PolicyNN:
    def __init__(self, weights_path=CHECKPOINT_PATH):
        self.__policy_model = keras.models.load_model(weights_path)

    def predict(self, player, board):
        assert player in PLAYERS, "Policy Network: Unknown player id"

        board = PolicyNN.__board2tensorboard(player, board)
        prediction = self.__policy_model.predict(board)

        return PolicyNN.__predict2move_range(prediction)

    @staticmethod
    def __board2tensorboard(player, board):
        new_board = np.zeros((15, 15, 3))

        new_board[:, :, 0][board == PLAYERS[0]] = PLAYERS[0]
        new_board[:, :, 1][board == PLAYERS[1]] = PLAYERS[1]
        new_board[:, :, 2][board != 0] = 0
        new_board[:, :, 2][board == 0] = player

        return np.expand_dims(new_board, 0)

    @staticmethod
    def __idx2coord(idx):
        return idx // 15, idx % 15

    @staticmethod
    def __predict2move_range(move_vect):
        move_vect = np.flip(np.argsort(move_vect))
        x_vect = list(map(lambda x: x // 15, move_vect))
        y_vect = list(map(lambda x: x % 15, move_vect))

        return x_vect, y_vect


class PinkyBrains:
    def __init__(self, uid):
        assert uid in PLAYERS, "AI Brain: User Id is not from list"
        self.__elder_brother = PolicyNN()
        self.__my_uid = uid

    @staticmethod
    def __encode_movement(coord):
        x, y = coord

        if x == 15:
            return {"code": "pass",
                    "args": []}

        return {
            "code": "move",
            "args": [movement_encoder_y[y], movement_encoder_x[x]]
        }

    @staticmethod
    def __is_used_cell(step, board):
        x, y = step

        if (x != 15) and (not board[x, y]):
            return 0

        return 1

    def put2any(self, board):
        prediction_x, prediction_y = self.__elder_brother.predict(self.__my_uid, board)

        i = 0
        while (i < len(prediction_x[0])) and PinkyBrains.__is_used_cell((prediction_x[0][i], prediction_y[0][i]), board):
            i += 1

        if i == len(prediction_x[0]):
            return PinkyBrains.__encode_movement((15, 1))

        return PinkyBrains.__encode_movement((prediction_x[0][i], prediction_y[0][i]))


def move2cord(move):
    if move == '--':
        return 15, 0

    move = (move[0], move[1:])
    x = X_MAPPING[move[1]]
    y = Y_MAPPING[move[0]]

    return x, y


def set_move(move):
    if sys.stdout.closed:
        return False

    sys.stdout.write(move + '\n')
    sys.stdout.flush()

    return True


def main():
    pid = os.getpid()
    LOG_FORMAT = f'{pid}:%(levelname)s:%(asctime)s: %(message)s'

    logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
    logging.debug("Start dummy backend...")

    try:
        my_uid = 0
        opponent_uid = 0
        game_board = np.zeros((15, 15))
        model = None
        while True:
            if not sys.stdin.closed:
                board_list_str = sys.stdin.readline()

                if board_list_str:
                    board_list = board_list_str.split()
                else:
                    board_list = None
            else:
                board_list = None

            if not board_list_str:
                logging.debug("Game is over!")
                return

            if not my_uid:
                my_uid = -1
                opponent_uid = 1
                if board_list == []:
                    my_uid = 1
                    opponent_uid = -1

                model = PinkyBrains(my_uid)

            if board_list != []:
                x, y = move2cord(board_list[-1])
                game_board[x, y] = opponent_uid

            logging.debug('Game: [%s]', board_list_str)
            my_move = model.put2any(game_board)
            my_move = my_move['args']

            my_move = my_move[0] + my_move[1]
            x, y = move2cord(my_move)
            game_board[x, y] = my_uid

            if not set_move(my_move):
                logging.error("Impossible set move!")
                return

            logging.debug('Random move: %s', my_move)

    except:
        logging.error('Error!', exc_info=True, stack_info=True)


if __name__ == "__main__":
    main()
