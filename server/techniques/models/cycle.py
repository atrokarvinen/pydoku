from models.pointer import Pointer
from models.square import Square
from techniques.models.connectionType import ConnectionType
from techniques.models.cyclePart import CyclePart


class Cycle:
    def __init__(self) -> None:
        self.parts: list[CyclePart] = []
        self.start: CyclePart = None
        self.last: CyclePart = None
        self.has_discontinuous_weak_link = False
        self.has_discontinuous_strong_link = False
        self.covered_connections = set()
        self.is_valid = True

    def append(self, part: CyclePart):
        self.parts.append(part)

        if (self.start is None):
            self.start = part

        self.check_weak_link(part)
        self.check_strong_link(part)
        self.check_duplicate_connections(part)

        self.last = part

    def check_weak_link(self, part: CyclePart):
        if (self.last is None):
            return
        discontinuous_weak_link = \
            part.connection.type == ConnectionType.WEAK \
            and self.last.connection.type == ConnectionType.WEAK
        if (discontinuous_weak_link):
            if (self.has_discontinuous_weak_link):
                self.is_valid = False
            self.has_discontinuous_weak_link = True

    def check_strong_link(self, part: CyclePart):
        if (self.last is None):
            return
        discontinuous_strong_link = \
            part.connection.type == ConnectionType.STRONG \
            and self.last.connection.type == ConnectionType.STRONG
        if (discontinuous_strong_link):
            if (self.has_discontinuous_strong_link):
                self.is_valid = False
            self.has_discontinuous_strong_link = True

    def check_duplicate_connections(self, part: CyclePart):
        if (part.connection in self.covered_connections):
            self.is_valid = False
        self.covered_connections.add(part.connection)

    def to_square_list(self) -> list[Square]:
        squares = []
        for part in self.parts:
            squares.append(part.start)
        return squares

    def to_pointers(self) -> list[Pointer]:
        pointers = []
        for part in self.parts:
            dashed = part.connection.type == ConnectionType.WEAK
            pointers.append(Pointer(part.start, part.end, dashed=dashed))
        return pointers

    def get_weak_squares(self) -> list[Square]:
        squares = []
        for part in self.parts:
            if part.connection.type == ConnectionType.WEAK:
                if part.start not in squares:
                    squares.append(part.start)
                if part.end not in squares:
                    squares.append(part.end)
        return squares

    def to_list_string(self) -> str:
        square_list = self.to_square_list()
        sorted_list = sorted(square_list)
        list_string = ""
        for square in sorted_list:
            list_string += f"({square.row}, {square.column}) -> "
        list_string += f"({self.last.end.row}, {self.last.end.column})"
        return list_string

    def is_complete(self) -> bool:
        return \
            self.start is not None \
            and self.last is not None \
            and self.start.start == self.last.end \
            and len(self.parts) > 1

    def is_nice(self) -> bool:
        is_even_length = len(self.parts) % 2 == 0
        return \
            self.is_complete() \
            and not self.has_discontinuous_weak_link \
            and not self.has_discontinuous_strong_link \
            and is_even_length \
            and self.is_valid

    def copy(self) -> "Cycle":
        cycle = Cycle()
        cycle.has_discontinuous_strong_link = self.has_discontinuous_strong_link
        cycle.has_discontinuous_weak_link = self.has_discontinuous_weak_link
        for part in self.parts:
            cycle.append(part)
        return cycle

    def __str__(self) -> str:
        cycle_str = ""
        for part in self.parts:
            cycle_str += f"{(part.start.row, part.start.column)} -> "
        cycle_str += f"{(self.last.end.row, self.last.end.column)}"
        return cycle_str
