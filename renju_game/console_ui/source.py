import numpy as np

class ConsoleInterface(InterfaceAbstract):
    def __init__(self):
        pass

    def update_board(self, board):
        print(chr(27) + "[2J")

        x_shape, y_shape = board.shape
        for i in range(x_shape):
            for j in range(y_shape):
                print(" |", end='')
            print()

            for el in board[i]:
                print("-{}".format(el), end='')
            print("-", end='')

        for j in range(y_shape):
            print(" |", end='')
        print()

    def show_message(self, line, end):
        print(line, end=end)

