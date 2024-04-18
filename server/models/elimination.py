from models.eliminationReason import EliminationReason


class Elimination:
    def __init__(self, row: int, column: int, number: int, causedBy: EliminationReason):
        self.row = row
        self.column = column
        self.number = number
        self.causedBy = causedBy

    def serialize(self):
        return {
            "row": self.row,
            "column": self.column,
            "number": self.number,
            "causedBy": self.causedBy.serialize()
        }
