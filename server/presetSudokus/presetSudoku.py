from presetSudokus.difficulty import Difficulty


class PresetSudoku:
    def __init__(self, sudoku: str, name: str, difficulty: Difficulty) -> None:
        self.id: str = None
        self.sudoku = sudoku
        self.name = name
        self.difficulty = difficulty

    def serialize(self):
        return {
            "id": self.id,
            "sudoku": self.sudoku,
            "name": self.name,
            "difficulty": self.difficulty.value
        }
