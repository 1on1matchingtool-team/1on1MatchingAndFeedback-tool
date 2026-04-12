# Testing Branch — README

This is an experimental branch. I felt free to play around with pytest here since I had never used it before starting this internship. Nothing here is final. It has been a big learning exercise for me and this readme is here to give guidance to the next interns about how I built it, why I made certain choices and what works and what can be improved.

---

## Background: Why a pytest test suite for this project?

This project is a coaching session management tool that matches startup teams with coaches using an algorithm. It has a Flask backend, a SQLite database, a REST API, and a matching algorithm that reads from and writes to JSON files.

The specific risks that made a test suite necessary:

- The matching algorithm has complex priority logic with 9 priority levels, shadow banning, hard exclusions, and constraints around double booking.
- The validation rules for coaches and startups were spread across multiple files and had inconsistencies.
- The API accepts JSON input from users, which means bad data can come in at any time.

---

## Why Factory Boy and Faker?

When I started thinking about how to generate test data I had several options.

1. Hardcode everything manually. Write plain Python dictionaries in every test file. This works for small test suites but becomes unmanageable quickly.
2. Simple pytest fixtures returning hardcoded data. Better than option 1 because data is centralized but still hardcoded and not flexible for generating variety.
3. Factory Boy + Faker. Factory Boy generates complete model instances with one line of code. Faker fills those instances with realistic random data.

I chose Factory Boy and Faker because: Faker generates different realistic names every time (variety); creating a coach is just CoachFactory() instead of a 10-line dictionary (minimal boilerplate); you only override the specific field you are testing; Factory Boy connects directly to the test database session (database integration).

One important distinction I learned: Faker is great for fields where the specific value does not matter. But for algorithm tests, the specific values drive the logic. Coach_grade = -1 means hard exclusion, meetings_count = 0 means zero meetings priority. So algorithm tests use hardcoded fixtures instead.

---

## The configuration file: why it was needed

I created config.py at the root of the project with two classes, Config for production and TestConfig for testing. Values are read from a .env file using python-dotenv, with sensible defaults if the file is not present. The .env file is in .gitignore and never committed. This means the database name is defined in one place, a new developer copies .env.example to .env and is set up immediately, and tests automatically use different settings without touching production configuration.

---

## TEST_MODE: why I needed to wrap the algorithm

When I reviewed algo.py to prepare for algorithm testing, I found two problems:

1. File loading at import time. The JSON files were loaded at the top of the file, outside any function. Every time a test imports the algorithm, Python immediately tries to open the production data files.
2. Algorithm execution at import time. At the bottom of the file, outside any function, the algorithm was called and results were written back to JSON files. Importing the file in a test would actually run the full algorithm and overwrite production data.

The fix: I added a TEST_MODE environment variable — when True, file loading is skipped entirely. I also wrapped the execution code in if __name__ == "__main__": so it only runs when executing the file directly. The TEST_MODE flag is set automatically in conftest.py before any test runs.

---

## Main findings and things I learned

Boundary value analysis. Test at the edges of allowed ranges, not just the middle. For a name with min 1 and max 50 characters, test at 0, 1, 2, 3, 25, 49, 50, 51, 62. Bugs most commonly hide at boundaries. I built test_constraints.py as a single source of truth: if a constraint changes, it changes in one place.

Invariant testing for the algorithm. The algorithm uses random.shuffle() within priority buckets for fairness. Rather than testing exact order (which would be non-deterministic), we test invariants, which are properties that must always be true. We don't care whether startup A or B goes first within priority 1. We care that all priority 1 startups are assigned before any priority 2 startup.

Inconsistencies discovered through testing. Writing tests revealed that coach_validation.py still referenced CoachName as a single field after the model had been split into FirstName and LastName. There was also an indentation bug causing FirstName and LastName validation to only run for PATCH requests, never for POST.

auto_split_person_name design issue. The validator automatically splits names before validation. This causes problems, e.g. Mary Jane sent as FirstName gets split into FirstName=Mary, LastName=Jane, thus corrupting valid data. Flagged for removal.

Unicode combining characters. Hindi, Bengali, Tamil, and Telugu scripts use combining characters (diacritics) that fall under Unicode category \p{M} not \p{L}. The NAME_ALLOWED_REGEX in base_validators.py only allows \p{L} so these scripts fail. Flagged to colleague for fix.

Double booking is the hardest constraint to test. The internal global_taken_slots structure that prevents double booking is not exposed in the return value. Following mentor's suggestion, we use limited slots + high priority startups + multiple startups at same priority to force deterministic competition. Known gap documented in test_no_double_booking.py.

Title field — format only validation. The Title field is validated by validate_role() which checks format only, not whether the value is in an allowed list. Any string matching the pattern passes. Discussed with mentor.

---

## Test Results

Total: 226 passed, 10 failed out of 236 tests.

All 10 failures are known and documented:

- 8 failures: Hindi, Bengali, Tamil, Telugu scripts blocked by NAME_ALLOWED_REGEX missing \p{M} — colleague's bug to fix
- 1 failure: name--name passes when expected to fail — design decision pending with mentor
- 1 failure: Ó'Brien rejected as startup name because apostrophe not in validate_startup_name pattern — design decision pending with mentor

---

## Test Structure

```
backend/tests/
├── conftest.py              
├── factories.py            
├── test_constraints.py      _ central rules
├── test_coaches.py          — coach validation tests
├── test_startup.py          — startup validation tests
├── test_initialization.py   
└── test_algorithm/
    ├── __init__.py
    ├── conftest.py          — algorithm-specific fixtures 
    ├── test_basic_assignments.py   
    ├── test_zero_meetings.py       
    ├── test_hard_exclusion.py      
    ├── test_no_double_booking.py   
    └── test_priority_matrix.py     
```

---

## Known Gaps and Future Improvements

- Double booking at scale: testing with 50 coaches and 20 startups requires access to global_taken_slots which is internal state not exposed by the return value
- test_edge_cases.py not yet built: scale tests (20 startups, 50 coaches), shadow ban at scale, empty slots at scale
- test_data_integrity.py not yet built: meetings_count incremented correctly, output JSON structure valid
- Integration tests not yet built: tests that go through the actual API endpoints rather than calling validators directly
- Engine tests not yet built: colleague built a new database-driven matching engine (engine.py) that needs its own test branch
- NAME_ALLOWED_REGEX missing \p{M}: blocks Hindi, Bengali, Tamil, Telugu scripts
- auto_split_person_name: corrupts double first names like Mary Jane

---

## How to Run the Tests

Make sure dependencies are installed:

```bash
pip install pytest factory-boy faker python-dotenv regex
```

Run all tests:

```bash
python -m pytest
```

Run a specific file:

```bash
python -m pytest backend/tests/test_coaches.py -v
```

Run just the algorithm tests:

```bash
python -m pytest backend/tests/test_algorithm/ -v
```

Note: use python -m pytest instead of pytest directly on Windows to avoid PATH issues.
