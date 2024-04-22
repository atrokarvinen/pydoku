from models.board import Board
from models.singleCandidate import SingleCandidate as SingleCandidateModel


class SingleCandidate:
    def __init__(self) -> None:
        pass

    def get_single_candidates(self, board: Board) -> list[SingleCandidateModel]:
        flat_squares = board.flatten()

        single_candidates = []
        for square in flat_squares:
            row = square.row
            column = square.column
            if (not square.is_empty()):
                continue
            possible_numbers = square.possible_numbers
            if (len(possible_numbers) == 0):
                print("No possible numbers")
                continue
            if (len(possible_numbers) == 1):
                number = possible_numbers[0]
                single_candidate = SingleCandidateModel(row, column, number)
                single_candidates.append(single_candidate)

        return single_candidates
