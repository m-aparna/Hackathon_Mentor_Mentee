# Hackathon_Mentor_Mentee


---

## Tech Stack

This project follows a clean, modular FastAPI architecture with SQLAlchemy-based persistence and
Pydantic validation, designed for easy extension and testing.


|-------------|------------------------------------------|
| Framework   | FastAPI 0.111                            |
| Server      | Uvicorn (ASGI)                           |
| ORM         | SQLAlchemy 2.0                           |
| Database    | MySQL 8+ (via PyMySQL driver)            |
| Validation  | Pydantic v2                              |
| Testing     | pytest + httpx + SQLite in-memory        |

---

### Prerequisites

- Python 3.10+
- MySQL 8.0+ running locally (or remote)


### 1. Clone / enter the project

```bash
    git clone 
```

### 2. Create venv:
```bash
    py -3.12 -m venv .venv
```

```bash
    python -m venv .venv
```

### 3. Activate it:

```bash
    .\\.venv\Scripts\activate.ps1
```

### 4. Install packages

```bash
    pip install -r requirements.txt
```


### 5. Run the app

```bash
    cd app
    uvicorn main:app --reload
```

 Visit **http://localhost:8000/docs** for the interactive Swagger UI.


 ## Database Setup (MySQL) Create DB and configuration

Tables are created automatically by SQLAlchemy on startup (`create_tables()` in `main.py`).  
You only need to create the database and user once:



```bash
CREATE DATABASE IF NOT EXISTS mentorship_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'mentorship_user'@'localhost' IDENTIFIED BY 'mentorship_pass';
GRANT ALL PRIVILEGES ON mentorship_db.* TO 'mentorship_user'@'localhost';
FLUSH PRIVILEGES;
```


# Mentee Endpoints:


![Mentee Endpoints](assets/mentee_endpoints.png)


# Mentor Endpoints:

![Mentor Endpoints](assets/mentor_endpoints.png)


# Mentorship Endpoints(Mentor <-> Mentee):

Mentorship is the relationship layer

It answers questions like:

Which mentor is assigned to which mentee?

Is this mentorship active or ended?

When did the mentorship start?

![Mentor Endpoints](assets/mentorship_endpoints.png)

# Goals Endpoints:


# Resource Endpoints:(Optional)


# Skill Endpoints:(Optional)



### Tables created


 Table           | Description                              |
|-----------------|------------------------------------------|
| `users`         | Mentors, mentees                         |
| `mentorships`   | Mentor–mentee pairings                   |
| `goals`         | SMART goals belonging to a mentee        |
| `progress_logs` | Progress updates on a goal               |
| `resources`     | Learning resources linked to a skill     |

---




- Swagger UI  →  http://localhost:8000/docs  
- Health      →  http://localhost:8000/health


## API Reference

### Mentee  

| Method | Path           | Description         |
|--------|----------------|---------------------|
| POST   | `/mentee/`      | Create user         |
| GET    | `/mentee/`      | List all users      |
| GET    | `/mentee/{id}`  | Get user by ID      |
| PATCH  | `/mentee/{id}`  | Update user         |
| DELETE | `/mentee/{id}`  | Delete user         |

### Mentor  `/users`

| Method | Path           | Description         |
|--------|----------------|---------------------|
| POST   | `/mentor/`      | Create user         |
| GET    | `/mentor/`      | List all users      |
| GET    | `/mentor/{id}`  | Get user by ID      |
| PATCH  | `/mentor/{id}`  | Update user         |
| DELETE | `/mentor/{id}`  | Delete user         |


*Roles:** `mentor` · `mentee` 


### Mentorships  `/mentorships`

| Method | Path                   | Description               |
|--------|------------------------|---------------------------|
| POST   | `/mentorships/`        | Create mentorship         |
| GET    | `/mentorships/`        | List all mentorships      |
| GET    | `/mentorships/{id}`    | Get by ID                 |
| PATCH  | `/mentorships/{id}`    | Update status             |
| DELETE | `/mentorships/{id}`    | Delete mentorship         |


**Statuses:** `active` · `paused` · `completed`


### Goals  `/goals` and Progress Logs `/progress-logs`

| Method | Path                          | Description               |
|--------|-------------------------------|---------------------------|
| POST   | `/goals/`                     | Create goal               |
| GET    | `/goals/?mentee_id=`          | List goals (filter opt.)  |
| GET    | `/goals/{id}`                 | Get goal by ID            |
| PATCH  | `/goals/{id}`                 | Update goal               |
| DELETE | `/goals/{id}`                 | Delete goal               |
| POST   | `/progress-logs/`             | Add progress log          |
| GET    | `/progress-logs/goal/{id}`    | Get logs for a goal       |
| DELETE | `/progress-logs/{id}`         | Delete a log entry        |

**Goal statuses:** `not_started` · `in_progress` · `completed` · `blocked`


### Resources  `/resources`

| Method | Path               | Description                        |
|--------|--------------------|------------------------------------|
| POST   | `/resources/`      | Create resource                    |
| GET    | `/resources/?skill_id=` | List (optionally filter by skill) |
| GET    | `/resources/{id}`  | Get by ID                          |
| PATCH  | `/resources/{id}`  | Update resource                    |
| DELETE | `/resources/{id}`  | Delete resource                    |




## Extending the App

- **Authentication** – Add OAuth2 / JWT using `fastapi.security`
- **Frontend** – Point any React/Vue SPA at `http://localhost:8000`; CORS is pre-configured for `*`
- Mentor Recommendation
- At-Risk Detection - A mentee is flagged when their active mentorship has had no session in the last N days (default 14) AND their average goal progress is below 30%.
- Mentor Dashboard Returns the mentor's active mentees with per-mentee summaries: total goals, completed goals, average progress, and last session date.
- 