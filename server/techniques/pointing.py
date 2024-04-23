from models.board import Board
from models.eliminationGroup import EliminationGroup
from models.eliminationNote import EliminationNote
from models.square import Square


class Pointing:
    def __init__(self) -> None:
        pass

    def get_pointing(self, board: Board) -> list[EliminationGroup]:
        groups = []
        for i in range(board.size):
            squares_in_box = board.get_squares_in_box_number(i)
            notes = [*range(1, board.size+1)]
            for note in notes:
                squares_with_note = [
                    s for s in squares_in_box if note in s.possible_numbers]
                too_many_squares_with_note = len(
                    squares_with_note) > board.box_size
                too_few_squares_with_note = len(squares_with_note) <= 1
                if too_few_squares_with_note or too_many_squares_with_note:
                    continue

                # Row
                is_every_square_in_same_row = all(
                    [s.row == squares_with_note[0].row for s in squares_with_note])
                if is_every_square_in_same_row:
                    row = squares_with_note[0].row
                    squares_in_row = board.get_squares_in_row(row)
                    other_squares_in_row = [
                        s for s in squares_in_row if s not in squares_with_note and note in s.possible_numbers
                    ]
                    eliminated_notes = [
                        EliminationNote(
                            s.row, s.column, note) for s in other_squares_in_row
                    ]
                    if (len(eliminated_notes) == 0):
                        continue
                    elimination = EliminationGroup(
                        row=squares_with_note[0].row,
                        column=squares_with_note[0].column,
                        number=note,
                        technique="pointing",
                        forming_notes=[EliminationNote(
                            s.row, s.column, note) for s in squares_with_note],
                        eliminated_notes=eliminated_notes
                    )
                    groups.append(elimination)

                # Column
                is_every_square_in_same_column = all(
                    [s.column == squares_with_note[0].column for s in squares_with_note])
                if is_every_square_in_same_column:
                    column = squares_with_note[0].column
                    squares_in_column = board.get_squares_in_column(column)
                    other_squares_in_column = [
                        s for s in squares_in_column if s not in squares_with_note and note in s.possible_numbers
                    ]
                    eliminated_notes = [
                        EliminationNote(
                            s.row, s.column, note) for s in other_squares_in_column
                    ]
                    if (len(eliminated_notes) == 0):
                        continue
                    elimination = EliminationGroup(
                        row=squares_with_note[0].row,
                        column=squares_with_note[0].column,
                        number=note,
                        technique="pointing",
                        forming_notes=[EliminationNote(
                            s.row, s.column, note) for s in squares_with_note],
                        eliminated_notes=eliminated_notes
                    )
                    groups.append(elimination)

        return groups
