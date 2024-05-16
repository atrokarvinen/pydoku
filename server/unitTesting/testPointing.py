import unittest

from models.board import Board
from models.numberedNote import NumberedNote
from techniques.pointing import Pointing
from unitTesting.customAsserts import CustomAsserts


class TestPointingTechnique(unittest.TestCase, CustomAsserts):
    def test_returns_elimination_for_row(self):
        solver = Pointing()
        board = Board(9)
        board.initialize_empty()
        board.set_notes(0, 0, [1])
        board.set_notes(0, 1, [1])
        board.set_notes(0, 5, [1])
        board.set_notes(0, 6, [1])

        solution = solver.get_next_solution(board)

        self.assertNotEqual(solution, None)
        self.assertListEqualNoOrder(solution.causing_notes, [
            NumberedNote(0, 0, 1), NumberedNote(0, 1, 1)])
        self.assertListEqualNoOrder(solution.eliminated_notes, [
            NumberedNote(0, 5, 1), NumberedNote(0, 6, 1)])

    def test_returns_elimination_for_column(self):
        solver = Pointing()
        board = Board(9)
        board.initialize_empty()
        board.set_notes(0, 0, [1])
        board.set_notes(1, 0, [1])
        board.set_notes(5, 0, [1])
        board.set_notes(6, 0, [1])

        solution = solver.get_next_solution(board)

        self.assertNotEqual(solution, None)
        self.assertListEqualNoOrder(solution.causing_notes, [
            NumberedNote(0, 0, 1), NumberedNote(1, 0, 1)])
        self.assertListEqualNoOrder(solution.eliminated_notes, [
            NumberedNote(5, 0, 1), NumberedNote(6, 0, 1)])

    def test_returns_none_when_only_one_note_points(self):
        solver = Pointing()
        board = Board(9)
        board.initialize_empty()
        board.set_notes(0, 0, [1])
        board.set_notes(6, 0, [1])

        solution = solver.get_next_solution(board)

        self.assertEqual(solution, None)

    def test_returns_none_when_too_many_notes_point(self):
        solver = Pointing()
        board = Board(9)
        board.initialize_empty()
        board.set_notes(0, 0, [1])
        board.set_notes(0, 1, [1])
        board.set_notes(1, 1, [1])
        board.set_notes(0, 5, [1])
        board.set_notes(0, 6, [1])

        solution = solver.get_next_solution(board)

        self.assertEqual(solution, None)
