from sqlalchemy.orm import Session

from database.databaseModels import SolverSettingsModel
from database.solverRepository import SolverRepository


class SolverSettingsRepository:
    def __init__(self, session: Session):
        self.session = session
        self.solver_repository = SolverRepository(session)

    def get_settings(self):
        return self.session.query(SolverSettingsModel).first()

    def get_settings_by_user_id(self, user_id):
        print("Getting settings for user:", user_id)
        settings = self.session\
            .query(SolverSettingsModel)\
            .filter(SolverSettingsModel.user_id == user_id)\
            .first()
        if settings is None:
            print("Settings not found, creating new settings")
            return self.create_settings(user_id)
        return settings

    def create_settings(self, user_id):
        solvers = self.solver_repository.get_solvers()
        solver_settings = []
        for (index, solver) in enumerate(solvers):
            setting = SolverSettingsModel(
                user_id=user_id,
                solver_id=solver.id,
                priority=index,
                enabled=1)
            solver_settings.append(setting)
        self.session.add_all(solver_settings)
        self.session.commit()
        print("Created new settings for user:", user_id)
        return solver_settings

    def delete_settings(self, user_id):
        settings = self.get_settings_by_user_id(user_id)
        self.session.delete(settings)
        self.session.commit()
        print("Deleted settings for user:", user_id)
