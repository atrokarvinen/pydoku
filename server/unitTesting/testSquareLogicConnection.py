import unittest

from models.square import Square
from techniques.utils.squareLogic import SquareLogic
from unitTesting.customAsserts import CustomAsserts


class TestSquareLogicConnection(unittest.TestCase, CustomAsserts):
    def test_returns_strongly_connected_by_row(self):
        squares = [
            Square(0, 0, 0, 0, [1]),
            Square(0, 1, 0, 0, [1]),
        ]
        result = SquareLogic.is_strongly_connected_by_row(
            squares, squares[0], squares[1], 1)

        self.assertTrue(result)

    def test_returns_not_strongly_connected_by_row(self):
        squares = [
            Square(0, 0, 0, 0, [1]),
            Square(0, 1, 0, 0, [1]),
            Square(0, 2, 0, 0, [1]),
        ]
        result = SquareLogic.is_strongly_connected_by_row(
            squares, squares[0], squares[1], 1)

        self.assertFalse(result)

    def test_returns_strongly_connected_by_column(self):
        squares = [
            Square(0, 0, 0, 0, [1]),
            Square(1, 0, 0, 0, [1]),
        ]
        result = SquareLogic.is_strongly_connected_by_column(
            squares, squares[0], squares[1], 1)

        self.assertTrue(result)

    def test_returns_not_strongly_connected_by_column(self):
        squares = [
            Square(0, 0, 0, 0, [1]),
            Square(1, 0, 0, 0, [1]),
            Square(2, 0, 0, 0, [1]),
        ]
        result = SquareLogic.is_strongly_connected_by_column(
            squares, squares[0], squares[1], 1)

        self.assertFalse(result)

    def test_returns_strongly_connected_by_box(self):
        squares = [
            Square(0, 0, 0, 0, [1]),
            Square(1, 1, 0, 0, [1]),
        ]
        result = SquareLogic.is_strongly_connected_by_box(
            squares, squares[0], squares[1], 1)

        self.assertTrue(result)

    def test_returns_not_strongly_connected_by_box(self):
        squares = [
            Square(0, 0, 0, 0, [1]),
            Square(1, 1, 0, 0, [1]),
            Square(2, 2, 0, 0, [1]),
        ]
        result = SquareLogic.is_strongly_connected_by_box(
            squares, squares[0], squares[1], 1)

        self.assertFalse(result)

    def test_returns_strongly_connected(self):
        squares = [
            Square(0, 0, 0, 0, [1]),
            Square(0, 1, 0, 0, [1]),
            Square(1, 0, 0, 0, [1]),
        ]
        result = SquareLogic.is_strongly_connected(
            squares, squares[0], squares[1], 1)
        self.assertTrue(result)

    def test_returns_not_strongly_connected(self):
        squares = [
            Square(0, 0, 0, 0, [1]),
            Square(1, 0, 0, 0, [1]),
            Square(2, 0, 0, 0, [1]),
            Square(3, 0, 0, 0, [1]),
        ]

        result = SquareLogic.is_strongly_connected(
            squares, squares[0], squares[1], 1)

        self.assertFalse(result)
