import unittest

from models.board import Board
from techniques.utils.squareConnectionLookup import SquareConnectionLookup
from techniques.utils.squareLookup import SquareLookup


class TestSquareConnectionLookup(unittest.TestCase):
    def setUp(self) -> None:
        self.board = Board(9)
        self.board.initialize_empty()

    def test_returns(self):
        self.board.set_notes(0, 0, [1])
        self.board.set_notes(0, 1, [1])
        self.board.set_notes(1, 0, [1])
        self.board.set_notes(1, 1, [1])

        lookup = SquareLookup(self.board)
        conn_lookup = SquareConnectionLookup(lookup)

        pass
