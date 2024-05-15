from database.userModel import UserModel


class UserRepository:
    def create_user(self, session):
        user = UserModel()
        session.add(user)
        session.commit()
        return user
