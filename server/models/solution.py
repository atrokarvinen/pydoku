from models.board import Board
from models.singleCandidate import SingleCandidate
from models.elimination import Elimination


class Solution:
    def __init__(self, initial_board: Board) -> None:
        self.eliminations: list[Elimination] = []
        self.single_candidates: list[SingleCandidate] = []
        self.solution_index = 0
        self.sudoku = initial_board
        self.final_sudoku = initial_board
        self.is_solved = False
        self.error: str = None

    def add_elimination(self, elimination: Elimination) -> None:
        elimination.solution_index = self.solution_index
        self.eliminations.append(elimination)
        self.solution_index += 1

    def add_single_candidate(self, single_candidate: SingleCandidate) -> None:
        single_candidate.solutionIndex = self.solution_index
        self.single_candidates.append(single_candidate)
        self.solution_index += 1

    def serialize(self) -> dict:
        return {
            "isSolved": self.is_solved,
            "sudoku": self.sudoku.serialize(),
            "finalSudoku": self.final_sudoku.serialize(),
            "eliminations": [elimination.serialize() for elimination in self.eliminations],
            "singleCandidates": [single_candidate.serialize() for single_candidate in self.single_candidates],
            "error": self.error
        }
