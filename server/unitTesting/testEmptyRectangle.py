import unittest

from models.board import Board
from models.numberedNote import NumberedNote
from techniques.emptyRectangle import EmptyRectangle
from unitTesting.customAsserts import CustomAsserts


class TestEmptyRectangle(unittest.TestCase, CustomAsserts):
    def setUp(self) -> None:
        self.solver = EmptyRectangle()
        self.board = Board(9)
        self.board.initialize_empty()

    def test_returns_elimination_when_empty_rectangle_exists_with_two_numbers(self):
        self.board.set_notes(4, 4, [1])
        self.board.set_notes(5, 1, [1])
        self.board.set_notes(5, 5, [1])
        self.board.set_notes(6, 1, [1])

        self.board.set_notes(6, 4, [1])

        solution = self.solver.get_next_solution(self.board)

        self.assertNotEqual(solution, None)
        self.assertListEqualNoOrder(solution.causing_notes, [
            NumberedNote(4, 4, 1),
            NumberedNote(5, 1, 1),
            NumberedNote(5, 5, 1),
            NumberedNote(6, 1, 1),
        ])
        self.assertListEqualNoOrder(solution.eliminated_notes, [
            NumberedNote(6, 4, 1)
        ])

    def test_returns_elimination_when_empty_rectangle_exists_with_five_numbers(self):
        self.board.set_notes(3, 3, [1])
        self.board.set_notes(3, 4, [1])
        self.board.set_notes(3, 5, [1])
        self.board.set_notes(4, 5, [1])
        self.board.set_notes(5, 5, [1])

        self.board.set_notes(7, 5, [1])
        self.board.set_notes(7, 8, [1])

        self.board.set_notes(0, 8, [1])
        self.board.set_notes(3, 8, [1])

        solution = self.solver.get_next_solution(self.board)

        self.assertNotEqual(solution, None)
        self.assertListEqualNoOrder(solution.causing_notes, [
            NumberedNote(3, 3, 1),
            NumberedNote(3, 4, 1),
            NumberedNote(3, 5, 1),
            NumberedNote(4, 5, 1),
            NumberedNote(5, 5, 1),
            NumberedNote(7, 5, 1),
            NumberedNote(7, 8, 1),
        ])
        self.assertListEqualNoOrder(solution.eliminated_notes, [
            NumberedNote(3, 8, 1)
        ])

    def test_returns_none_when_candidate_sees_wrong_side_of_rectangle(self):
        self.board.set_notes(0, 6, [1])
        self.board.set_notes(0, 7, [1])
        self.board.set_notes(0, 8, [1])
        self.board.set_notes(1, 8, [1])

        self.board.set_notes(0, 1, [1])
        self.board.set_notes(5, 1, [1])

        self.board.set_notes(5, 6, [1])
        self.board.set_notes(5, 2, [1])

        solution = self.solver.get_next_solution(self.board)

        self.assertEqual(solution, None)
