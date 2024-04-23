from models.singleCandidate import SingleCandidate
from models.elimination import Elimination


class Solution:
    def __init__(self, initial_board) -> None:
        self.eliminations = []
        self.single_candidates = []
        self.solution_index = 0
        self.initial_board = initial_board
        self.is_solved = False

    def add_eliminations(self, eliminations: list[Elimination]) -> None:
        for group in eliminations:
            self.add_elimination(group)

    def add_elimination(self, group: Elimination) -> None:
        group.solution_index = self.solution_index
        self.eliminations.append(group)
        self.solution_index += 1

    def add_single_candidate(self, single_candidate: SingleCandidate) -> None:
        single_candidate.solutionIndex = self.solution_index
        self.single_candidates.append(single_candidate)
        self.solution_index += 1

    def add_single_candidates(self, single_candidates: list[SingleCandidate]) -> None:
        for singleCandidate in single_candidates:
            self.add_single_candidate(singleCandidate)

    def serialize(self) -> dict:
        return {
            "isSolved": self.is_solved,
            "sudoku": self.initial_board.serialize(),
            "eliminations": [elimination.serialize() for elimination in self.eliminations],
            "singleCandidates": [single_candidate.serialize() for single_candidate in self.single_candidates]
        }
