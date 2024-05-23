import copy
from models.board import Board
from models.elimination import Elimination
from models.numberedNote import NumberedNote
from techniques.eliminatorBase import EliminatorBase
from techniques.models.cycle import Cycle
from techniques.utils.cycleFinder import CycleFinder
from techniques.utils.squareConnectionLookup import SquareConnectionLookup
from techniques.utils.squareLogic import SquareLogic
from techniques.utils.squareLookup import SquareLookup


class XCycle(EliminatorBase):
    def get_next_solution(self, board: Board) -> Elimination:
        lookup = SquareLookup(board)
        connection_lookup = SquareConnectionLookup(lookup)
        cycle_finder = CycleFinder(lookup, connection_lookup)
        notes = board.get_range()
        for note in notes:
            cycles = cycle_finder.find_cycles(note)
            elimination = self.detect_elimination(
                lookup, connection_lookup, cycles, note)
            if elimination:
                return elimination
        return None

    def detect_elimination(
            self,
            lookup: SquareLookup,
            connection_lookup: SquareConnectionLookup,
            cycles: list[Cycle],
            number: int) -> Elimination:
        squares = lookup.get_squares_by_number(number)
        for cycle in cycles:
            if not cycle.is_nice():
                continue
            cycle_squares = cycle.to_square_list()
            other_squares = SquareLogic.subtract_squares(
                squares, cycle_squares)
            eliminated_notes = []
            for square in other_squares:
                endpoints = connection_lookup.get_connections_endpoints(
                    square, number)
                intersection = [
                    value for value in endpoints if value in cycle_squares]
                if len(intersection) >= 2:
                    eliminated_notes.append(NumberedNote(
                        square.row, square.column, number))
            if len(eliminated_notes) == 0:
                continue
            elimination = Elimination(
                technique="x-cycle",
                causing_square=None,
                causing_notes=[NumberedNote(s.row, s.column, number)
                               for s in cycle_squares],
                eliminated_notes=eliminated_notes,
                highlighted_regions=[],
                pointers=cycle.to_pointers()
            )
            return elimination

        return None
