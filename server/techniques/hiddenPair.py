import math
from models.board import Board
from models.elimination import Elimination
from models.numberedNote import NumberedNote
from models.square import Square


class HiddenPair:
    def __init__(self) -> None:
        pass

    def get_sets_of_n(self, sets, remaining_elements, pair, n):
        if (len(pair) == n):
            sets.append(pair)
        for i in range(len(remaining_elements)):
            picked = remaining_elements[i]
            self.get_sets_of_n(
                sets, remaining_elements[i+1:], pair + [picked], n)
        return sets

    def get_hidden_pairs(self, board: Board) -> list[Elimination]:
        max_pair_count = math.floor(board.size/2)
        hidden_pairs = []
        for pair_count in range(2, max_pair_count+1):
            pairs = self.get_hidden_pairs_of_n(board, pair_count)
            hidden_pairs += pairs
        return hidden_pairs

    def get_hidden_pairs_of_n(self, board: Board, pair_count: int) -> list[Elimination]:
        board_range = range(board.size)

        rows = [board.get_empty_squares_in_row(i) for i in board_range]
        row_eliminations = self.iterate_lines(rows, pair_count)

        columns = [board.get_empty_squares_in_column(i) for i in board_range]
        column_eliminations = self.iterate_lines(columns, pair_count)

        boxes = [board.get_empty_squares_in_box(i) for i in board_range]
        box_eliminations = self.iterate_lines(boxes, pair_count)

        return row_eliminations + column_eliminations + box_eliminations

    def iterate_lines(self, lines: list[list[Square]], pair_count: int) -> list[Elimination]:
        hidden_pairs = []
        for line in lines:
            square_sets = self.get_sets_of_n([], line, [], pair_count)
            for square_set in square_sets:
                other_squares = [s for s in line if s not in square_set]
                if (len(square_set) < pair_count or len(other_squares) == 0):
                    continue
                pairs = self.get_pairs_in_line(
                    pair_count, square_set, other_squares)
                hidden_pairs += pairs

        return hidden_pairs

    def get_pairs_in_line(
            self,
            pair_count: int,
            squares: list[Square],
            other_squares: list[Square]) -> list[Elimination]:

        naked_pairs = []
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

            naked_pairs.append(elimination)

        return naked_pairs
