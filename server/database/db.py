from flask_sqlalchemy import SQLAlchemy

from database.baseModel import Base


db = SQLAlchemy(model_class=Base)
