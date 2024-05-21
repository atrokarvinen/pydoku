import unittest

from models.board import Board
from models.numberedNote import NumberedNote
from techniques.yWing import YWing
from unitTesting.customAsserts import CustomAsserts


class TestYWing(unittest.TestCase, CustomAsserts):
    def setUp(self) -> None:
        self.solver = YWing()
        self.board = Board(9)
        self.board.initialize_empty()

    def test_returns_elimination_when_y_wing_exists(self):
        self.board.set_notes(0, 1, [1, 2])
        self.board.set_notes(0, 5, [2, 3])
        self.board.set_notes(8, 1, [1, 3])
        self.board.set_notes(8, 5, [3])

        solution = self.solver.get_next_solution(self.board)

        self.assertNotEqual(solution, None)
        self.assertListEqualNoOrder(solution.causing_notes, [
            NumberedNote(0, 1, 1),
            NumberedNote(0, 1, 2),
            NumberedNote(0, 5, 2),
            NumberedNote(0, 5, 3),
            NumberedNote(8, 1, 1),
            NumberedNote(8, 1, 3),
        ])
        self.assertListEqualNoOrder(solution.eliminated_notes, [
            NumberedNote(8, 5, 3),
        ])

    def test_returns_none_when_pincers_do_not_share_number(self):
        self.board.set_notes(0, 1, [1, 2])
        self.board.set_notes(0, 5, [2, 5])
        self.board.set_notes(8, 1, [1, 6])
        self.board.set_notes(8, 5, [3])

        solution = self.solver.get_next_solution(self.board)

        self.assertEqual(solution, None)

    def test_returns_none_when_pincers_and_pivot_do_not_share_number(self):
        self.board.set_notes(0, 1, [1, 2])
        self.board.set_notes(0, 5, [3, 4])
        self.board.set_notes(8, 1, [5, 6])
        self.board.set_notes(8, 5, [3])

        solution = self.solver.get_next_solution(self.board)

        self.assertEqual(solution, None)

    def test_returns_none_when_pincers_and_pivot_have_too_many_same_numbers(self):
        self.board.set_notes(0, 1, [1, 2])
        self.board.set_notes(0, 5, [1, 3])
        self.board.set_notes(8, 1, [1, 3])
        self.board.set_notes(8, 5, [3])

        solution = self.solver.get_next_solution(self.board)

        self.assertEqual(solution, None)
