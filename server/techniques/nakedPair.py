from models.board import Board
from models.elimination import Elimination
from models.numberedNote import NumberedNote
from models.square import Square
from techniques.eliminatorBase import EliminatorBase
from techniques.pairBase import PairBase
from techniques.utils.squareLogic import SquareLogic


class NakedPair(EliminatorBase, PairBase):
    def get_next_solution(self, board: Board) -> Elimination:
        elimination = self.find_pair(board)
        return elimination

    def find_pair_from_region(self,
                              pair: list[Square],
                              other_squares: list[Square]) -> Elimination:
        is_pair_valid = self.validate_pair(pair)
        if (not is_pair_valid):
            return None
        all_notes_same = self.do_notes_form_pair(pair)
        if (not all_notes_same):
            return None
        squares = other_squares
        eliminated_notes = self.get_eliminated_notes(pair, squares)
        if (len(eliminated_notes) == 0):
            return None
        elimination = self.pair_to_elimination(pair, eliminated_notes)
        return elimination

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
