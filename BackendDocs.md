# Backend Documentation
#### Updated 2 April 2026

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

### 4.2 **`database/__init__.py`**

This file imports and exposes all database models, so they can be accessed easily throughout the application.

#### Imports:

- Models: `BannedToMeet`, `CoachAssignments`, `Coaches`, `CoachSlots`, `DailyFeedback`, `FeedbackHistory`, `Startups`

#### Purpose:

- Provides centralized access to all database models.
- Ensures app.py and other modules can import models from a single location.

### 4.3 **`database/base.py`**

Defines and initializes the shared SQLAlchemy database object used across the backend.

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
Updated ERD (Entity–Relationship Diagram) reflecting the current database schema (March 2026 Update).
Includes the remastered Coaches model (`Title`, `FirstName`, `LastName`) and corrected relationships with cascade delete behavior.

#### 4.5.2 **`backend/dataGen/info/rules.md`**
Contains matching logic, constraints, and business rules.
Updated to align with the new structured coach naming and consistent foreign key relationships. 

#### 4.5.3 **`backend/dataGen/info/tested_data.md`**
Includes sample data and meeting count tests used during development.
Also documents cascade delete test scenarios performed in March 2026. 

#### 4.5.4 **`schema_clean.sql`**
- Clean SQL schema used for generating the ERD. 
- Uses unquoted identifiers and SQLite-compatible types.
- Updated to reflect the new Coaches fields (`Title`, `FirstName`, `LastName`) and corrected foreign key constraints with `ON DELETE CASCADE`.

#### 4.5.5 **`schema.sql`**
Full schema used by the backend, now updated with structured coach names, JSON fields, and cascade delete rules across all models. 

#### 4.5.6 **`engine.py`**
- Contains the core matching logic used to assign startups to coach slots.
- Filters valid slots, applies priority rules, enforces bans, prevents double‑booking, and writes finalized assignments to the database.

#### 4.5.7 **`date_utils.py`**
- Provides centralized date‑parsing utilities used across routes and the matching engine. 
- Standardizes how dates are interpreted, prevents inconsistent formats, and avoids circular imports.

---

## 5. Database Models

All models are defined in `database/models`.
Each model corresponds to a table in `sauna.db` and follows a consistent structure with:
- clearly defined columns
- foreign‑key relationships
- JSON‑based fields stored as TEXT
- full CRUD support
- unified validation for `POST` and `PATCH`
The complete schema is shown in the ERD `(db_model_updated_mar2026.png)`.

### 5.1 Startups
Represents a startup participating in the program.

**Key characteristics:**
- Uses strict validation for JSON fields (`StartupMembers`, `StartupSocialMedia`, `PreviousNames`)
- Tracks metadata such as `Status`, `MeetingsCount`, and `Website`
- Connected to: `DailyFeedback`, `FeedbackHistory`, `CoachAssignments`, `BannedToMeet`
- Deleting a startup cascades through all dependent records

### 5.2 Coaches
Represents a coach in the program.

