from models.square import Square
from techniques.models.connection import Connection
from techniques.models.connectionType import ConnectionType
from techniques.models.cyclePart import CyclePart
from techniques.utils.squareLogic import SquareLogic


class CycleFinder:
    def find_cycles(self, squares: list[Square], number: int) -> list[list[CyclePart]]:
        cycles = []
        for square in squares:
            visited = []
            cycle = []
            self.find_cycle(cycle, square, squares, visited, number)
            cycles.append(cycle)

        return cycles

    def find_cycle(
            self,
            cycle: list[CyclePart],
            square: Square,
            squares: list[Square],
            visited: list[Square],
            number: int) -> list[Square]:
        visited.append(square)
        cycle_part = self.get_next_cycle_part(square, squares, visited, number)
        if cycle_part is None:
            return cycle
        cycle.append(cycle_part)
        next_square = cycle_part.end
        return self.find_cycle(cycle, next_square, squares, visited, number)

    def get_next_cycle_part(
            self,
            square: Square,
            squares: list[Square],
            visited: list[Square],
            number: int) -> CyclePart:
        for s in squares:
            if (s in visited):
                continue
            connection = SquareLogic.get_square_connection(
                squares, square, s, number)
            if connection.type == ConnectionType.NONE:
                continue
            cycle_part = CyclePart(square, s, connection)
            return cycle_part

        return None
