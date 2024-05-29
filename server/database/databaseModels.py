from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.baseModel import Base


class SolverModel(Base):
    __tablename__ = "solvers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    solver_settings: Mapped[List["SolverSettingsModel"]] = \
        relationship(back_populates="solver")


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    solver_settings: Mapped[List["SolverSettingsModel"]] = \
        relationship(back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}>"

    def serialize(self):
        return {"id": self.id, }


class SolverSettingsModel(Base):
    __tablename__ = "solver_settings"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["UserModel"] = relationship(back_populates="solver_settings")
    solver_id: Mapped[int] = mapped_column(ForeignKey("solvers.id"))
    solver: Mapped["SolverModel"] = relationship(
        back_populates="solver_settings")

    priority: Mapped[int] = mapped_column()
    enabled: Mapped[int] = mapped_column()
