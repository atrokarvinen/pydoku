import copy
import math
from models.square import Square
from models.elimination import Elimination
from models.eliminationReason import EliminationReason
from models.singleCandidate import SingleCandidate
from testing.easySudoku import easySudoku

type Board = list[list[Square]]


class Sudoku:
    def __init__(self):
        self.board = []
        self.eliminations = []

    def setBoard(self, board: Board):
        self.board = board

    def parse(self) -> Board:
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
                square = Square(i, j, charAsNumber)
                row.append(square)
            board.append(row)

        return board

    def flattenBoard(self, board: Board) -> list[Square]:
        flatBoard = []
        for row in board:
            for square in row:
                flatBoard.append(square)
        return flatBoard

    def addInitialPossibilities(self, board: Board) -> Board:
        initializedBoard = []
        size = len(board)
        for i in range(size):
            boardRow = []
            for j in range(size):
                square = board[i][j]
                number = square.number
                newSquare = Square(i, j, number)
                if (number == 0):
                    possibleNumbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                    newSquare.setPossibleNumbers(possibleNumbers)
                else:
                    newSquare.setNumber(number)
                boardRow.append(newSquare)
            initializedBoard.append(boardRow)

        return initializedBoard

    def scanRows(self, board: Board) -> list[Elimination]:
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
                    for compareColumn in range(size):
                        if (compareColumn == column):
                            continue
                        otherSquare = rows[row][compareColumn]
                        otherNumber = otherSquare.number
                        if (otherNumber == 0):
                            continue
                        if (number == otherNumber):
                            causedBy = EliminationReason(
                                row, compareColumn, number)
                            elimination = Elimination(
                                row, column, number, causedBy)
                            eliminations.append(elimination)

        return eliminations

    def scanColumns(self, board: Board) -> list[Elimination]:
        size = len(board)
        flatSquares = self.flattenBoard(board)

        eliminations = []
        for square in flatSquares:
            row = square.row
            column = square.column
            number = square.number
            if (number != 0):
                continue
            for number in square.possibleNumbers:
                for compareRow in range(size):
                    if (compareRow == row):
                        continue
                    otherSquare = board[compareRow][column]
                    otherNumber = otherSquare.number
                    if (otherNumber == 0):
                        continue
                    if (number == otherNumber):
                        causedBy = EliminationReason(
                            compareRow, column, number)
                        elimination = Elimination(
                            row, column, number, causedBy)
                        eliminations.append(elimination)

        return eliminations

    def getSquaresInBox(self, board: Board, boxIndex: int) -> list[Square]:
        size = len(board)
        boxSize = int(math.sqrt(size))
        flatSquares = self.flattenBoard(board)
        squares = []
        for square in flatSquares:
            box = square.getBox(boxSize)
            if (box == boxIndex):
                squares.append(square)
        return squares

    def scanBoxes(self, board: Board) -> list[Elimination]:
        size = len(board)
        boxSize = math.sqrt(size)
        eliminations = []
        flatSquares = self.flattenBoard(board)

        for square in flatSquares:
            row = square.row
            column = square.column
            number = square.number
            box = square.getBox(boxSize)
            if (number != 0):
                continue
            squaresInBox = self.getSquaresInBox(board, box)
            for number in square.possibleNumbers:
                for otherSquare in squaresInBox:
                    if (otherSquare.row == row and otherSquare.column == column):
                        continue
                    otherNumber = otherSquare.number
                    if (otherNumber == 0):
                        continue
                    if (number == otherNumber):
                        causedBy = EliminationReason(
                            otherSquare.row, otherSquare.column, number)
                        elimination = Elimination(
                            row, column, number, causedBy)
                        eliminations.append(elimination)

        return eliminations

    def getSingleCandidates(self, board: Board) -> list[SingleCandidate]:
        flatSquares = self.flattenBoard(board)

        singleCandidates = []
        for square in flatSquares:
            row = square.row
            column = square.column
            number = square.number
            if (number != 0):
                continue
            possibleNumbers = square.possibleNumbers
            if (len(possibleNumbers) == 0):
                print("No possible numbers")
                continue
            if (len(possibleNumbers) == 1):
                singleCandidate = SingleCandidate(
                    row, column, possibleNumbers[0])
                singleCandidates.append(singleCandidate)

        return singleCandidates

    def isSolved(self, board: Board) -> list[Square]:
        boxSize = math.sqrt(len(board))
        flatSquares = self.flattenBoard(board)
        errorSquares = []
        board[0][0].number = 3
        for square in flatSquares:
            row = square.row
            column = square.column
            box = square.getBox(boxSize)
            if (square.number == 0):
                errorSquares.append(square)
                continue

            squaresInRow = board[row]
            squaresInColumn = [board[i][column] for i in range(len(board))]
            squaresInBox = self.getSquaresInBox(board, box)

            otherSquares = squaresInRow + squaresInColumn + squaresInBox
            for otherSquare in otherSquares:
                if (otherSquare.row == row and otherSquare.column == column):
                    continue
                if (otherSquare.number == square.number):
                    errorSquares.append(square)
                    errorSquares.append(otherSquare)

        uniqueErrorSquares = []
        for errorSquare in errorSquares:
            if (errorSquare not in uniqueErrorSquares):
                uniqueErrorSquares.append(errorSquare)
        return uniqueErrorSquares

    def applyEliminations(self, board: Board, eliminations: list[Elimination]) -> Board:
        boardCopy = copy.deepcopy(board)
        for elimination in eliminations:
            row = elimination.row
            column = elimination.column
            number = elimination.number

            square = boardCopy[row][column]
            square.removePossibleNumber(number)

        return boardCopy

    def applySingleCandidates(self, board: Board, candidates: list[SingleCandidate]) -> Board:
        boardCopy = copy.deepcopy(board)
        for candidate in candidates:
            row = candidate.row
            column = candidate.column
            number = candidate.number

            square = boardCopy[row][column]
            square.setNumber(number)

        return boardCopy
