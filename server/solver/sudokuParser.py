import math
from models.board import Board
from models.square import Square


class SudokuParser:
    @staticmethod
    def parse(sudoku_string: str, size: int = 9) -> Board:
        sudoku_length = len(sudoku_string)
        if (sudoku_length != size * size):
            print("Invalid sudoku length")
            return

        char_array = list(sudoku_string)
        board = Board(size)
        for row in range(size):
            row_squares = []
            for col in range(size):
                square = SudokuParser.create_square(row, col, char_array, size)
                row_squares.append(square)
            board.append(row_squares)

        return board

    @staticmethod
    def create_square(row: int, col: int, char_array: str, size: int) -> Square:
        box_size = math.sqrt(size)
        char = char_array[row * size + col]
        if (char == '.' or char == '0' or char == ' '):
            char_as_number = 0
        else:
            char_as_number = int(char)
        box = math.floor(row/box_size) * box_size + math.floor(col/box_size)
        square = Square(row, col, box, char_as_number)
        return square
