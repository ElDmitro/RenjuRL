import numpy as np


class ConsoleInterface:
    def __init__(self, **kwargs):
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
            print("-", end='\n')

        for i in range(y_shape):
            print(" |", end='')
        print()

    def show_message(self, line, end='\n'):
        print(line, end=end)

    def get_command(self):
        return self.__parse_command(input())

    def __parse_command(self, line):
        line = line.split()
        return {'code': line[0], 'args': line[1:]}

