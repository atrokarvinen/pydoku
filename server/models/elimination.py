import copy
from models.numberedNote import NumberedNote
from models.numberedSquare import NumberedSquare
from models.board import Board
from models.solutionStep import SolutionStep


class Elimination(SolutionStep):
    def __init__(self,
                 technique: str,
                 causing_square: NumberedSquare,
                 causing_notes: list[NumberedNote],
                 eliminated_notes: list[NumberedNote]):
        self.type = "elimination"
        self.causing_square = causing_square
        self.causing_notes = causing_notes
        self.technique = technique
        self.eliminated_notes = eliminated_notes
        self.solution_index = 0

    def apply(self, board: Board) -> Board:
        board_copy = copy.deepcopy(board)
        for eliminated_note in self.eliminated_notes:
            row = eliminated_note.row
            column = eliminated_note.column
            number = eliminated_note.number

            square = board_copy.get_square(row, column)
            square.remove_possible_number(number)

        return board_copy

    def is_elimination(self) -> bool:
        return True

    def serialize(self):
        return {
            "type": self.type,
            "causingSquare": self.causing_square.serialize() if self.causing_square else None,
            "causingNotes": [note.serialize() for note in self.causing_notes],
            "technique": self.technique,
            "eliminatedNotes": [note.serialize() for note in self.eliminated_notes],
            "solutionIndex": self.solution_index
        }