**Key characteristics:**
- Uses structured name fields: `Title`, `FirstName`, `LastName`
- Includes profile fields (email, phone, chat, expertise, social media)
- Connected to: `CoachSlots`, `CoachAssignments`, `DailyFeedback`, `FeedbackHistory`, `BannedToMeet`
- Deleting a coach now triggers selective cascade delete (see [Cascade Delete Behavior](#cascade-delete-behavior) section)

### 5.3 CoachSlots
Represents available time slots for each coach.

**Key characteristics:**
- Includes `Date`, `Slot`, `Duration`, and `IsBreak`
- Linked to `CoachId`
- Used by the matching engine and assignment logic
- Deleting a coach removes all future slots; past slots remain for history

### 5.4 CoachAssignments
Represents the mapping between a coach, a startup, and a specific slot.

**Key characteristics:**
- Includes `CoachId`, `StartupId`, `SlotId`, `Date`, `Duration`, `Slot`
- Tracks scheduled 1‑on‑1 meetings
- Deleting a coach removes future assignments; past assignments remain

### 5.5 DailyFeedback
Represents daily feedback given after each meeting.

**Key characteristics:**
- Stores `FeedbackText`, and `Date`
- Linked to `CoachId` and `StartupId`
- Forms the basis for historical feedback tracking
- CoachId becomes NULL when a coach is deleted
- Past feedback remains

### 5.6 FeedbackHistory
Represents historical revisions of feedback.

**Key characteristics:**
- Stores original and updated grades
- Linked to `DailyFeedbackId`, `StartupId`, and `CoachId`
- Uses corrected field names: `StartupTextFeedback`, `CoachTextFeedback`, `UpdatedStartupGrade`, `DateUpdatedStartupGrade`
- CoachId becomes NULL when a coach is deleted
- Never deleted automatically

### 5.7 BannedToMeet
Represents restrictions preventing certain coach–startup meetings.

**Key characteristics:**
- Stores `DateFrom`, `DateTo`, and `Reason`
- Enforces logical constraints (e.g., `DateTo ≥ DateFrom`)
- Used by the matching engine to avoid invalid pairings
- Deleted when either the coach or startup (parent) is deleted

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

- **Endpoints**: 
- `GET /startups`
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
      "level": "primary"
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

- **Endpoints**: 
- `GET /coaches`
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

- **Endpoints**: 
- `GET /coach_slots`
- `GET /coach_slots/<id>`
- `POST /coach_slots`
- `PATCH /coach_slots/<id>`
- `DELETE /coach_slots/<id>`

#### Example POST:

```json
{
  "CoachId": 1,
  "Date": "2026-03-01",
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

- **Endpoints**: 
- `GET /coach_assignments`
- `GET /coach_assignments/<id>`
- `POST /coach_assignments`
- `PATCH /coach_assignments/<id>`
- `DELETE /coach_assignments/<id>`

#### Example POST:

```json
{
  "CoachId": 2,
  "StartupId": 5,
  "SlotId": 12
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

- **Endpoints**: 
- `GET /daily_feedback`
- `GET /daily_feedback/<id>`
- `POST /daily_feedback`
- `PATCH /daily_feedback/<id>`
- `DELETE daily_feedback/<id>`

#### Example POST:

```json
{
  "CoachId": 1,
  "StartupId": 3,
  "Date": "2026-03-20",
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

- **Endpoints**: 
- `GET /feedback_history`
- `GET /daily_feedback/<id>`
- `POST /daily_feedback`
- `PATCH /daily_feedback/<id>`
- `DELETE daily_feedback/<id>`

**Notes:** *`FeedbackHistory` shouldn't be deleted but the DELETE method has been used for manual testing.*

#### Example POST:

```json
{
  "StartupName": "Test Startup",
  "DateFeedbackOriginal": "2026-03-30",
  "StartupGrade": 4,
  "CoachGrade": 5,
  "DailyFeedbackId": 10,
  "StartupId": 3
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

- **Endpoints**: 
- `GET /banned_to_meet`
- `GET /banned_to_meet/<id>`
- `POST /banned_to_meet`
- `PATCH /banned_to_meet/<id>`
- `DELETE banned_to_meet/<id>`

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

The backend features a unified validation layer for all `POST` and `PATCH` requests across seven models. Validation is currently enforces stricter rules, updated character limits, consistent JSON shapes, and centralized name‑splitting logic for coaches and startups.

### 7.1 Validation Philosophy

All POST and PATCH requests follow the same validation principles:

#### 7.1.1 Strict field validation: 
Only known fields are allowed; unknown fields trigger an error.
#### 7.1.2 Type checking: 
Every field must match the expected primitive type (string, integer, boolean, list, object).
#### 7.1.3 JSON shape validation: 
Nested structures (`StartupMembers`, `SocialMedia`, etc.) must follow the correct schema.
#### 7.1.4 Logical constraints
For example:
   - `DateTo` ≥ `DateFrom` 
   - Grades must be integers within allowed ranges
   - Foreign keys must reference existing records
#### 7.1.5 Whitespace handling
Empty strings, whitespace‑only values, and invalid Unicode sequences are rejected.
#### 7.1.6 PATCH partial updates
Only provided fields are validated and updated; empty PATCH bodies are rejected.
#### 7.1.7 Consistent error responses
All validation failures return
```json
{ "error": "Description of the validation error" }
```
#### 7.1.8 Record existence checks
PATCH/DELETE on non‑existent IDs return
```json
{ "error": "Not found" }
```
#### 7.1.9 Updated character limits
All string fields now follow strict min/max lengths (see table below).

| Field Type            | Allowed Length   |
|-----------------------|------------------|
| Coach Title           | 2-20 chars       |
| Coach FirstName       | 1–50 chars       |
| Coach LastName        | 1–60 chars       |
| StartupName           | 2–100 chars      |
| FeedbackText          | up to 2000 chars |
| Email                 | 2–200 chars      |
| Reason (BannedToMeet) | up to 500 chars  |

This type of validation rejects empty strings, whitespace‑only strings, and strings exceeding limits.

#### 7.1.10 Name‑Splitting Rule
The backend now uses a centralized name‑splitting utility for **Coaches**:
- Accepts any Unicode name (accents, emoji, multilingual characters)
- Automatically extracts:
   - Title (optional)
   - FirstName
   - LastName
- Handles:
   - multiple spaces
   - hyphenated names
   - middle names
   - titles like “Dr.”, “Prof.”, “Mr.”, “Ms.”
- Ensures consistent formatting across:
   - POST/PATCH validation
   - migration scripts
   - runtime logic

**StartupName does NOT use splitting**: it is validated as a single string using validate_startup_name() rules.

#### 7.1.11 Invalid Character Type Validation
The backend enforces strict character‑type rules depending on the purpose of each field. The functions are provided from `base_validatiors.py`.

 **1. `validate_unicode_name` (Coach names only)**

Used for FirstName, LastName, and internally during name‑splitting.
- **Allows:** Unicode letters (`\p{L}`, `\p{M}`), Accents, Spaces, Hyphens (`-`), Apostrophes (`'`)
- **Blocks:** Numbers, Symbols (`@#$%^&*…`), Emojis, Punctuation (except `'` and `-`)

**2. `validate_startup_name` (StartupName only)**

Startup names allow a wider range of characters.
- **Allows:** Unicode letter, Numbers, Spaces, Hyphens (`-`), Underscores (`_`), Dots (`.`) Plus signs (`+`)
- **Blocks:** All other symbols, Emojis, Slashes, brackets, quotes, etc.

**3. `validate_role` (StartupMembers → role field)**

- **Allows:** Letters, Numbers, Spaces, Hyphens (`-`), Dots (`.`), Backticks (`), Apostrophes (")
- **Blocks:** Symbols not listed above, Emojis

**4. `validate_social_media`**

- Must be a dict
- Keys must be strings
- Values must be valid URLs
- Blocks javascript: URLs for safety

**5. `validate_free_text`**

Used for fields like FeedbackText, Bio, etc.
**Allows:**
- Everything (including emoji)
- As long as it is a string and within length limits

**6. `validate_no_symbols`**

Used for fields that must be strictly alphanumeric.
- **Allows:** Letters, Numbers, Spaces
- **Blocks:** All symbols

**7. `validate_name_characters`**

Used inside name‑splitting to ensure raw name tokens contain only:
Unicode letters, Hyphens (`-`), Apostrophes (`"`), Hyphens (`-`), Spaces

### 7.2 Main Validation Cases (Across All Models)**

This subsection consolidates key validation scenarios from all seven models, representing crucial patterns of validation behavior essential for developers' understanding.

### 7.2.1 Unknown Fields
Occurs when the request contains keys not defined in the model.

**Example:**
```json
{ "RandomField": "test" }
```

**Error:**
```json
{ "error": "Unknown field: RandomField" }
```

### 7.2.2 Wrong Data Types
Triggered when a field has the wrong primitive type.

**Examples:**
```json
{ "Email": 123 }
{ "Duration": "sixty" }
{ "StartupId": "five" }
{ "FirstName": 99 }
```

**Errors:**
```json
{ "error": "Email must be a string" }
{ "error": "Duration must be an integer" }
{ "error": "StartupId must be an integer" }
{ "error": "FirstName must be a string" }
```

### 7.2.3 Wrong JSON Shapes
Used for nested structures that must follow a specific schema.

**Examples:**
```json
{ "StartupMembers": ["Alice"] }
{ "SocialMedia": "linkedin.com/john" }
{ "StartupSocialMedia": [] }
```

**Errors:**
```json
{ "error": "StartupMembers must be a list of objects" }
{ "error": "SocialMedia must be an object" }
{ "error": "StartupSocialMedia must be an object" }
```

### 7.2.4 Invalid Enum Values
Used when a field must match a predefined set of allowed values.

**Example:**
```json
{ "Status": "Active" }
```

**Error:**
```json
{ "error": "Status must be one of: alive, on-pause, dead" }
```

### 7.2.5 Invalid Date Formats
All dates must follow ISO format `YYYY-MM-DD`.

**Example:**
```json
{ "Date": "March 1st" }
```

**Error:**
```json
{ "error": "Date must be in YYYY-MM-DD format" }
```

### 7.2.6 Logical Constraints
Used when fields must satisfy a relationship.

**Example:**
```json
{ "DateFrom": "2026-03-10", "DateTo": "2026-03-01" }
```

**Error:**
```json
{ "error": "DateTo must be greater than or equal to DateFrom" }
```

### 7.2.7 Empty PATCH Body
PATCH must include at least one valid field.

**Example:**
```json
{}
```

**Error:**
```json
{ "error": "No valid fields provided for update" }
```

### 7.2.8 Record Not Found
Occurs when the ID does not exist in the database.

**Example:**
`PATCH /startups/9999`

**Error:**
```json
{ "error": "Not found" }
```

### 7.2.9 Character Limits
Triggered when a string exceeds or falls below allowed length.

**Example:** (Too Long StartupName - *Letter A repeated 150 times*)
```json
{ "StartupName": "A".repeat(150) }
```

**Error:**
```json
{ "error": "StartupName must be between 1 and 100 characters" }
```

**Example:** (Whitespace Only)
```json
{ "FirstName": "   " }
```

**Error:**
```json
{ "error": "FirstName cannot be empty or whitespace" }
```

### 7.2.10 Name Splitting

**Valid Example:**
```json
{
  "FirstName": "MrJosh",
  "LastName": "JoshMichaelSmith"
}
```
**Result after splitting:**
- Title: "Mr."
- FirstName: "Josh"
- LastName: "Michael Smith"

**Invalid Example:**
```json
{ "FirstName": "John 123 Mentor" }
```

**Error:**
```json
{ "error": "FirstName contains invalid characters" }
```

**StartupName Example** (No Splitting)
```json
{ "StartupName": "NextGen AI+Labs" }
```

It is valid because Startup names allow letters, numbers, spaces, hyphens, underscores, dots, and plus signs.

### 7.2.11 Invalid Character Types

**Example:** Invalid Coach Name Characters (`validate_unicode_name`)
```json
{ "FirstName": "Anna@" }
```

**Error:**
```json
{ "error": "FirstName contains invalid characters" }
```

**Example:** Invalid Role Characters (`validate_role`)
```json
{ "Role": "CEO!!!" }
```

**Error:**
```json
{ "error": "Role contains invalid characters" }
```

**Example:** Invalid SocialMedia URL
```json
{ "SocialMedia": { "linkedin": "javascript:alert(1)" } }
```

**Error:**
```json
{ "error": "SocialMedia.linkedin contains an unsafe URL" }
```

**Example:** Invalid Name Characters During Splitting (`validate_name_characters`)
```json
{ "FirstName": "John💥" }
```

**Error:**
```json
{ "error": "FirstName contains invalid characters" }
```

---

## 8. Cascade Delete Behavior

The backend has currently used a hybrid cascade and logic-based deletion system that retains historical data and safely removes future scheduling data associated with deleted coaches. This is achieved through SQL ON DELETE rules combined with custom logic at the Coach deletion endpoint.

### 8.1 Delete a Coach
Deleting a coach now triggers selective cleanup instead of full cascade deletion.

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
All BannedToMeet entries involving the coach are deleted.

### 8.2 Delete a Startup
Startup deletion remains a **full cascade**, because startups do not require historical preservation in the same way coaches do.
Removing a startup cascades through all related tables:
**DailyFeedback**, **FeedbackHistory**, **CoachAssignments**, **BannedToMeet**

### 8.3 Deleting a CoachSlot
When a slot is deleted, All **CoachAssignments** linked to that slot are automatically removed.

### 8.4 Deleting DailyFeedback
All **FeedbackHistory** entries referencing that **DailyFeedback** are deleted. It prevents orphaned history entries.

### 8.5 Summary of Cascade Rules

| Parent Deleted    | Behaior                                                                             |
|-------------------|-------------------------------------------------------------------------------------|
| Coach             | Delete future slots and assignments, preserve past, anonymize feedback, delete bans |
| Startup           | Delete all related feedback, history, assignments, bans                             |
| CoachSlot         | Delete related assignments                                                          |
| DailyFeedback     | Delete related FeedbackHistory                                                      |

### 8.6 Testing Summary

Cascade behavior was verified through a complete end‑to‑end test sequence, covering past and future slots, assignments, feedback, and restrictions.
The testing confirms that:
- Future slots and assignments associated with the deleted coach were removed.
- Past slots and assignments were retained for historical accuracy.
- DailyFeedback and FeedbackHistory entries were preserved, with the CoachId anonymized.
- BannedToMeet entries related to the deleted coach were eliminated.
- No orphaned foreign keys remained after the deletion process.
- Unrelated records and past program history were not impacted.

All cascade paths behaved as expected and matched the SQL schema and ERD.

---

## 9. API v1 (Routing Layer)
The `api_v1` folder contains the full routing layer for the backend, implemented using Flask Blueprints. 
These routes reveal all CRUD operations for the seven core models, along with filtering logic, validation, and the matching engine endpoint.

### 9.1 Purpose of `api_v1`
- Provide clean, modular routing using Blueprints
- Expose CRUD endpoints for all database models
- Apply validation, date parsing, and consistent error handling
- Serve as the integration point for the matching engine (POST /match)

### 9.2 Route Structure
These routes form the active API v1 layer and interact directly with the database.
Each endpoint follows consistent validation, filtering, and JSON response rules.

| Endpoint            | Method | Description                                        |
|---------------------|--------|----------------------------------------------------|
| /coaches	           | GET	   | Retrieve all coaches                           |
| /coaches	           |   POST	 | Create a new coach                               |
| /coaches/	          | PATCH	 | Update coach information                         | 
| /coach_slots	       | GET	   | Retrieve coach slots (supports future/past)    |   
| /coach_slots	       | POST	  | Create a new coach slot                         |  
| /daily_feedback	    | GET	   | Get daily feedback (requires startupId)        |   
| /feedback_history	  | GET	   | Get historical feedback (requires startupId)       |
| /banned_to_meet	    | POST	  | Create a ban between coach and startup          |   
| /coach_assignments  | 	GET	  | Retrieve generated assignments                  |   
| /match	             | POST	  | Run the matching engine and create assignments  |   

### 9.3 Matching Engine Endpoint
`POST /api/v1/match` runs the matching engine, which:
- Filters valid coach slots
- Computes startup priority
- Enforces bans
- Prevents double‑booking
- Writes assignments to the database

### 9.4 Status
- Fully implemented
- Replaces all earlier prototype routes
- Old placeholder endpoints have been removed or replaced

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

## 11 Environment Variables
The backend supports a small set of environment variables for configuration.
Defaults are provided for local development, and no additional setup is required for basic usage.

### 11.1 **`SQLALCHEMY_DATABASE_URI`**:
   - Defines the database connection string.
   - **Default** (development): `sqlite:///instance/sauna.db` 
   - Uses Flask’s `instance/` folder for safe, writable storage.

### 11.2 **`REACT_APP_BACKEND_URL`**:
   - Base URL for the frontend to communicate with the backend.
   - Typical local value: `http://localhost:5000`

### 11.3 **Optional Debug Variables**
These are helpful during development but not required in production:
   - `FLASK_ENV=development`
   - `FLASK_DEBUG=1`

They enable hot reload and detailed error messages.