from models.square import Square
from models.elimination import Elimination
from models.eliminationReason import EliminationReason
from testing.easySudoku import easySudoku

class Sudoku:
  def __init__(self, board):
    self.board = board
    self.solved_board = board
    self.solved = False

  def parse(self):
    print("Solving sudoku...")
    print("easy sudoku:" + str(easySudoku))
    
    size = 9
    sudokuLength = len(easySudoku)
    if (sudokuLength != size*size):
      print("Invalid sudoku length")
      return
    
    charArray = list(easySudoku)
    board = []
    for i in range(size):
      row = []
      for j in range(size):
        char = charArray[i*size+j]
        if (char == '.'):
          charAsNumber = 0
        else:
          charAsNumber = int(char)
        row.append(charAsNumber)
      board.append(row)
      print(str(row))
    
    return board
  
  def addInitialPossibilities(self, board):
    initializedBoard = []
    size = len(board)
    for i in range(size):
      boardRow = []
      for j in range(size):
        number = board[i][j]
        square = Square(i,j)
        if (number == 0):
          possibleNumbers = [1,2,3,4,5,6,7,8,9]
          square.setPossibleNumbers(possibleNumbers)
        else:
          square.setNumber(number)
        boardRow.append(square)
      initializedBoard.append(boardRow)
    
    return initializedBoard
        
  def scanRows(self, board):
    size = len(board)
    rows = board

    eliminations = []
    for row in range(size):
      for column in range(size):
        square = rows[row][column]
        squareNumber = square.number
        if (squareNumber != 0):
          continue
        for number in square.possibleNumbers:
          for i in range(size):
            if (i == column):
              continue
            otherSquare = rows[row][i]
            otherNumber = otherSquare.number
            if (otherNumber == 0):
              continue
            if (number == otherNumber):
              print("Elimination in row:" + str(row) + " column:" + str(column) + " number:" + str(number))
              causedBy = EliminationReason(row, column=i)
              elimination = Elimination(row, column, number, causedBy)
              eliminations.append(elimination)
    
    return eliminations
    # print ("rows:" + str(rows))
    
  def scanColumns(self,board):
    size = len(board)
    columns = []
    for i in range(size):
      column = []
      for j in range(size):
        column.append(board[j][i])
      columns.append(column)
    
    print("columns:" + str(columns))
    