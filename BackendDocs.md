# Backend Documentation
#### Updated 24 June 2026

## Table of Contents

1. [Overview](#1-overview)
2. [Folder Structure](#2-folder-structure)
3. [Configuration](#3-configuration)
4. [Key Files and Components](#4-key-files-and-components)
5. [Database Models](#5-database-models)
6. [API Endpoints](#6-api-endpoints)
7. [Validation Testing](#7-validation-testing)
8. [Cascade Delete Behavior](#8-cascade-delete-behavior)
9. [API v1 (Routing Layer)](#9-api-v1-routing-layer)
10. [Data Generation Scripts](#10-data-generation-scripts)
11. [Environment Variables](#11-environment-variables)

---

## 1. Overview

The backend of the **1on1MatchingAndFeedbackTool** utilizes Flask and Flask-SQLAlchemy for data management, offering full CRUD support for seven core models. 
It features a validation layer enforcing type rules and consistent error responses, managing data for startups, coaches, scheduling, and feedback via an SQLite database (`sauna.db`). 
Additionally, it includes a matching engine that assigns startups to coach slots based on priority, availability, and bans, ensuring conflict-free scheduling.

---

## 2. Folder Structure

```plaintext
backend/
├── api_v1/
│   ├── __init__.py
│   ├── banned_to_meet_routes.py
│   ├── coach_assignments_routes.py
│   ├── coach_routes.py
│   ├── coach_slots_routes.py
│   ├── daily_feedback_routes.py
│   ├── feedback_history_routes.py
│   ├── routes.py
│   └── startup_routes.py
├── data/
│   ├── assigned_startups.json
│   ├── assigned_startups_count.json
│   ├── coaches.json
│   ├── coachTimeWithBreaks.json
│   ├── daily_feedbacks.json
│   ├── startups.json
│   └── total_feedbacks.json
├── database/
│   ├── models
│   │   ├── banned_to_meet.py
│   │   ├── coach_assignments.py
│   │   ├── coach_slots.py
│   │   ├── coaches.py
│   │   ├── daily_feedback.py
│   │   ├── feedback_history.py
│   │   └── startups.py
│   ├── __init__.py
│   └── base.py
├── dataGen/
│   ├── info
│   │   ├── db_model.jpg
│   │   ├── db_model_updated_mar2026.jpg
│   │   ├── logic.model.jpg
│   │   ├── rules.md
│   │   └── tested_data.md
│   ├── filling_feedbacks.py
│   ├── gen_daily_feedbacks.py
│   ├── genCoachTime.py
│   ├── genStartups.py
│   ├── helper_meetings_count.py
│   ├── remove_shadow_ban.py
│   └── user_match_restrictor.py
├── instance/
│   └── sauna.db
├── matching_engine/
│   └── engine.py
├── scripts/
│   └── migrate_coach_names.py
├── testDatasets/
│    ├── testSet1/
│    │   ├── algo_output.md
│    │   ├── expected_assigned_startups.json
│    │   ├── expected_startups.json
│    │   ├── test_coachTimeWithBreaks.json
│    │   ├── test_startups.json
│    │   └── test_total_feedbacks.json
│    └── testSet2/
│    │   ├── algo_output.md
│    │   ├── expected_assigned_startups.json
│    │   ├── expected_startups.json
│    │   ├── test_coachTimeWithBreaks.json
│    │   ├── test_startups.json
│    │   └── test_total_feedbacks.json
│    └── testSetInformation.md
├── validation/
│   ├── banned_validation.py
│   ├── base_validators.py
│   ├── coach_assigment_validation.py
│   ├── coach_slot_validation.py
│   ├── coach_validation.py
│   ├── daily_feedback_validation.py
│   ├── feedback_history_validation.py
│   └── startup_validation.py
├── __init__.py
├── algo.py
├── app.py
├── date_utils.py
├── requirements.txt
├── schema.sql
└── schema_clean.sql
```

---

## 3. Configuration

- **Database**: SQLite `sauna.db`
- **Database URI**: `sqlite:///instance/sauna.db`
- **CORS**: Enabled for `http://localhost:3000`
- **Logging**: SQLAlchemy echo enabled for development
- **Models**: 7 tables with full foreign key relationships
- **Validation**: Unified validation layer for all POST and PATCH requests, including type checks, JSON shape rules, unknown‑field rejection, and logical constraints
- **Error Handling**: Consistent JSON error responses across all endpoints
- **ERD**: Located at `backend/dataGen/info/db_model_updated_feb2026.png`


---

## 4. Key Files and Components

### 4.1 `app.py`

This is the main entry point of the backend. It initializes Flask, configures the database, registers all CRUD routes, and applies the unified validation layer.

#### Features:
- Initializes Flask‑SQLAlchemy with `sauna.db`
- Registers CRUD routes for all seven models
- Applies validation for POST and PATCH requests
- Provides health and database connectivity checks
- Enables CORS for frontend integration
- Ensures consistent JSON error responses
- Ensures all models are imported before executing `db.create_all()` to fix missing tables and foreign keys.
- Handles `IntegrityError` for duplicate coach emails, returning clean JSON.

### 4.2 **`database/__init__.py`**

This file imports and exposes all database models, so they can be accessed easily throughout the application.

#### Imports:

- Models: `BannedToMeet`, `CoachAssignments`, `Coaches`, `CoachSlots`, `DailyFeedback`, `FeedbackHistory`, `Startups`

#### Purpose:

- Provides centralized access to all database models.
- Ensures app.py and other modules can import models from a single location.

### 4.3 **`database/base.py`**

- Defines and initializes the shared SQLAlchemy database object used across the backend.
- Ensures SQLAlchemy metadata is initialized and foreign key constraints are enforced (SQLite PRAGMA enabled in app.py).

```python
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
```

### 4.4 **Models in `database/models`**

The models represent the schema and data structure for entities in the application using SQLAlchemy ORM. They correspond directly to the tables in `sauna.db` and the ERD diagram.
JSON‑based fields (such as StartupMembers and SocialMedia) are stored as TEXT and validated before saving. All models support partial updates through PATCH with strict validation.

Key Models are presented in **Database Models**.

### 4.5 Documentation and Schema Files

#### 4.5.1 **`backend/dataGen/info/db_model_updated_mar2026.png`**
Updated ERD (Entity–Relationship Diagram) reflecting the current database schema.

#### 4.5.2 **`backend/dataGen/info/rules.md`**
Contains matching logic, constraints, and business rules.
Updated to align with the new structured coach naming and consistent foreign key relationships. 

#### 4.5.3 **`backend/dataGen/info/tested_data.md`**
Includes sample data and meeting count tests used during development.
Also documents cascade delete test scenarios performed in March 2026. 

#### 4.5.4 **`schema_clean.sql`**
- Clean SQL schema used for generating the ERD, reflects:
  - DailyFeedback / FeedbackHistory → StartupId NULL
  - CoachAssignments / BannedToMeet → StartupId NOT NULL
- Uses unquoted identifiers and SQLite-compatible types.

#### 4.5.5 **`schema.sql`**
Full backend schema with:
- Updated constraints
- Unique email for Coaches
- Correct delete behavior
- JSON fields
- Updated name fields

#### 4.5.6 **`engine.py`**
- Contains the core matching logic used to assign startups to coach slots.
- Filters valid slots, applies priority rules, enforces bans, prevents double‑booking, and writes finalized assignments to the database.

#### 4.5.7 **`date_utils.py`**
- Provides centralized date‑parsing utilities used across routes and the matching engine. 
- Standardizes how dates are interpreted, prevents inconsistent formats, and avoids circular imports.
- Ensures consistent date parsing for delete logic and slot filtering.

---

## 5. Database Models

All models are defined in `database/models`.
Each model corresponds to a table in `sauna.db` and follows a consistent structure with:
- clearly defined columns
- foreign‑key relationships
- JSON‑based fields stored as TEXT
- unified validation for `POST`/`PATCH`
- delete behavior mainly for startup and coach
- The full schema is shown in `(db_model_updated_mar2026.png)`.

### 5.1 Startups
Represents a startup participating in the program.

**Key characteristics:**
- Uses strict validation for JSON fields:
  - `StartupMembers`(human name rules, no emoji/digits)
  - `StartupSocialMedia`: (warning‑based)
  - `Website`: (warning‑based)
- Tracks automatic name history in `PreviousNames` on `PATCH`
- Tracks metadata such as `Status`, `MeetingsCount`, and `Website`
- Connected to: `DailyFeedback`, `FeedbackHistory`, `CoachAssignments`, `BannedToMeet`
- Delete behavior:
   - DailyFeedback.StartupId → set to NULL
   - FeedbackHistory.StartupId → set to NULL
   - CoachAssignments.StartupId → NOT NULL (blocks deletion)
   - BannedToMeet.StartupId → NOT NULL (blocks deletion)
   - Startup can only be deleted after dependent rows are removed

### 5.2 Coaches
Represents a coach in the program.

**Key characteristics:**
- Uses structured name fields: `Title`, `FirstName`, `LastName`
- Human name validation: Unicode letters + accents only (no emoji/digits)
- Email is unique; duplicate email returns clean error
- SocialMedia is warning‑based and flexible
- Connected to: `CoachSlots`, `CoachAssignments`, `DailyFeedback`, `FeedbackHistory`, `BannedToMeet`
- Delete behavior:
  - Future slots + assignments removed
  - Past assignments kept
  - DailyFeedback.CoachId → NULL
  - FeedbackHistory.CoachId → NULL

### 5.3 CoachSlots
Represents available time slots for each coach.

**Key characteristics:**
- Includes `Date`, `Slot`, `Duration`, and `IsBreak`
- Linked to `CoachId`
- Used by the matching engine and assignment logic
- Deleting a coach removes all future slots; past slots remain for history

### 5.4 CoachAssignments
Represents the mapping between a coach, a startup, and a specific slot and tracks scheduled 1‑on‑1 meetings.

**Key characteristics:**
- Includes `CoachId`, `StartupId`, `SlotId`, `Date`, `Duration`, `Slot`
- `StartupId` is NOT NULL (blocks startup deletion)
- Deleting a coach removes future assignments; past assignments remain
- Startup deletion requires manual removal of assignments first

### 5.5 DailyFeedback
Represents daily feedback after each meeting.

**Key characteristics:**
- Stores `FeedbackText`and `Date`
- Linked to `CoachId` and `StartupId`
- Forms the basis for historical feedback tracking
- CoachId and StartupId becomes NULL when deleted
- Feedback is never deleted automatically (Past feedback remains)

### 5.6 FeedbackHistory
Represents historical revisions of feedback.

**Key characteristics:**
- Stores original + updated grades and timestamps
- Linked to `DailyFeedbackId`, `StartupId`, and `CoachId`
- Uses corrected field names: `StartupTextFeedback`, `CoachTextFeedback`, `UpdatedStartupGrade`, `DateUpdatedStartupGrade`
- CoachId and StartupId becomes NULL when deleted
- Never deleted automatically

### 5.7 BannedToMeet
Represents restrictions preventing certain coach–startup meetings.

**Key characteristics:**
- Stores `DateFrom`, `DateTo`, and `Reason`
- Enforces logical constraints (`DateTo ≥ DateFrom`)
- Used by the matching engine to avoid invalid pairings
- `StartupId` is **NOT NULL** → blocks startup deletion
- Rows remain even if startup is deleted (must be removed manually first)

---

## 6. API Endpoints

The backend exposes RESTful CRUD endpoints for all seven core models and cascade behavior. Each model supports:

- **GET** (list and single item)
- **POST** (create)
- **PATCH** (partial update with strict validation)
- **DELETE** (remove)

All POST/PATCH requests pass through the unified validation layer, which enforces:
- type checking  
- JSON shape rules  
- unknown‑field rejection  
- logical constraints (e.g., `DateTo ≥ DateFrom`)  
- Website + SocialMedia warning system
- consistent JSON error responses
- limit length of characters

Below is a summary of each model’s endpoints and example request/response formats.

---

### 6.1 **Root Endpoint**

`GET /`: Returns a simple health check.

```json
{ "message": "API is running" }
```

### 6.2 **Database Connectivity**

`GET /test-db`: Verifies that the backend can connect to the SQLite database.

#### Response:

```json
{ "message": "Database connected successfully", "status": "ok" }
```

### 6.3 **Database Model Endpoints**

### **6.3.1 Startups**

**Endpoints**: 
- `GET /startups/all`
- `GET /startups/<id>`
- `POST /startups`
- `PATCH /startups/<id>`
- `DELETE /startups/<id>`

#### Example POST:

```json
{
  "StartupName": "Example Startup",
  "Website": "https://example.com",
  "Status": "alive",
  "StartupMembers": [
    {
      "name": "Alice Founder",
      "email": "alice@example.com",
      "role": "CEO"
    }
  ]
}
```

#### Example PATCH (Valid):
Update startup status

```json
{ "Status": "on-pause" }
```

#### Example Error (Invalid Type):
Status must be one of the allowed values

```json
{ "error": "Status must be one of: alive, on-pause, dead" }
```

### **6.3.2 Coaches**

**Endpoints**: 
- `GET /coaches/all`
- `GET /coaches/<id>`
- `POST /coaches`
- `PATCH /coaches/<id>`
- `DELETE /coaches/<id>`


#### Example POST:

```json
{
  "FirstName": "John",
  "LastName": "Mentor",
  "Email": "john.mentor@example.com",
  "Expertise": "Growth, fundraising",
  "SocialMedia": { "linkedin": "https://linkedin.com/in/johnmentor" }
}
```

#### Example PATCH (Valid)
Update coach’s contact info *(The phone number is only the example.)*

```json
{ "Phone": "+358401234567" }
```

#### Example Error (Invalid Type):

```json
{ "error": "Email must be a string" }
```

### **6.3.3 Coach Slots**

**Endpoints**: 
- `GET /coach_slots/all`
- `GET /coach_slots/<id>`
- `POST /coach_slots`
- `PATCH /coach_slots/<id>`
- `DELETE /coach_slots/<id>`

#### Example POST:

```json
{
  "CoachId": 1,
  "Date": "2026-03-30",
  "Slot": "10:00–10:20",
  "Duration": 20,
  "IsBreak": false
}
```

#### Example PATCH (Valid)
Update slot duration

```json
{ "Duration": 30 }
```

#### Example Error (Invalid Type):

```json
{ "error": "Duration must be an integer" }
```

### **6.3.4 Coach Assignments**

**Endpoints**: 
- `GET /coach_assignments/all`
- `GET /coach_assignments/<id>`
- `POST /coach_assignments`
- `PATCH /coach_assignments/<id>`
- `DELETE /coach_assignments/<id>`

#### Example POST:

```json
{
  "StartupId": 1,
  "StartupName": "Test Startup",
  "CoachId": 1,
  "SlotId": 1,
  "Slot": "10:00-11:00",
  "Duration": 60,
  "Date": "2026-03-30"
}
```

#### Example PATCH (Valid)
Update assigned slot

```json
{ "SlotId": 15 }
```

#### Example Error (Invalid Type):

```json
{ "error": "SlotId must be an integer" }
```

### **6.3.5 Daily Feedback**

**Endpoints**: 
- `GET /daily_feedback/all`
- `GET /daily_feedback/<id>`
- `POST /daily_feedback`
- `PATCH /daily_feedback/<id>`
- `DELETE daily_feedback/<id>`

#### Example POST:

```json
{
  "CoachId": 1,
  "StartupId": 1,
  "Date": "2026-03-30",
  "FeedbackText": "Great progress today."
}
```

#### Example PATCH (Valid)
Update feedback text

```json
{ "FeedbackText": "Improved clarity in pitch." }
```

#### Example Error (Invalid Type):

```json
{ "error": "FeedbackText must be a string" }
```

### **6.3.6 Feedback History**

**Endpoints**: 
- `GET /feedback_history/all`
- `GET /daily_feedback/<id>`
- `POST /daily_feedback`
- `PATCH /daily_feedback/<id>`
- `DELETE daily_feedback/<id>` *(manual test only)*

**Notes:** *`FeedbackHistory` shouldn't be deleted but the DELETE method has been used for manual testing.*

#### Example POST:

```json
{
  "StartupId": 1,
  "StartupName": "Test Startup",
  "CoachId": 1,
  "DailyFeedbackId": 1,
  "StartupGrade": 4,
  "CoachGrade": 5,
  "StartupTextFeedback": "Startup feedback",
  "CoachTextFeedback": "Coach feedback",
  "DateFeedbackOriginal": "2026-03-30"
}

```

#### Example PATCH (Valid)
Update updated grade

```json
{ "UpdatedStartupGrade": 3 }
```

#### Example Error (Invalid Type):

```json
{ "error": "UpdatedStartupGrade must be an integer between 1 and 5" }
```

### **6.3.7 Banned To Meet**

**Endpoints**: 
- `GET /banned_to_meet/all`
- `GET /banned_to_meet/<id>`
- `POST /banned_to_meet`
- `PATCH /banned_to_meet/<id>`
- `DELETE banned_to_meet/<id>` *(manual test only)*

**Notes:** *`BannedToMeet` shouldn't be deleted but the DELETE method has been used for manual testing.*

#### Example POST:

```json
{
  "StartupId": 1,
  "CoachId": 2,
  "DateFrom": "2026-03-01",
  "DateTo": "2026-03-10",
  "Reason": "Conflict of interest"
}
```

#### Example PATCH (Valid)
Update DateTo

```json
{ "DateTo": "2026-03-15" }
```

#### Example Error (Invalid Logic):

```json
{ "error": "DateTo must be greater than or equal to DateFrom" }
```

---

## 7. Validation Testing

The backend features a unified validation layer for all `POST` and `PATCH` requests across seven models. Validation enforces strict field rules, updated character limits, human‑name rules, warning‑based URL checks, and consistent JSON error responses.

### 7.1 Core Validation Rules
1. **Strict field validation:** unknown fields → error
```json
{ "error": "Unknown field: RandomField" }
```
2. **Type checking:** each field must match expected primitive type
```json
{ "error": "Duration must be an integer" }
```
3. **JSON shape validation:** nested fields (`StartupMembers`, `SocialMedia`) must follow schema
```json
{ "error": "StartupMembers must be a list of objects" }
```
4. **Logical constraints:** `DateTo ≥ DateFrom`, grades 1–5, valid foreign keys
5. **Whitespace handling:** empty/whitespace strings rejected
6. **PATCH rules:** must contain at least one valid field
```json
{ "error": "No valid fields provided for update" }
```
7. **Record existence:** missing IDs
```json
{ "error": "Not found" }
```
8. **Consistent error format:** all failures return
```json
{ "error": "Description of the validation error" }
```
9. **Warnings for URL‑like fields:** Website + SocialMedia return `"warnings": []` when format is imperfect
```json
{ "warnings": ["Website missing protocol (http/https)"] }
```

### 7.2 Character limits
All string fields now follow strict min/max lengths (see table below).

| Field Type            | Allowed Length   |
|-----------------------|------------------|
| Coach Title           | 2-20 chars       |
| Coach FirstName       | 1–50 chars       |
| Coach LastName        | 1–60 chars       |
| StartupName           | 1–100 chars      |
| FeedbackText          | up to 2000 chars |
| Email                 | 2–100 chars      |
| Reason (BannedToMeet) | up to 500 chars  |
| Bio                   | up to 500 chars  |

This type of validation rejects empty strings, whitespace‑only strings, and strings exceeding limits.

### 7.3 Name Rules (Human-Based)
Used for Coaches `FirstName`/`LastName` and `StartupMembers`:
- **Allows:** Unicode letters, accents, spaces, hyphens, apostrophes
- **Blocks:** digits, emoji, symbols
- Length enforced per field

**Valid Example:**
```json
{ "FirstName": "María-José" }
```

**Invalid Example:**
```json
{ "FirstName": "John💥" }
```

**Error:**
```json
{ "error": "FirstName contains invalid characters" }
```

### 7.4 StartupName Validation
StartupName is not split and allows:
- letters, numbers, symbols, emoji
- length ≤ 100

**Valid Example:** 
```json
{ "StartupName": "NextGen AI🚀 Labs++" }
```
StartupName allows emoji + symbols.

### 7.5 SocialMedia Validation (Warning-Based)
- Accepts plain text, handles, partial URLs, full URLs
- Warning‑based
- Rejects only unsafe schemes (`javascript:`)

**Warning Example:** 
```json
{ "SocialMedia": { "linkedin": "linkedin.com/in/john" } }
```

Returns:
```json
{ "warnings": ["linkedin missing protocol (http/https)"] }
```

**Invalid Example:**
```json
{ "SocialMedia": { "linkedin": "javascript:alert(1)" } }
```

**Error:**
```json
{ "error": "SocialMedia.linkedin contains an unsafe URL" }
```

### 7.6 Website Validation (Warning-Based)
- Accepts URL‑like strings
- Warns on missing protocol or `http://`
- Rejects only empty, whitespace, `<script>`, `javascript:`

**Warning Example:** 
```json
{ "Website": "example.com" }
```

Returns:
```json
{ "warnings": ["Website missing protocol (http/https)"] }
```

**Invalid Example:**
```json
{ "Website": "javascript:alert(1)" }
```

**Error:**
```json
{ "error": "Invalid website URL" }
```

### 7.7 Duplicate Email (Coaches)

**Invalid Example:**
```json
{ "Email": "existing@example.com" }
```

**Error:**
```json
{ "error": "Email already exists" }
```

### 7.8 StartupName History Tracking (PATCH)

```json
{ "StartupName": "New Name" }
```
Automatically appends to `PreviousNames`.

---

## 8. Cascade Delete Behavior

The backend uses a **hybrid deletion system** combining SQL foreign‑key rules with custom logic.
The goal is to preserve historical data, protect reporting integrity, and avoid accidental data loss.

### 8.1 Delete a Coach
Deleting a coach now triggers selective cleanup instead of full cascade.

**8.1.1 Future data is deleted**
These records are removed because they represent upcoming commitments: 
**Future CoachSlots** and **Future CoachAssignments**

**8.1.2 Past data is preserved**
These records remain in the database for historical accuracy:
**Past CoachSlots** and **Past CoachAssignments**

**8.1.3 Feedback is anonymized, not deleted**
To preserve program history while removing personal identifiers:
- `DailyFeedback.CoachId` to `NULL`
- `FeedbackHistory.CoachId` to `NULL`

**8.1.4 Restrictions are removed**
All `BannedToMeet` rows involving the coach are deleted.

### 8.2 Delete a Startup
Startup deletion **does NOT use cascade delete**.
Instead, it follows a manual, controlled sequence:

#### 8.2.1 What becomes NULL
- DailyFeedback.StartupId → NULL
- FeedbackHistory.StartupId → NULL
Feedback is preserved but anonymized.

#### 8.2.2 What must stay (NOT deleted)
- CoachAssignments (StartupId NOT NULL)
- BannedToMeet (StartupId NOT NULL)
These rows must remain for historical and audit purposes.

#### 8.2.3 Required delete sequence
A startup cannot be deleted until dependent rows are removed:
1. Delete all CoachAssignments for that Startup
2. Delete all BannedToMeet rows for that Startup
3. Then DELETE the Startup

### 8.3 Deleting a CoachSlot
When a slot is deleted, All **CoachAssignments** linked to that slot are automatically removed. It prevents orphaned assignments.

### 8.4 Deleting DailyFeedback
All **FeedbackHistory** entries referencing that **DailyFeedback** are deleted. It prevents orphaned history rows.

### 8.5 Summary of Cascade Rules

| Parent Deleted    | Behaior                                                                         |
|-------------------|---------------------------------------------------------------------------------|
| Coach             | Delete future slots + assignments; keep past; anonymize feedback; delete bans   |
| Startup           | Anonymize feedback; **assignments + bans must be removed manually**; no cascade |
| CoachSlot         | Delete related assignments                                                      |
| DailyFeedback     | Delete related FeedbackHistory                                                  |

### 8.6 Testing Summary

Cascade behavior was verified through a complete end‑to‑end test sequence, covering past and future slots, assignments, feedback, and restrictions.
The testing confirms that:
- Coach deletion removes future data, preserves past, anonymizes feedback
- Startup deletion requires manual cleanup (assignments + bans)
- Feedback tables correctly set IDs to NULL
- No orphaned foreign keys remain
- Historical integrity is preserved

All cascade paths behaved as expected and matched the SQL schema and ERD.

---

## 9. API v1 (Routing Layer)
The `api_v1` folder contains the full routing layer for the backend, implemented using Flask Blueprints. 
It exposes all CRUD operations, applies validation, returns warnings, and handles delete logic exactly as defined in the models.

### 9.1 Purpose of `api_v1`
- Provide clean, modular routing using Blueprints
- Expose CRUD endpoints for all database models
- Apply validation, date parsing, and consistent error handling
- Enforce date parsing and foreign‑key rules
- Integrate the matching engine (POST /match)
- Ensure consistent JSON responses across all routes

### 9.2 Route Structure
These routes form the active API v1 layer and interact directly with the database.
Each endpoint follows consistent validation, filtering, and JSON response rules.

**Active API v1 Endpoints**

| Endpoint           | Method        | Description                                                                     |
|--------------------|---------------|---------------------------------------------------------------------------------|
| /coaches/	        | GET/POST	     | List or create coaches (name validation + duplicate email check)                |
| /coaches/<id>	     | PATCH/DELETE	 | Update coach fields or delete coach (future-only cleanup)                       |
| /startups/         | GET/POST	     | List or create startups (Website/SocialMedia warnings)                          | 
| /startups/<id>     | PATCH/DELETE	 | Update startup (name history tracking) or delete (manual cleanup required)      |   
| /coach_slots	      | GET/POST      | Retrieve or create coach slots                                                  |  
| /coach_assignments | GET/POST	     | Retrieve or create assignments                                                  |  
| /match	            | POST	         | Run the matching engine and create assignments                                  |   

### 9.3 Matching Engine Endpoint
`POST /api/v1/match` runs the matching engine, which:
- Filters valid coach slots
- Applies priority rules
- Enforces bans
- Prevents double‑booking
- Writes assignments to the database
- Returns a clean JSON summary
Matching logic is unaffected by validation changes (name rules, URL warnings, etc.).

### 9.4 Status
- Fully implemented and stable
- All prototype routes removed
- All validation, warnings, and delete behavior integrated
- Startup deletion now requires manual cleanup (assignments + bans)
- Coach deletion uses selective cleanup (future only)

---

## 10. Data Generation Scripts

The `backend/dataGen` folder contains helper scripts used during development to generate test data, simulate program workflows, and reset test conditions.
These scripts are for **development only** and **not part of the production API.**

### 10.1 **`genStartups.py`**:
- Generates sample startup data, including:
   - `StartupMembers` 
   - `StartupSocialMedia` 
   - `PreviousNames` 
- Useful for populating the database during resting.

### 10.2. **`filling_feedbacks.py`**
- Create test entries for:
  - `DailyFeedback`
  - `FeedbackHistory`
- Used to validate feedback routes, priority scoring, and matching behavior.

### 10.3 `remove_shadow_ban.py` 
- Utility for clearing entries in `BannedToMeet`.
- Used to reset constraints when testing scheduling and matching scenarios.

### 10.4 Documentation Files in `dataGen/info`
- **`db_model_updated_mar2026.png`**: Updated ERD diagram reflecting the current schema
- **`rules.md`**: Matching logic, constraints, and business rules
- **`tested_data.md`**: Sample data, meeting count tests, and imbalance scenarios
- Useful for populating the database during development.

---

## 11. Environment Variables
The backend supports a small set of environment variables for configuration.
Defaults are provided for local development, and no additional setup is required for basic usage.

### 11.1 **`SQLALCHEMY_DATABASE_URI`**:
   - Defines the database connection string.
   - **Default** (development): `sqlite:///instance/sauna.db` 
   - Uses Flask’s `instance/` folder for safe, writable storage.

### 11.2 **`REACT_APP_BACKEND_URL`**:
   - Base URL for the frontend to communicate with the backend.
   - Typical local value: `http://localhost:5000` (Now updated to `http://127.0.0.1:5000`)

### 11.3 **Optional Debug Variables**
These are helpful during development but not required in production:
   - `FLASK_ENV=development`
   - `FLASK_DEBUG=1`

---

## Documentation Maintenance

This document reflects the backend architecture and implementation as of **24 June 2026**.

Future contributors are encouraged to keep this documentation synchronized with the codebase whenever new features, API endpoints, database models, routing logic, or validation behavior are introduced. Maintaining accurate documentation helps future developers understand the system architecture and reduces onboarding time for new contributors.