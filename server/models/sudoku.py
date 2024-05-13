import copy
import math
from models.square import Square
from models.solution import Solution
from models.board import Board
from techniques.biValueUniversalGrave import BiValueUniversalGrave
from techniques.emptyRectangle import EmptyRectangle
from techniques.yWing import YWing
from techniques.xWing import XWing
from techniques.solverBase import SolverBase
from techniques.simpleColoring import SimpleColoring
from techniques.hiddenPair import HiddenPair
from techniques.claiming import Claiming
from techniques.pointing import Pointing
from techniques.nakedPair import NakedPair
from techniques.scan import Scan
from techniques.singleCandidate import SingleCandidate as SingleCandidateTechnique


class Sudoku:
    def __init__(self):
        self.board = Board(9)
        self.techniques: list[SolverBase] = [
            Scan(),
            SingleCandidateTechnique(),
            NakedPair(),
            Pointing(),
            Claiming(),
            HiddenPair(),
            XWing(),
            YWing(),
            SimpleColoring(),
            EmptyRectangle(),
            BiValueUniversalGrave()
        ]

    def set_board(self, board: Board):
        self.board = board

    def parse(self, sudoku_string) -> Board:
        size = 9
        box_size = math.sqrt(size)
        sudoku_length = len(sudoku_string)
        if (sudoku_length != size*size):
            print("Invalid sudoku length")
            return

        char_array = list(sudoku_string)
        board = Board(size)
        for i in range(size):
            row = []
            for j in range(size):
                char = char_array[i*size+j]
                if (char == '.'):
                    char_as_number = 0
                else:
                    char_as_number = int(char)
                box = math.floor(i/box_size)*box_size + math.floor(j/box_size)
                square = Square(i, j, box, char_as_number)
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
            squares_in_box = board.get_squares_in_box_by_square(square)

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
        is_empty = all([len(s.possible_numbers) == 0 for s in board.flatten()])
        if (is_empty):
            self.add_initial_possibilities(board)
        iteration = 0
        initial_board = copy.deepcopy(board)
        solution = Solution(initial_board)
        empty_square_count = len([s for s in board.flatten() if s.is_empty()])
        max_iterations = (board.size + 1) * empty_square_count
        while (True):
            print("Iteration: " + str(iteration))
            next_solution = None
            for solver in self.techniques:
                next_solution = solver.get_next_solution(board)
                if (next_solution is not None):
                    break

            if (next_solution is None):
                print("No new solution found. Unable to solve sudoku")
                break

            board = next_solution.apply(board)
            if (next_solution.is_elimination()):
                solution.add_elimination(next_solution)
            else:
                solution.add_single_candidate(next_solution)

            if (self.is_board_full(board)):
                error_squares = self.is_solved(board)
                if (len(error_squares) == 0):
                    solution.is_solved = True
                    print("Sudoku solved")
                    break
                if (iteration == max_iterations):
                    print("Max iterations reached, unable to solve sudoku")
                    break

            if (iteration == max_iterations):
                print("Max iterations reached, unable to solve sudoku")
                break

            iteration += 1

        print("Found eliminations: " + str(len(solution.eliminations)))
        print("Found single candidates: " +
              str(len(solution.single_candidates)))
        return solution

    def is_board_full(self, board: Board) -> bool:
        return all([not s.is_empty() for s in board.flatten()])
