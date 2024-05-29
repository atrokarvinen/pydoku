from solver.settings import Settings
from solver.solver import Solver


class SettingsMapper:
    def map_from_json(self, data) -> Settings:
        settings = Settings()
        settings.solvers = [self.map_solver_from_json(
            solver) for solver in data["solvers"]]
        return settings

    def map_solver_from_json(self, data) -> Solver:
        solver = Solver(data["name"])
        solver.id = data["id"]
        solver.priority = data["priority"]
        solver.enabled = data["enabled"]
        return solver
