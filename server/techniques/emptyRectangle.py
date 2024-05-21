from models.board import Board
from models.highlightedRegion import HighlightedRegion
from models.numberedNote import NumberedNote
from models.elimination import Elimination
from models.pointer import Pointer
from models.square import Square
from techniques.models.emptyRectangleConnection import EmptyRectangleConnection
from techniques.models.emptyRectangleModel import EmptyRectangleModel
from techniques.utils.squareLogic import SquareLogic
from techniques.eliminatorBase import EliminatorBase


class EmptyRectangle(EliminatorBase):
    def get_next_solution(self, board: Board) -> Elimination:
        empty_rectangles = self.detect_empty_rectangles(board)
        if (len(empty_rectangles) == 0):
            return None

        for rect in empty_rectangles:
            connection = self.find_strong_connection(rect, board)
            if (connection is None):
                continue

            elimination = self.check_eliminations(rect, connection, board)
            if (elimination is not None):
                return elimination

        return None

    def detect_empty_rectangles(self, board: Board) -> list[EmptyRectangleModel]:
        board_range = board.get_range_zero_indexed()
        notes = board.get_range()
        empty_rectangles = []
        for box in board_range:
            squares_in_box = board.get_empty_squares_in_box(box)
            if (len(squares_in_box) < 2):
                continue

            for note in notes:
                squares = [
                    s for s in squares_in_box if note in s.possible_numbers]
                empty_rectangles += self.get_empty_rectangles(squares, note)

        return empty_rectangles

    def get_empty_rectangles(self, squares: list[Square], number: int) -> list[EmptyRectangleModel]:
        if (len(squares) <= 1 or len(squares) > 5):
            return []
        unique_rows = set([s.row for s in squares])
        unique_columns = set([s.column for s in squares])
        if (len(unique_rows) == 1 or len(unique_columns) == 1):
            return []
        rectangles = []
        for row in unique_rows:
            for column in unique_columns:
                squares_in_row_or_column = [
                    s for s in squares if s.row == row or s.column == column]
                if (len(squares_in_row_or_column) == len(squares)):
                    box = squares[0].box
                    rect = EmptyRectangleModel(
                        row, column, box, number, squares)
                    rectangles.append(rect)
        return rectangles

    def find_strong_connection(self, empty_rectangle: EmptyRectangleModel, board: Board) -> EmptyRectangleConnection:
        row = empty_rectangle.row
        column = empty_rectangle.column
        note = empty_rectangle.number

        squares_in_row = board.get_empty_squares_in_row(row)
        squares_in_column = board.get_empty_squares_in_column(column)

        squares_in_row_with_note = [
            s for s in squares_in_row if note in s.possible_numbers and s not in empty_rectangle.squares]
        squares_in_column_with_note = [
            s for s in squares_in_column if note in s.possible_numbers and s not in empty_rectangle.squares]

        for row_square in squares_in_row_with_note:
            column = row_square.column
            squares_in_column = board.get_empty_squares_in_column(column)
            for column_square in squares_in_column:
                is_same_box = row_square.box == column_square.box
                if (is_same_box):
                    continue
                is_strongly_connected = SquareLogic.is_strongly_connected_by_column(
                    squares_in_column, row_square, column_square, note)
                if (is_strongly_connected):
                    return EmptyRectangleConnection(region_type="column", row=row, column=column, number=note, square_main=row_square, square_other=column_square)

        for column_square in squares_in_column_with_note:
            row = column_square.row
            squares_in_row = board.get_empty_squares_in_row(row)
            for row_square in squares_in_row:
                is_same_box = row_square.box == column_square.box
                if (is_same_box):
                    continue
                is_strongly_connected = SquareLogic.is_strongly_connected_by_row(
                    squares_in_row, column_square, row_square, note)
                if (is_strongly_connected):
                    return EmptyRectangleConnection(region_type="row", row=row, column=column, number=note, square_main=column_square, square_other=row_square)

        return None

    def check_eliminations(self,
                           empty_rectangle: EmptyRectangleModel,
                           connection: EmptyRectangleConnection,
                           board: Board) -> Elimination:
        square_other = connection.square_other

        if (connection.region_type == "row"):
            squares_in_region = board.get_empty_squares_in_column(
                square_other.column)
        if (connection.region_type == "column"):
            squares_in_region = board.get_empty_squares_in_row(
                square_other.row)

        rectangle_squares = empty_rectangle.squares
        number = empty_rectangle.number
        for square in squares_in_region:
            if (square == square_other or square == connection.square_main):
                continue
            if (number not in square.possible_numbers):
                continue
            sees_connection = SquareLogic.is_connected(
                square, square_other)
            sees_rectangle = \
                square.row == empty_rectangle.row \
                or square.column == empty_rectangle.column
            sees_both = sees_connection and sees_rectangle
            if (not sees_both):
                continue

            causing_rectangle_notes = [NumberedNote(
                s.row, s.column, number) for s in rectangle_squares]
            causing_connection_notes = [
                NumberedNote(square_other.row, square_other.column, number),
                NumberedNote(connection.square_main.row, connection.square_main.column, number)]
            causing_notes = causing_rectangle_notes + causing_connection_notes
            eliminated_notes = [NumberedNote(
                square.row, square.column, number)]

            highlighted_regions = self.get_highlighted_regions(empty_rectangle)
            pointers = self.get_pointers(rectangle_squares, connection, square)

            return Elimination(
                technique="empty-rectangle",
                causing_notes=causing_notes,
                causing_square=None,
                eliminated_notes=eliminated_notes,
                highlighted_regions=highlighted_regions,
                pointers=pointers
            )

    def get_highlighted_regions(self, rect: EmptyRectangleModel) -> list[HighlightedRegion]:
        return [
            HighlightedRegion("row", rect.row),
            HighlightedRegion("column", rect.column),
        ]

    def get_pointers(
            self,
            squares: list[Square],
            connection: EmptyRectangleConnection,
            eliminated_square: Square) -> list[Pointer]:
        closest_square: Square = SquareLogic.get_closest_square(
            squares, eliminated_square)
        return [
            Pointer(connection.square_main.to_point(),
                    connection.square_other.to_point()),
            Pointer(connection.square_other.to_point(),
                    eliminated_square.to_point()),
            Pointer(closest_square.to_point(), eliminated_square.to_point()),
        ]
