from models.eliminationNote import EliminationNote


class EliminationGroup:
    def __init__(self,
                 row: int,
                 column: int,
                 number: int,
                 technique: str,
                 eliminated_notes: list[EliminationNote]):
        self.type = "elimination"
        self.row = row
        self.column = column
        self.number = number
        self.technique = technique
        self.eliminated_notes = eliminated_notes
        self.solution_index = 0

    def serialize(self):
        return {
            "type": self.type,
            "row": self.row,
            "column": self.column,
            "number": self.number,
            "technique": self.technique,
            "eliminatedNotes": [note.serialize() for note in self.eliminated_notes],
            "solutionIndex": self.solution_index
        }
