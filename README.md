# Hackathon Mentor-Mentee Growth Platform

## Problem Statement

In many colleges, bootcamps, and early-career programs, mentorship is managed informally.
Mentors and mentees may connect, but there is often no structured way to:

- track who is mentoring whom
- define clear learning goals
- monitor progress over time
- recommend useful learning resources
- separate general mentorship guidance from goal-specific learning material

As a result, mentorship becomes difficult to scale, progress is hard to measure, and both mentors and mentees lack a shared system of accountability.

## Our Solution

This project provides a backend API for a Mentor-Mentee Growth Platform.

This platform solves the problem of unstructured mentorship by giving mentors and mentees a system to define relationships, set goals, track progress, and recommend reusable resources. Some resources support the overall mentorship, while others are tied to a specific goal. That makes the platform flexible enough for both continuous improvement and focused learning.


It helps teams manage the full mentorship journey by supporting:

- mentor and mentee profile management
- mentorship pairing and status tracking
- goal creation and progress logging
- reusable learning resources
- resource recommendations at two levels:
- mentorship-level for continuous improvement
- goal-level for focused learning against a specific goal

In short, the platform turns mentorship from an informal conversation into a structured, trackable growth process.

## Example Use Case

Imagine a mentor, Priya, is guiding a mentee, Arun.

- Priya and Arun are connected through a mentorship.
- Arun has a goal: `Learn FastAPI`.
- Priya recommends a resource: `FastAPI Tutorial`.
- That resource can be attached directly to Arun's goal because it helps with that exact objective.

At the same time, Priya may also recommend broader resources such as:

- `PPT Design Basics`
- `Communication Skills Deck`
- `AI Career Roadmap`

These broader resources do not need to belong to one goal. They can stay attached to the mentorship as general improvement material.

This gives the system two useful layers:

1. Mentorship resources: for overall growth and continuous improvement
2. Goal resources: for specific, goal-focused learning

## What the Platform Provides

### 1. User Management

The system manages two user types:

- Mentors
- Mentees

Each user has profile details such as name, email, department, and skills.

### 2. Mentorship Management

A mentorship represents the working relationship between one mentor and one mentee.

It answers questions like:

- Who is mentoring whom?
- Is the mentorship active, paused, or completed?
- When did the mentorship start?

### 3. Goal Tracking

Each mentorship can define goals for the mentee.

Examples:

- Learn FastAPI
- Improve presentation skills
- Build an AI project portfolio

Goals can be updated as work progresses, and progress logs can record percentage completion and updates.

### 4. Resource Management

Resources are reusable learning materials such as:

- tutorials
- articles
- videos
- slide decks
- roadmaps

A resource can exist independently, which means the platform can also store useful content that is not yet attached to any mentorship or goal.

### 5. Flexible Resource Relationships

The project supports both of the following:
#### 1. Mentorship-level resource


“This is a general resource for the mentee’s overall growth in that mentorship.”

Example:

- Mentor: Priya
- Mentee: Arun
- Mentorship: Priya mentoring Arun
- Resource: PPT Design Basics



- Mentorship: Priya <-> Arun

        Resources:


        PPT Design Basics

        Communication Skills Deck


“Maybe Arun is improving overall communication and presentation skills. This resource is useful for the whole mentorship, not tied to one exact goal. So we attach it to the mentorship.”

Meaning:

- it supports continuous improvement
- it stays useful even if goals change


#### 2. Goal-level resource

“This is a focused resource for one specific goal.”

Example:

- Goal: Learn FastAPI

- Resource: FastAPI Tutorial


“Here Arun has a concrete goal: learn FastAPI. So we attach the FastAPI tutorial directly to that goal. That way, when we open the goal, we can immediately see the resources that help complete it.”

- Goal: Learn FastAPI

        Resources:

        FastAPI Tutorial

        REST API Best Practices


Meaning:

- it is targeted
- it gives context for that one goal


Resources are reusable learning items. We don’t force every resource to belong to a goal. Some resources are broader and belong to the mentorship as a whole, like PPT learning, communication, or career guidance. But if a resource is specifically meant to help complete one goal, like a FastAPI tutorial for the ‘Learn FastAPI’ goal, we can also attach it directly to that goal.


