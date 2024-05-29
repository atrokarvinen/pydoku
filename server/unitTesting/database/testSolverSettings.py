import unittest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from database.baseModel import Base
from database.relaModel import Child, Parent
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

    def test_create_settings(self):
        settings = self.repository.create_settings(1)
        self.assertIsNotNone(settings)

    def test_get_settings_by_user_id(self):
        settings = self.repository.get_settings_by_user_id(1)
        self.assertGreater(len(settings), 0)

    def test_relationship(self):
        parent = self.session.query(Parent).first()
        child = self.session.query(Child).first()

        self.session.add(Parent())
        self.session.commit()

        parent2 = self.session.query(Parent).first()
        self.assertIsNotNone(parent2)

        self.session.add(Child(parent_id=parent2.id))
        self.session.commit()

        child2 = self.session.query(Child).first()
        self.assertIsNotNone(child2)
        self.assertIsNotNone(child2.parent)
        pass
