# tests/factories.py
# Factory Boy factories for generating test data.
# Use these instead of manually creating model instances in tests.

import factory
from factory.faker import Faker
from backend.database.base import db
from backend.database.models.coaches import Coaches
from backend.database.models.startups import Startups


class CoachFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory for creating Coach instances in the test database."""

    class Meta:
        model = Coaches
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    # Required fields
    FirstName = Faker("first_name")
    LastName = Faker("last_name")
    Email = factory.Sequence(lambda n: f"coach{n}@example.com")

    # Optional fields
    Phone = Faker("phone_number")
    Chat = None
    Bio = Faker("text", max_nb_chars=500)
    Expertise = Faker("job")
    SocialMedia = None

    # Counters
    CoachingSessions = 0
    BatchesCoached = 0


class StartupFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory for creating Startup instances in the test database."""

    class Meta:
        model = Startups
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    # Required fields
    StartupName = Faker("company")
    Website = factory.Sequence(lambda n: f"https://www.startup{n}.com")
    Status = "alive"
    PreviousNames = []
    StartupMembers = [
        {
            "name": "Startup Founder",
            "email": "founder@example.com",
            "role": "founder"
        }
    ]   

    # Optional fields
    StartupSocialMedia = None
    StartupDescription = Faker("catch_phrase")

    # Internal field
    MeetingsCount = 0