Mentorship resources are for overall development, while goal resources are for specific achievement.


- `Mentorship <-> Resource`
  - for general, ongoing improvement across the mentorship
- `Goal <-> Resource`
  - for targeted support of a specific goal

---

## Core Data Model

### Main Entities

- `Mentor`
- `Mentee`
- `Mentorship`
- `Goal`
- `ProgressLog`
- `Resource`

### Relationships

- One mentor can have many mentorships
- One mentee can have many mentorships
- One mentorship can have many goals
- One goal can have many progress logs
- One mentorship can have many resources
- One goal can have many resources
- One resource can be reused across many mentorships and many goals

## Tech Stack

This project follows a clean, modular FastAPI architecture with SQLAlchemy-based persistence and
Pydantic validation, designed for easy extension and testing.

| Layer       |     Technology Used
|-------------|------------------------------------------|
| Framework   | FastAPI 0.111                            |
| Server      | Uvicorn (ASGI)                           |
| ORM         | SQLAlchemy 2.0                           |
| Database    | MySQL 8+ (via PyMySQL driver)            |
| Validation  | Pydantic v2                              |
| Testing     | pytest + httpx + SQLite in-memory        |

---

## Project Setup

### Prerequisites

- Python 3.10+
- MySQL 8.0+ running locally (or remote)


### 1. Clone / enter the project

```bash
    git clone https://github.com/m-aparna/Hackathon_Mentor_Mentee.git
    cd Hackathon_Mentor_Mentee
```

```
    git remote add origin <https://github.com/m-aparna/Hackathon_Mentor_Mentee.git>
    Connect to remote repository
    
```

### 2. Create virtual environment (venv):
```bash
    py -3.12 -m venv .venv
```

 or 


```bash
    python -m venv .venv
```

### 3. Activate the virtual environment:

On Windows PowerShell:

```bash
.\.venv\Scripts\activate.ps1

```
On macOS/Linux:

```bash
source .venv/bin/activate
```

### 4. Install packages or dependencies:

```bash
    pip install -r requirements.txt
```

### 5. Create your environment file

```bash
cp .env.example .env
```
Then update `DATABASE_URL` in `.env` with your real MySQL credentials.


Example:

```env
DATABASE_URL=mysql+pymysql://mentorship_user:mentorship_pass@localhost:3306/mentorship_db
SECRET_KEY=changeme
DEBUG=True
```

## Database Setup

Create the database and user once in MySQL:

```sql
CREATE DATABASE IF NOT EXISTS mentorship_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'mentorship_user'@'localhost' IDENTIFIED BY 'mentorship_pass';
GRANT ALL PRIVILEGES ON mentorship_db.* TO 'mentorship_user'@'localhost';
FLUSH PRIVILEGES;
```

Tables are created automatically by SQLAlchemy on startup.

Note: if you add new columns or new relationship tables after tables already exist, you should use a migration or manually update the database schema.


## Run the App

From the project root:

```bash
uvicorn app.main:app --reload
```

Or from inside the `app` folder:

```bash
uvicorn main:app --reload
```

Visit **http://localhost:8000/docs** for the interactive Swagger UI.



Tables are created automatically by SQLAlchemy on startup (`create_tables()` in `main.py`).  
You only need to create the database and user once:



Open:

