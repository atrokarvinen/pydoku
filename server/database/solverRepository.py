from sqlalchemy.orm import Session

from database.databaseModels import SolverModel


class SolverRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_solvers(self) -> list[SolverModel]:
        self.ensure_seeded()
        return self.session.query(SolverModel).all()

    def ensure_seeded(self):
        solvers = self.session.query(SolverModel).all()
        if (len(solvers) > 0):
            return
        self.session.add_all([
            SolverModel(name="Scan"),
            SolverModel(name="Single Candidate"),
            SolverModel(name="Naked Pair"),
            SolverModel(name="Pointing"),
            SolverModel(name="Claiming"),
            SolverModel(name="Hidden Pair"),
            SolverModel(name="X-Wing"),
            SolverModel(name="Simple Coloring"),
            SolverModel(name="Y-Wing"),
            SolverModel(name="Empty Rectangle"),
            SolverModel(name="Bi-Value Universal Grave"),
            SolverModel(name="X-Cycle")
        ])
        self.session.commit()
