import math
from models.board import Board
from models.eliminationGroup import EliminationGroup
from models.eliminationNote import EliminationNote
from models.square import Square


class NakedPair:
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

    def are_all_notes_same(self, squares: list[Square]) -> bool:
        first_square = squares[0]
        notes = first_square.possible_numbers
        for square in squares:
            if (square.possible_numbers != notes):
                return False
        return True

    def pair_to_elimination(self, pair: list[Square], eliminated_notes: list[EliminationNote]) -> EliminationGroup:
        row = pair[0].row
        column = pair[0].column
        number = pair[0].possible_numbers[0]
        forming_notes = []
        for square in pair:
            notes = square.possible_numbers
            for note in notes:
                forming_notes.append(EliminationNote(
                    square.row, square.column, note))

        if (len(pair) == 2):
            technique = "naked-pair"
        elif (len(pair) == 3):
            technique = "naked-triple"
        elif (len(pair) == 4):
            technique = "naked-quad"
        else:
            technique = "naked-" + str(len(pair))

        return EliminationGroup(
            row=row,
            column=column,
            number=number,
            technique=technique,
            forming_notes=forming_notes,
            eliminated_notes=eliminated_notes
        )

    def squares_outside_pair(self, squares: list[Square], pair: list[Square]) -> list[Square]:
        return [square for square in squares if square not in pair]

    def get_eliminated_notes(self, pair: list[Square], square_set: list[Square]) -> list[EliminationNote]:
        eliminates_notes = []
        pair_to_look = pair[0].possible_numbers
        squares_outside_pair = self.squares_outside_pair(
            square_set, pair)
        for square_outside_pair in squares_outside_pair:
            for note in square_outside_pair.possible_numbers:
                if (note in pair_to_look):
                    eliminates_notes.append(EliminationNote(
                        square_outside_pair.row,
                        square_outside_pair.column,
                        note))
        return eliminates_notes

    def get_naked_pairs(self, board: Board) -> list[EliminationGroup]:
        max_pair_count = math.floor(board.size/2)
        naked_pairs = []
        for pair_count in range(2, max_pair_count+1):
            pairs = self.get_naked_pairs_of_n(board, pair_count)
            naked_pairs += pairs
        return naked_pairs

    def get_naked_pairs_of_n(self, board: Board, pair_count: int) -> list[EliminationGroup]:
        naked_pairs = []
        rows = [board.get_empty_squares_in_row(i) for i in range(board.size)]
        for row in rows:
            sets = self.get_sets_of_n([], row, [], pair_count)
            for pair in sets:
                all_notes_same = self.are_all_notes_same(pair)
                if (not all_notes_same):
                    continue
                all_notes_correct_length = len(
                    pair[0].possible_numbers) == pair_count
                if (not all_notes_correct_length):
                    continue
                squares_in_row = board.get_squares_in_row(pair[0].row)
                other_squares_in_row = [
                    s for s in squares_in_row if s not in pair]
                eliminated_notes = self.get_eliminated_notes(
                    pair, other_squares_in_row)
                if (len(eliminated_notes) == 0):
                    continue
                elimination = self.pair_to_elimination(pair, eliminated_notes)
                naked_pairs.append(elimination)

        columns = [board.get_empty_squares_in_column(
            i) for i in range(board.size)]
        for column in columns:
            sets = self.get_sets_of_n([], column, [], pair_count)
            for pair in sets:
                all_notes_same = self.are_all_notes_same(pair)
                if (not all_notes_same):
                    continue
                all_notes_correct_length = len(
                    pair[0].possible_numbers) == pair_count
                if (not all_notes_correct_length):
                    continue
                squares_in_column = board.get_squares_in_column(pair[0].column)
                other_squares_in_column = [
                    s for s in squares_in_column if s not in pair]
                eliminated_notes = self.get_eliminated_notes(
                    pair, other_squares_in_column)
                if (len(eliminated_notes) == 0):
                    continue
                elimination = self.pair_to_elimination(pair, eliminated_notes)
                naked_pairs.append(elimination)

        boxes = [board.get_empty_squares_in_box_number(
            i) for i in range(board.size)]
        for box in boxes:
            sets = self.get_sets_of_n([], box, [], pair_count)
            for pair in sets:
                all_notes_same = self.are_all_notes_same(pair)
                if (not all_notes_same):
                    continue
                all_notes_correct_length = len(
                    pair[0].possible_numbers) == pair_count
                if (not all_notes_correct_length):
                    continue
                squares_in_box = board.get_squares_in_box(pair[0])
                other_squares_in_box = [
                    s for s in squares_in_box if s not in pair]
                eliminated_notes = self.get_eliminated_notes(
                    pair, other_squares_in_box)
                if (len(eliminated_notes) == 0):
                    continue
                elimination = self.pair_to_elimination(pair, eliminated_notes)
                naked_pairs.append(elimination)

        return naked_pairs
