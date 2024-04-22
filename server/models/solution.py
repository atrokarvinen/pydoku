from models.elimination import Elimination
from models.singleCandidate import SingleCandidate
from models.eliminationGroup import EliminationGroup


class Solution:
    def __init__(self, initial_board) -> None:
        self.eliminations = []
        self.elimination_groups = []
        self.single_candidates = []
        self.solution_index = 0
        self.initial_board = initial_board
        self.is_solved = False

    def add_elimination(self, elimination: Elimination) -> None:
        elimination.solutionIndex = self.solution_index
        self.eliminations.append(elimination)
        self.solution_index += 1

    def add_eliminations(self, eliminations: list[Elimination]) -> None:
        for elimination in eliminations:
            self.add_elimination(elimination)

    def add_elimination_groups(self, elimination_groups: list[EliminationGroup]) -> None:
        for group in elimination_groups:
            self.add_elimination_group(group)

    def add_elimination_group(self, group: EliminationGroup) -> None:
        group.solution_index = self.solution_index
        self.elimination_groups.append(group)
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
            "eliminationGroups": [elimination_group.serialize() for elimination_group in self.elimination_groups],
            "singleCandidates": [single_candidate.serialize() for single_candidate in self.single_candidates]
        }
