import copy
import math
from models.square import Square
from models.elimination import Elimination
from models.singleCandidate import SingleCandidate
from models.solution import Solution
from models.board import Board
from models.eliminationGroup import EliminationGroup
from techniques.pointing import Pointing
from techniques.nakedPair import NakedPair
from techniques.scan import Scan
from techniques.singleCandidate import SingleCandidate as SingleCandidateTechnique
from testing.sudokus import expert_sudoku1


class Sudoku:
    def __init__(self):
        self.board = Board(9)
        self.eliminations = []
        self.scan_technique = Scan()
        self.single_candidate_technique = SingleCandidateTechnique()
        self.naked_pair_technique = NakedPair()
        self.pointing_technique = Pointing()

    def set_board(self, board: Board):
        self.board = board

    def parse(self) -> Board:
        size = 9
        testSudoku = expert_sudoku1
        sudoku_length = len(testSudoku)
        if (sudoku_length != size*size):
            print("Invalid sudoku length")
            return

        char_array = list(testSudoku)
        board = Board(size)
        for i in range(size):
            row = []
            for j in range(size):
                char = char_array[i*size+j]
                if (char == '.'):
                    char_as_number = 0
                else:
                    char_as_number = int(char)
                square = Square(i, j, char_as_number)
                row.append(square)
            board.append(row)

        return board

    def add_initial_possibilities(self, board: Board) -> Board:
        board.add_initial_possibilities()
        return board

    def is_solved(self, board: Board) -> list[Square]:
        flat_squares = board.flatten()
        error_squares = []
        for square in flat_squares:
            row = square.row
            column = square.column
            if (square.is_empty()):
                error_squares.append(square)
                continue

            squares_in_row = board.get_squares_in_row(row)
            squares_in_column = board.get_squares_in_column(column)
            squares_in_box = board.get_squares_in_box(square)

            other_Squares = squares_in_row + squares_in_column + squares_in_box
            for other_square in other_Squares:
                if (other_square.row == row and other_square.column == column):
                    continue
                if (other_square.number == square.number):
                    error_squares.append(square)
                    error_squares.append(other_square)

        unique_error_squares = []
        for error_square in error_squares:
            if (error_square not in unique_error_squares):
                unique_error_squares.append(error_square)
        return unique_error_squares

    def solve(self, empty_board: Board) -> Solution:
        board = copy.deepcopy(empty_board)
        self.add_initial_possibilities(board)
        iteration = 0
        solution = Solution(board)
        max_iterations = 100
        while (True):
            print("Iteration: " + str(iteration) +
                  ", solution index: " + str(solution.solution_index))
            scan_groups = self.scan_technique.scan(board)
            naked_pair_groups = self.naked_pair_technique.get_naked_pairs(
                board)
            pointing_groups = self.pointing_technique.get_pointing(board)
            elimination_groups = scan_groups + naked_pair_groups + pointing_groups
            if (len(elimination_groups) > 0):
                first_group = elimination_groups[0]
                board = self.apply_elimination_group(board, first_group)
                solution.add_elimination_group(first_group)

            single_candidates = self.single_candidate_technique.get_single_candidates(
                board)
            board = self.apply_single_candidates(board, single_candidates)

            solution.add_single_candidates(single_candidates)

            error_squares = self.is_solved(board)
            if (len(elimination_groups) == 0 and len(single_candidates) == 0):
                print(
                    "No eliminations or single candidates found. Unable to solve sudoku")
                break
            if (len(error_squares) == 0):
                solution.is_solved = True
                print("Sudoku solved")
                break
            if (iteration == max_iterations):
                print("Max iterations reached, unable to solve sudoku")
                break

            iteration += 1

        print("Found eliminations: " + str(len(solution.elimination_groups)))
        print("Found single candidates: " +
              str(len(solution.single_candidates)))
        return solution

    def elimination_matches(self, elimination: Elimination, other_elimination: Elimination) -> bool:
        return elimination.row == other_elimination.row \
            and elimination.column == other_elimination.column \
            and elimination.number == other_elimination.number

    def filter_unique_eliminations(self, eliminations: list[Elimination]) -> list[Elimination]:
        unique_eliminations: list[Elimination] = []
        for elimination in eliminations:
            already_added = False
            for added_elimination in unique_eliminations:
                if (self.elimination_matches(elimination, added_elimination)):
                    already_added = True
                    break
            if (not already_added):
                unique_eliminations.append(elimination)

        return unique_eliminations

    def apply_elimination_group(self, board: Board, eliminationGroup: EliminationGroup) -> Board:
        board_copy = copy.deepcopy(board)
        for elimination in eliminationGroup.eliminated_notes:
            row = elimination.row
            column = elimination.column
            number = elimination.number

            square = board_copy.get_square(row, column)
            square.remove_possible_number(number)

        return board_copy

    def apply_elimination_groups(self, board: Board, eliminations: list[EliminationGroup]) -> Board:
        board_copy = copy.deepcopy(board)
        for eliminationGroup in eliminations:
            for elimination in eliminationGroup.eliminated_notes:
                row = elimination.row
                column = elimination.column
                number = elimination.number

                square = board_copy.get_square(row, column)
                square.remove_possible_number(number)

        return board_copy

    def apply_eliminations(self, board: Board, eliminations: list[Elimination]) -> Board:
        board_copy = copy.deepcopy(board)
        for elimination in eliminations:
            row = elimination.row
            column = elimination.column
            number = elimination.number

            square = board_copy.get_square(row, column)
            square.remove_possible_number(number)

        return board_copy

    def apply_single_candidates(self, board: Board, candidates: list[SingleCandidate]) -> Board:
        board_copy = copy.deepcopy(board)
        for candidate in candidates:
            row = candidate.row
            column = candidate.column
            number = candidate.number

            square = board_copy.get_square(row, column)
            square.set_number(number)

        return board_copy
