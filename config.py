import os

class Config:
    STATIC_URL_PATH = 'static'
    SECRET_KEY = os.getenv('Flask_app_secret_key')