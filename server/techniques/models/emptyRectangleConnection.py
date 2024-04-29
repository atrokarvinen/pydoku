from models.square import Square


class EmptyRectangleConnection:
    def __init__(self,
                 region_type: str,
                 row: int,
                 column: int,
                 number: int,
                 square_main: Square,
                 square_other: Square) -> None:
        self.region_type = region_type
        self.row = row
        self.column = column
        self.number = number
        self.square_main = square_main
        self.square_other = square_other
