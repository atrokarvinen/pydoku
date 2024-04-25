from models.board import Board
from models.solutionStep import SolutionStep


class SolverBase:
    def get_next_solution(self, board: Board) -> SolutionStep:
        raise NotImplementedError
