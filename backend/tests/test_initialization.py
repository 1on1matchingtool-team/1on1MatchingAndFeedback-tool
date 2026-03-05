# test_initialization.py
# This file tests that the Flask app and database are correctly
# initialized and configured before any real business logic is tested.
# These are the most fundamental tests - if these fail, nothing else will work.

def test_app_is_created(app): #Verifies that the Flask app is successfully created by create_app().
    assert app is not None

def test_app_is_in_testing_mode(app): # Verifies that the test configuration override works correctly.
    assert app.config["TESTING"] is True

def test_database_is_created(database): # Verifies that the database tables are created successfully.
    from sqlalchemy import inspect # Tool for examining DB structure
    inspector = inspect(database.engine) 
    tables = inspector.get_table_names() # Get list of tables in the database
    assert "startups" in tables
    assert "coaches" in tables

