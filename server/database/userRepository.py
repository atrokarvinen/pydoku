from database.userModel import UserModel


class UserRepository:
    def get_user(self, session, user_id):
        return session.query(UserModel).filter(UserModel.id == user_id).first()

    def create_user(self, session):
        user = UserModel()
        session.add(user)
        session.commit()
        return user
