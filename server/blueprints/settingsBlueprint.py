from flask import Blueprint, request
from flask_cors import CORS

from blueprints.common import get_user_id
from database.solverRepository import SolverRepository
from database.solverSettingsRepository import SolverSettingsRepository
from mappers.settingsMapper import SettingsMapper
from database.db import db


settings_blueprint = Blueprint("settings", __name__)


@settings_blueprint.route("")
def get_settings():
    user_id = get_user_id()
    if user_id is None:
        return "User not found", 404
    with db.session() as session:
        SolverRepository(session).ensure_seeded()
        dbSettings = SolverSettingsRepository(
            session).get_settings_by_user_id(user_id)
        settings = SettingsMapper().map_from_db_models(dbSettings)
    return settings.serialize()


@settings_blueprint.route("", methods=["PUT"])
def update_settings():
    user_id = get_user_id()
    if user_id is None:
        return "User not found", 404
    json = request.get_json()
    settings = SettingsMapper().map_from_json(json)
    with db.session() as session:
        SolverSettingsRepository(session).update_settings(user_id, settings)
    return settings.serialize()


@settings_blueprint.route("/restore")
def restore_default_settings():
    user_id = get_user_id()
    if user_id is None:
        return "User not found", 404
    with db.session() as session:
        defaults = SolverSettingsRepository(session).restore_defaults(user_id)
        settings = SettingsMapper().map_from_db_models(defaults)
    return settings.serialize()
