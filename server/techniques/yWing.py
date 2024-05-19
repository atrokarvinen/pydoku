from models.board import Board
from models.elimination import Elimination
from models.numberedNote import NumberedNote
from models.square import Square
from techniques.eliminatorBase import EliminatorBase
from techniques.utils.squareLogic import SquareLogic


class YWing(EliminatorBase):
    def get_next_solution(self, board: Board) -> Elimination:
        empty_squares = board.flatten_empty()
        pivot_squares = [
            s for s in empty_squares if len(s.possible_numbers) == 2]
        for pivot in pivot_squares:
            pivot_number1 = pivot.possible_numbers[0]
            pivot_number2 = pivot.possible_numbers[1]
            squares_in_row = board.get_squares_in_row(pivot.row)
            squares_in_column = board.get_squares_in_column(pivot.column)
            squares_in_box = board.get_squares_in_box(pivot.box)
            other_squares = squares_in_row + squares_in_column + squares_in_box
            pincer_squares: list[Square] = []
            for other_square in other_squares:
                if (other_square == pivot):
                    continue
                if (len(other_square.possible_numbers) != 2):
                    continue
                if (pivot_number1 in other_square.possible_numbers or pivot_number2 in other_square.possible_numbers):
                    pincer_squares.append(other_square)

            for pincer1 in pincer_squares:
                for pincer2 in pincer_squares:
                    if (pincer1 == pincer2):
                        continue
                    pincer_numbers = pincer1.possible_numbers + pincer2.possible_numbers
                    pivot_numbers_in_pincers = pivot_number1 in pincer_numbers and pivot_number2 in pincer_numbers
                    pincer_numbers_not_in_pivot = [
                        p for p in pincer_numbers if p != pivot_number1 and p != pivot_number2]
                    if (len(pincer_numbers_not_in_pivot) != 2):
                        continue
                    pincers_have_same_numbers = pincer_numbers_not_in_pivot[
                        0] == pincer_numbers_not_in_pivot[1]
                    if (not pivot_numbers_in_pincers or not pincers_have_same_numbers):
                        continue

                    shared_number = pincer_numbers_not_in_pivot[0]

                    eliminated_notes = []
                    for square in empty_squares:
                        if (square == pivot or square == pincer1 or square == pincer2):
                            continue
                        seen_by_pincers = SquareLogic.is_connected(
                            square, pincer1) and SquareLogic.is_connected(square, pincer2)
                        if (seen_by_pincers and shared_number in square.possible_numbers):
                            eliminated_notes.append(NumberedNote(
                                square.row, square.column, shared_number))

                    if (len(eliminated_notes) == 0):
                        continue

                    print("Found Y-Wing")

                    elimination = Elimination(
                        technique="y-wing",
                        eliminated_notes=eliminated_notes,
                        causing_notes=[
                            NumberedNote(pivot.row, pivot.column,
                                         pivot_number1),
                            NumberedNote(pivot.row, pivot.column,
                                         pivot_number2),
                            NumberedNote(
                                pincer1.row, pincer1.column, pincer1.possible_numbers[0]),
                            NumberedNote(
                                pincer1.row, pincer1.column, pincer1.possible_numbers[1]),
                            NumberedNote(
                                pincer2.row, pincer2.column, pincer2.possible_numbers[0]),
                            NumberedNote(
                                pincer2.row, pincer2.column, pincer2.possible_numbers[1])
                        ],
                        causing_square=None)
                    return elimination
        return None
