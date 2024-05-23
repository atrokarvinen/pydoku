from models.square import Square
from techniques.models.cyclePart import CyclePart
from techniques.utils.squareLogic import SquareLogic
from techniques.utils.squareLookup import SquareLookup


class SquareConnectionLookup:
    def __init__(self, square_lookup: SquareLookup) -> None:
        self.square_lookup = square_lookup
        self.connections_by_square = {}
        self.initialize()

    def initialize(self):
        notes = self.square_lookup.board.get_range()
        for note in notes:
            squares: list[Square] = self.square_lookup.lookups_by_number[note]["squares"]
            for i in range(len(squares)):
                s1 = squares[i]
                key = (s1.row, s1.column, note)
                self.connections_by_square[key] = []
                for j in range(len(squares)):
                    if i == j:
                        continue
                    s2 = squares[j]
                    connections = SquareLogic.get_square_connections(
                        squares, s1, s2, note)
                    cycle_parts = [CyclePart(s1, s2, c) for c in connections]
                    self.connections_by_square[key].extend(cycle_parts)

    def get_connections(self, square: Square, number: int) -> list[CyclePart]:
        key = (square.row, square.column, number)
        return self.connections_by_square[key]

    def get_connections_endpoints(self, square: Square, number: int) -> list[Square]:
        connections = self.get_connections(square, number)
        endpoints = [c.end for c in connections]
        unique_endpoints = SquareLogic.get_unique_squares(endpoints)
        return unique_endpoints
