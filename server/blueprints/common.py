from flask import request


def get_user_id():
    if "UserId" not in request.headers:
        return None
    headers = request.headers
    return headers["UserId"]
