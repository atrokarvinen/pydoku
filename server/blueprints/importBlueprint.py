from flask import Blueprint, request

from machineVision.imageSaver import ImageSaver
from machineVision.sudokuDetector import SudokuDetector
from models.sudoku import Sudoku
from presetSudokus.presetProvider import PresetProvider
from solver.sudokuParser import SudokuParser


import_blueprint = Blueprint("import", __name__)


@import_blueprint.route("/image", methods=["POST"])
def import_sudoku_from_image():
    mv = SudokuDetector()
    file = request.files["file"]
    file_saver = ImageSaver()
    filename = file_saver.save(file)
    try:
        img = mv.load_image(filename)
        (sudoku_string, error) = mv.detect(img)
        if error:
            return {"message": error}, 400
        sudoku = SudokuParser.parse(sudoku_string)
        return sudoku.serialize()
    except:
        return "Sudoku detection failed", 400
    finally:
        file_saver.try_delete_image(filename)


@import_blueprint.route("/string", methods=["POST"])
def import_sudoku_from_string():
    sudoku_string = request.get_json()["sudoku"]
    sudoku = SudokuParser.parse(sudoku_string)
    return sudoku.serialize()


@import_blueprint.route("/preset")
def get_import_presets():
    presets = PresetProvider().get_preset_sudokus()
    return [preset.serialize() for preset in presets]


@import_blueprint.route("/preset/<preset_id>")
def import_from_preset(preset_id: str):
    print("Importing preset:", preset_id)
    preset = PresetProvider().get_preset_sudoku(preset_id)
    sudoku = SudokuParser.parse(preset.sudoku)
    return sudoku.serialize()
