import sys, os, re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.database.base import db
from backend.database.models.coaches import Coaches
from backend.app import app
from backend.validation.base_validators import (
    normalize_name,
    insert_spaces_if_missing,
    remove_invalid_symbols,
    TITLES
)

def split_name(full_name):
    full_name = normalize_name(full_name)
    full_name = insert_spaces_if_missing(full_name)
    full_name = remove_invalid_symbols(full_name)

    if not full_name:
        return None, "", ""

    parts = full_name.split()
    title = None

    # Detect title
    first_token = parts[0].lower()
    if first_token in TITLES:
        title = parts[0].capitalize().strip(".") + "."
        parts = parts[1:]  # Remove title from the list

    # If nothing left after removing title
    if len(parts) == 0:
        return title,  "", ""
    # If only one name left
    if len(parts) == 1:
        return title, parts[0], ""

    # First name = first token, LastName = rest (middle + last)
    first = parts[0]
    last = " ".join(parts[1:])
    return title, first, last

def migrate():
    with app.app_context():
        coaches = Coaches.query.all()

        for coach in coaches:
            title, first, last = split_name(coach.CoachName)
            coach.Title = title
            coach.FirstName = first
            coach.LastName = last

        db.session.commit()
        print("Migration completed successfully: CoachName → Title + FirstName + LastName")

if __name__ == "__main__":
    migrate()