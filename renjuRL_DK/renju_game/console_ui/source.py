import numpy as np


class ConsoleInterface:
    __black_chip = '*'
    __white_chip = '#'
    __empty_cell = 'o'
    __win_chip = '@'

    def __init__(self, **kwargs):
        if 'black_chip' in kwargs.keys():
            self.__black_chip = kwargs['black_chip']
        if 'white_chip' in kwargs.keys():
            self.__white_chip = kwargs['white_chip']
        if 'empty_cell' in kwargs.keys():
            self.__empty_cell = kwargs['empty_cell']
        if 'win_chip' in kwargs.keys():
            self.__win_chip = kwargs['win_chip']

        pass

    def __swap2chr(self, board):
        board = board.copy()

        board[board == 1] = ord(self.__black_chip)
        board[board == -1] = ord(self.__white_chip)
        board[board == 0] = ord(self.__empty_cell)
        board[board == 9] = ord(self.__win_chip)

        return board

    def update_board(self, board):
        print(chr(27) + "[2J")

        x_shape, y_shape = board.shape

        board = self.__swap2chr(board)

        for i in range(x_shape):
            print("   ", end='')
            for j in range(y_shape):
                print(" |", end='')
            print()
            print("{:x}: ".format(15 - i), end='')

            for el in board[i]:
                print("-{}".format(chr(el)), end='')
            print("-", end='\n')

        print("   ", end='')
        for i in range(y_shape):
            print(" |", end='')
        print()

        print("   ", end='')
        for el in list("abcdefghijklmno"):
            print(" {}".format(el), end='')
        print()

    def show_message(self, line, end='\n'):
        print(line, end=end)

    def get_command(self):
        return self.__parse_command(input())

    def __parse_command(self, line):
        line = line.split()
        return {'code': line[0], 'args': line[1:]}

    def close_thm(self):
        pass

