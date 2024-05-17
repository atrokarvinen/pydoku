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

    def test_returns_elimination_for_column(self):
        solver = NakedPair()
        board = Board(9)
        board.initialize_empty()
        board.set_notes(0, 0, [1, 2])
        board.set_notes(1, 0, [1, 2])
        board.set_notes(5, 0, [1])
        board.set_notes(6, 0, [2])

        solution = solver.get_next_solution(board)

        self.assertNotEqual(solution, None)
        self.assertListEqualNoOrder(solution.causing_notes, [
            NumberedNote(0, 0, 2), NumberedNote(0, 0, 1),
            NumberedNote(1, 0, 1), NumberedNote(1, 0, 2)])
        self.assertListEqualNoOrder(solution.eliminated_notes, [
            NumberedNote(5, 0, 1), NumberedNote(6, 0, 2)])

    def test_returns_elimination_for_box(self):
        solver = NakedPair()
        board = Board(9)
        board.initialize_empty()
        board.set_notes(0, 0, [1, 2])
        board.set_notes(1, 1, [1, 2])
        board.set_notes(0, 1, [1])
        board.set_notes(1, 0, [2])

        solution = solver.get_next_solution(board)

        self.assertNotEqual(solution, None)
        self.assertListEqualNoOrder(solution.causing_notes, [
            NumberedNote(0, 0, 2), NumberedNote(0, 0, 1),
            NumberedNote(1, 1, 1), NumberedNote(1, 1, 2)])
        self.assertListEqualNoOrder(solution.eliminated_notes, [
            NumberedNote(0, 1, 1), NumberedNote(1, 0, 2)])

    def test_returns_elimination_for_triple(self):
        solver = NakedPair()
        board = Board(9)
        board.initialize_empty()
        board.set_notes(0, 0, [1, 2, 3])
        board.set_notes(0, 1, [1, 2, 3])
        board.set_notes(0, 2, [1, 2, 3])
        board.set_notes(0, 5, [1])
        board.set_notes(0, 6, [2])
        board.set_notes(0, 7, [3])

        solution = solver.get_next_solution(board)

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
        solver = NakedPair()
        board = Board(9)
        board.initialize_empty()
        board.set_notes(0, 0, [1, 2])
        board.set_notes(0, 1, [2, 3])
        board.set_notes(0, 2, [1, 3])
        board.set_notes(0, 5, [1])
        board.set_notes(0, 6, [2])
        board.set_notes(0, 7, [3])

        solution = solver.get_next_solution(board)

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
        solver = NakedPair()
        board = Board(9)
        board.initialize_empty()
        board.set_notes(0, 0, [1, 2])
        board.set_notes(0, 1, [1, 9])
        board.set_notes(0, 5, [1])
        board.set_notes(0, 6, [2])

        solution = solver.get_next_solution(board)

        self.assertEqual(solution, None)
