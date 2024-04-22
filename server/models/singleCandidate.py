class SingleCandidate:
    def __init__(self, row: int, column: int, number: int) -> None:
        self.type = "single-candidate"
        self.column = column
        self.number = number
        self.row = row
        self.solutionIndex = 0

    def serialize(self) -> dict:
        return {
            "type": self.type,
            "row": self.row,
            "column": self.column,
            "number": self.number,
            "solutionIndex": self.solutionIndex
        }
