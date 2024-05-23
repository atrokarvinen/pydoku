from models.square import Square
from techniques.models.connectionType import ConnectionType
from techniques.models.cycle import Cycle
from techniques.models.cyclePart import CyclePart
from techniques.models.regionType import RegionType
from techniques.utils.squareConnectionLookup import SquareConnectionLookup
from techniques.utils.squareLookup import SquareLookup


class CycleFinder:
    def __init__(self,
                 square_lookup: SquareLookup,
                 connection_lookup: SquareConnectionLookup) -> None:
        self.iterations = 0
        self.square_lookup = square_lookup
        self.connection_lookup = connection_lookup

    def find_cycles(self, number: int) -> list[Cycle]:
        self.iterations = 0
        cycles = []
        squares = self.square_lookup.get_squares_by_number(number)
        for square in squares:
            visited = []
            cycle = Cycle()
            self.find_cycle(cycles, cycle, square, square,
                            squares, visited, number)

        print("found cycles: ", len(cycles))
        print("iterations: ", self.iterations)
        nice_cycles = [c for c in cycles if c.is_nice()]
        print("nice cycles: ", len(nice_cycles))
        return cycles

    def find_cycle(
            self,
            cycles: list[list[CyclePart]],
            cycle: Cycle,
            start_square: Square,
            square: Square,
            squares: list[Square],
            visited: list[Square],
            number: int):
        self.iterations += 1
        if not cycle.is_valid:
            return
        if cycle.is_complete():
            cycles.append(cycle)
            return
        visited.append(square)
        previous_part = cycle.last
        connections = self.get_connections(
            start_square, square, previous_part, squares, visited, number)
        valid_start = self.validate_start(
            cycle, start_square, square, connections)
        if (not valid_start):
            return
        for cycle_part in connections:
            branched_cycle = cycle.copy()
            branched_cycle.append(cycle_part)
            branched_visited = visited.copy()
            next_square = cycle_part.end
            self.find_cycle(
                cycles,
                branched_cycle,
                start_square,
                next_square,
                squares,
                branched_visited,
                number)

    def get_connections(
            self,
            start_square: Square,
            square: Square,
            previous_part: CyclePart,
            squares: list[Square],
            visited: list[Square],
            number: int) -> list[CyclePart]:
        connections = []
        previous_connection_region = previous_part.connection.region if previous_part else RegionType.NONE
        square_links = self.connection_lookup.get_connections(square, number)
        for connection in square_links:
            is_visited = connection.end in visited and connection.end != start_square
            if is_visited:
                continue
            is_different_region = connection.connection.region != previous_connection_region
            if is_different_region:
                connections.append(
                    CyclePart(square, connection.end, connection.connection))

        return connections

    def validate_start(self, cycle: Cycle, start_square: Square, square: Square, connections: list[CyclePart]) -> bool:
        is_start = square == start_square
        if (not is_start):
            return True
        if (len(connections) <= 1):
            return False
        if (len(connections) == 2):
            types_are_same = connections[0].connection.type == connections[1].connection.type
            if (types_are_same):
                both_strong = connections[0].connection.type == ConnectionType.STRONG
                cycle.has_discontinuous_strong_link = both_strong
                both_weak = connections[0].connection.type == ConnectionType.WEAK
                cycle.has_discontinuous_weak_link = both_weak
        return True
