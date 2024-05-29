import unittest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from database.baseModel import Base
from database.databaseModels import UserModel
from database.solverSettingsRepository import SolverSettingsRepository


class TestSolverSettings(unittest.TestCase):
    def setUp(self) -> None:
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        self.session = sessionmaker(bind=engine)()
        self.repository = SolverSettingsRepository(self.session)

    def test_get_settings(self):
        settings = self.repository.get_settings()
        self.assertIsNone(settings)

    def test_get_settings_by_user_id(self):
        settings = self.repository.get_settings_by_user_id(1)
        self.assertGreater(len(settings), 0)

    def test_create_settings(self):
        settings = self.repository.create_settings(1)
        self.assertGreater(len(settings), 0)

    def test_create_relationship(self):
        self.session.add(UserModel())
        self.session.commit()

        created_user = self.session.query(UserModel).first()
        self.assertEqual(created_user.id, 1)

        self.repository.create_settings(1)
        settings = self.repository.get_settings_by_user_id(1)

        self.assertEqual(settings[0].user_id, 1)
        self.assertEqual(settings[0].user.id, 1)

    def test_delete_settings(self):
        settings = self.repository.create_settings(1)
        self.repository.delete_settings(1)
