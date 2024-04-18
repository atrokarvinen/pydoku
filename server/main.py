from flask import Flask, request
from flask_cors import CORS

from models.sudoku import Sudoku

app = Flask(__name__)
CORS(app)

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

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

@app.route("/sudoku/row-scan", methods=["POST"])
def scanSudokuRows():
    payload = request.get_json()
    sudoku = payload["sudoku"]
    print(sudoku)
    return sudoku

if __name__ == "__main__":
    app.run(debug=True)