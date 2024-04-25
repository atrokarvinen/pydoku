from models.board import Board


class SolutionStep:
    def apply(self, board: Board) -> Board:
        raise NotImplementedError

    def is_elimination(self) -> bool:
        raise NotImplementedError
