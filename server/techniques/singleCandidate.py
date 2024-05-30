from models.board import Board
from models.highlightedRectangle import HighlightedRectangle
from models.highlightedRegion import HighlightedRegion
from models.point import Point
from models.singleCandidate import SingleCandidate as SingleCandidateModel
from models.square import Square
from techniques.solverBase import SolverBase


class SingleCandidate(SolverBase):
    def get_next_solution(self, board: Board) -> SingleCandidateModel:
        boardRange = range(board.size)
        rows = [board.get_squares_in_row(i) for i in boardRange]
        columns = [board.get_squares_in_column(i) for i in boardRange]
        boxes = [board.get_squares_in_box(i) for i in boardRange]
        single_squares = [[s] for s in board.flatten() if s.is_empty()]

        single_candidate = self.iterate_sets(single_squares, "cell")
        if (single_candidate is not None):
            return single_candidate

        single_candidate = self.iterate_sets(rows, "row")
        if (single_candidate is not None):
            return single_candidate

        single_candidate = self.iterate_sets(columns, "column")
        if (single_candidate is not None):
            return single_candidate

        single_candidate = self.iterate_sets(boxes, "box")
        if (single_candidate is not None):
            return single_candidate

        return None

    def iterate_sets(self, sets: list[list[Square]], alignment: str) -> SingleCandidateModel:
        for square_set in sets:
            candidate = self.single_candidates_in_set(square_set, alignment)
            if (candidate is not None):
                return candidate
        return None

    def single_candidates_in_set(self, square_set: list[Square], alignment: str) -> SingleCandidateModel:
        notes_by_count = {}
        for square in square_set:
            for note in square.possible_numbers:
                notes_by_count[note] = notes_by_count.get(note, 0) + 1

        if len(square_set) == 1 and len(notes_by_count) > 1:
            return None

        for note, count in notes_by_count.items():
            if count != 1:
                continue
            any_has_number = any([s.number == note for s in square_set])
            if any_has_number:
                continue
            for square in square_set:
                if not note in square.possible_numbers:
                    continue
                row = square.row
                column = square.column
                other_numbers = [
                    n for n in square.possible_numbers if n != note]
                highlighted_regions = self.get_highlighted_regions(
                    square, alignment)
                highlighted_rectangles = self.get_highlighted_rectangles(
                    square, alignment)
                single_candidate = SingleCandidateModel(
                    row,
                    column,
                    note,
                    other_numbers,
                    highlighted_regions,
                    highlighted_rectangles,
                    alignment)
                return single_candidate

        return None

    def get_highlighted_regions(self, square: Square, alignment: str) -> list[HighlightedRegion]:
        if (alignment == "row"):
            return [HighlightedRegion(alignment, square.row)]
        elif (alignment == "column"):
            return [HighlightedRegion(alignment, square.column)]
        elif (alignment == "box"):
            return [HighlightedRegion(alignment, square.box)]
        return []

    def get_highlighted_rectangles(self, square: Square, alignment: str) -> list[HighlightedRectangle]:
        if (alignment != "cell"):
            return []
        return [HighlightedRectangle(square.to_point(), square.to_point())]
