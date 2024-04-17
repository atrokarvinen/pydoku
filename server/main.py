from flask import Flask
from flask_cors import CORS

from models.sudoku import Sudoku

app = Flask(__name__)
CORS(app)

@app.route("/hello")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/sudoku")
def getSudoku():
    sudoku = Sudoku()
    board = sudoku.parse()
    return [[square.serialize() for square in row] for row in board]

@app.route("/sudoku/notes")
def getSudokuNotes():
    sudoku = Sudoku()
    board = sudoku.parse()
    initializedBoard = sudoku.addInitialPossibilities(board)
    return [[square.serialize() for square in row] for row in initializedBoard]

if __name__ == "__main__":
    app.run(debug=True)