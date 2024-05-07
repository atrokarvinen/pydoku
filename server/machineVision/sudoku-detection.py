from sudokuDetector import SudokuDetector

detector = SudokuDetector()

# Sudoku 1
sudoku = detector.detect(
    "C:/Users/atro.karvinen/source/repos/2-omat-projektit/pydoku/server/machineVision/testImages/sudoku_with_noise.JPG")

print("detected sudoku: " + sudoku)
expected_sudoku = "7...9..126.5....4.2..7.........7.........927...325.9.1.68.2.....4..15.6..9.6.352."
print("expected sudoku: " + expected_sudoku)

# Sudoku 2
sudoku = detector.detect(
    "C:/Users/atro.karvinen/source/repos/2-omat-projektit/pydoku/server/machineVision/testImages/example_sudoku_hard.JPG")

print("detected sudoku: " + sudoku)
expected_sudoku = "8321..4..7....921.1...48.5..8...7.3161...4...2..8...4...9....85.......6......237."
print("expected sudoku: " + expected_sudoku)
