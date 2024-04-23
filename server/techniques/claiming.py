from models.board import Board
from models.eliminationGroup import EliminationGroup
from models.eliminationNote import EliminationNote


class Claiming:
    def __init__(self) -> None:
        pass

    def get_claiming(self, board: Board) -> list[EliminationGroup]:
        elimination_groups = []
        columns = [board.get_empty_squares_in_column(
            i) for i in range(board.size)]
        rows = [board.get_empty_squares_in_row(i) for i in range(board.size)]
        squares_sets = columns + rows
        notes = [*range(1, board.size+1)]
        for squares in squares_sets:
            for note in notes:
                squares_with_note = [
                    s for s in squares if note in s.possible_numbers]
                too_many_squares_with_note = len(
                    squares_with_note) > board.box_size
                too_few_squares_with_note = len(squares_with_note) <= 1
                if too_few_squares_with_note or too_many_squares_with_note:
                    continue

                squares_in_same_box = all(
                    [squares_with_note[0].box == s.box for s in squares_with_note])
                if not squares_in_same_box:
                    continue

                squares_in_box = board.get_squares_in_box_number(
                    squares_with_note[0].box)
                claimed_squares = [
                    s for s in squares_in_box if s not in squares_with_note and note in s.possible_numbers
                ]
                if len(claimed_squares) == 0:
                    continue
                elimination_group = EliminationGroup(
                    row=squares_with_note[0].row,
                    column=squares_with_note[0].column,
                    number=note,
                    technique="claiming",
                    forming_notes=[EliminationNote(
                        s.row, s.column, note) for s in squares_with_note],
                    eliminated_notes=[EliminationNote(
                        s.row, s.column, note) for s in claimed_squares]
                )
                elimination_groups.append(elimination_group)

        return elimination_groups
