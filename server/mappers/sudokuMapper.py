from models.sudoku import Sudoku


class SudokuMapper:
    def mapFromJson(self, data) -> Sudoku:
        sudoku = data["sudoku"]

        self.sudoku.set_data(data)
        return self.sudoku