from flask import Flask, request
from flask_cors import CORS

from models.sudoku import Sudoku
from mappers.sudokuMapper import SudokuMapper
from models.solution import Solution

app = Flask(__name__)
CORS(app)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response


@app.route("/")
def tester():
    return "Hello"


@app.route("/sudoku")
def get_sudoku():
    sudoku = Sudoku()
    board = sudoku.parse()
    return board.serialize()


@app.route("/sudoku/notes")
def get_sudoku_notes():
    sudoku = Sudoku()
    board = sudoku.parse()
    sudoku.add_initial_possibilities(board)
    return board.serialize()


@app.route("/sudoku/row-scan", methods=["POST"])
def scan_sudoku_rows():
    sudoku_json = request.get_json()
    mapper = SudokuMapper()
    sudoku = mapper.map_from_json(sudoku_json)
    board = sudoku.board
    eliminations = sudoku.scan_rows(board)
    return serialize_eliminations(eliminations)


@app.route("/sudoku/column-scan", methods=["POST"])
def scan_sudoku_columns():
    sudoku_json = request.get_json()
    mapper = SudokuMapper()
    sudoku = mapper.map_from_json(sudoku_json)
    board = sudoku.board
    eliminations = sudoku.scan_columns(board)
    return serialize_eliminations(eliminations)


@app.route("/sudoku/box-scan", methods=["POST"])
def scan_sudoku_boxes():
    sudoku_json = request.get_json()
    mapper = SudokuMapper()
    sudoku = mapper.map_from_json(sudoku_json)
    board = sudoku.board
    eliminations = sudoku.scan_boxes(board)
    return serialize_eliminations(eliminations)


@app.route("/sudoku/all-scan", methods=["POST"])
def scan_sudoku_all():
    sudoku_json = request.get_json()
    mapper = SudokuMapper()
    sudoku = mapper.map_from_json(sudoku_json)
    board = sudoku.board
    row_eliminations = sudoku.scan_rows(board)
    column_eliminations = sudoku.scan_columns(board)
    box_eliminations = sudoku.scan_boxes(board)
    eliminations = row_eliminations + column_eliminations + box_eliminations
    return serialize_eliminations(eliminations)


@app.route("/sudoku/single-candidate", methods=["POST"])
def get_single_candidates():
    sudoku_json = request.get_json()
    mapper = SudokuMapper()
    sudoku = mapper.map_from_json(sudoku_json)
    board = sudoku.board
    single_candidates = sudoku.get_single_candidates(board)
    return [square.serialize() for square in single_candidates]


@app.route("/sudoku/is-solved", methods=["POST"])
def check_sudoku_solved():
    sudoku_json = request.get_json()
    mapper = SudokuMapper()
    sudoku = mapper.map_from_json(sudoku_json)
    board = sudoku.board
    error_squares = sudoku.is_solved(board)
    return [square.serialize() for square in error_squares]


@app.route("/sudoku/solve", methods=["POST"])
def solve_sudoku():
    sudoku_json = request.get_json()
    mapper = SudokuMapper()
    sudoku = mapper.map_from_json(sudoku_json)
    board = sudoku.board
    solution = sudoku.solve(board)
    return serialize_solution(solution)


def serialize_eliminations(eliminations):
    return [elimination.serialize() for elimination in eliminations]


def serialize_solution(solution: Solution):
    return solution.serialize()
