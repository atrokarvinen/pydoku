from models.board import Board
from models.numberedNote import NumberedNote
from models.elimination import Elimination
from models.square import Square
from techniques.eliminatorBase import EliminatorBase


class XWing(EliminatorBase):
    def get_next_solution(self, board: Board) -> Elimination:
        note_range = board.get_range()
        board_range = board.get_range_zero_indexed()
        rows = [board.get_empty_squares_in_row(i) for i in board_range]
        cols = [board.get_empty_squares_in_column(i) for i in board_range]

        for number in note_range:
            row_elimination = self.find_x_wings(rows, number, board, "row")
            if (row_elimination):
                return row_elimination

            col_elimination = self.find_x_wings(
                cols, number, board, "column")
            if (col_elimination):
                return col_elimination
        return None

    def find_x_wings(self,
                     regions: list[list[Square]],
                     number: int,
                     board: Board,
                     region_type: str):
        for region1 in regions:
            for region2 in regions:
                if (region1 == region2):
                    continue

                region1_squares_with_note = [
                    s for s in region1 if number in s.possible_numbers]
                region2_squares_with_note = [
                    s for s in region2 if number in s.possible_numbers]

                if (len(region1_squares_with_note) != 2 or len(region2_squares_with_note) != 2):
                    continue

                s1 = region1_squares_with_note[0]
                s2 = region1_squares_with_note[1]
                s3 = region2_squares_with_note[0]
                s4 = region2_squares_with_note[1]
                squares = [s1, s2, s3, s4]
                squares_form_rectangle = self.squares_form_rectangle(squares)

                if (not squares_form_rectangle):
                    continue

                return self.to_elimination(board, squares, number, region_type)
        return None

    def squares_form_rectangle(self, squares: list[Square]) -> bool:
        rows_by_count = {}
        cols_by_count = {}
        for s in squares:
            if (s.row not in rows_by_count):
                rows_by_count[s.row] = 0
            rows_by_count[s.row] += 1

            if (s.column not in cols_by_count):
                cols_by_count[s.column] = 0
            cols_by_count[s.column] += 1

        return all([count == 2 for count in rows_by_count.values()]) \
            and all([count == 2 for count in cols_by_count.values()])

    def to_elimination(self,
                       board: Board,
                       squares: list[Square],
                       number: int,
                       region_type: str) -> Elimination:

        row1 = board.get_empty_squares_in_row(squares[0].row)
        row2 = board.get_empty_squares_in_row(squares[1].row)
        col1 = board.get_empty_squares_in_column(squares[0].column)
        col2 = board.get_empty_squares_in_column(squares[1].column)

        other_region1_squares = col1 if region_type == "row" else row1
        other_region2_squares = col2 if region_type == "row" else row2
        squares_under_elimination = other_region1_squares + other_region2_squares

        causing_squares = squares
        eliminated_notes = []
        for square in squares_under_elimination:
            if (square in causing_squares):
                continue
            if (number in square.possible_numbers):
                eliminated_notes.append(NumberedNote(
                    square.row, square.column, number))
        if (len(eliminated_notes) == 0):
            return None

        print("Found x-wing")

        return Elimination(
            causing_notes=[NumberedNote(
                s.row, s.column, number) for s in causing_squares],
            eliminated_notes=eliminated_notes,
            causing_square=None,
            technique="x-wing")
