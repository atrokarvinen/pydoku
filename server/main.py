from flask import Flask, request
from flask_cors import CORS

from models.sudoku import Sudoku
from mappers.sudokuMapper import SudokuMapper

app = Flask(__name__)
CORS(app)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response


@app.route("/sudoku")
def getSudoku():
    sudoku = Sudoku()
    board = sudoku.parse()
    return serializeBoard(board)


@app.route("/sudoku/notes")
def getSudokuNotes():
    sudoku = Sudoku()
    board = sudoku.parse()
    initializedBoard = sudoku.addInitialPossibilities(board)
    return serializeBoard(initializedBoard)


@app.route("/sudoku/row-scan", methods=["POST"])
def scanSudokuRows():
    sudokuJson = request.get_json()
    mapper = SudokuMapper()
    sudoku = mapper.mapFromJson(sudokuJson)
    board = sudoku.board
    eliminations = sudoku.scanRows(board)
    eliminatedSudoku = sudoku.applyEliminations(board, eliminations)
    # return serializeBoard(eliminatedSudoku)
    return serializeEliminations(eliminations)


@app.route("/sudoku/column-scan", methods=["POST"])
def scanSudokuColumns():
    sudokuJson = request.get_json()
    mapper = SudokuMapper()
    sudoku = mapper.mapFromJson(sudokuJson)
    board = sudoku.board
    eliminations = sudoku.scanColumns(board)
    eliminatedSudoku = sudoku.applyEliminations(board, eliminations)
    return serializeBoard(eliminatedSudoku)


@app.route("/sudoku/box-scan", methods=["POST"])
def scanSudokuBoxes():
    sudokuJson = request.get_json()
    mapper = SudokuMapper()
    sudoku = mapper.mapFromJson(sudokuJson)
    board = sudoku.board
    eliminations = sudoku.scanBoxes(board)
    eliminatedSudoku = sudoku.applyEliminations(board, eliminations)
    return serializeBoard(eliminatedSudoku)


@app.route("/sudoku/all-scan", methods=["POST"])
def scanSudokuAll():
    sudokuJson = request.get_json()
    mapper = SudokuMapper()
    sudoku = mapper.mapFromJson(sudokuJson)
    board = sudoku.board
    rowEliminations = sudoku.scanRows(board)
    columnEliminations = sudoku.scanColumns(board)
    boxEliminations = sudoku.scanBoxes(board)
    eliminations = rowEliminations + columnEliminations + boxEliminations
    eliminatedSudoku = sudoku.applyEliminations(board, eliminations)
    return serializeBoard(eliminatedSudoku)


@app.route("/sudoku/single-candidate", methods=["POST"])
def getSingleCandidates():
    sudokuJson = request.get_json()
    mapper = SudokuMapper()
    sudoku = mapper.mapFromJson(sudokuJson)
    board = sudoku.board
    singleCandidates = sudoku.getSingleCandidates(board)
    newSudoku = sudoku.applySingleCandidates(board, singleCandidates)
    return serializeBoard(newSudoku)


@app.route("/sudoku/is-solved", methods=["POST"])
def checkSudokuSolved():
    sudokuJson = request.get_json()
    mapper = SudokuMapper()
    sudoku = mapper.mapFromJson(sudokuJson)
    board = sudoku.board
    errorSquares = sudoku.isSolved(board)
    return [square.serialize() for square in errorSquares]


def serializeBoard(board):
    return [[square.serialize() for square in row] for row in board]


def serializeEliminations(eliminations):
    return [elimination.serialize() for elimination in eliminations]


if __name__ == "__main__":
    app.run(debug=True)
