from models.board import Board
from models.elimination import Elimination
from models.numberedNote import NumberedNote
from models.square import Square
from techniques.eliminatorBase import EliminatorBase
from techniques.pairBase import PairBase
from techniques.squareLogic import SquareLogic
from techniques.utils.combinatorics import Combinatorics


class HiddenPair(EliminatorBase, PairBase):
    def get_next_solution(self, board: Board) -> Elimination:
        elimination = self.find_pair(board)
        return elimination

    def find_pair_from_region(
            self,
            squares: list[Square],
            other_squares: list[Square]) -> Elimination:
        pair_count = len(squares)
        all_squares = squares + other_squares

        notes_by_count = {}
        for square in all_squares:
            for note in square.possible_numbers:
                notes_by_count[note] = notes_by_count.get(note, 0) + 1

        notes_with_pair_count = [
            note for note, count in notes_by_count.items() if count <= pair_count and count > 1]

        possible_note_pairs = Combinatorics.get_sets_of_n(
            [], notes_with_pair_count, [], pair_count)
        for note_pair in possible_note_pairs:
            is_valid_pair = self.validate_pair(
                squares, note_pair, other_squares)
            if (not is_valid_pair):
                continue

            eliminated_notes = self.get_eliminated_notes(
                squares, note_pair)
            if (len(eliminated_notes) == 0):
                continue
            elimination = self.pair_to_elimination(
                squares, eliminated_notes, note_pair)

            return elimination

        return None

    def validate_pair(self, pair: list[Square], note_pair: list[int], other_squares: list[Square]) -> bool:
        squares_valid = all([len(s.possible_numbers) > 1 for s in pair])
        if (not squares_valid):
            return False
        other_squares_have_note = any(
            [note in s.possible_numbers for s in other_squares for note in note_pair])
        if (other_squares_have_note):
            return False
        unique_notes = SquareLogic.get_unique_notes(pair)
        note_pair_is_contained = all(
            [note in unique_notes for note in note_pair]
        )
        return note_pair_is_contained

    def get_eliminated_notes(self, pair: list[Square], note_pair: list[int]) -> list[NumberedNote]:
        eliminated_notes = []
        for square in pair:
            notes_not_in_pair = [
                note for note in square.possible_numbers if note not in note_pair]
            eliminated_notes += [NumberedNote(
                square.row,
                square.column,
                note) for note in notes_not_in_pair]
        return eliminated_notes

    def pair_to_elimination(self,
                            pair: list[Square],
                            eliminated_notes: list[NumberedNote],
                            note_pair: list[int]) -> Elimination:
        causing_notes = []
        for square in pair:
            for note in note_pair:
                has_note = note in square.possible_numbers
                if (not has_note):
                    continue
                causing_notes.append(NumberedNote(
                    square.row, square.column, note))

        if (len(pair) == 2):
            technique = "hidden-pair"
        elif (len(pair) == 3):
            technique = "hidden-triple"
        elif (len(pair) == 4):
            technique = "hidden-quad"
        else:
            technique = "hidden-" + str(len(pair))

        return Elimination(
            technique=technique,
            causing_square=None,
            causing_notes=causing_notes,
            eliminated_notes=eliminated_notes)
