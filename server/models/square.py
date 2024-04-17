class Square:
  def __init__(self, row, column, number):
    self.row = row
    self.column = column
    self.number = number
    self.possibleNumbers = []
    
  def setNumber(self, number):
    self.number = number
    self.possibleNumbers = []
    
  def setPossibleNumbers(self, possibleNumbers):
    self.number = 0
    self.possibleNumbers = possibleNumbers
    
  def removePossibleNumber(self, number):
    if (number in self.possibleNumbers):
      self.possibleNumbers.remove(number)
  
  def serialize(self):
    return {
      "row": self.row,
      "column": self.column,
      "number": self.number,
      "possibleNumbers": self.possibleNumbers
    }
  