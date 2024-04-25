import math
from models.board import Board
from models.elimination import Elimination
from models.numberedNote import NumberedNote
from models.square import Square
from models.solutionStep import SolutionStep
from techniques.eliminatorBase import EliminatorBase


class HiddenPair(EliminatorBase):
    def get_next_solution(self, board: Board) -> SolutionStep:
        max_pair_count = math.floor(board.size/2)
        for pair_count in range(2, max_pair_count+1):
            pair = self.find_hidden_pair_of_n(board, pair_count)
            if (pair is not None):
                return pair
        return None

    def find_hidden_pair_of_n(self, board: Board, pair_count: int) -> Elimination:
        board_range = range(board.size)

        rows = [board.get_empty_squares_in_row(i) for i in board_range]
        row_elimination = self.iterate_regions(rows, pair_count)
        if (row_elimination is not None):
            return row_elimination

        columns = [board.get_empty_squares_in_column(i) for i in board_range]
        column_elimination = self.iterate_regions(columns, pair_count)
        if (column_elimination is not None):
            return column_elimination

        boxes = [board.get_empty_squares_in_box(i) for i in board_range]
        box_elimination = self.iterate_regions(boxes, pair_count)
        if (box_elimination is not None):
            return box_elimination

        return None

    def iterate_regions(self, regions: list[list[Square]], pair_count: int) -> Elimination:
        for region in regions:
            square_sets = self.get_sets_of_n([], region, [], pair_count)
            for square_set in square_sets:
                other_squares = [s for s in region if s not in square_set]
                if (len(square_set) < pair_count or len(other_squares) == 0):
                    continue
                pair = self.find_pair_in_region(
                    pair_count, square_set, other_squares)
                if (pair is not None):
                    return pair

        return None

    def find_pair_in_region(
            self,
            pair_count: int,
            squares: list[Square],
            other_squares: list[Square]) -> Elimination:

        all_squares = squares + other_squares

        notes_by_count = {}
        for square in all_squares:
            for note in square.possible_numbers:
                notes_by_count[note] = notes_by_count.get(note, 0) + 1

        notes_with_pair_count = [
            note for note, count in notes_by_count.items() if count == pair_count]

        possible_note_pairs = self.get_sets_of_n(
            [], notes_with_pair_count, [], pair_count)
        for note_pair in possible_note_pairs:
            squares_contain_note_pair = True
            for note in note_pair:
                all_squares_have_note = all(
                    [note in square.possible_numbers for square in squares])
                if (not all_squares_have_note):
                    squares_contain_note_pair = False
                    continue
            if (not squares_contain_note_pair):
                continue

            eliminated_notes = []
            causing_notes = []
            for square in squares:
                notes_not_in_pair = [
                    note for note in square.possible_numbers if note not in note_pair]
                eliminated_notes += [NumberedNote(
                    square.row,
                    square.column,
                    note) for note in notes_not_in_pair]
                causing_notes += [NumberedNote(
                    square.row,
                    square.column,
                    note) for note in note_pair]

            if (len(eliminated_notes) == 0):
                continue

            if (pair_count == 2):
                technique = "hidden-pair"
            elif (pair_count == 3):
                technique = "hidden-triple"
            elif (pair_count == 4):
                technique = "hidden-quad"
            elimination = Elimination(
                technique=technique,
                causing_square=None,
                causing_notes=causing_notes,
                eliminated_notes=eliminated_notes)

            return elimination

        return None

    def get_sets_of_n(self, sets, remaining_elements, pair, n):
        if (len(pair) == n):
            sets.append(pair)
        for i in range(len(remaining_elements)):
            picked = remaining_elements[i]
            self.get_sets_of_n(
                sets, remaining_elements[i+1:], pair + [picked], n)
        return sets
