class Square:
    def __init__(self, row: int, column: int, number: int):
        self.row = row
        self.column = column
        self.number = number
        self.possibleNumbers = []

    def getBox(self, boxSize: int) -> int:
        return (self.row // boxSize) * boxSize + self.column // boxSize

    def setNumber(self, number: int):
        self.number = number
        self.possibleNumbers = []

    def setPossibleNumbers(self, possibleNumbers: list[int]):
        self.possibleNumbers = possibleNumbers

    def removePossibleNumber(self, number: int):
        if (number in self.possibleNumbers):
            self.possibleNumbers.remove(number)

    def serialize(self):
        return {
            "row": self.row,
            "column": self.column,
            "number": self.number,
            "possibleNumbers": self.possibleNumbers
        }
