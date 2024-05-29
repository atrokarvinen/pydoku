from sqlalchemy.orm import Session
from database.databaseModels import UserModel


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_user(self, user_id):
        return self.session.query(UserModel).filter(UserModel.id == user_id).first()

    def create_user(self):
        user = UserModel()
        self.session.add(user)
        self.session.commit()
        return user
