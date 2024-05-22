import unittest

from models.square import Square
from techniques.utils.cycleFinder import CycleFinder
from unitTesting.customAsserts import CustomAsserts


class TestCycleFinder(unittest.TestCase, CustomAsserts):
    def setUp(self) -> None:
        self.finder = CycleFinder()

    def test_finds_cycle(self):
        squares = [
            Square(0, 0, 0, 0, [1]),
            Square(1, 0, 0, 0, [1]),
            Square(2, 0, 0, 0, [1]),
            Square(3, 0, 0, 0, [1]),
        ]

        cycles = self.finder.find_cycles(squares, 1)

        self.assertGreater(len(cycles), 0)
