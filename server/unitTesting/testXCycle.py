import unittest

from models.board import Board
from models.numberedNote import NumberedNote
from techniques.xCycle import XCycle
from unitTesting.customAsserts import CustomAsserts


class TestXCycle(unittest.TestCase, CustomAsserts):
    def setUp(self):
        self.solver = XCycle()
        self.board = Board(9)
        self.board.initialize_empty()

    def test_x_cycle(self):
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

        self.board.set_notes(6, 3, [1])
        self.board.set_notes(6, 5, [1])
        self.board.set_notes(6, 7, [1])

        self.board.set_notes(7, 1, [1])
        self.board.set_notes(7, 4, [1])

        self.board.set_notes(8, 1, [1])
        self.board.set_notes(8, 7, [1])

        solution = self.solver.get_next_solution(self.board)

        self.assertNotEqual(solution, None)
        self.assertListEqualNoOrder(solution.causing_notes, [
            NumberedNote(1, 4, 1),
            NumberedNote(1, 7, 1),
            NumberedNote(7, 1, 1),
            NumberedNote(7, 4, 1),
            NumberedNote(8, 1, 1),
            NumberedNote(8, 7, 1),
        ])
        self.assertListEqualNoOrder(solution.eliminated_notes, [
            NumberedNote(2, 1, 1),
            NumberedNote(0, 4, 1),
            NumberedNote(2, 7, 1),
            NumberedNote(3, 4, 1),
            NumberedNote(6, 7, 1),
        ])
