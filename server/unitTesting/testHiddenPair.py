import unittest

from models.board import Board
from models.numberedNote import NumberedNote
from techniques.hiddenPair import HiddenPair
from unitTesting.customAsserts import CustomAsserts


class TestHiddenPair(unittest.TestCase, CustomAsserts):
    def setUp(self) -> None:
        self.solver = HiddenPair()
        self.board = Board(9)
        self.board.initialize_empty()

    def test_returns_elimination_for_row(self):
        self.board.set_notes(0, 0, [1, 2, 9])
        self.board.set_notes(0, 1, [1, 2, 9])
        self.board.set_notes(0, 7, [9])
        self.board.set_notes(7, 0, [9])
        self.board.set_notes(1, 1, [9])

        solution = self.solver.get_next_solution(self.board)

        self.assertNotEqual(solution, None)
        self.assertListEqualNoOrder(solution.causing_notes, [
            NumberedNote(0, 0, 2), NumberedNote(0, 0, 1),
            NumberedNote(0, 1, 1), NumberedNote(0, 1, 2)])
        self.assertListEqualNoOrder(solution.eliminated_notes, [
            NumberedNote(0, 0, 9), NumberedNote(0, 1, 9)])

    def test_returns_elimination_for_column(self):
        self.board.set_notes(0, 0, [1, 2, 9])
        self.board.set_notes(1, 0, [1, 2, 9])
        self.board.set_notes(0, 7, [9])
        self.board.set_notes(7, 0, [9])
        self.board.set_notes(1, 1, [9])

        solution = self.solver.get_next_solution(self.board)

        self.assertNotEqual(solution, None)
        self.assertListEqualNoOrder(solution.causing_notes, [
            NumberedNote(0, 0, 2), NumberedNote(0, 0, 1),
            NumberedNote(1, 0, 1), NumberedNote(1, 0, 2)])
        self.assertListEqualNoOrder(solution.eliminated_notes, [
            NumberedNote(0, 0, 9), NumberedNote(1, 0, 9)])

    def test_returns_elimination_for_box(self):
        self.board.set_notes(0, 0, [1, 2, 9])
        self.board.set_notes(1, 1, [1, 2, 9])
        self.board.set_notes(0, 7, [9])
        self.board.set_notes(7, 0, [9])
        self.board.set_notes(2, 2, [9])

        solution = self.solver.get_next_solution(self.board)

        self.assertNotEqual(solution, None)
        self.assertListEqualNoOrder(solution.causing_notes, [
            NumberedNote(0, 0, 2), NumberedNote(0, 0, 1),
            NumberedNote(1, 1, 1), NumberedNote(1, 1, 2)])
        self.assertListEqualNoOrder(solution.eliminated_notes, [
            NumberedNote(0, 0, 9), NumberedNote(1, 1, 9)])

    def test_returns_elimination_for_triple(self):
        self.board.set_notes(0, 0, [1, 2, 3, 9])
        self.board.set_notes(0, 1, [1, 2, 3, 9])
        self.board.set_notes(0, 2, [1, 2, 3, 9])
        self.board.set_notes(0, 7, [9])
        self.board.set_notes(7, 0, [9])
        self.board.set_notes(1, 1, [9])

        solution = self.solver.get_next_solution(self.board)

        self.assertNotEqual(solution, None)
        self.assertListEqualNoOrder(solution.causing_notes, [
            NumberedNote(0, 0, 1),
            NumberedNote(0, 0, 2),
            NumberedNote(0, 0, 3),
            NumberedNote(0, 1, 1),
            NumberedNote(0, 1, 2),
            NumberedNote(0, 1, 3),
            NumberedNote(0, 2, 1),
            NumberedNote(0, 2, 2),
            NumberedNote(0, 2, 3)])

        self.assertListEqualNoOrder(solution.eliminated_notes, [
            NumberedNote(0, 0, 9), NumberedNote(0, 1, 9), NumberedNote(0, 2, 9)])

    def test_returns_elimination_for_partial_triple(self):
        self.board.set_notes(0, 0, [1, 2, 9])
        self.board.set_notes(0, 1, [1, 3, 9])
        self.board.set_notes(0, 2, [2, 3, 9])
        self.board.set_notes(0, 7, [9])
        self.board.set_notes(7, 0, [9])
        self.board.set_notes(1, 1, [9])

        solution = self.solver.get_next_solution(self.board)

        self.assertNotEqual(solution, None)
        self.assertListEqualNoOrder(solution.causing_notes, [
            NumberedNote(0, 0, 1), NumberedNote(0, 0, 2),
            NumberedNote(0, 1, 1), NumberedNote(0, 1, 3),
            NumberedNote(0, 2, 2), NumberedNote(0, 2, 3)])
        self.assertListEqualNoOrder(solution.eliminated_notes, [
            NumberedNote(0, 0, 9), NumberedNote(0, 1, 9), NumberedNote(0, 2, 9)])

    def test_returns_none_for_no_pair(self):
        self.board.set_notes(0, 0, [1, 2, 9])
        self.board.set_notes(0, 1, [1, 9, 8])
        self.board.set_notes(1, 0, [1, 9, 8])
        self.board.set_notes(1, 1, [1, 9, 8])

        self.board.set_notes(7, 0, [1, 2, 9])
        self.board.set_notes(7, 1, [1, 9, 8])
        self.board.set_notes(8, 0, [1, 9, 8])
        self.board.set_notes(8, 1, [1, 9, 8])

        self.board.set_notes(0, 7, [1, 2, 9])
        self.board.set_notes(0, 8, [1, 9, 8])
        self.board.set_notes(1, 7, [1, 9, 8])
        self.board.set_notes(1, 8, [1, 9, 8])

        self.board.set_notes(7, 7, [1, 2, 9])
        self.board.set_notes(7, 8, [1, 9, 8])
        self.board.set_notes(8, 7, [1, 9, 8])
        self.board.set_notes(8, 8, [1, 9, 8])

        solution = self.solver.get_next_solution(self.board)

        self.assertEqual(solution, None)
