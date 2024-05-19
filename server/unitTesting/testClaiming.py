import unittest

from models.board import Board
from models.numberedNote import NumberedNote
from techniques.claiming import Claiming
from unitTesting.customAsserts import CustomAsserts


class TestClaiming(unittest.TestCase, CustomAsserts):
    def setUp(self) -> None:
        self.solver = Claiming()
        self.board = Board(9)
        self.board.initialize_empty()

    def test_returns_elimination_for_row(self):
        self.board.set_notes(0, 0, [1])
        self.board.set_notes(0, 1, [1])
        self.board.set_notes(0, 2, [1])
        self.board.set_notes(1, 1, [1])
        self.board.set_notes(7, 1, [1])

        solution = self.solver.get_next_solution(self.board)

        self.assertNotEqual(solution, None)
        self.assertListEqualNoOrder(solution.causing_notes, [
            NumberedNote(0, 0, 1),
            NumberedNote(0, 1, 1),
            NumberedNote(0, 2, 1)])
        self.assertListEqualNoOrder(solution.eliminated_notes, [
                                    NumberedNote(1, 1, 1)])

    def test_returns_elimination_for_column(self):
        self.board.set_notes(0, 0, [1])
        self.board.set_notes(1, 0, [1])
        self.board.set_notes(2, 0, [1])
        self.board.set_notes(1, 1, [1])
        self.board.set_notes(1, 7, [1])

        solution = self.solver.get_next_solution(self.board)

        self.assertNotEqual(solution, None)
        self.assertListEqualNoOrder(solution.causing_notes, [
            NumberedNote(0, 0, 1),
            NumberedNote(1, 0, 1),
            NumberedNote(2, 0, 1)])
        self.assertListEqualNoOrder(solution.eliminated_notes, [
                                    NumberedNote(1, 1, 1)])

    def test_returns_none_when_no_elimination(self):
        self.board.set_notes(0, 0, [1])
        self.board.set_notes(0, 1, [1])
        self.board.set_notes(0, 2, [1])

        solution = self.solver.get_next_solution(self.board)

        self.assertEqual(solution, None)

    def test_returns_none_when_claiming_unavailable(self):
        self.board.set_notes(0, 0, [1])
        self.board.set_notes(0, 1, [1])
        self.board.set_notes(1, 0, [1])
        self.board.set_notes(1, 1, [1])

        self.board.set_notes(2, 2, [1])

        self.board.set_notes(0, 7, [1])
        self.board.set_notes(1, 7, [1])
        self.board.set_notes(7, 0, [1])
        self.board.set_notes(7, 1, [1])

        solution = self.solver.get_next_solution(self.board)

        self.assertEqual(solution, None)
