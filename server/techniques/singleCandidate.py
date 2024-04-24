from models.board import Board
from models.singleCandidate import SingleCandidate as SingleCandidateModel
from models.square import Square


class SingleCandidate:
    def __init__(self) -> None:
        pass

    def get_single_candidates(self, board: Board) -> list[SingleCandidateModel]:
        boardRange = range(board.size)
        rows = [board.get_empty_squares_in_row(i) for i in boardRange]
        columns = [board.get_empty_squares_in_column(i) for i in boardRange]
        boxes = [board.get_empty_squares_in_box(i) for i in boardRange]
        single_squares = [[s] for s in board.flatten() if s.is_empty()]

        single_candidates = []
        single_candidates += self.iterate_sets(rows, "row")
        single_candidates += self.iterate_sets(columns, "column")
        single_candidates += self.iterate_sets(boxes, "box")
        single_candidates += self.iterate_sets(single_squares, "cell")

        unique_candidates = self.get_unique_candidates(single_candidates)
        return unique_candidates

    def get_unique_candidates(self, single_candidates: list[SingleCandidateModel]) -> list[SingleCandidateModel]:
        unique_candidates = []
        for candidate in single_candidates:
            square_in_unique_candidates = False
            for unique_candidate in unique_candidates:
                if candidate.row == unique_candidate.row \
                        and candidate.column == unique_candidate.column \
                        and candidate.number == unique_candidate.number:
                    square_in_unique_candidates = True
                    break
            if not square_in_unique_candidates:
                unique_candidates.append(candidate)
        return unique_candidates

    def iterate_sets(self, sets: list[list[Square]], alignment: str) -> list[SingleCandidateModel]:
        single_candidates = []
        for set in sets:
            single_candidates += self.single_candidates_in_set(set, alignment)
        return single_candidates

    def single_candidates_in_set(self, square_set: list[Square], alignment: str) -> list[SingleCandidateModel]:
        notes_by_count = {}
        for square in square_set:
            for note in square.possible_numbers:
                notes_by_count[note] = notes_by_count.get(note, 0) + 1

        if len(square_set) == 1 and len(notes_by_count) > 1:
            return []

        single_candidates = []
        for note, count in notes_by_count.items():
            if count != 1:
                continue
            for square in square_set:
                if not note in square.possible_numbers:
                    continue
                row = square.row
                column = square.column
                single_candidate = SingleCandidateModel(
                    row, column, note, alignment)
                single_candidates.append(single_candidate)

        return single_candidates
