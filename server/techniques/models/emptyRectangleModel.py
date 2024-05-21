from models.square import Square


class EmptyRectangleModel:
    def __init__(self, row: int, column: int, box: int, number: int, squares: list[Square]) -> None:
        self.row = row
        self.column = column
        self.box = box
        self.number = number
        self.squares = squares

    def __eq__(self, other) -> bool:
        if not isinstance(other, EmptyRectangleModel):
            return False
        return self.row == other.row \
            and self.column == other.column \
            and self.number == other.number
