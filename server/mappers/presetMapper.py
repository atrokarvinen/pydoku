from models.sudoku import Sudoku
from models.square import Square
from models.board import Board
from presetSudokus.presetSudoku import PresetSudoku


class PresetMapper:
    def map_from_json(self, data) -> PresetSudoku:
        sudokuJson = data["sudoku"]

        sudoku = PresetSudoku(
            sudokuJson["sudoku"],
            sudokuJson["name"],
            sudokuJson["difficulty"]
        )

        return sudoku
