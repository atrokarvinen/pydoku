import unittest

from models.square import Square
from techniques.emptyRectangle import EmptyRectangle
from techniques.models.emptyRectangleModel import EmptyRectangleModel
from techniques.utils.squareLogic import SquareLogic
from unitTesting.customAsserts import CustomAsserts


class TestEmptyRectangleGet(unittest.TestCase, CustomAsserts):
    def setUp(self) -> None:
        self.solver = EmptyRectangle()

    def test_squares_form_empty_rectangle_two_squares(self):
        square1 = Square(1, 1, 0, 0)
        square2 = Square(2, 2, 0, 0)
        squares = [square1, square2]

        rectangles = self.solver.get_empty_rectangles(squares, 1)

        self.assertNotEqual(rectangles, None)
        self.assertEqual(rectangles, [
            EmptyRectangleModel(1, 2, 0, 1, []),
            EmptyRectangleModel(2, 1, 0, 1, []),
        ])

    def test_squares_form_empty_rectangle_five_squares(self):
        square1 = Square(0, 0, 0, 0)
        square2 = Square(0, 1, 0, 0)
        square3 = Square(0, 2, 0, 0)
        square4 = Square(1, 0, 0, 0)
        square5 = Square(2, 0, 0, 0)
        squares = [square1, square2, square3, square4, square5]

        rectangles = self.solver.get_empty_rectangles(squares, 1)

        self.assertListEqualNoOrder(rectangles, [
            EmptyRectangleModel(0, 0, 0, 1, []),
        ])

    def test_squares_do_not_form_empty_rectangle_all_same_row(self):
        square1 = Square(0, 0, 0, 0)
        square2 = Square(0, 1, 0, 0)
        square3 = Square(0, 2, 0, 0)
        squares = [square1, square2, square3]

        rectangles = self.solver.get_empty_rectangles(squares, 1)

        self.assertEqual(rectangles, [])

    def test_squares_do_not_form_empty_rectangle_not_in_line(self):
        square1 = Square(0, 0, 0, 0)
        square2 = Square(1, 1, 0, 0)
        square3 = Square(2, 2, 0, 0)
        squares = [square1, square2, square3]

        rectangles = self.solver.get_empty_rectangles(squares, 1)

        self.assertEqual(rectangles, [])

    def test_squares_do_not_form_empty_rectangle_two_lines(self):
        square1 = Square(0, 0, 0, 0)
        square2 = Square(0, 1, 0, 0)
        square3 = Square(1, 0, 0, 0)
        square4 = Square(1, 1, 0, 0)
        squares = [square1, square2, square3, square4]

        rectangles = self.solver.get_empty_rectangles(squares, 1)

        self.assertEqual(rectangles, [])
