import copy
from models.board import Board
from models.elimination import Elimination
from techniques.eliminatorBase import EliminatorBase


class XCycle(EliminatorBase):
    def get_next_solution(self, board: Board) -> Elimination:
        return None

    def get_loops(self, board: Board):
        empty_squares = board.flatten_empty()
        boardRange = board.get_range()
        for number in boardRange:
            squares_with_note = [
                s for s in empty_squares if number in s.possible_numbers]
            if len(squares_with_note) < 4:
                continue
            loops = []
            for start_square in squares_with_note:
                is_explored = self.square_in_loops(loops, start_square)
                if is_explored:
                    continue

                loop = []
                all_squares = copy.deepcopy(squares_with_note)
                possible_squares = squares_with_note
                if (len(loop) < 2):
                    continue

                loops.append(loop)

        return None

    def square_in_loops(self, loops, square):
        for loop in loops:
            if square in loop:
                return True
        return False

    def detect_eliminations(self, board: Board, loops):
        # If seen by two weak links, eliminate number
        return None
