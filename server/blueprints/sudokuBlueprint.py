from flask import Blueprint, request

from blueprints.common import get_user_id
from database.solverSettingsRepository import SolverSettingsRepository
from mappers.settingsMapper import SettingsMapper
from mappers.sudokuMapper import SudokuMapper
from models.solution import Solution
from models.sudoku import Sudoku
from presetSudokus.sudokus import hard_sudoku1
from database.db import db


sudoku_blueprint = Blueprint("sudoku", __name__)


@sudoku_blueprint.route("")
def get_sudoku():
    sudoku = Sudoku()
    board = sudoku.parse(hard_sudoku1)
    return board.serialize()


@sudoku_blueprint.route("/solve", methods=["POST"])
def solve_sudoku():
    user_id = get_user_id()
    if user_id is None:
        return "User not found", 404
    sudoku_json = request.get_json()
    mapper = SudokuMapper()
    board = mapper.map_from_json(sudoku_json)
    with db.session() as session:
        solver_settings = SolverSettingsRepository(
            session).get_settings_by_user_id(user_id)
        settings = SettingsMapper().map_from_db_models(solver_settings)
    sudoku = Sudoku()
    sudoku.board = board
    sudoku.settings = settings

    solution = sudoku.solve(board)
    return serialize_solution(solution)


def serialize_solution(solution: Solution):
    return solution.serialize()
