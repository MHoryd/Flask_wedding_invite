import os

class Config:
    STATIC_URL_PATH = 'static'
    SECRET_KEY = os.environ.get('Flask_app_secret_key')