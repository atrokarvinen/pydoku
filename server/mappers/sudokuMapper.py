from models.sudoku import Sudoku
from models.square import Square


class SudokuMapper:
    def mapFromJson(self, data) -> Sudoku:
        sudokuJson = data["sudoku"]

        board = []
        for row in sudokuJson:
            squares = []
            for square in row:
                mappedSquare = Square(
                    square["row"], square["column"], square["number"])
                possibleNumbers = [
                    number for number in square["possibleNumbers"]]
                mappedSquare.setPossibleNumbers(possibleNumbers)
                squares.append(mappedSquare)
            board.append(squares)

        sudoku = Sudoku()
        sudoku.setBoard(board)

        return sudoku
