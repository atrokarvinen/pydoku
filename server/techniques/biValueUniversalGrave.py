from models.board import Board
from models.elimination import Elimination
from models.numberedNote import NumberedNote
from models.square import Square
from techniques.utils.squareLogic import SquareLogic
from techniques.eliminatorBase import EliminatorBase


class BiValueUniversalGrave(EliminatorBase):
    def get_next_solution(self, board: Board) -> Elimination:
        bug_square = self.detect_bug_square(board)
        if (bug_square is None):
            return None

        row = bug_square.row
        column = bug_square.column
        box = bug_square.box

        squares_in_row = board.get_squares_in_row(row)
        squares_in_column = board.get_squares_in_column(column)
        squares_in_box = board.get_squares_in_box(box)

        bug_note_row = self.detect_bug_note(squares_in_row)
        bug_note_column = self.detect_bug_note(squares_in_column)
        bug_note_box = self.detect_bug_note(squares_in_box)

        if (bug_note_row == bug_note_column == bug_note_box):
            note = bug_note_row
            causing_notes = [NumberedNote(row, column, note)]
            other_notes = [n for n in bug_square.possible_numbers if n != note]
            eliminated_notes = [NumberedNote(
                row, column, n) for n in other_notes]
            elimination = Elimination(
                technique="bug",
                causing_square=None,
                causing_notes=causing_notes,
                eliminated_notes=eliminated_notes
            )
            print("Found bug in square", row, column, "note", note)
            return elimination
        return None

    def detect_bug_square(self, board: Board) -> Square:
        empty_squares = board.flatten_empty()
        non_bi_value_squares = []
        for square in empty_squares:
            if (len(square.possible_numbers) == 2):
                continue
            else:
                non_bi_value_squares.append(square)

        if (len(non_bi_value_squares) != 1):
            return None

        return non_bi_value_squares[0]

    def detect_bug_note(self, region: list[Square]) -> bool:
        notes_by_count = SquareLogic.count_notes_in_region(region)
        for note, count in notes_by_count.items():
            if (count != 3):
                continue
            return note
