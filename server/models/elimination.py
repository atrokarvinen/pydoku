from models.numberedNote import NumberedNote
from models.numberedSquare import NumberedSquare


class Elimination:
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

    def serialize(self):
        return {
            "type": self.type,
            "causingSquare": self.causing_square.serialize() if self.causing_square else None,
            "causingNotes": [note.serialize() for note in self.causing_notes],
            "technique": self.technique,
            "eliminatedNotes": [note.serialize() for note in self.eliminated_notes],
            "solutionIndex": self.solution_index
        }
