from flask import Flask
from config import Config



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from app.main import bp as bp_main
    app.register_blueprint(bp_main)


    return app