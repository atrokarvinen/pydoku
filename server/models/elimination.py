from models.eliminationReason import EliminationReason


class Elimination:
    def __init__(self, row: int, column: int, number: int, caused_by: EliminationReason):
        self.row = row
        self.column = column
        self.number = number
        self.caused_by = caused_by

    def serialize(self):
        return {
            "row": self.row,
            "column": self.column,
            "number": self.number,
            "causedBy": self.caused_by.serialize()
        }
