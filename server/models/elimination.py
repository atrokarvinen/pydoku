from models.eliminationNote import EliminationNote


class Elimination:
    def __init__(self,
                 row: int,
                 column: int,
                 number: int,
                 technique: str,
                 forming_notes: list[EliminationNote],
                 eliminated_notes: list[EliminationNote]):
        self.type = "elimination"
        self.row = row
        self.column = column
        self.number = number
        self.forming_notes = forming_notes
        self.technique = technique
        self.eliminated_notes = eliminated_notes
        self.solution_index = 0

    def serialize(self):
        return {
            "type": self.type,
            "row": self.row,
            "column": self.column,
            "number": self.number,
            "formingNotes": [note.serialize() for note in self.forming_notes],
            "technique": self.technique,
            "eliminatedNotes": [note.serialize() for note in self.eliminated_notes],
            "solutionIndex": self.solution_index
        }
