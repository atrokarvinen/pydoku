from sqlalchemy import Column, Integer, String
from database.baseModel import Base


class SudokuModel(Base):
    __tablename__ = "sudokus"

    id = Column(Integer, primary_key=True, index=True)
    sudoku = Column(String)
    user_id = Column(Integer)

    def __repr__(self) -> str:
        return f"<Sudoku(id={self.id}, sudoku={self.sudoku}, user_id={self.user_id})>"
