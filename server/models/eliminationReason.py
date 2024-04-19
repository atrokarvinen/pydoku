class EliminationReason:
    def __init__(self, row: int, column: int, number: int, strategy: str):
        self.row = row
        self.column = column
        self.number = number
        self.strategy = strategy

    def serialize(self):
        return {
            "row": self.row,
            "column": self.column,
            "number": self.number,
            "strategy": self.strategy
        }
