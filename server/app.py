import os
from flask import Flask, request
from flask_cors import CORS

from models.sudoku import Sudoku
from mappers.sudokuMapper import SudokuMapper
from models.solution import Solution
from machineVision.sudokuDetector import SudokuDetector
from pathlib import Path
from testing.sudokus import expert_sudoku3


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


@app.route("/sudoku")
def get_sudoku():
    sudoku = Sudoku()
    board = sudoku.parse(expert_sudoku3)
    return board.serialize()


@app.route("/sudoku/import/image", methods=["POST"])
def import_sudoku_from_image():
    file = request.files["file"]
    print("importing image file: " + str(file))
    current_path = Path(__file__).parent
    filename = os.path.join(
        current_path, "machineVision/testImages", file.filename)
    print("saving to path: " + filename)
    file.save(filename)
    mv = SudokuDetector()
    img = mv.load_image(filename)
    sudoku_string = mv.detect(img)
    solver = Sudoku()
    sudoku = solver.parse(sudoku_string)
    return sudoku.serialize()


@app.route("/sudoku/import/string", methods=["POST"])
def import_sudoku_from_string():
    sudoku_string = request.get_json()["sudoku"]
    solver = Sudoku()
    sudoku = solver.parse(sudoku_string)
    return sudoku.serialize()


@app.route("/sudoku/notes")
def get_sudoku_notes():
    sudoku = Sudoku()
    board = sudoku.parse(expert_sudoku3)
    sudoku.add_initial_possibilities(board)
    return board.serialize()


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
