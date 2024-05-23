class Point:
    def __init__(self, row: int, column: int) -> None:
        self.row = row
        self.column = column

    def serialize(self):
        return {
            "row": self.row,
            "column": self.column
        }

    def __eq__(self, value: object) -> bool:
        return isinstance(value, Point) \
            and self.row == value.row \
            and self.column == value.column

    def __hash__(self) -> int:
        return hash((self.row, self.column))

    def __repr__(self) -> str:
        return f"Point({self.row}, {self.column})"
