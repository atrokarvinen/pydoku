from models.board import Board
from models.elimination import Elimination
from models.highlightedRegion import HighlightedRegion
from models.numberedNote import NumberedNote
from models.square import Square
from techniques.eliminatorBase import EliminatorBase


class Claiming(EliminatorBase):
    def get_next_solution(self, board: Board) -> Elimination:
        rows = [board.get_squares_in_row(i) for i in range(board.size)]
        columns = [board.get_squares_in_column(i) for i in range(board.size)]
        square_sets = rows + columns
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
        any_has_number = any([s.number == note for s in all_squares])
        if any_has_number:
            return None
        squares = [s for s in all_squares if note in s.possible_numbers]
        is_valid = self.validate_squares(squares, board.box_size)
        if not is_valid:
            return None

        box = squares[0].box
        squares_in_box = board.get_squares_in_box(box)
        claimed_squares = [
            s for s in squares_in_box if s not in squares and note in s.possible_numbers
        ]
        if len(claimed_squares) == 0:
            return None

        highlighted_regions = self.get_highlighted_regions(squares)
        elimination = Elimination(
            technique="claiming",
            causing_square=None,
            causing_notes=[NumberedNote(s.row, s.column, note)
                           for s in squares],
            eliminated_notes=[NumberedNote(
                s.row, s.column, note) for s in claimed_squares],
            highlighted_regions=highlighted_regions
        )
        print("Claiming found")
        return elimination

    def validate_squares(self, squares: list[Square], box_size: int) -> bool:
        too_few_squares_with_note = len(squares) <= 1
        if too_few_squares_with_note:
            return False

        too_many_squares_with_note = len(squares) > box_size
        if too_many_squares_with_note:
            return False

        squares_in_same_box = all([squares[0].box == s.box for s in squares])
        if not squares_in_same_box:
            return False

        return True

    def get_highlighted_regions(self, squares: list[Square]) -> list[HighlightedRegion]:
        first_square = squares[0]
        box = first_square.box
        row = first_square.row
        column = first_square.column
        is_row_set = len(set([s.row for s in squares])) == 1
        highlighted_regions = [
            HighlightedRegion("box", box),
            HighlightedRegion("row", row) if is_row_set else
            HighlightedRegion("column", column),
        ]
        return highlighted_regions
