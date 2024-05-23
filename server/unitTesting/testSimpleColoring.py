import unittest

from models.board import Board
from models.numberedNote import NumberedNote
from techniques.simpleColoring import SimpleColoring
from unitTesting.customAsserts import CustomAsserts


class TestSimpleColoring(unittest.TestCase, CustomAsserts):
    def setUp(self) -> None:
        self.solver = SimpleColoring()
        self.board = Board(9)
        self.board.initialize_empty()

    def test_color_conflicts_returns_elimination(self):
        self.board.set_notes(0, 1, [1])
        self.board.set_notes(0, 2, [1])
        self.board.set_notes(0, 5, [1])

        self.board.set_notes(1, 1, [1])
        self.board.set_notes(1, 3, [1])

        self.board.set_notes(3, 2, [1])
        self.board.set_notes(3, 3, [1])

        self.board.set_notes(4, 1, [1])
        self.board.set_notes(4, 6, [1])

        self.board.set_notes(5, 5, [1])
        self.board.set_notes(5, 6, [1])

        solution = self.solver.get_next_solution(self.board)

        self.assertNotEqual(solution, None)
        self.assertListEqualNoOrder(solution.causing_notes, [
            NumberedNote(1, 3, 1),
            NumberedNote(3, 2, 1),
            NumberedNote(4, 6, 1),
            NumberedNote(5, 5, 1),
        ])
        self.assertListEqualNoOrder(solution.eliminated_notes, [
            NumberedNote(0, 2, 1),
            NumberedNote(0, 5, 1),
            NumberedNote(1, 1, 1),
            NumberedNote(3, 3, 1),
            NumberedNote(4, 1, 1),
            NumberedNote(5, 6, 1),
        ])

    def test_seen_by_both_colors_returns_elimination(self):
        self.board.set_notes(0, 0, [1])
        self.board.set_notes(0, 5, [1])
        self.board.set_notes(0, 8, [1])

        self.board.set_notes(1, 1, [1])
        self.board.set_notes(1, 3, [1])

        self.board.set_notes(2, 0, [1])
        self.board.set_notes(2, 6, [1])
        self.board.set_notes(2, 7, [1])

        self.board.set_notes(4, 6, [1])
        self.board.set_notes(4, 7, [1])
        self.board.set_notes(4, 8, [1])

        self.board.set_notes(6, 1, [1])
        self.board.set_notes(6, 6, [1])
        self.board.set_notes(6, 7, [1])
        self.board.set_notes(6, 8, [1])

        self.board.set_notes(7, 3, [1])
        self.board.set_notes(7, 6, [1])

        self.board.set_notes(8, 0, [1])
        self.board.set_notes(8, 5, [1])
        self.board.set_notes(8, 6, [1])

        solution = self.solver.get_next_solution(self.board)

        self.assertNotEqual(solution, None)
        self.assertListEqualNoOrder(solution.causing_notes, [
            NumberedNote(0, 5, 1),
            NumberedNote(1, 1, 1),
            NumberedNote(1, 3, 1),
            NumberedNote(6, 1, 1),
            NumberedNote(7, 3, 1),
            NumberedNote(7, 6, 1),
            NumberedNote(8, 0, 1),
            NumberedNote(8, 5, 1),
        ])
        self.assertListEqualNoOrder(solution.eliminated_notes, [
            NumberedNote(8, 6, 1),
        ])

    def test_returns_none_when_no_cycle_found(self):
        self.board.set_notes(0, 0, [1])
        self.board.set_notes(0, 4, [1])
        self.board.set_notes(0, 5, [1])

        self.board.set_notes(1, 4, [1])
        self.board.set_notes(1, 7, [1])

        self.board.set_notes(2, 1, [1])
        self.board.set_notes(2, 3, [1])
        self.board.set_notes(2, 5, [1])
        self.board.set_notes(2, 6, [1])
        self.board.set_notes(2, 7, [1])

        self.board.set_notes(3, 3, [1])
        self.board.set_notes(3, 4, [1])
        self.board.set_notes(3, 5, [1])

        self.board.set_notes(4, 6, [1])
        self.board.set_notes(4, 8, [1])

        self.board.set_notes(6, 1, [1])
        self.board.set_notes(6, 3, [1])
        self.board.set_notes(6, 5, [1])
        self.board.set_notes(6, 6, [1])
        self.board.set_notes(6, 7, [1])

        self.board.set_notes(7, 0, [1])
        self.board.set_notes(7, 1, [1])
        self.board.set_notes(7, 4, [1])

        self.board.set_notes(8, 1, [1])
        self.board.set_notes(8, 7, [1])
        self.board.set_notes(8, 8, [1])

        solution = self.solver.get_next_solution(self.board)

        self.assertEqual(solution, None)
