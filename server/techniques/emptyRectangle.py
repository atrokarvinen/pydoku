from models.board import Board
from models.numberedNote import NumberedNote
from models.elimination import Elimination
from techniques.models.emptyRectangleConnection import EmptyRectangleConnection
from techniques.models.emptyRectangleModel import EmptyRectangleModel
from techniques.utils.squareLogic import SquareLogic
from techniques.eliminatorBase import EliminatorBase


class EmptyRectangle(EliminatorBase):
    def get_next_solution(self, board: Board) -> Elimination:
        empty_rectangles = self.detect_empty_rectangles(board)
        if (len(empty_rectangles) == 0):
            return None

        for empty_rectangle in empty_rectangles:
            connection = self.find_strong_connection(
                empty_rectangle, board)
            if (connection is None):
                continue

            elimination = self.check_eliminations(
                empty_rectangle, connection, board)
            if (elimination is not None):
                return elimination

        return None

    def detect_empty_rectangles(self, board: Board) -> list[EmptyRectangleModel]:
        board_range = board.get_range_zero_indexed()
        notes = board.get_range()
        empty_rectangles = []
        for box in board_range:
            squares_in_box = board.get_empty_squares_in_box(box)
            if (len(squares_in_box) < 3):
                continue

            for note in notes:
                if (box == 8 and note == 4):
                    pass

                squares_with_note = [
                    s for s in squares_in_box if note in s.possible_numbers]
                if (len(squares_with_note) < 3 or len(squares_with_note) > 5):
                    continue

                notes_by_row = {}
                for square in squares_with_note:
                    if (square.row not in notes_by_row):
                        notes_by_row[square.row] = []
                    notes_by_row[square.row].append(square)

                rows_with_multiple_notes = [
                    r for r in notes_by_row if len(notes_by_row[r]) > 1]

                notes_by_column = {}
                for square in squares_with_note:
                    if (square.column not in notes_by_column):
                        notes_by_column[square.column] = []
                    notes_by_column[square.column].append(square)

                columns_with_multiple_notes = [
                    c for c in notes_by_column if len(notes_by_column[c]) > 1]

                if (len(rows_with_multiple_notes) != 1 or len(columns_with_multiple_notes) != 1):
                    continue

                empty_rectangle = EmptyRectangleModel(
                    rows_with_multiple_notes[0],
                    columns_with_multiple_notes[0],
                    box,
                    note,
                    squares_with_note)

                empty_rectangles.append(empty_rectangle)

        return empty_rectangles

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
            sees_rectangle = any([SquareLogic.is_connected(
                square, s) for s in rectangle_squares])
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

            return Elimination(
                technique="empty-rectangle",
                causing_notes=causing_notes,
                causing_square=None,
                eliminated_notes=eliminated_notes
            )
