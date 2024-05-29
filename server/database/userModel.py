from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.baseModel import Base
from database.solverSettingsModel import SolverSettingsModel


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    solver_settings: Mapped[List[SolverSettingsModel]] = \
        relationship(back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}>"

    def serialize(self):
        return {"id": self.id, }
