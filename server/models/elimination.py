from models.highlightedRectangle import HighlightedRectangle
from models.highlightedRegion import HighlightedRegion
from models.numberedNote import NumberedNote
from models.numberedSquare import NumberedSquare
from models.board import Board
from models.pointer import Pointer
from models.solutionStep import SolutionStep


class Elimination(SolutionStep):
    def __init__(self,
                 technique: str,
                 causing_square: NumberedSquare,
                 causing_notes: list[NumberedNote],
                 eliminated_notes: list[NumberedNote],
                 highlighted_regions: list[HighlightedRegion] = [],
                 highlighted_rectangles: list[HighlightedRectangle] = [],
                 pointers: list[Pointer] = []) -> None:
        self.type = "elimination"
        self.causing_square = causing_square
        self.causing_notes = causing_notes
        self.technique = technique
        self.eliminated_notes = eliminated_notes
        self.highlighted_regions = highlighted_regions
        self.highlighted_rectangles = highlighted_rectangles
        self.pointers = pointers
        self.solution_index = 0

    def apply(self, board: Board) -> Board:
        for eliminated_note in self.eliminated_notes:
            row = eliminated_note.row
            column = eliminated_note.column
            number = eliminated_note.number

            square = board.get_square(row, column)
            square.remove_possible_number(number)

        return board

    def is_elimination(self) -> bool:
        return True

    def serialize(self):
        return {
            "type": self.type,
            "causingSquare": self.causing_square.serialize() if self.causing_square else None,
            "causingNotes": [note.serialize() for note in self.causing_notes],
            "technique": self.technique,
            "eliminatedNotes": [note.serialize() for note in self.eliminated_notes],
            "highlightedRegions": [region.serialize() for region in self.highlighted_regions],
            "highlightedRectangles": [rectangle.serialize() for rectangle in self.highlighted_rectangles],
            "pointers": [pointer.serialize() for pointer in self.pointers],
            "solutionIndex": self.solution_index
        }
