import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DB_URI = os.getenv('DB_URI', )
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = os.getenv('DEBUG', False)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
