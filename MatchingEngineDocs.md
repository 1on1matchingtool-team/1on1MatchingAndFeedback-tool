# Matching Engine Documentation
#### Updated 2 April 2026

## Table of Contents

1. [Overview](#1-overview)
2. [Goals and Design Principles](#2-goals-and-design-principles)
3. [Data Inputs](#3-data-inputs)
4. [Matching Flow](#4-matching-flow)
5. [Priority Logic](#5-priority-logic)
6. [Ban Logic](#6-ban-logic)
7. [Slot Selection and Double‑Booking Prevention](#7-slot-selection-and-double-booking-prevention)
8. [Why These Choices Were Made (Design Rationale)](#8-why-these-choices-were-made-design-rationale)
9. [Summary of Work Completed](#9-summary-of-work-completed)

---

## 1. Overview
The matching engine assigns startups to coach slots based on priority, availability, and constraints.
It is implemented in `backend/matching_engine/engine.py` and triggered via `POST /api/v1/match`.

The engine is completely separate from the older JSON‑based simulation system.
It operates on real SQLAlchemy models, enforces strict scheduling rules, and produces deterministic, conflict‑free assignments written to the CoachAssignments table.

---

## 2. Goals and Design Principles
The engine was built around these core principles:
- **Deterministic**: Same input → same output. No randomness.
- **Fair**: Startups with lower grades or fewer meetings get priority.
- **Safe**: No double‑booking of coaches, startups, or slots.
- **Transparent**: Every rule is explicit and documented.
- **Maintainable**: Logic is centralized, readable, and easy to extend.

---

## 3. Data Inputs
The engine reads from the following database tables:

| Table                  | Purpose                                    |
|------------------------|--------------------------------------------|
| **CoachSlots**         | Available future slots (non‑break)         |
| **Startups**           | Startup metadata                           |
| **FeedbackHistory**    | Grades used for priority scoring           |
| **BannedToMeet**       | Hard exclusions                            |
| **CoachAssignments**   | Prevents slot reuse and duplicate meetings |
All inputs are validated before use.

---

## 4. Matching Flow
The engine follows a strict, predictable sequence:
1. Load all future, non‑break slots 
2. Sort slots by date, time, and coach 
3. Load all startups 
4. Compute priority for each startup 
5. Iterate through slots in order 
6. For each slot, find the highest‑priority eligible startup 
7. Check bans and previous assignments 
8. Create a CoachAssignment row 
9. Continue until all slots are filled or no startups remain

---

## 5. Priority Logic
Startup priority is computed using:

1. StartupGrade (from FeedbackHistory)
Lower grade → higher priority
Because lower grades indicate the startup needs more support.
2. Meeting Count
Startups with fewer meetings are prioritized.
3. Trend (future extension)
Recent feedback can be weighted more heavily.
4. Tie‑breaking
If two startups have identical priority:
- Lower StartupId wins
- Ensures deterministic ordering

---

## 6. Ban Logic
Before assigning a startup to a coach, the engine checks:
1. BannedToMeet table
If a startup is banned from a coach → **skip**
2. Historical negative feedback
If a coach previously gave `CoachGrade = -1` → **skip**
3. Admin restrictions
If admin manually banned the pair → **skip**

---

## 7. Slot Selection & Double‑Booking Prevention

### 7.1 Slot Selection Rules
Only slots that meet all criteria are used:
- Future date
- Not a break slot
- Not already assigned
- Belongs to an active coach
Slots are sorted by:
   1. Date
   2. Start time
   3. CoachId

### 7.2 Double‑Booking Prevention
The engine makes sure:
- Startup cannot be assigned twice in the same run
- Coach cannot have two startups in the same slot
- Slot cannot be reused
- Banned pair is never matched
- Startup cannot meet the same coach twice in the same day

---

## 8. Why These Choices Were Made (Design Rationale)
Here is the reasoning behind the architecture.

### 8.1 Deterministic ordering
Avoids randomness because:
- Debugging becomes easier
- Testing becomes reliable
- Results are predictable

### 8.2 Feedback‑based priority
Lower grades → higher priority
The program’s goal is to support struggling startups first.

### 8.3 Hard bans
Protects both coaches and startups from unwanted or harmful pairings.

### 8.4 Slot‑first iteration
Chosen because:
- Prevents coach overload
- Produces balanced schedules
- Keeps logic simple and maintainable

### 8.5 Database‑driven, not JSON‑driven
The old simulation engine used JSON files.
The new engine uses SQLAlchemy because it:
- Integrates with the real app
- Supports validation
- Avoids file corruption
- Scales better

---

## 9. Summary of Work Completed
The matching engine is now a fully operational component of the backend, utilizing SQLAlchemy models and executing deterministic priority rules. 
It enforces bans and avoids double-booking, integrating seamlessly with the API v1 routing layer to ensure consistent and conflict-free assignments. 
The design prioritizes clarity, maintainability, and fairness, transitioning from a JSON-based simulation to a robust database-driven solution for real deployment.