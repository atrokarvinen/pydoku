import asyncio
import copy
import time
import func_timeout
from models.solutionStep import SolutionStep
from models.square import Square
from models.solution import Solution
from models.board import Board
from solver.settings import Settings
from techniques.biValueUniversalGrave import BiValueUniversalGrave
from techniques.emptyRectangle import EmptyRectangle
from techniques.xCycle import XCycle
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
            SimpleColoring(),
            YWing(),
            EmptyRectangle(),
            BiValueUniversalGrave(),
            XCycle(),
        ]
        self.settings: Settings = Settings()

    def add_initial_possibilities(self, board: Board) -> Board:
        board.add_initial_possibilities()
        return board

    def is_solved(self, board: Board) -> list[Square]:
        return len(self.get_error_squares(board)) == 0

    def get_error_squares(self, board: Board) -> list[Square]:
        flat_squares = board.flatten()
        error_squares = []
        for square in flat_squares:
            row = square.row
            column = square.column
            if (square.number == 0):
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

    def solve(self, input_board: Board) -> Solution:
        error = self.validate_board(input_board)
        if (error is not None):
            return Solution(input_board)
        board = self.preprocess_board(input_board)
        solution = Solution(copy.deepcopy(board))
        techniques = self.settings.create_solvers()

        iteration = 0
        empty_square_count = len([s for s in board.flatten() if s.is_empty()])
        max_iterations = (board.size + 1) * empty_square_count
        while (True):
            print("Iteration: " + str(iteration))
            (next_step, error) = self.get_next_solution_step(board, techniques)
            if (error is not None):
                print("Error: " + error)
                break
            if (next_step is None):
                print("No new solution found. Unable to solve sudoku")
                break

            board = self.apply_solution_step(board, solution, next_step)

            if (self.is_solved(board)):
                solution.is_solved = True
                print("Sudoku solved")
                break
            if (iteration == max_iterations):
                print("Max iterations reached, unable to solve sudoku")
                break

            iteration += 1

        solution.final_sudoku = board
        return solution

    def validate_board(self, board: Board) -> str:
        if (self.is_solved(board)):
            return "Sudoku already solved"
        if (self.is_board_empty(board)):
            return "Sudoku is empty"
        return None

    def preprocess_board(self, board: Board) -> Board:
        board = copy.deepcopy(board)
        is_not_initialized = all(
            [len(s.possible_numbers) == 0 for s in board.flatten()])
        if (is_not_initialized):
            self.add_initial_possibilities(board)
        return board

    def get_next_solution_step(
            self,
            board: Board,
            techniques: list[SolverBase]) -> tuple[SolutionStep, str]:
        for solver in techniques:
            try:
                next_step = func_timeout.func_timeout(
                    timeout=2,
                    func=solver.get_next_solution,
                    args=(board,))
                if (next_step is not None):
                    return (next_step, None)
            except func_timeout.FunctionTimedOut:
                error = f"Timeout error for solver {solver.__class__.__name__}"
                return (None, error)

    def apply_solution_step(self, board: Board, solution: Solution, solution_step: SolutionStep) -> Board:
        if (solution_step.is_elimination()):
            solution.add_elimination(solution_step)
        else:
            solution.add_single_candidate(solution_step)
        return solution_step.apply(board)

    def is_board_full(self, board: Board) -> bool:
        return all([not s.is_empty() for s in board.flatten()])

    def is_board_empty(self, board: Board) -> bool:
        return all([s.is_empty() for s in board.flatten()])
