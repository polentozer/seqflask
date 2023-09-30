"""Flask config"""
from os import path, environ
from dotenv import load_dotenv

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"))


class Config:
    """Flask configuration variables."""

    # General config
    FLASK_APP = environ.get("FLASK_APP")
    FLASK_ENV = environ.get("FLASK_ENV")
    SECRET_KEY = environ.get("SECRET_KEY")
    DEBUG = environ.get("DEBUG")

    # Static assets
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
