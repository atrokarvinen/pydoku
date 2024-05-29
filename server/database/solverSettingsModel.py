from sqlalchemy import ForeignKey
from database.baseModel import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship


class SolverSettingsModel(Base):
    __tablename__ = "solver_settings"

    id: Mapped[int] = mapped_column(primary_key=True)

    # user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # user: Mapped[UserModel] = relationship(back_populates="solver_settings")
    # solver_id: Mapped[int] = mapped_column(ForeignKey("solvers.id"))

    user_id: Mapped[int] = mapped_column()
    solver_id: Mapped[int] = mapped_column()

    priority: Mapped[int] = mapped_column()
    enabled: Mapped[int] = mapped_column()
