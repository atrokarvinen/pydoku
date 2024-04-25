from models.board import Board
from models.elimination import Elimination
from models.numberedNote import NumberedNote
from models.numberedSquare import NumberedSquare
from models.solutionStep import SolutionStep
from techniques.eliminatorBase import EliminatorBase


class Scan(EliminatorBase):
    def get_next_solution(self, board: Board) -> SolutionStep:
        flat_squares = board.flatten_not_empty()
        for square in flat_squares:
            row = square.row
            column = square.column
            number = square.number

            squares_in_row = board.get_empty_squares_in_row(row)
            squares_in_column = board.get_empty_squares_in_column(column)
            squares_in_box = board.get_empty_squares_in_box(square)

            other_squares = squares_in_row + squares_in_column + squares_in_box

            eliminated_notes = []
            for other_square in other_squares:
                if (other_square.row == row and other_square.column == column):
                    continue
                if (number in other_square.possible_numbers):
                    eliminated_note = NumberedNote(
                        other_square.row,
                        other_square.column,
                        number)
                    eliminated_notes.append(eliminated_note)

            if (len(eliminated_notes) == 0):
                continue

            elimination = Elimination(
                technique="scan",
                causing_square=NumberedSquare(row, column, number),
                causing_notes=[],
                eliminated_notes=eliminated_notes,
            )
            return elimination

        return None
