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
        connection: Connection = SquareLogic.get_square_connection(
            all_squares, square1, square2, number)
        return connection.type == ConnectionType.STRONG

    @staticmethod
    def get_square_connection(
            all_squares: list[Square],
            square1: Square,
            square2: Square,
            number: int) -> Connection:
        if square1 == square2:
            return Connection.none()
        (connecting_region, region_value) = SquareLogic.get_connected_region(
            [square1, square2])
        if connecting_region == RegionType.NONE:
            return Connection.none()

        squares_in_row = [s for s in all_squares if s.row == square1.row]
        is_strong_by_row = SquareLogic.is_strongly_connected_by_row(
            squares_in_row, square1, square2, number)
        if is_strong_by_row:
            return Connection(ConnectionType.STRONG, RegionType.ROW, square1.row)

        squares_in_column = [
            s for s in all_squares if s.column == square1.column]
        is_strong_by_column = SquareLogic.is_strongly_connected_by_column(
            squares_in_column, square1, square2, number)
        if is_strong_by_column:
            return Connection(ConnectionType.STRONG, RegionType.COLUMN, square1.column)

        squares_in_box = [
            s for s in all_squares if s.box == square1.box]
        is_strong_by_box = SquareLogic.is_strongly_connected_by_box(
            squares_in_box, square1, square2, number)
        if is_strong_by_box:
            return Connection(ConnectionType.STRONG, RegionType.BOX, square1.box)

        return Connection(ConnectionType.WEAK, connecting_region, region_value)

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
        if (len(others) == 0):
            return ConnectionType.STRONG
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
    def get_connected_region(squares: list[Square]):
        if SquareLogic.squares_have_same_row(squares):
            return (RegionType.ROW, squares[0].row)
        if SquareLogic.squares_have_same_column(squares):
            return (RegionType.COLUMN, squares[0].column)
        if SquareLogic.squares_have_same_box(squares):
            return (RegionType.BOX, squares[0].box)
        return (RegionType.NONE, 0)

    @staticmethod
    def get_highlighted_region(squares: list[Square]) -> HighlightedRegion:
        region_type = SquareLogic.get_connected_region(squares)
        if region_type == RegionType.ROW:
            return HighlightedRegion("row", squares[0].row)
        elif region_type == RegionType.COLUMN:
            return HighlightedRegion("column", squares[0].column)
        elif region_type == RegionType.BOX:
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
