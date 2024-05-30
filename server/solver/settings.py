from solver.solver import Solver
from solver.solverFactory import SolverFactory
from techniques.solverBase import SolverBase


class Settings:
    def __init__(self) -> None:
        self.solvers: list[Solver] = self.get_solvers()
        self.solver_factory = SolverFactory()

    def get_solvers(self) -> list[Solver]:
        solvers = [
            Solver("Scan"),
            Solver("Single Candidate"),
            Solver("Naked Pair"),
            Solver("Pointing"),
            Solver("Claiming"),
            Solver("Hidden Pair"),
            Solver("X-Wing"),
            Solver("Simple Coloring"),
            Solver("Y-Wing"),
            Solver("Empty Rectangle"),
            Solver("Bi-Value Universal Grave"),
            Solver("X-Cycle"),
        ]
        for index, solver in enumerate(solvers):
            solver.id = str(index + 1)
            solver.priority = index
            solver.enabled = True
        return solvers

    def create_solvers(self) -> list[SolverBase]:
        return [self.solver_factory.create_solver(solver) for solver in self.solvers if solver.enabled]

    def serialize(self):
        return {"solvers": [solver.serialize() for solver in self.solvers]}
