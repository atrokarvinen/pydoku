import copy
from models.board import Board
from models.elimination import Elimination
from models.pointer import Pointer
from models.square import Square
from models.numberedNote import NumberedNote
from techniques.models.coloredNote import ColoredNote
from techniques.eliminatorBase import EliminatorBase
from techniques.models.loopPart import LoopPart
from techniques.utils.squareLogic import SquareLogic


class SimpleColoring(EliminatorBase):
    def get_next_solution(self, board: Board) -> Elimination:
        squares = board.flatten()
        empty_squares = [s for s in squares if s.is_empty()]
        boardRange = board.get_range()
        for number in boardRange:
            squares_with_note = [
                s for s in empty_squares if number in s.possible_numbers]
            if len(squares_with_note) < 2:
                continue
            chains = []
            for start_square in squares_with_note:
                is_explored = self.square_in_chains(chains, start_square)
                if is_explored:
                    continue

                chain = []
                all_squares = copy.deepcopy(squares_with_note)
                possible_squares = squares_with_note
                start_color = 1
                self.recurse_chain(chain,
                                   all_squares,
                                   possible_squares,
                                   start_square,
                                   start_color,
                                   number)

                if (len(chain) < 2):
                    continue

                unique_chain = self.uniquefy_chain(chain)

                conflicting_color = self.detect_conflicting_color(unique_chain)
                if conflicting_color is not None:
                    self.print_chain(unique_chain, number)
                    print("Conflicting color: " + str(conflicting_color))
                    elimination = self.conflict_to_elimination(
                        unique_chain, conflicting_color)
                    return elimination

                seen_by_both = self.detect_squares_seen_by_both(
                    unique_chain, squares_with_note)
                if len(seen_by_both) > 0:
                    self.print_chain(unique_chain, number)
                    print("Squares seen by both colors.")
                    elimination = self.seen_by_both_to_elimination(
                        unique_chain, seen_by_both)
                    return elimination

                chains.append(unique_chain)

        return None

    def recurse_chain(
            self,
            chain: list[ColoredNote],
            all_squares: list[Square],
            possible_chain_squares: list[Square],
            current_square: Square,
            color: int,
            number: int):
        squares_not_in_chain = self.exclude_chain(all_squares, chain)
        for square in squares_not_in_chain:
            is_strongly_connected = SquareLogic.is_strongly_connected(
                all_squares, current_square, square, number)
            if not is_strongly_connected:
                continue
            chain.append(ColoredNote(
                square.row,
                square.column,
                square.box,
                number,
                color,
                LoopPart(current_square, square, "strong")))
            if (square in possible_chain_squares):
                possible_chain_squares.remove(square)
            next_color = 1 if color == 2 else 2
            self.recurse_chain(chain,
                               all_squares,
                               possible_chain_squares,
                               square,
                               next_color,
                               number)

    def exclude_chain(self, all_squares: list[Square], chain: list[ColoredNote]) -> list[Square]:
        squares_not_in_chain = []
        for square in all_squares:
            square_in_chain = False
            for chain_square in chain:
                if (chain_square.is_same_location(square)):
                    square_in_chain = True
            if (not square_in_chain):
                squares_not_in_chain.append(square)
        return squares_not_in_chain

    def get_next_square(
            self,
            all_squares: list[Square],
            possible_chain_squares: list[Square],
            current_square: Square,
            number: int):
        for square in possible_chain_squares:
            if SquareLogic.is_strongly_connected(all_squares, current_square, square, number):
                return square
        return None

    def square_in_chains(self, chains: list[list[ColoredNote]], square: Square) -> bool:
        for chain in chains:
            for chain_square in chain:
                if (chain_square.is_same_location(square)):
                    return True
        return False

    def uniquefy_chain(self, chain: list[ColoredNote]) -> list[ColoredNote]:
        unique_chain: list[ColoredNote] = []
        for square in chain:
            already_added = False
            for unique_square in unique_chain:
                if (unique_square.is_same_location(square)):
                    already_added = True
                    break
            if (not already_added):
                unique_chain.append(square)
        return unique_chain

    def detect_conflicting_color(self, chain: list[ColoredNote]) -> int:
        for square1 in chain:
            for square2 in chain:
                if (square1.is_same_location(square2)):
                    continue
                is_connected = square1.is_connected(square2)
                same_color = square1.color == square2.color
                if (is_connected and same_color):
                    print("Conflicting squares: (" + str(square1.column + 1) + ", " +
                          str(square1.row + 1) + ") and (" + str(square2.column + 1) + ", " +
                          str(square2.row + 1) + ")")
                    return square1.color
        return None

    def detect_squares_seen_by_both(self, chain: list[ColoredNote], squares: list[Square]) -> list[Square]:
        squares_seen_by_both = []
        for square in squares:
            square_in_chain = False
            for chain_square in chain:
                if (chain_square.is_same_location(square)):
                    square_in_chain = True
            if (square_in_chain):
                continue
            seen_chain_squares = [s for s in chain if s.is_connected(square)]
            seen_colors = [s.color for s in seen_chain_squares]
            if (1 in seen_colors and 2 in seen_colors):
                squares_seen_by_both.append(square)

        return squares_seen_by_both

    def conflict_to_elimination(self, chain: list[ColoredNote], conflicting_color: int) -> Elimination:
        causing_color = [s for s in chain if s.color != conflicting_color]
        eliminated_color = [s for s in chain if s.color == conflicting_color]

        causing_notes = [x.to_numbered_note() for x in causing_color]
        eliminated_notes = [NumberedNote(x.row, x.column, x.number)
                            for x in eliminated_color]
        pointers = self.chain_to_pointers(chain)
        return Elimination(
            technique="simple-coloring",
            causing_square=None,
            causing_notes=causing_notes,
            eliminated_notes=eliminated_notes,
            pointers=pointers)

    def seen_by_both_to_elimination(self, chain: list[ColoredNote], seen_by_both: list[Square]) -> Elimination:
        number = chain[0].number
        causing_notes = [x.to_numbered_note() for x in chain]
        eliminated_notes = [NumberedNote(x.row, x.column, number)
                            for x in seen_by_both]
        pointers = self.chain_to_pointers(chain)
        return Elimination(
            technique="simple-coloring",
            causing_square=None,
            causing_notes=causing_notes,
            eliminated_notes=eliminated_notes,
            pointers=pointers)

    def chain_to_pointers(self, chain: list[ColoredNote]) -> list[Pointer]:
        pointers = []
        for chain_part in chain:
            if (chain_part == chain[1]):
                continue
            pointers.append(Pointer(
                chain_part.link.start.to_point(),
                chain_part.link.end.to_point()
            ))
        return pointers

    def print_chain(self, chain: list[ColoredNote], number: int):
        print("Simple coloring chain. Chain length: " + str(len(chain)))
        sorted_chain = sorted(chain, key=lambda x: (x.column, x.row))
        for square in sorted_chain:
            print("(" + str(square.column + 1) + ", " +
                  str(square.row+1) + "): " +
                  " - " + str(number) +
                  " - " + ("yellow" if square.color == 2 else "blue"))
