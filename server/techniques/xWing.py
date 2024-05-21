from models.board import Board
from models.highlightedRegion import HighlightedRegion
from models.numberedNote import NumberedNote
from models.elimination import Elimination
from models.point import Point
from models.pointer import Pointer
from models.square import Square
from techniques.eliminatorBase import EliminatorBase
from techniques.utils.squareLogic import SquareLogic


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
        unique_rows = set([s.row for s in squares])
        unique_cols = set([s.column for s in squares])
        return len(unique_rows) == 2 and len(unique_cols) == 2

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

        highlighted_regions = self.get_highlighted_regions(causing_squares)
        pointers = self.get_pointers(causing_squares)
        return Elimination(
            technique="x-wing",
            causing_square=None,
            causing_notes=[NumberedNote(
                s.row, s.column, number) for s in causing_squares],
            eliminated_notes=eliminated_notes,
            highlighted_regions=highlighted_regions,
            pointers=pointers)

    def get_highlighted_regions(self, causing_squares: list[Square]) -> list[HighlightedRegion]:
        unique_rows = set([s.row for s in causing_squares])
        unique_cols = set([s.column for s in causing_squares])
        highlighted_regions = []
        for row in unique_rows:
            highlighted_regions.append(HighlightedRegion("row", row))
        for col in unique_cols:
            highlighted_regions.append(HighlightedRegion("column", col))
        return highlighted_regions

    def get_pointers(self, causing_squares: list[Square]) -> list[Pointer]:
        visited = []
        pointers = []
        for s1 in causing_squares:
            for s2 in causing_squares:
                if (s1 == s2 or s1 in visited or s2 in visited):
                    continue
                same_row = SquareLogic.squares_have_same_row([s1, s2])
                same_column = SquareLogic.squares_have_same_column([s1, s2])
                if (same_row or same_column):
                    continue
                pointers.append(
                    Pointer(s1.to_point(), s2.to_point(), bidirectional=True))
                visited.append(s1)
                visited.append(s2)
        return pointers
