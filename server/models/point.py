class Point:
    def __init__(self, row: int, column: int) -> None:
        self.row = row
        self.column = column

    def serialize(self):
        return {
            "row": self.row,
            "column": self.column
        }
