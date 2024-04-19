from models.elimination import Elimination
from models.singleCandidate import SingleCandidate


class Solution:
    def __init__(self) -> None:
        self.eliminations = []
        self.singleCandidates = []
        self.solutionIndex = 0

    def add_elimination(self, elimination: Elimination) -> None:
        elimination.solutionIndex = self.solutionIndex
        self.eliminations.append(elimination)
        self.solutionIndex += 1

    def add_eliminations(self, eliminations: list[Elimination]) -> None:
        for elimination in eliminations:
            self.add_elimination(elimination)

    def add_single_candidate(self, singleCandidate: SingleCandidate) -> None:
        singleCandidate.solutionIndex = self.solutionIndex
        self.singleCandidates.append(singleCandidate)
        self.solutionIndex += 1

    def add_single_candidates(self, singleCandidates: list[SingleCandidate]) -> None:
        for singleCandidate in singleCandidates:
            self.add_single_candidate(singleCandidate)

    def serialize(self) -> dict:
        return {
            "eliminations": [elimination.serialize() for elimination in self.eliminations],
            "singleCandidates": [singleCandidate.serialize() for singleCandidate in self.singleCandidates]
        }
