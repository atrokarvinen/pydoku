import os
from flask import Flask
from flask_cors import CORS
from database.db import db
from blueprints.authBlueprint import auth_blueprint
from blueprints.importBlueprint import import_blueprint
from blueprints.settingsBlueprint import settings_blueprint
from blueprints.sudokuBlueprint import sudoku_blueprint


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("CONNECTION_STRING")
    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    app.register_blueprint(import_blueprint, url_prefix="/import")
    app.register_blueprint(settings_blueprint, url_prefix="/settings")
    app.register_blueprint(sudoku_blueprint, url_prefix="/sudoku")

    db.init_app(app)
    CORS(app)

    with app.app_context():
        db.create_all()

    return app
