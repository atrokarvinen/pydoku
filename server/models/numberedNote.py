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

    def __eq__(self, other):
        return self.row == other.row \
            and self.column == other.column \
            and self.number == other.number

    def __repr__(self):
        return f"NumberedNote({self.row}, {self.column}, {self.number})"

    def __lt__(self, other):
        return self.__repr__() < other.__repr__()
