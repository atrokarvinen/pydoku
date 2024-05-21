import unittest

from models.board import Board
from models.numberedNote import NumberedNote
from techniques.xWing import XWing
from unitTesting.customAsserts import CustomAsserts


class TestXWing(unittest.TestCase, CustomAsserts):
    def setUp(self) -> None:
        self.solver = XWing()
        self.board = Board(9)
        self.board.initialize_empty()

    def test_returns_column_elimination_when_x_wing_exists(self):
        self.board.set_notes(0, 0, [1])
        self.board.set_notes(3, 0, [1])
        self.board.set_notes(0, 3, [1])
        self.board.set_notes(3, 3, [1])

        self.board.set_notes(1, 0, [1])

        solution = self.solver.get_next_solution(self.board)

        self.assertNotEqual(solution, None)
        self.assertListEqualNoOrder(solution.causing_notes, [
            NumberedNote(0, 0, 1),
            NumberedNote(3, 0, 1),
            NumberedNote(0, 3, 1),
            NumberedNote(3, 3, 1),
        ])
        self.assertListEqualNoOrder(solution.eliminated_notes, [
            NumberedNote(1, 0, 1),
        ])

    def test_returns_row_elimination_when_x_wing_exists(self):
        self.board.set_notes(0, 0, [1])
        self.board.set_notes(3, 0, [1])
        self.board.set_notes(0, 3, [1])
        self.board.set_notes(3, 3, [1])

        self.board.set_notes(0, 1, [1])

        solution = self.solver.get_next_solution(self.board)

        self.assertNotEqual(solution, None)
        self.assertListEqualNoOrder(solution.causing_notes, [
            NumberedNote(0, 0, 1),
            NumberedNote(3, 0, 1),
            NumberedNote(0, 3, 1),
            NumberedNote(3, 3, 1),
        ])
        self.assertListEqualNoOrder(solution.eliminated_notes, [
            NumberedNote(0, 1, 1),
        ])

    def test_returns_none_when_notes_not_in_rectangle(self):
        self.board.set_notes(0, 0, [1])
        self.board.set_notes(3, 0, [1])
        self.board.set_notes(0, 4, [1])
        self.board.set_notes(3, 3, [1])

        self.board.set_notes(1, 0, [1])

        solution = self.solver.get_next_solution(self.board)

        self.assertEqual(solution, None)

    def test_returns_none_when_too_many_notes_in_region(self):
        self.board.set_notes(0, 0, [1])
        self.board.set_notes(3, 0, [1])
        self.board.set_notes(4, 0, [1])
        self.board.set_notes(0, 3, [1])
        self.board.set_notes(0, 4, [1])
        self.board.set_notes(3, 3, [1])

        self.board.set_notes(1, 0, [1])

        solution = self.solver.get_next_solution(self.board)

        self.assertEqual(solution, None)
