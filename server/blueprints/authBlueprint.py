from flask import Blueprint
from database.db import db
from database.userRepository import UserRepository


auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/create")
def create_user():
    with db.session() as session:
        user = UserRepository(session).create_user()
        return user.serialize()
