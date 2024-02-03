from flask import Flask
from config import Config
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os, json

limiter = Limiter(key_func=get_remote_address, storage_uri="memory://")

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    limiter.init_app(app)
    from app.main import bp as bp_main
    app.register_blueprint(bp_main)
    ensure_answers_json_exists()


    return app


def ensure_answers_json_exists():
    answers_json_path = "answers.json"
    if not os.path.exists(answers_json_path):
        with open(answers_json_path, 'w') as file:
            json.dump([], file)