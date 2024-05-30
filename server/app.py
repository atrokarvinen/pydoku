from appFactory import create_app
from dotenv import load_dotenv
from flask import Response

load_dotenv()

app = create_app()


@app.after_request
def after_request(response: Response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,UserId')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response
