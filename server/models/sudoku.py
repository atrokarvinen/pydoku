import copy
import math
from models.square import Square
from models.elimination import Elimination
from models.eliminationReason import EliminationReason
from models.singleCandidate import SingleCandidate
from models.solution import Solution
from testing.easySudoku import easy_sudoku

type Board = list[list[Square]]


class Sudoku:
    def __init__(self):
        self.board = []
        self.eliminations = []

    def set_board(self, board: Board):
        self.board = board

    def parse(self) -> Board:
        size = 9
        sudoku_length = len(easy_sudoku)
        if (sudoku_length != size*size):
            print("Invalid sudoku length")
            return

        char_array = list(easy_sudoku)
        board = []
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

    def flatten_board(self, board: Board) -> list[Square]:
        flat_board = []
        for row in board:
            for square in row:
                flat_board.append(square)
        return flat_board

    def add_initial_possibilities(self, board: Board) -> Board:
        initialized_board = []
        size = len(board)
        for i in range(size):
            boardRow = []
            for j in range(size):
                square = board[i][j]
                number = square.number
                new_square = Square(i, j, number)
                if (number == 0):
                    possible_numbers = [*range(1, size+1)]
                    new_square.set_possible_numbers(possible_numbers)
                else:
                    new_square.set_number(number)
                boardRow.append(new_square)
            initialized_board.append(boardRow)

        return initialized_board

    def scan_rows(self, board: Board) -> list[Elimination]:
        size = len(board)
        rows = board

        eliminations = []
        for row in range(size):
            for column in range(size):
                square = rows[row][column]
                square_number = square.number
                if (square_number != 0):
                    continue
                for number in square.possible_numbers:
                    for compare_column in range(size):
                        if (compare_column == column):
                            continue
                        other_square = rows[row][compare_column]
                        other_number = other_square.number
                        if (other_number == 0):
                            continue
                        if (number == other_number):
                            caused_by = EliminationReason(
                                row, compare_column, number, "row-scan")
                            elimination = Elimination(
                                row, column, number, caused_by)
                            eliminations.append(elimination)

        return eliminations

    def scan_columns(self, board: Board) -> list[Elimination]:
        size = len(board)
        flat_squares = self.flatten_board(board)

        eliminations = []
        for square in flat_squares:
            row = square.row
            column = square.column
            number = square.number
            if (number != 0):
                continue
            for number in square.possible_numbers:
                for compare_row in range(size):
                    if (compare_row == row):
                        continue
                    other_square = board[compare_row][column]
                    other_number = other_square.number
                    if (other_number == 0):
                        continue
                    if (number == other_number):
                        caused_by = EliminationReason(
                            compare_row, column, number, "column-scan")
                        elimination = Elimination(
                            row, column, number, caused_by)
                        eliminations.append(elimination)

        return eliminations

    def get_squares_in_box(self, board: Board, boxIndex: int) -> list[Square]:
        size = len(board)
        box_size = int(math.sqrt(size))
        flat_squares = self.flatten_board(board)
        squares = []
        for square in flat_squares:
            box = square.get_box(box_size)
            if (box == boxIndex):
                squares.append(square)
        return squares

    def scan_boxes(self, board: Board) -> list[Elimination]:
        size = len(board)
        box_size = math.sqrt(size)
        eliminations = []
        flat_squares = self.flatten_board(board)

        for square in flat_squares:
            row = square.row
            column = square.column
            number = square.number
            box = square.get_box(box_size)
            if (number != 0):
                continue
            squares_in_box = self.get_squares_in_box(board, box)
            for number in square.possible_numbers:
                for other_square in squares_in_box:
                    if (other_square.row == row and other_square.column == column):
                        continue
                    other_number = other_square.number
                    if (other_number == 0):
                        continue
                    if (number == other_number):
                        caused_by = EliminationReason(
                            other_square.row, other_square.column, number, "box-scan")
                        elimination = Elimination(
                            row, column, number, caused_by)
                        eliminations.append(elimination)

        return eliminations

    def get_single_candidates(self, board: Board) -> list[SingleCandidate]:
        flat_squares = self.flatten_board(board)

        single_candidates = []
        for square in flat_squares:
            row = square.row
            column = square.column
            number = square.number
            if (number != 0):
                continue
            possible_numbers = square.possible_numbers
            if (len(possible_numbers) == 0):
                print("No possible numbers")
                continue
            if (len(possible_numbers) == 1):
                single_candidate = SingleCandidate(
                    row, column, possible_numbers[0])
                single_candidates.append(single_candidate)

        return single_candidates

    def is_solved(self, board: Board) -> list[Square]:
        box_size = math.sqrt(len(board))
        flat_squares = self.flatten_board(board)
        error_squares = []
        for square in flat_squares:
            row = square.row
            column = square.column
            box = square.get_box(box_size)
            if (square.number == 0):
                error_squares.append(square)
                continue

            squares_in_row = board[row]
            squares_in_column = [board[i][column] for i in range(len(board))]
            squares_in_box = self.get_squares_in_box(board, box)

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

    def solve(self, board: Board) -> Solution:
        board_copy = copy.deepcopy(board)
        iteration = 0
        solution = Solution()
        while (iteration < 100):
            eliminations = self.scan_rows(board_copy) + self.scan_columns(
                board_copy) + self.scan_boxes(board_copy)
            unique_eliminations = self.filter_unique_eliminations(eliminations)
            board_copy = self.apply_eliminations(
                board_copy, unique_eliminations)

            single_candidates = self.get_single_candidates(board_copy)
            board_copy = self.apply_single_candidates(
                board_copy, single_candidates)

            solution.add_eliminations(unique_eliminations)
            solution.add_single_candidates(single_candidates)

            print("Iteration: " + str(iteration))
            error_squares = self.is_solved(board_copy)
            if (len(error_squares) == 0):
                print("Sudoku solved")
                break

            iteration += 1
        print("Found eliminations: " + str(len(solution.eliminations)))
        print("Found single candidates: " +
              str(len(solution.singleCandidates)))
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

    def apply_eliminations(self, board: Board, eliminations: list[Elimination]) -> Board:
        board_copy = copy.deepcopy(board)
        for elimination in eliminations:
            row = elimination.row
            column = elimination.column
            number = elimination.number

            square = board_copy[row][column]
            square.remove_possible_number(number)

        return board_copy

    def apply_single_candidates(self, board: Board, candidates: list[SingleCandidate]) -> Board:
        board_copy = copy.deepcopy(board)
        for candidate in candidates:
            row = candidate.row
            column = candidate.column
            number = candidate.number

            square = board_copy[row][column]
            square.set_number(number)

        return board_copy
