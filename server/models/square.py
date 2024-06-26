from models.point import Point


class Square:
    def __init__(
            self,
            row: int,
            column: int,
            box: int = None,
            number: int = 0,
            possible_numbers: list[int] = []) -> None:
        self.row = row
        self.column = column
        self.box = box if box is not None else (row // 3) * 3 + column // 3
        self.number = number
        self.is_initial = number != 0
        self.possible_numbers = possible_numbers

    def is_empty(self) -> bool:
        return self.number == 0 and len(self.possible_numbers) > 0

    def is_same_location(self, square) -> bool:
        return self.row == square.row and self.column == square.column

    def set_number(self, number: int):
        self.number = number
        self.possible_numbers = []

    def set_possible_numbers(self, possible_numbers: list[int]):
        self.possible_numbers = possible_numbers

    def remove_possible_number(self, number: int):
        if (number in self.possible_numbers):
            self.possible_numbers.remove(number)

    def to_point(self):
        return Point(self.row, self.column)

    def serialize(self):
        return {
            "row": self.row,
            "column": self.column,
            "number": self.number,
            "box": self.box,
            "isInitial": self.is_initial,
            "possibleNumbers": self.possible_numbers
        }

    def __repr__(self) -> str:
        return f"Square({self.row}, {self.column})"

    def __eq__(self, value: object) -> bool:
        return isinstance(value, Square) and self.row == value.row and self.column == value.column

    def __lt__(self, value: object) -> bool:
        return self.row < value.row or (self.row == value.row and self.column < value.column)
