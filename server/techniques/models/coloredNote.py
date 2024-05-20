from techniques.models.loopPart import LoopPart


class ColoredNote:
    def __init__(self,
                 row: int,
                 column: int,
                 box: int,
                 number: int,
                 color: int,
                 link: LoopPart) -> None:
        self.row = row
        self.column = column
        self.box = box
        self.number = number
        self.color = color
        self.link = link

    def is_same_location(self, square) -> bool:
        return self.row == square.row and self.column == square.column

    def is_connected(self, other) -> bool:
        return self.row == other.row \
            or self.column == other.column \
            or self.box == other.box

    def equals(self, other) -> bool:
        return self.row == other.row \
            and self.column == other.column \
            and self.number == other.number \
            and self.color == other.color
