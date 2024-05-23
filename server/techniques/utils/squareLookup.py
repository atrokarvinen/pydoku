from models.board import Board


class SquareLookup:
    def __init__(self, board: Board) -> None:
        self.board = board
        self.lookups_by_number = {}
        self.is_initialized = False
        self.initialize()

    def initialize(self):
        if self.is_initialized:
            return
        empty_squares = self.board.flatten_empty()
        notes = self.board.get_range()
        for note in notes:
            lookup = {}
            lookup["row"] = {}
            lookup["column"] = {}
            lookup["box"] = {}
            lookup["squares"] = []
            self.lookups_by_number[note] = lookup
            for square in empty_squares:
                if (note not in square.possible_numbers):
                    continue
                row = square.row
                column = square.column
                box = square.box
                if (lookup.get("row").get(row) is None):
                    lookup["row"][row] = []
                lookup["row"][row].append(square)
                if (lookup.get("column").get(column) is None):
                    lookup["column"][column] = []
                lookup["column"][column].append(square)
                if (lookup.get("box").get(box) is None):
                    lookup["box"][box] = []
                lookup["box"][box].append(square)
                lookup["squares"].append(square)

        self.is_initialized = True

    def get_squares_by_number(self, number: int) -> list:
        return self.lookups_by_number[number]["squares"]

    def get_squares_by_row(self, number: int, row: int) -> list:
        return self.lookups_by_number[number]["row"][row]

    def get_squares_by_column(self, number: int, column: int) -> list:
        return self.lookups_by_number[number]["column"][column]

    def get_squares_by_box(self, number: int, box: int) -> list:
        return self.lookups_by_number[number]["box"][box]
