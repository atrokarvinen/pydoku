from models.eliminationReason import EliminationReason


class Elimination:
    def __init__(self, row: int, column: int, number: int, caused_by: EliminationReason):
        self.type = "elimination"
        self.row = row
        self.column = column
        self.number = number
        self.caused_by = caused_by
        self.solutionIndex = 0

    def serialize(self):
        return {
            "type": self.type,
            "row": self.row,
            "column": self.column,
            "number": self.number,
            "causedBy": self.caused_by.serialize(),
            "solutionIndex": self.solutionIndex
        }
