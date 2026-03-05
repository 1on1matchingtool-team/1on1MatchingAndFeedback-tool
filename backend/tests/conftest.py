import pytest
from backend.app import create_app
from backend.database.base import db as _db

# conftest.py is a special pytest file that holds fixtures.
# Fixtures are reusable setup functions that pytest automatically
# injects into tests that request them by name.
# This file is discovered automatically by pytest - no imports needed.


@pytest.fixture
def app():
    """
    Creates a fresh Flask app configured for testing.
    
    Key differences from the real app:
    - Uses an in-memory SQLite database (not sauna.db)
    - TESTING=True makes Flask propagate errors instead of hiding them
    - SQLALCHEMY_ECHO=False keeps the terminal output clean during tests
    """

    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_ECHO": False,
    })
    return app

@pytest.fixture
def database(app):
    """
    Creates all database tables before each test and drops them after.
    
    Uses 'yield' to split setup and teardown in one function:
    - Everything before yield runs BEFORE the test
    - Everything after yield runs AFTER the test
    
    This ensures every test starts with a clean empty database.
    """
    with app.app_context():
        _db.create_all()
        yield _db
        _db.drop_all()