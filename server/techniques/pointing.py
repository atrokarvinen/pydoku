from models.board import Board
from models.elimination import Elimination
from models.highlightedRegion import HighlightedRegion
from models.numberedNote import NumberedNote
from models.square import Square
from techniques.eliminatorBase import EliminatorBase
from techniques.utils.squareLogic import SquareLogic


class Pointing(EliminatorBase):
    def get_next_solution(self, board: Board) -> Elimination:
        board_range = board.get_range_zero_indexed()
        square_sets = [board.get_empty_squares_in_box(i) for i in board_range]
        elimination = self.iterate_square_sets(board, square_sets)
        return elimination

    def iterate_square_sets(self, board: Board, square_sets: list[list[Square]]) -> Elimination:
        notes = [*range(1, board.size+1)]
        for squares in square_sets:
            for note in notes:
                elimination = self.find_elimination(board, squares, note)
                if elimination is not None:
                    return elimination

        return None

    def find_elimination(self, board: Board, all_squares: list[Square], note: int) -> Elimination:
        squares = [s for s in all_squares if note in s.possible_numbers]
        too_many_squares_with_note = len(squares) > board.box_size
        too_few_squares_with_note = len(squares) <= 1
        if too_few_squares_with_note or too_many_squares_with_note:
            return None

        other_squares = self.validate_pointing(board, squares, note)
        if (other_squares is None):
            return None

        eliminated_notes = [NumberedNote(
            s.row, s.column, note) for s in other_squares]
        if (len(eliminated_notes) == 0):
            return None
        highlighted_regions = self.get_highlighted_regions(squares)
        elimination = Elimination(
            technique="pointing",
            causing_square=None,
            causing_notes=[NumberedNote(s.row, s.column, note)
                           for s in squares],
            eliminated_notes=eliminated_notes,
            highlighted_regions=highlighted_regions
        )
        return elimination

    def validate_pointing(self, board: Board, squares: list[Square], note: int):
        first_square = squares[0]
        is_same_row = SquareLogic.squares_have_same_row(squares)
        row = board.get_empty_squares_in_row(first_square.row)
        other_squares_row = [
            s for s in row if s not in squares and note in s.possible_numbers
        ]

        is_same_column = SquareLogic.squares_have_same_column(squares)
        column = board.get_empty_squares_in_column(first_square.column)
        other_squares_column = [
            s for s in column if s not in squares and note in s.possible_numbers
        ]

        if (is_same_row and len(other_squares_row) > 0):
            return other_squares_row
        elif (is_same_column and len(other_squares_column)):
            return other_squares_column

        return None

    def get_highlighted_regions(self, squares: list[Square]) -> list[HighlightedRegion]:
        first_square = squares[0]
        is_same_row = SquareLogic.squares_have_same_row(squares)
        if (is_same_row):
            return [HighlightedRegion("row", first_square.row)]

        return [HighlightedRegion("column", first_square.column)]
