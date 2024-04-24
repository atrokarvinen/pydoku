class SingleCandidate:
    def __init__(self, row: int, column: int, number: int, alignment: str) -> None:
        self.type = "single-candidate"
        self.column = column
        self.number = number
        self.row = row
        self.alignment = alignment

        self.solutionIndex = 0

    def serialize(self) -> dict:
        return {
            "type": self.type,
            "row": self.row,
            "column": self.column,
            "number": self.number,
            "alignment": self.alignment,
            "solutionIndex": self.solutionIndex
        }
