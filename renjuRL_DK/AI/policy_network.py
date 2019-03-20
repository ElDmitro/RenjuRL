import numpy as np

import keras

from renjuRL_DK.renju_game.brains.BoardManager import PLAYERS

CHECKPOINT_PATH = '/home/eldmitro/Notebook/RenjuRL/renjuRL_DK/AI/v1'


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



