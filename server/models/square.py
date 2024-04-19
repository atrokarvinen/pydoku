class Square:
    def __init__(self, row: int, column: int, number: int):
        self.row = row
        self.column = column
        self.number = number
        self.possible_numbers = []

    def get_box(self, box_size: int) -> int:
        return (self.row // box_size) * box_size + self.column // box_size

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
            "possibleNumbers": self.possible_numbers
        }
