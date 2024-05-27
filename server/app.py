from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from database.baseModel import Base
from database.userRepository import UserRepository
from mappers.presetMapper import PresetMapper
from models.sudoku import Sudoku
from mappers.sudokuMapper import SudokuMapper
from models.solution import Solution
from machineVision.sudokuDetector import SudokuDetector
from machineVision.imageSaver import ImageSaver
from presetSudokus.presetProvider import PresetProvider
from presetSudokus.sudokus import x_cycle_example2
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("CONNECTION_STRING")
db.init_app(app)
CORS(app)

with app.app_context():
    db.create_all()


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,UserId')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response


@app.route("/auth/create")
def create_user():
    with db.session() as session:
        user = UserRepository().create_user(session)
        return user.serialize()


@app.route("/sudoku")
def get_sudoku():
    sudoku = Sudoku()
    board = sudoku.parse(x_cycle_example2)
    return board.serialize()


@app.route("/sudoku/import/image", methods=["POST"])
def import_sudoku_from_image():
    mv = SudokuDetector()
    file = request.files["file"]
    file_saver = ImageSaver()
    filename = file_saver.save(file)
    try:
        img = mv.load_image(filename)
        sudoku_string = mv.detect(img)
        sudoku = Sudoku().parse(sudoku_string)
        return sudoku.serialize()
    except:
        return "Error"
    finally:
        file_saver.try_delete_image(filename)


@app.route("/sudoku/import/string", methods=["POST"])
def import_sudoku_from_string():
    sudoku_string = request.get_json()["sudoku"]
    sudoku = Sudoku().parse(sudoku_string)
    return sudoku.serialize()


@app.route("/sudoku/import/preset")
def get_import_presets():
    presets = PresetProvider().get_preset_sudokus()
    return [preset.serialize() for preset in presets]


@app.route("/sudoku/import/preset/<preset_id>")
def import_from_preset(preset_id: str):
    print("Importing preset:", preset_id)
    preset = PresetProvider().get_preset_sudoku(preset_id)
    sudoku = Sudoku().parse(preset.sudoku)
    return sudoku.serialize()


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


def get_user_id():
    headers = request.headers
    return headers["UserId"]
