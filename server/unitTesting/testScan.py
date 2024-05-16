import unittest

from models.board import Board
from models.elimination import Elimination
from models.numberedNote import NumberedNote
from models.numberedSquare import NumberedSquare
from techniques.scan import Scan


class TestScanTechnique(unittest.TestCase):
    def test_returns_none_for_empty_board(self):
        scan = Scan()
        board = Board(9)
        board.initialize_empty()

        solution = scan.get_next_solution(board)

        self.assertEqual(solution, None)

    def test_returns_elimination_in_row(self):
        scan = Scan()
        board = Board(9)
        board.initialize_empty()
        board.set_square(0, 0, 1)
        board.set_notes(0, 1, [1])

        solution = scan.get_next_solution(board)

        self.assertNotEqual(solution, None)
        self.assertEqual(solution.causing_square, NumberedSquare(0, 0, 1))
        self.assertEqual(solution.eliminated_notes, [NumberedNote(0, 1, 1)])

    def test_returns_elimination_in_column(self):
        scan = Scan()
        board = Board(9)
        board.initialize_empty()
        board.set_square(0, 0, 1)
        board.set_notes(1, 0, [1])

        solution = scan.get_next_solution(board)

        self.assertNotEqual(solution, None)
        self.assertEqual(solution.causing_square, NumberedSquare(0, 0, 1))
        self.assertEqual(solution.eliminated_notes, [NumberedNote(1, 0, 1)])

    def test_returns_elimination_in_box(self):
        scan = Scan()
        board = Board(9)
        board.initialize_empty()
        board.set_square(0, 0, 1)
        board.set_notes(1, 1, [1])

        solution = scan.get_next_solution(board)

        self.assertNotEqual(solution, None)
        self.assertEqual(solution.causing_square, NumberedSquare(0, 0, 1))
        self.assertEqual(solution.eliminated_notes, [NumberedNote(1, 1, 1)])


if __name__ == '__main__':
    unittest.main()
