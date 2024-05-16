from models.board import Board
from models.elimination import Elimination
from models.highlightedRegion import HighlightedRegion
from models.numberedNote import NumberedNote
from models.numberedSquare import NumberedSquare
from models.square import Square
from techniques.eliminatorBase import EliminatorBase


class Scan(EliminatorBase):
    def get_next_solution(self, board: Board) -> Elimination:
        flat_squares = board.flatten_not_empty()
        for square in flat_squares:
            row = square.row
            column = square.column
            box = square.box
            number = square.number

            squares_in_row = board.get_empty_squares_in_row(row)
            squares_in_column = board.get_empty_squares_in_column(column)
            squares_in_box = board.get_empty_squares_in_box(box)

            other_squares = squares_in_row + squares_in_column + squares_in_box

            eliminated_notes: list[NumberedNote] = []
            for other_square in other_squares:
                if (other_square.row == row and other_square.column == column):
                    continue
                already_eliminated = any(
                    note.row == other_square.row and note.column == other_square.column and note.number == number for note in eliminated_notes)
                if (number in other_square.possible_numbers and not already_eliminated):
                    eliminated_note = NumberedNote(
                        other_square.row,
                        other_square.column,
                        number)
                    eliminated_notes.append(eliminated_note)

            if (len(eliminated_notes) == 0):
                continue

            highlighted_regions = self.get_highlighted_regions(square)

            elimination = Elimination(
                technique="scan",
                causing_square=NumberedSquare(row, column, number),
                causing_notes=[],
                eliminated_notes=eliminated_notes,
                highlighted_regions=highlighted_regions
            )
            return elimination

        return None

    def get_highlighted_regions(self, square: Square) -> list[HighlightedRegion]:
        row = square.row
        column = square.column
        box = square.box

        return [
            HighlightedRegion("row", row),
            HighlightedRegion("column", column),
            HighlightedRegion("box", box)
        ]
