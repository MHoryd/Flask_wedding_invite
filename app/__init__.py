from flask import Flask,jsonify
from config import Config
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(key_func=get_remote_address, storage_uri="memory://")

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    limiter.init_app(app)
    from app.main import bp as bp_main
    app.register_blueprint(bp_main)


    return app