- Swagger UI: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`



## API Overview

### Mentees

| Method | Path | Description |
|--------|------|-------------|
| POST | `/mentees/` | Create mentee |
| GET | `/mentees/` | List mentees |
| GET | `/mentees/{mentee_id}` | Get mentee by ID |
| PATCH | `/mentees/{mentee_id}` | Update mentee |
| DELETE | `/mentees/{mentee_id}` | Delete mentee |

### Mentors

| Method | Path | Description |
|--------|------|-------------|
| POST | `/mentors/` | Create mentor |
| GET | `/mentors/` | List mentors |
| GET | `/mentors/{mentor_id}` | Get mentor by ID |
| PATCH | `/mentors/{mentor_id}` | Update mentor |
| DELETE | `/mentors/{mentor_id}` | Delete mentor |

### Mentorships

| Method | Path | Description |
|--------|------|-------------|
| POST | `/mentorships/` | Create mentorship |
| GET | `/mentorships/` | List mentorships |
| GET | `/mentorships/{mentorship_id}` | Get mentorship by ID |
| PATCH | `/mentorships/{mentorship_id}` | Update mentorship status |
| DELETE | `/mentorships/{mentorship_id}` | Delete mentorship |

Statuses:

- `active`
- `paused`
- `completed`

### Goals and Progress Logs

| Method | Path | Description |
|--------|------|-------------|
| POST | `/goals/` | Create goal |
| GET | `/goals/` | List goals |
| GET | `/goals/?mentorship_id=` | Filter goals by mentorship |
| GET | `/goals/{goal_id}` | Get goal by ID |
| PATCH | `/goals/{goal_id}` | Update goal |
| DELETE | `/goals/{goal_id}` | Delete goal |
| POST | `/progress-logs/` | Create progress log |
| DELETE | `/progress-logs/{log_id}` | Delete progress log |

Goal statuses:

- `not_started`
- `in_progress`
- `completed`
- `blocked`

### Resources

| Method | Path | Description |
|--------|------|-------------|
| POST | `/resources/` | Create resource |
| GET | `/resources/` | List resources |
| GET | `/resources/{resource_id}` | Get resource by ID |
| PATCH | `/resources/{resource_id}` | Update resource |
| DELETE | `/resources/{resource_id}` | Delete resource |

### Mentorship Resource Mapping

| Method | Path | Description |
|--------|------|-------------|
| POST | `/mentorship/{mentorship_id}/resources/{resource_id}` | Attach resource to mentorship |
| GET | `/mentorship/{mentorship_id}/resources` | List resources for mentorship |
| DELETE | `/mentorship/{mentorship_id}/resources/{resource_id}` | Remove resource from mentorship |

### Goal Resource Mapping

| Method | Path | Description |
|--------|------|-------------|
| POST | `/goals/{goal_id}/resources/{resource_id}` | Attach resource to goal |
| GET | `/goals/{goal_id}/resources` | List resources for goal |
| DELETE | `/goals/{goal_id}/resources/{resource_id}` | Remove resource from goal |



# Mentee Endpoints:


![Mentee Endpoints](assets/mentee_endpoints.png)


# Mentor Endpoints:

![Mentor Endpoints](assets/mentor_endpoints.png)


# Mentorship Endpoints(Mentor <-> Mentee):

![Mentor Endpoints](assets/mentorship_endpoints.png)

# Goals Endpoints:

![Goals Endpoints](assets/goals.png)

# Resource Endpoints:

![Resource Endpoints](assets/Resource.png)

# Mentorship Resource Endpoints:

![Mentorship Resource Endpoints](assets/mentorship_resource.png)

# Goal based Resource Endpoints:

![Goal Resource Endpoints](assets/goal_resource.png)



### Tables created


   Table               |       Description                                |
|----------------------|--------------------------------------------------|
| `users`              |     Mentors, mentees                             |
| `mentorships`        |     Mentor–mentee pairings                       |
| `goals`              |     Goals belonging to a mentee                  |
| `progress_logs`      |     Progress updates on a goal                   |
| `resources`          |     Resources that can be used                   |
| 'Goal_resources'     |     Resources based on goals                     |
|'Mentorship_resources'|     Resources based on mentorship 
---



## Future Enhancements:

- **Authentication** – Add login authentication
- **Frontend** – Add UI for better visibility 
- **Goal-Resource** relenvance validation using skills, or tags.
- **Mentor Recommendation** Engine based on skills match
- **Flagging** - A mentee is flagged when their active mentorship has had no session in the last N days (default 14) AND their average goal progress is below 30%.
- **Mentor Dashboard** Returns the mentor's active mentees with per-mentee summaries:           total goals, completed goals, average progress, and last session date.
- **Session scheduling and feedback tracking**
- **HR** user for getting visibilty on mentorship and progress