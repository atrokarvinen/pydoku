from models.sudoku import Sudoku


def run():
    sudoku = Sudoku()
    board = sudoku.parse()
    print("Parsed board:" + str(board))
    initializedBoard = sudoku.add_initial_possibilities(board)
    # sudoku.scanColumns(board)
    eliminations = sudoku.scan_rows(initializedBoard)
    print("Eliminations:" + str(len(eliminations)))


run()
