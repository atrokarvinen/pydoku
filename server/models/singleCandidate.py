from models.board import Board
from models.highlightedRegion import HighlightedRegion
from models.solutionStep import SolutionStep


class SingleCandidate(SolutionStep):
    def __init__(self,
                 row: int,
                 column: int,
                 number: int,
                 other_numbers: list[int],
                 highlighted_regions: list[HighlightedRegion],
                 alignment: str) -> None:
        self.type = "single-candidate"
        self.column = column
        self.row = row
        self.number = number
        self.other_numbers = other_numbers
        self.highlightedRegions = highlighted_regions
        self.alignment = alignment

        self.solutionIndex = 0

    def apply(self, board: Board) -> Board:
        row = self.row
        column = self.column
        number = self.number

        square = board.get_square(row, column)
        square.set_number(number)

        return board

    def is_elimination(self) -> bool:
        return False

    def serialize(self) -> dict:
        return {
            "type": self.type,
            "row": self.row,
            "column": self.column,
            "number": self.number,
            "otherNumbers": self.other_numbers,
            "highlightedRegions": [region.serialize() for region in self.highlightedRegions],
            "alignment": self.alignment,
            "solutionIndex": self.solutionIndex
        }
