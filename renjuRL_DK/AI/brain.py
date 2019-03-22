import numpy as np

from renjuRL_DK.renju_game.brains.BoardManager import PLAYERS, X_RANGE, Y_RANGE
from renjuRL_DK.AI.policy_network import PolicyNN

movement_encoder_x = dict(zip(range(len(X_RANGE)), X_RANGE))
movement_encoder_y = dict(zip(range(len(Y_RANGE)), Y_RANGE))


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
