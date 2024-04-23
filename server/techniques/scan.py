from models.board import Board
from models.elimination import Elimination
from models.numberedNote import NumberedNote
from models.numberedSquare import NumberedSquare


class Scan:
    def __init__(self):
        pass

    def scan(self, board: Board) -> list[Elimination]:
        elimination_groups = []
        flat_squares = board.flatten()
        for square in flat_squares:
            if (square.is_empty()):
                continue
            row = square.row
            column = square.column
            number = square.number

            squares_in_row = board.get_squares_in_row(row)
            squares_in_column = board.get_squares_in_column(column)
            squares_in_box = board.get_squares_in_box(square)

            other_squares = squares_in_row + squares_in_column + squares_in_box

            eliminated_notes = []
            elimination_group = Elimination(
                technique="scan",
                causing_square=NumberedSquare(row, column, number),
                causing_notes=[],
                eliminated_notes=eliminated_notes,
            )
            for other_square in other_squares:
                if (other_square.row == row and other_square.column == column):
                    continue
                if (other_square.possible_numbers.count(number)):
                    eliminated_note = NumberedNote(
                        other_square.row,
                        other_square.column,
                        number)
                    eliminated_notes.append(eliminated_note)
            if (len(eliminated_notes) > 0):
                elimination_groups.append(elimination_group)

        return elimination_groups
