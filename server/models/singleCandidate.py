class SingleCandidate:
    def __init__(self, row: int, column: int, number: int) -> None:
        self.column = column
        self.number = number
        self.row = row

    def serialize(self) -> dict:
        return {
            "row": self.row,
            "column": self.column,
            "number": self.number
        }
