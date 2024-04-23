class NumberedNote:
    def __init__(self, row: int, column: int, number: int):
        self.row = row
        self.column = column
        self.number = number

    def serialize(self):
        return {
            "row": self.row,
            "column": self.column,
            "number": self.number
        }
