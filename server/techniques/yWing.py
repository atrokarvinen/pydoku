from models.board import Board
from models.elimination import Elimination
from models.highlightedRegion import HighlightedRegion
from models.numberedNote import NumberedNote
from models.point import Point
from models.pointer import Pointer
from models.square import Square
from techniques.eliminatorBase import EliminatorBase
from techniques.utils.squareLogic import SquareLogic


class YWing(EliminatorBase):
    def get_next_solution(self, board: Board) -> Elimination:
        empty_squares = board.flatten_empty()
        pivot_squares = [
            s for s in empty_squares if len(s.possible_numbers) == 2]
        for pivot in pivot_squares:
            pivot_number1 = pivot.possible_numbers[0]
            pivot_number2 = pivot.possible_numbers[1]
            squares_in_row = board.get_squares_in_row(pivot.row)
            squares_in_column = board.get_squares_in_column(pivot.column)
            squares_in_box = board.get_squares_in_box(pivot.box)
            region_squares = squares_in_row + squares_in_column + squares_in_box
            squares_seen_by_pivot: list[Square] = SquareLogic.subtract_squares(
                region_squares, [pivot])
            pincer_squares: list[Square] = []
            for other_square in squares_seen_by_pivot:
                if (len(other_square.possible_numbers) != 2):
                    continue
                if (pivot_number1 in other_square.possible_numbers or pivot_number2 in other_square.possible_numbers):
                    pincer_squares.append(other_square)

            for pincer1 in pincer_squares:
                for pincer2 in pincer_squares:
                    if (pincer1 == pincer2):
                        continue
                    elimination = self.check_pincers(
                        pincer1, pincer2, pivot, empty_squares)
                    if (elimination is not None):
                        return elimination

        return None

    def check_pincers(
            self,
            pincer1: Square,
            pincer2: Square,
            pivot: Square,
            empty_squares: list[Square]) -> Elimination:
        pivot_number1 = pivot.possible_numbers[0]
        pivot_number2 = pivot.possible_numbers[1]
        pincer_numbers = pincer1.possible_numbers + pincer2.possible_numbers
        pivot_numbers_in_pincers = pivot_number1 in pincer_numbers and pivot_number2 in pincer_numbers
        pincer_numbers_not_in_pivot = [
            p for p in pincer_numbers if p != pivot_number1 and p != pivot_number2]
        if (len(pincer_numbers_not_in_pivot) != 2):
            return None
        pincers_have_same_numbers = pincer_numbers_not_in_pivot[
            0] == pincer_numbers_not_in_pivot[1]
        if (not pivot_numbers_in_pincers or not pincers_have_same_numbers):
            return None

        shared_number = pincer_numbers_not_in_pivot[0]
        eliminated_notes = []
        eliminated_squares = []
        for square in empty_squares:
            if (square == pivot or square == pincer1 or square == pincer2):
                continue
            seen_by_pincers = SquareLogic.is_connected(
                square, pincer1) and SquareLogic.is_connected(square, pincer2)
            if (seen_by_pincers and shared_number in square.possible_numbers):
                eliminated_squares.append(square)
                eliminated_notes.append(NumberedNote(
                    square.row, square.column, shared_number))

        if (len(eliminated_notes) == 0):
            return None

        print("Found Y-Wing")

        highlighted_regions = self.get_highlighted_regions(
            pincer1, pincer2, pivot, eliminated_squares)
        pointers = self.get_pointers(pincer1, pincer2, pivot)
        elimination = Elimination(
            technique="y-wing",
            eliminated_notes=eliminated_notes,
            causing_notes=[
                NumberedNote(pivot.row, pivot.column, pivot_number1),
                NumberedNote(pivot.row, pivot.column, pivot_number2),
                NumberedNote(pincer1.row, pincer1.column,
                             pincer1.possible_numbers[0]),
                NumberedNote(pincer1.row, pincer1.column,
                             pincer1.possible_numbers[1]),
                NumberedNote(pincer2.row, pincer2.column,
                             pincer2.possible_numbers[0]),
                NumberedNote(pincer2.row, pincer2.column,
                             pincer2.possible_numbers[1])
            ],
            highlighted_regions=highlighted_regions,
            pointers=pointers,
            causing_square=None)
        return elimination

    def get_highlighted_regions(
            self,
            pincer1: Square,
            pincer2: Square,
            pivot: Square,
            eliminated_notes: list[Square]) -> list[HighlightedRegion]:
        elimination_highlights = []
        for note in eliminated_notes:
            region1 = SquareLogic.get_highlighted_region([pincer1, note])
            elimination_highlights.append(region1)
            region2 = SquareLogic.get_highlighted_region([pincer2, note])
            elimination_highlights.append(region2)
        pincer_highlights = [
            SquareLogic.get_highlighted_region([pivot, pincer1]),
            SquareLogic.get_highlighted_region([pivot, pincer2]),
        ]
        return elimination_highlights

    def get_pointers(self, pincer1: Square, pincer2: Square, pivot: Square) -> list[Pointer]:
        return [
            Pointer(
                Point(pivot.row, pivot.column),
                Point(pincer1.row, pincer1.column)
            ),
            Pointer(
                Point(pivot.row, pivot.column),
                Point(pincer2.row, pincer2.column)
            )]
