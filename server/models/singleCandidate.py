import copy
from models.board import Board
from models.solutionStep import SolutionStep


class SingleCandidate(SolutionStep):
    def __init__(self, row: int, column: int, number: int, alignment: str) -> None:
        self.type = "single-candidate"
        self.column = column
        self.number = number
        self.row = row
        self.alignment = alignment

        self.solutionIndex = 0

    def apply(self, board: Board) -> Board:
        board_copy = copy.deepcopy(board)

        row = self.row
        column = self.column
        number = self.number

        square = board_copy.get_square(row, column)
        square.set_number(number)

        return board_copy

    def is_elimination(self) -> bool:
        return False

    def serialize(self) -> dict:
        return {
            "type": self.type,
            "row": self.row,
            "column": self.column,
            "number": self.number,
            "alignment": self.alignment,
            "solutionIndex": self.solutionIndex
        }
