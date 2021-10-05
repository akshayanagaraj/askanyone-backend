from flask import Flask, Blueprint, jsonify, request, make_response, Response
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
#from auth import generate_token, get_user_details
from askanyone_v1.router import askanyone_v1


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response

app.register_blueprint(askanyone_v1, url_prefix='/api/v1/')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)