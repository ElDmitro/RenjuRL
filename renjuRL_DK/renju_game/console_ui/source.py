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

    @staticmethod
    def show_message(line, end='\n'):
        print(line, end=end)

    @staticmethod
    def get_command():
        ConsoleInterface.show_message("\nYour turn $:", end=' ')
        return ConsoleInterface.__parse_command(input())

    @staticmethod
    def __parse_command(line):
        line = line.split()
        return {'code': line[0], 'args': line[1:]}

    @staticmethod
    def close_thm():
        ConsoleInterface.show_message("Are you sure? [y/n]:", end='')
        if input() == 'y':
            return 1

        return 0

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
            print("    ", end='')
            for j in range(y_shape):
                print(" |", end='')
            print()
            print("{:02d}: ".format(15 - i), end='')

            for el in board[i]:
                print("-{}".format(chr(el)), end='')
            print("-", end='\n')

        print("    ", end='')
        for i in range(y_shape):
            print(" |", end='')
        print()

        print("    ", end='')
        for el in list("abcdefghijklmno"):
            print(" {}".format(el), end='')
        print()



