import unittest

from models.square import Square
from techniques.utils.cycleFinder import CycleFinder
from unitTesting.customAsserts import CustomAsserts


class TestCycleFinder(unittest.TestCase, CustomAsserts):
    def setUp(self) -> None:
        self.finder = CycleFinder()

    def test_finds_cycle(self):
        squares = [
            Square(0, 0, possible_numbers=[1]),
            Square(8, 0, possible_numbers=[1]),
            Square(8, 8, possible_numbers=[1]),
            Square(0, 8, possible_numbers=[1]),
        ]

        cycles = self.finder.find_cycles(squares, 1)

    def test_finds_cycle_with_multiple_numbers_1(self):
        squares = [
            Square(0, 1, possible_numbers=[1]),
            Square(0, 2, possible_numbers=[1]),
            Square(0, 5, possible_numbers=[1]),

            Square(1, 1, possible_numbers=[1]),
            Square(1, 3, possible_numbers=[1]),

            Square(3, 2, possible_numbers=[1]),
            Square(3, 3, possible_numbers=[1]),

            Square(4, 1, possible_numbers=[1]),
            Square(4, 6, possible_numbers=[1]),

            Square(5, 5, possible_numbers=[1]),
            Square(5, 6, possible_numbers=[1]),
        ]

        cycles = self.finder.find_cycles(squares, 1)

        pass

    def test_finds_cycle_with_multiple_numbers_2(self):
        squares = [
            Square(0, 0, possible_numbers=[1]),
            Square(0, 5, possible_numbers=[1]),
            Square(0, 8, possible_numbers=[1]),

            Square(1, 1, possible_numbers=[1]),
            Square(1, 3, possible_numbers=[1]),

            Square(2, 0, possible_numbers=[1]),
            Square(2, 6, possible_numbers=[1]),
            Square(2, 7, possible_numbers=[1]),

            # Square(4, 6, possible_numbers=[1]),
            # Square(4, 7, possible_numbers=[1]),
            # Square(4, 8, possible_numbers=[1]),

            # Square(6, 1, possible_numbers=[1]),
            # Square(6, 6, possible_numbers=[1]),
            # Square(6, 7, possible_numbers=[1]),
            # Square(6, 8, possible_numbers=[1]),

            # Square(7, 3, possible_numbers=[1]),
            # Square(7, 6, possible_numbers=[1]),

            # Square(8, 0, possible_numbers=[1]),
            # Square(8, 5, possible_numbers=[1]),
            # Square(8, 6, possible_numbers=[1]),
        ]

        cycles = self.finder.find_cycles(squares, 1)
        # for cycle in cycles:
        #     print(cycle)

        square_lists = [cycle.to_list_string() for cycle in cycles]
        lists_by_count = {}
        for square_list in square_lists:
            if square_list not in lists_by_count:
                lists_by_count[square_list] = 0
            lists_by_count[square_list] += 1

        counts = [count for count in lists_by_count.values()]
        sorted_counts = sorted(counts, reverse=True)
        print("counts", sorted_counts)
        duplicate_totals = 0
        for count in sorted_counts:
            if count > 1:
                duplicate_totals += count
            else:
                break
        print("duplicate_totals", duplicate_totals)

        valid_cycles = [cycle for cycle in cycles if cycle.is_valid]
        print("valid_cycles", len(valid_cycles))

        pass

    def test_finds_cycle_with_multiple_numbers_3(self):
        squares = [
            Square(0, 0, possible_numbers=[1]),
            Square(0, 4, possible_numbers=[1]),
            Square(0, 5, possible_numbers=[1]),

            Square(1, 4, possible_numbers=[1]),
            Square(1, 7, possible_numbers=[1]),

            Square(2, 1, possible_numbers=[1]),
            Square(2, 3, possible_numbers=[1]),
            Square(2, 5, possible_numbers=[1]),
            Square(2, 6, possible_numbers=[1]),
            Square(2, 7, possible_numbers=[1]),

            Square(3, 3, possible_numbers=[1]),
            Square(3, 4, possible_numbers=[1]),
            Square(3, 5, possible_numbers=[1]),

            Square(6, 3, possible_numbers=[1]),
            Square(6, 5, possible_numbers=[1]),
            Square(6, 7, possible_numbers=[1]),

            Square(7, 1, possible_numbers=[1]),
            Square(7, 4, possible_numbers=[1]),

            Square(8, 1, possible_numbers=[1]),
            Square(8, 7, possible_numbers=[1]),
        ]

        cycles = self.finder.find_cycles(squares, 1)

        filtered_cycles = [c for c in cycles if
                           len(c.parts) == 6
                           and c.start.start.row == 1
                           and c.start.start.column == 4]

        pass

    def test_does_not_find_cycle(self):
        squares = [
            Square(0, 0, possible_numbers=[1]),
            Square(1, 0, possible_numbers=[1]),
            Square(2, 0, possible_numbers=[1]),
            Square(3, 0, possible_numbers=[1]),
        ]

        cycles = self.finder.find_cycles(squares, 1)
