import math
from models.board import Board
from models.elimination import Elimination
from models.highlightedRegion import HighlightedRegion
from models.numberedNote import NumberedNote
from models.square import Square
from techniques.eliminatorBase import EliminatorBase
from techniques.utils.squareLogic import SquareLogic
from techniques.utils.combinatorics import Combinatorics


class PairBase():
    def find_pair(self, board: Board) -> Elimination:
        max_pair_count = math.floor(board.size/2)
        for pair_count in range(2, max_pair_count+1):
            pair = self.find_pair_of_n(board, pair_count)
            if (pair is not None):
                return pair
        return None

    def find_pair_of_n(self, board: Board, pair_count: int) -> Elimination:
        board_range = range(board.size)
        rows = [board.get_empty_squares_in_row(i) for i in board_range]
        row_elimination = self.find_pair_from_regions(rows, pair_count)
        if (row_elimination is not None):
            return row_elimination

        columns = [board.get_empty_squares_in_column(i) for i in board_range]
        column_elimination = self.find_pair_from_regions(columns, pair_count)
        if (column_elimination is not None):
            return column_elimination

        boxes = [board.get_empty_squares_in_box(i) for i in board_range]
        box_elimination = self.find_pair_from_regions(boxes, pair_count)
        if (box_elimination is not None):
            return box_elimination

        return None

    def find_pair_from_regions(self, regions: list[list[Square]], pair_count: int) -> Elimination:
        for region in regions:
            square_sets = Combinatorics.get_sets_of_n(
                [], region, [], pair_count)
            for square_set in square_sets:
                other_squares = [s for s in region if s not in square_set]
                if (len(square_set) < pair_count or len(other_squares) == 0):
                    continue
                pair = self.find_pair_from_region(square_set, other_squares)
                if (pair is not None):
                    return pair

        return None

    def find_pair_from_region(self,
                              pair: list[Square],
                              other_squares: list[Square]) -> Elimination:
        # Implemented by child classes
        pass

    def get_highlighted_regions(self, pair: list[Square], other_squares: list[Square]) -> list[HighlightedRegion]:
        first_square = pair[0]
        all_squares = pair + other_squares
        is_row_pair = SquareLogic.squares_have_same_row(all_squares)
        if (is_row_pair):
            return [HighlightedRegion("row", first_square.row)]
        is_column_pair = SquareLogic.squares_have_same_column(all_squares)
        if (is_column_pair):
            return [HighlightedRegion("column", first_square.column)]
        return [HighlightedRegion("box", first_square.box)]
