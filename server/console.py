from models.sudoku import Sudoku

def run():
  print("Starting server...")
  sudoku = Sudoku(board=1)
  board = sudoku.parse()
  print("Parsed board:" + str(board))
  initializedBoard = sudoku.addInitialPossibilities(board)
  # sudoku.scanColumns(board)
  eliminations = sudoku.scanRows(initializedBoard)
  print("Eliminations:" + str(len(eliminations)))

run()