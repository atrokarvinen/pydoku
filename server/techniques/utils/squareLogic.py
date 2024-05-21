from models.highlightedRegion import HighlightedRegion
from models.square import Square
from techniques.models.emptyRectangleModel import EmptyRectangleModel


class SquareLogic:
    def is_connected(square1: Square, square2: Square) -> bool:
        return square1.row == square2.row \
            or square1.column == square2.column \
            or square1.box == square2.box

    def is_strongly_connected(
            all_squares: list[Square],
            square1: Square,
            square2: Square,
            number: int):
        if square1 == square2:
            return False
        if not SquareLogic.is_connected(square1, square2):
            return False

        squares_in_row = [s for s in all_squares if s.row == square1.row]
        is_connected_by_row = SquareLogic.is_strongly_connected_by_row(
            squares_in_row, square1, square2, number)
        if is_connected_by_row:
            return True

        squares_in_column = [
            s for s in all_squares if s.column == square1.column]
        is_connected_by_column = SquareLogic.is_strongly_connected_by_column(
            squares_in_column, square1, square2, number)
        if is_connected_by_column:
            return True

        squares_in_box = [
            s for s in all_squares if s.box == square1.box]
        is_connected_by_box = SquareLogic.is_strongly_connected_by_box(
            squares_in_box, square1, square2, number)
        if is_connected_by_box:
            return True

        return False

    def is_strongly_connected_by_row(squares_in_row: list[Square], square1: Square, square2: Square, number: int):
        other_squares_in_same_row = [
            s for s in squares_in_row if
            not s.is_same_location(square1)
            and not s.is_same_location(square2)]
        if (len(other_squares_in_same_row) == 0):
            return True
        notes_in_others = [
            note for s in other_squares_in_same_row for note in s.possible_numbers]
        if number in notes_in_others:
            return False
        return True

    def is_strongly_connected_by_column(squares_in_column: list[Square], square1: Square, square2: Square, number: int):
        other_squares_in_same_column = [
            s for s in squares_in_column if
            not s.is_same_location(square1)
            and not s.is_same_location(square2)]
        if len(other_squares_in_same_column) == 0:
            return True
        notes_in_others = [
            note for s in other_squares_in_same_column for note in s.possible_numbers]
        if number in notes_in_others:
            return False
        return True

    def is_strongly_connected_by_box(squares_in_box: list[Square], square1: Square, square2: Square, number: int):
        other_squares_in_same_box = [
            s for s in squares_in_box if
            not s.is_same_location(square1)
            and not s.is_same_location(square2)]
        if len(other_squares_in_same_box) == 0:
            return True
        notes_in_others = [
            note for s in other_squares_in_same_box for note in s.possible_numbers]
        if number in notes_in_others:
            return False
        return True

    def count_notes_in_region(region: list[Square]) -> dict[int, int]:
        notes_by_count = {}
        for square in region:
            for note in square.possible_numbers:
                if note not in notes_by_count:
                    notes_by_count[note] = 0
                notes_by_count[note] += 1
        return notes_by_count

    def get_unique_notes(squares: list[Square]) -> set[int]:
        unique_notes = set()
        for square in squares:
            for note in square.possible_numbers:
                unique_notes.add(note)
        return unique_notes

    def squares_have_same_row(squares: list[Square]) -> bool:
        rows = set([s.row for s in squares])
        return len(rows) == 1

    def squares_have_same_column(squares: list[Square]) -> bool:
        columns = set([s.column for s in squares])
        return len(columns) == 1

    def squares_have_same_box(squares: list[Square]) -> bool:
        boxes = set([s.box for s in squares])
        return len(boxes) == 1

    def get_connected_region(squares: list[Square]) -> HighlightedRegion:
        if SquareLogic.squares_have_same_row(squares):
            return HighlightedRegion("row", squares[0].row)
        if SquareLogic.squares_have_same_column(squares):
            return HighlightedRegion("column", squares[0].column)
        if SquareLogic.squares_have_same_box(squares):
            return HighlightedRegion("box", squares[0].box)
        return None

    def subtract_squares(squares1: list[Square], squares2: list[Square]) -> list[Square]:
        return [s for s in squares1 if s not in squares2]

    def get_closest_square(squares: list[Square], square: Square) -> Square:
        closest_square = None
        closest_distance = 1000
        for s in squares:
            distance = abs(s.row - square.row) + abs(s.column - square.column)
            if distance < closest_distance:
                closest_square = s
                closest_distance = distance
        return closest_square
