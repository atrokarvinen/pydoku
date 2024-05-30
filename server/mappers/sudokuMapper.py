from models.square import Square
from models.board import Board


class SudokuMapper:
    def map_from_json(self, data) -> Board:
        sudokuJson = data["sudoku"]

        board = Board(len(sudokuJson))
        for row in sudokuJson:
            squares = []
            for square in row:
                mappedSquare = Square(
                    square["row"],
                    square["column"],
                    square["box"],
                    square["number"]
                )
                possibleNumbers = [
                    number for number in square["possibleNumbers"]]
                mappedSquare.set_possible_numbers(possibleNumbers)
                squares.append(mappedSquare)
            board.append(squares)

        return board
