class Square:
  def __init__(self, row, column):
    self.row = row
    self.column = column
    self.number = 0
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
  
  
  