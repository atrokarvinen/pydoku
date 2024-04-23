from models.square import Square


class Board:
    def __init__(self, size: int):
        self.rows: list[list[Square]] = []
        self.size = size
        self.box_size = int(size ** 0.5)

    def get_square(self, row: int, column: int):
        return self.rows[row][column]

    def get_squares_in_row(self, row: int) -> list[Square]:
        return self.rows[row]

    def get_squares_in_column(self, column: int) -> list[Square]:
        return [row[column] for row in self.rows]

    def get_empty_squares_in_row(self, row: int) -> list[Square]:
        return [square for square in self.rows[row] if square.is_empty()]

    def get_empty_squares_in_column(self, column: int) -> list[Square]:
        return [row[column] for row in self.rows if row[column].is_empty()]

    def get_box_of_square(self, square: Square):
        return (square.row // self.box_size) * self.box_size + square.column // self.box_size

    def get_squares_in_box(self, square: Square) -> list[Square]:
        box = self.get_box_of_square(square)
        return self.get_squares_in_box_number(box)

    def get_squares_in_box_number(self, box: int) -> list[Square]:
        flat_squares = self.flatten()
        squares = [s for s in flat_squares if self.get_box_of_square(s) == box]
        return squares

    def append(self, row: list[Square]):
        self.rows.append(row)

    def add_initial_possibilities(self):
        for row in self.rows:
            for square in row:
                if square.number == 0:
                    possible_numbers = [*range(1, self.size+1)]
                    square.set_possible_numbers(possible_numbers)

    def flatten(self):
        return [square for row in self.rows for square in row]

    def serialize(self):
        return [[square.serialize() for square in row] for row in self.rows]
