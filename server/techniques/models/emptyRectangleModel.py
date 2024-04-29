from models.square import Square


class EmptyRectangleModel:
    def __init__(self, row: int, column: int, box: int, number: int, squares: list[Square]) -> None:
        self.row = row
        self.column = column
        self.box = box
        self.number = number
        self.squares = squares
