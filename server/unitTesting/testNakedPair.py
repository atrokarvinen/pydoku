import unittest

from models.board import Board
from models.numberedNote import NumberedNote
from techniques.nakedPair import NakedPair
from unitTesting.customAsserts import CustomAsserts


class TestNakedPair(unittest.TestCase, CustomAsserts):
    def setUp(self) -> None:
        self.solver = NakedPair()
        self.board = Board(9)
        self.board.initialize_empty()

    def test_returns_elimination_for_row(self):
        self.board.set_notes(0, 0, [1, 2])
        self.board.set_notes(0, 1, [1, 2])
        self.board.set_notes(0, 5, [1])
        self.board.set_notes(0, 6, [2])

        solution = self.solver.get_next_solution(self.board)

        self.assertNotEqual(solution, None)
        self.assertListEqualNoOrder(solution.causing_notes, [
            NumberedNote(0, 0, 2), NumberedNote(0, 0, 1),
            NumberedNote(0, 1, 1), NumberedNote(0, 1, 2)])
        self.assertListEqualNoOrder(solution.eliminated_notes, [
            NumberedNote(0, 5, 1), NumberedNote(0, 6, 2)])

    def test_returns_elimination_for_column(self):
        self.board.initialize_empty()
        self.board.set_notes(0, 0, [1, 2])
        self.board.set_notes(1, 0, [1, 2])
        self.board.set_notes(5, 0, [1])
        self.board.set_notes(6, 0, [2])

        solution = self.solver.get_next_solution(self.board)

        self.assertNotEqual(solution, None)
        self.assertListEqualNoOrder(solution.causing_notes, [
            NumberedNote(0, 0, 2), NumberedNote(0, 0, 1),
            NumberedNote(1, 0, 1), NumberedNote(1, 0, 2)])
        self.assertListEqualNoOrder(solution.eliminated_notes, [
            NumberedNote(5, 0, 1), NumberedNote(6, 0, 2)])

    def test_returns_elimination_for_box(self):
        self.board.set_notes(0, 0, [1, 2])
        self.board.set_notes(1, 1, [1, 2])
        self.board.set_notes(0, 1, [1])
        self.board.set_notes(1, 0, [2])

        solution = self.solver.get_next_solution(self.board)

        self.assertNotEqual(solution, None)
        self.assertListEqualNoOrder(solution.causing_notes, [
            NumberedNote(0, 0, 2), NumberedNote(0, 0, 1),
            NumberedNote(1, 1, 1), NumberedNote(1, 1, 2)])
        self.assertListEqualNoOrder(solution.eliminated_notes, [
            NumberedNote(0, 1, 1), NumberedNote(1, 0, 2)])

    def test_returns_elimination_for_triple(self):
        self.board.set_notes(0, 0, [1, 2, 3])
        self.board.set_notes(0, 1, [1, 2, 3])
        self.board.set_notes(0, 2, [1, 2, 3])
        self.board.set_notes(0, 5, [1])
        self.board.set_notes(0, 6, [2])
        self.board.set_notes(0, 7, [3])

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
            NumberedNote(0, 2, 3),
        ])
        self.assertListEqualNoOrder(solution.eliminated_notes, [
            NumberedNote(0, 5, 1), NumberedNote(0, 6, 2), NumberedNote(0, 7, 3)])

    def test_returns_elimination_for_partial_triple(self):
        self.board.set_notes(0, 0, [1, 2])
        self.board.set_notes(0, 1, [2, 3])
        self.board.set_notes(0, 2, [1, 3])
        self.board.set_notes(0, 5, [1])
        self.board.set_notes(0, 6, [2])
        self.board.set_notes(0, 7, [3])

        solution = self.solver.get_next_solution(self.board)

        self.assertNotEqual(solution, None)
        self.assertListEqualNoOrder(solution.causing_notes, [
            NumberedNote(0, 0, 1),
            NumberedNote(0, 0, 2),
            NumberedNote(0, 1, 2),
            NumberedNote(0, 1, 3),
            NumberedNote(0, 2, 1),
            NumberedNote(0, 2, 3),
        ])
        self.assertListEqualNoOrder(solution.eliminated_notes, [
            NumberedNote(0, 5, 1), NumberedNote(0, 6, 2), NumberedNote(0, 7, 3)])

    def test_returns_none_when_no_pair(self):
        self.board.set_notes(0, 0, [1, 2])
        self.board.set_notes(0, 1, [1, 9])
        self.board.set_notes(0, 5, [1])
        self.board.set_notes(0, 6, [2])

        solution = self.solver.get_next_solution(self.board)

        self.assertEqual(solution, None)
