import os
from dotenv import load_dotenv

# Load variables from .env file into the environment
load_dotenv()


class Config:
    """Base configuration. Values are read from the .env file.
    If a value is not set in .env, the default value is used."""

    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    DB_NAME = os.getenv("DB_NAME", "sauna.db")
    DB_PATH = os.getenv("DB_PATH", os.path.join(BASEDIR, "backend", "instance"))

    # Full path to the database, combining path and name
    DB_FULL_PATH = os.path.join(DB_PATH, DB_NAME)

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_FULL_PATH}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    TEST_MODE = False

class TestConfig(Config):
    """Test configuration. Inherits from Config and overrides
    settings for testing."""

    TESTING = True
    SQLALCHEMY_ECHO = False  # Keep terminal clean during tests
    TEST_MODE = True  # signals to algorithm not to load JSON files