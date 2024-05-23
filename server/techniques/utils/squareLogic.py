from models.highlightedRegion import HighlightedRegion
from models.square import Square
from techniques.models.connection import Connection
from techniques.models.connectionType import ConnectionType
from techniques.models.regionType import RegionType


class SquareLogic:
    @staticmethod
    def is_connected(square1: Square, square2: Square) -> bool:
        return square1.row == square2.row \
            or square1.column == square2.column \
            or square1.box == square2.box

    @staticmethod
    def is_strongly_connected(
            all_squares: list[Square],
            square1: Square,
            square2: Square,
            number: int):
        connections = SquareLogic.get_square_connections(
            all_squares, square1, square2, number)
        any_strong = any(
            [c.type == ConnectionType.STRONG for c in connections])
        return any_strong

    @staticmethod
    def get_square_connections(
            all_squares: list[Square],
            s1: Square,
            s2: Square,
            number: int) -> list[Connection]:
        if s1 == s2:
            return []
        connecting_regions = SquareLogic.get_connected_regions(
            [s1, s2])
        if len(connecting_regions) == 0:
            return []

        connections = []
        if (RegionType.ROW in connecting_regions):
            squares_in_row = [s for s in all_squares if s.row == s1.row]
            is_strong = SquareLogic.is_strongly_connected_by_row(
                squares_in_row, s1, s2, number)
            connection_type = ConnectionType.STRONG if is_strong else ConnectionType.WEAK
            connections.append(Connection(
                connection_type, RegionType.ROW, s1.row))
        elif (RegionType.COLUMN in connecting_regions):
            squares_in_column = [
                s for s in all_squares if s.column == s1.column]
            is_strong = SquareLogic.is_strongly_connected_by_column(
                squares_in_column, s1, s2, number)
            connection_type = ConnectionType.STRONG if is_strong else ConnectionType.WEAK
            connections.append(Connection(
                connection_type, RegionType.COLUMN, s1.column))
        if (RegionType.BOX in connecting_regions):
            squares_in_box = [
                s for s in all_squares if s.box == s1.box]
            is_strong = SquareLogic.is_strongly_connected_by_box(
                squares_in_box, s1, s2, number)
            connection_type = ConnectionType.STRONG if is_strong else ConnectionType.WEAK
            connections.append(Connection(
                connection_type, RegionType.BOX, s1.box))

        return connections

    @staticmethod
    def is_strongly_connected_by_row(squares: list[Square], s1: Square, s2: Square, number: int):
        connection = SquareLogic.get_connection_in_row(
            squares, s1, s2, number)
        return connection.type == ConnectionType.STRONG

    @staticmethod
    def get_connection_in_row(squares: list[Square], s1: Square, s2: Square, number: int):
        connection_type = SquareLogic.get_connection_in_region(
            squares, s1, s2, number, SquareLogic.squares_have_same_row)
        return Connection(connection_type, RegionType.ROW, s1.row)

    def is_strongly_connected_by_column(squares: list[Square], s1: Square, s2: Square, number: int):
        connection = SquareLogic.get_connection_in_column(
            squares, s1, s2, number)
        return connection.type == ConnectionType.STRONG

    @staticmethod
    def get_connection_in_column(squares: list[Square], s1: Square, s2: Square, number: int):
        connection_type = SquareLogic.get_connection_in_region(
            squares, s1, s2, number, SquareLogic.squares_have_same_column)
        return Connection(connection_type, RegionType.COLUMN, s1.column)

    @staticmethod
    def is_strongly_connected_by_box(squares: list[Square], s1: Square, s2: Square, number: int):
        connection = SquareLogic.get_connection_in_box(
            squares, s1, s2, number)
        return connection.type == ConnectionType.STRONG

    @staticmethod
    def get_connection_in_box(squares: list[Square], s1: Square, s2: Square, number: int):
        connection_type = SquareLogic.get_connection_in_region(
            squares, s1, s2, number, SquareLogic.squares_have_same_box)
        return Connection(connection_type, RegionType.BOX, s1.box)

    @staticmethod
    def get_connection_in_region(
            squares: list[Square],
            s1: Square,
            s2: Square,
            number: int,
            is_same_region_func) -> ConnectionType:
        if (not is_same_region_func([s1, s2])):
            return ConnectionType.NONE

        others = SquareLogic.subtract_squares(squares, [s1, s2])
        notes_in_others = [note for s in others for note in s.possible_numbers]
        if number in notes_in_others:
            return ConnectionType.WEAK
        return ConnectionType.STRONG

    @staticmethod
    def count_notes_in_region(region: list[Square]) -> dict[int, int]:
        notes_by_count = {}
        for square in region:
            for note in square.possible_numbers:
                if note not in notes_by_count:
                    notes_by_count[note] = 0
                notes_by_count[note] += 1
        return notes_by_count

    @staticmethod
    def get_unique_notes(squares: list[Square]) -> set[int]:
        unique_notes = set()
        for square in squares:
            for note in square.possible_numbers:
                unique_notes.add(note)
        return unique_notes

    @staticmethod
    def get_unique_squares(squares: list[Square]) -> list[Square]:
        unique_squares = []
        for square in squares:
            if square not in unique_squares:
                unique_squares.append(square)
        return unique_squares

    @staticmethod
    def squares_have_same_row(squares: list[Square]) -> bool:
        rows = set([s.row for s in squares])
        return len(rows) == 1

    @staticmethod
    def squares_have_same_column(squares: list[Square]) -> bool:
        columns = set([s.column for s in squares])
        return len(columns) == 1

    @staticmethod
    def squares_have_same_box(squares: list[Square]) -> bool:
        boxes = set([s.box for s in squares])
        return len(boxes) == 1

    @staticmethod
    def get_connected_regions(squares: list[Square]):
        connections = []
        if SquareLogic.squares_have_same_row(squares):
            connections.append(RegionType.ROW)
        elif SquareLogic.squares_have_same_column(squares):
            connections.append(RegionType.COLUMN)
        if SquareLogic.squares_have_same_box(squares):
            connections.append(RegionType.BOX)
        return connections

    @staticmethod
    def get_highlighted_region(squares: list[Square]) -> HighlightedRegion:
        connected_regions = SquareLogic.get_connected_regions(squares)
        if RegionType.ROW in connected_regions:
            return HighlightedRegion("row", squares[0].row)
        elif RegionType.COLUMN in connected_regions:
            return HighlightedRegion("column", squares[0].column)
        elif RegionType.BOX in connected_regions:
            return HighlightedRegion("box", squares[0].box)
        return None

    @staticmethod
    def subtract_squares(squares1: list[Square], squares2: list[Square]) -> list[Square]:
        return [s for s in squares1 if s not in squares2]

    @staticmethod
    def get_closest_square(squares: list[Square], square: Square) -> Square:
        closest_square = None
        closest_distance = 1000
        for s in squares:
            distance = abs(s.row - square.row) + abs(s.column - square.column)
            if distance < closest_distance:
                closest_square = s
                closest_distance = distance
        return closest_square
