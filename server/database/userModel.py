from sqlalchemy import Column, Integer, String
from database.baseModel import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    def __repr__(self):
        return f"<User(id={self.id}>"

    def serialize(self):
        return {"id": self.id, }
