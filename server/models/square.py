class Square:
    def __init__(self, row: int, column: int, number: int, box: int):
        self.row = row
        self.column = column
        self.number = number
        self.possible_numbers = []
        self.box = box

    def is_empty(self) -> bool:
        return self.number == 0

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

    def serialize(self):
        return {
            "row": self.row,
            "column": self.column,
            "number": self.number,
            "possibleNumbers": self.possible_numbers,
            "box": self.box
        }
