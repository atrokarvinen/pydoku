import unittest

from models.board import Board
from models.numberedNote import NumberedNote
from techniques.nakedPair import NakedPair
from unitTesting.customAsserts import CustomAsserts


class TestNakedPair(unittest.TestCase, CustomAsserts):
    def test_returns_elimination_for_row(self):
        solver = NakedPair()
        board = Board(9)
        board.initialize_empty()
        board.set_notes(0, 0, [1, 2])
        board.set_notes(0, 1, [1, 2])
        board.set_notes(0, 5, [1])
        board.set_notes(0, 6, [2])

        solution = solver.get_next_solution(board)

        self.assertNotEqual(solution, None)
        self.assertListEqualNoOrder(solution.causing_notes, [
            NumberedNote(0, 0, 2), NumberedNote(0, 0, 1),
            NumberedNote(0, 1, 1), NumberedNote(0, 1, 2)])
        self.assertListEqualNoOrder(solution.eliminated_notes, [
            NumberedNote(0, 5, 1), NumberedNote(0, 6, 2)])
