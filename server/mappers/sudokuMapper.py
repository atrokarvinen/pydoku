from models.sudoku import Sudoku
from models.square import Square


class SudokuMapper:
    def map_from_json(self, data) -> Sudoku:
        sudokuJson = data["sudoku"]

        board = []
        for row in sudokuJson:
            squares = []
            for square in row:
                mappedSquare = Square(
                    square["row"], square["column"], square["number"])
                possibleNumbers = [
                    number for number in square["possibleNumbers"]]
                mappedSquare.set_possible_numbers(possibleNumbers)
                squares.append(mappedSquare)
            board.append(squares)

        sudoku = Sudoku()
        sudoku.set_board(board)

        return sudoku
