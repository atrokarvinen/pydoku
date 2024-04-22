from models.board import Board
from models.eliminationGroup import EliminationGroup
from models.eliminationNote import EliminationNote
from models.square import Square


class NakedPair:
    def __init__(self) -> None:
        pass

    def pairs_match(self, pair1: list[int], pair2: list[int]) -> bool:
        sorted_pair1 = sorted(pair1)
        sorted_pair2 = sorted(pair2)
        return sorted_pair1 == sorted_pair2

    def pair_to_elimination(self, pair: list[Square], eliminated_notes: list[EliminationNote]) -> EliminationGroup:
        row = pair[0].row
        column = pair[0].column
        number = pair[0].possible_numbers[0]
        forming_notes = []
        # forming_notes = [square.possible_numbers for square in pair for square.possible_numbers in square]
        for square in pair:
            notes = square.possible_numbers
            for note in notes:
                forming_notes.append(EliminationNote(
                    square.row, square.column, note))

        return EliminationGroup(
            row=row,
            column=column,
            number=number,
            technique="naked-pair",
            forming_notes=forming_notes,
            eliminated_notes=eliminated_notes
        )

    def squares_outside_pair(self, squares: list[Square], pair: list[Square]) -> list[Square]:
        return [square for square in squares if square not in pair]

    def get_eliminates_notes(self, pair: list[Square], square_set: list[Square]) -> list[EliminationNote]:
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
        flat_squares = board.flatten()

        pair_count = 2
        naked_pairs = []
        for square in flat_squares:
            row = square.row
            column = square.column
            if (not square.is_empty()):
                continue

            pair_to_look = square.possible_numbers
            if (len(pair_to_look) != pair_count):
                continue

            squares_in_row = board.get_squares_in_row(row)
            squares_in_column = board.get_squares_in_column(column)
            squares_in_box = board.get_squares_in_box(square)

            for other_square in squares_in_row:
                if (other_square.row == row and other_square.column == column):
                    continue
                if (self.pairs_match(pair_to_look, other_square.possible_numbers)):
                    pair = [square, other_square]
                    eliminated_notes = self.get_eliminates_notes(
                        pair, squares_in_row)
                    if (len(eliminated_notes) == 0):
                        continue
                    elimination = self.pair_to_elimination(
                        pair, eliminated_notes)
                    naked_pairs.append(elimination)

            for other_square in squares_in_column:
                if (other_square.row == row and other_square.column == column):
                    continue
                if (self.pairs_match(pair_to_look, other_square.possible_numbers)):
                    pair = [square, other_square]
                    eliminated_notes = self.get_eliminates_notes(
                        pair, squares_in_column)
                    if (len(eliminated_notes) == 0):
                        continue
                    elimination = self.pair_to_elimination(
                        pair, eliminated_notes)
                    naked_pairs.append(elimination)

            for other_square in squares_in_box:
                if (other_square.row == row and other_square.column == column):
                    continue
                if (self.pairs_match(pair_to_look, other_square.possible_numbers)):
                    pair = [square, other_square]
                    eliminated_notes = self.get_eliminates_notes(
                        pair, squares_in_box)
                    if (len(eliminated_notes) == 0):
                        continue
                    elimination = self.pair_to_elimination(
                        pair, eliminated_notes)
                    naked_pairs.append(elimination)

        return naked_pairs
