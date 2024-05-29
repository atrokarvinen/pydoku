from sqlalchemy import Column, Integer, String
from database.baseModel import Base


class SolverModel(Base):
    __tablename__ = "solvers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
