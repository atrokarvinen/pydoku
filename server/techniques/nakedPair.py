import math
from models.board import Board
from models.elimination import Elimination
from models.numberedNote import NumberedNote
from models.square import Square
from techniques.eliminatorBase import EliminatorBase
from techniques.squareLogic import SquareLogic


class NakedPair(EliminatorBase):
    def get_next_solution(self, board: Board) -> Elimination:
        max_pair_count = math.floor(board.size/2)
        for pair_count in range(2, max_pair_count+1):
            pair = self.find_naked_pair_of_n(board, pair_count)
            if (pair is not None):
                return pair
        return None

    def get_sets_of_n(self, sets, remaining_elements, pair, n) -> list[list[Square]]:
        if (len(pair) == n):
            sets.append(pair)
        for i in range(len(remaining_elements)):
            picked = remaining_elements[i]
            self.get_sets_of_n(
                sets, remaining_elements[i+1:], pair + [picked], n)
        return sets

    def validate_pair(self, pair: list[Square]) -> bool:
        pair_count = len(pair)
        any_too_few_notes = any(
            len(square.possible_numbers) <= 1 for square in pair)
        any_too_many_notes = any(
            len(square.possible_numbers) > pair_count for square in pair)
        if (any_too_few_notes or any_too_many_notes):
            return False
        return True

    def do_notes_form_pair(self, squares: list[Square]) -> bool:
        unique_notes = SquareLogic.get_unique_notes(squares)
        return len(unique_notes) == len(squares)

    def pair_to_elimination(self, pair: list[Square], eliminated_notes: list[NumberedNote]) -> Elimination:
        causing_notes = []
        for square in pair:
            notes = square.possible_numbers
            for note in notes:
                causing_notes.append(NumberedNote(
                    square.row, square.column, note))

        if (len(pair) == 2):
            technique = "naked-pair"
        elif (len(pair) == 3):
            technique = "naked-triple"
        elif (len(pair) == 4):
            technique = "naked-quad"
        else:
            technique = "naked-" + str(len(pair))

        return Elimination(
            technique=technique,
            causing_square=None,
            causing_notes=causing_notes,
            eliminated_notes=eliminated_notes
        )

    def squares_outside_pair(self, squares: list[Square], pair: list[Square]) -> list[Square]:
        return [square for square in squares if square not in pair]

    def get_eliminated_notes(self, pair: list[Square], square_set: list[Square]) -> list[NumberedNote]:
        eliminates_notes = []
        notes_in_pair = SquareLogic.get_unique_notes(pair)
        squares_outside_pair = self.squares_outside_pair(
            square_set, pair)
        for square_outside_pair in squares_outside_pair:
            for note in square_outside_pair.possible_numbers:
                if (note in notes_in_pair):
                    eliminates_notes.append(NumberedNote(
                        square_outside_pair.row,
                        square_outside_pair.column,
                        note))
        return eliminates_notes

    def find_naked_pair_of_n(self, board: Board, pair_count: int) -> Elimination:
        row_elimination = self.get_pair_in_region(
            board,
            pair_count,
            board.get_empty_squares_in_row,
            board.get_empty_squares_in_row_by_square)
        if (row_elimination is not None):
            return row_elimination

        column_elimination = self.get_pair_in_region(
            board,
            pair_count,
            board.get_empty_squares_in_column,
            board.get_empty_squares_in_column_by_square)
        if (column_elimination is not None):
            return column_elimination

        box_elimination = self.get_pair_in_region(
            board,
            pair_count,
            board.get_empty_squares_in_box,
            board.get_empty_squares_in_box_by_square)
        if (box_elimination is not None):
            return box_elimination

    def get_pair_in_region(self, board: Board, pair_count: int, region_getter, region_getter_by_square) -> Elimination:
        lines = [region_getter(i) for i in range(board.size)]
        for line in lines:
            sets = self.get_sets_of_n([], line, [], pair_count)
            for pair in sets:
                is_pair_valid = self.validate_pair(pair)
                if (not is_pair_valid):
                    continue
                all_notes_same = self.do_notes_form_pair(pair)
                if (not all_notes_same):
                    continue
                squares_in_region = region_getter_by_square(pair[0])
                squares = [s for s in squares_in_region if s not in pair]
                eliminated_notes = self.get_eliminated_notes(pair, squares)
                if (len(eliminated_notes) == 0):
                    continue
                elimination = self.pair_to_elimination(pair, eliminated_notes)
                return elimination
        return None
