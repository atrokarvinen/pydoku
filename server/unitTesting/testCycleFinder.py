import unittest

from models.board import Board
from models.square import Square
from techniques.utils.cycleFinder import CycleFinder
from techniques.utils.squareConnectionLookup import SquareConnectionLookup
from techniques.utils.squareLookup import SquareLookup
from unitTesting.customAsserts import CustomAsserts


class TestCycleFinder(unittest.TestCase, CustomAsserts):
    def setUp(self) -> None:
        self.board = Board(9)
        self.board.initialize_empty()
        lookup = SquareLookup(self.board)
        conn_lookup = SquareConnectionLookup(lookup)
        self.finder = CycleFinder(lookup, conn_lookup)

    def test_finds_no_cycle_when_two_strong_links(self):
        self.board.set_notes(0, 0, [1])
        self.board.set_notes(8, 0, [1])
        self.board.set_notes(8, 8, [1])
        self.board.set_notes(0, 8, [1])
        lookup = SquareLookup(self.board)
        conn_lookup = SquareConnectionLookup(lookup)
        self.finder = CycleFinder(lookup, conn_lookup)

        cycles = self.finder.find_cycles(1)

        self.assertEqual(len(cycles), 0)

    def test_finds_no_cycle_when_two_weak_links(self):
        self.board.set_notes(0, 0, [1])
        self.board.set_notes(4, 0, [1])
        self.board.set_notes(8, 0, [1])
        self.board.set_notes(0, 4, [1])
        self.board.set_notes(0, 8, [1])
        self.board.set_notes(4, 4, [1])
        self.board.set_notes(4, 8, [1])
        self.board.set_notes(8, 4, [1])
        self.board.set_notes(8, 8, [1])
        lookup = SquareLookup(self.board)
        conn_lookup = SquareConnectionLookup(lookup)
        self.finder = CycleFinder(lookup, conn_lookup)

        cycles = self.finder.find_cycles(1)

        self.assertCountEqual(cycles, [])

    def test_finds_nice_cycle(self):
        self.board.set_notes(0, 0, [1])
        self.board.set_notes(8, 0, [1])
        self.board.set_notes(8, 4, [1])
        self.board.set_notes(8, 8, [1])
        self.board.set_notes(0, 8, [1])
        self.board.set_notes(0, 4, [1])

        lookup = SquareLookup(self.board)
        conn_lookup = SquareConnectionLookup(lookup)
        self.finder = CycleFinder(lookup, conn_lookup)

        cycles = self.finder.find_cycles(1)

        cycle_list = [c.to_list_string() for c in cycles]
        expected_str = "(0, 0) -> (0, 8) -> (8, 8) -> (8, 0) -> (0, 0)"
        self.assertIn(expected_str, cycle_list)
        index = cycle_list.index(expected_str)
        cycle = cycles[index]
        self.assertEqual(cycle.is_nice(), True)

    def test_find_discontinuous_weak_cycle(self):
        self.board.set_notes(0, 0, [1])
        self.board.set_notes(0, 4, [1])
        self.board.set_notes(0, 7, [1])
        self.board.set_notes(4, 0, [1])
        self.board.set_notes(4, 4, [1])
        self.board.set_notes(4, 8, [1])
        self.board.set_notes(8, 0, [1])
        self.board.set_notes(6, 6, [1])
        self.board.set_notes(7, 7, [1])
        self.board.set_notes(8, 8, [1])

        lookup = SquareLookup(self.board)
        conn_lookup = SquareConnectionLookup(lookup)
        self.finder = CycleFinder(lookup, conn_lookup)

        cycles = self.finder.find_cycles(1)

        cycle_list = [c.to_list_string() for c in cycles]
        expected_str = "(0, 0) -> (0, 7) -> (7, 7) -> (8, 8) -> (8, 0) -> (0, 0)"
        self.assertIn(expected_str, cycle_list)
        index = cycle_list.index(expected_str)
        cycle = cycles[index]
        self.assertEqual(cycle.has_discontinuous_weak_link, True)

    def test_finds_cycle_with_multiple_numbers(self):
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

        lookup = SquareLookup(self.board)
        conn_lookup = SquareConnectionLookup(lookup)
        self.finder = CycleFinder(lookup, conn_lookup)

        cycles = self.finder.find_cycles(1)

        filtered_cycles = [c for c in cycles if
                           len(c.parts) == 6
                           and c.start.start.row == 1
                           and c.start.start.column == 4]

        self.assertEqual(len(filtered_cycles), 2)
        cycle_list = [c.to_list_string() for c in filtered_cycles]
        expected_str = "(1, 4) -> (1, 7) -> (8, 7) -> (8, 1) -> (7, 1) -> (7, 4) -> (1, 4)"
        self.assertIn(expected_str, cycle_list)
