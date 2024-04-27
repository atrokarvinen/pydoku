from models.square import Square


class SquareLogic:
    def is_connected(square1: Square, square2: Square) -> bool:
        return square1.row == square2.row \
            or square1.column == square2.column \
            or square1.box == square2.box
