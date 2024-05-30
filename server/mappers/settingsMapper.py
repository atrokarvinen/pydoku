from database.databaseModels import SolverSettingsModel
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

    def map_from_db_models(self, models: list[SolverSettingsModel]) -> Settings:
        settings = Settings()
        settings.solvers = [self.map_from_db_model(m) for m in models]
        return settings

    def map_from_db_model(self, model: SolverSettingsModel) -> Solver:
        solver = Solver(model.solver.name)
        solver.id = model.solver_id
        solver.priority = model.priority
        solver.enabled = model.enabled
        return solver
