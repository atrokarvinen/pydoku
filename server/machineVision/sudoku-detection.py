from sudokuDetector import SudokuDetector

detector = SudokuDetector()


def test_detect_sudoku(file_path: str, expected_sudoku: str):
    base_path = "C:/Users/atro.karvinen/source/repos/2-omat-projektit/pydoku/server/machineVision/testImages/"
    full_path = base_path + file_path
    img = detector.load_image(full_path)
    sudoku = detector.detect(img)
    print("detected sudoku: " + sudoku)
    print("expected sudoku: " + expected_sudoku)


# Sudoku 1
expected_sudoku = "7...9..126.5....4.2..7.........7.........927...325.9.1.68.2.....4..15.6..9.6.352."
test_detect_sudoku("sudoku_with_noise.JPG", expected_sudoku)

# Sudoku 2
expected_sudoku = "8321..4..7....921.1...48.5..8...7.3161...4...2..8...4...9....85.......6......237."
test_detect_sudoku("example_sudoku_hard.JPG", expected_sudoku)

# Sudoku 3
expected_sudoku = "....873.9...9.6....45........48..6.528.....915.6..17........56....3.8...4.856...."
test_detect_sudoku("screenshot_dark_mode.jpg", expected_sudoku)

# Sudoku 4
expected_sudoku = "....873.9...9.6....45........48..6.528.....915.6..17........56....3.8...4.856...."
test_detect_sudoku("screenshot_light_mode.jpg", expected_sudoku)
