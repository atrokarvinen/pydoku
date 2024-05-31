from flask import Blueprint, request

from blueprints.common import get_user_id
from database.solverSettingsRepository import SolverSettingsRepository
from mappers.settingsMapper import SettingsMapper
from mappers.sudokuMapper import SudokuMapper
from models.sudoku import Sudoku
from presetSudokus.sudokus import x_wing_example
from database.db import db
from solver.sudokuParser import SudokuParser


sudoku_blueprint = Blueprint("sudoku", __name__)


@sudoku_blueprint.route("")
def get_sudoku():
    board = SudokuParser.parse(x_wing_example)
    return board.serialize()


@sudoku_blueprint.route("/solve", methods=["POST"])
def solve_sudoku():
    user_id = get_user_id()
    if user_id is None:
        return {"message": "User not found"}, 404
    sudoku_json = request.get_json()
    board = SudokuMapper().map_from_json(sudoku_json)
    with db.session() as session:
        solver_settings = SolverSettingsRepository(
            session).get_settings_by_user_id(user_id)
        settings = SettingsMapper().map_from_db_models(solver_settings)
    sudoku = Sudoku()
    sudoku.board = board
    sudoku.settings = settings

    (solution, error) = sudoku.solve(board)
    if error is not None:
        return {"message": error}, 400
    return solution.serialize()
