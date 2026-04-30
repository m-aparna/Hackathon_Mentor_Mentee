# Mentor-Mentee Growth Platform Diagrams

## ER Diagram

```mermaid
erDiagram
    MENTOR {
        int id PK
        string name
        string email
        enum role
        string department
        json skills
    }

    MENTEE {
        int id PK
        string name
        string email
        enum role
        string department
        json skills
    }

    MENTORSHIP {
        int id PK
        int mentor_id FK
        int mentee_id FK
        date start_date
        enum status
    }

    GOAL {
        int id PK
        int mentorship_id FK
        string title
        string description
        enum status
    }

    PROGRESS_LOG {
        int id PK
        int goal_id FK
        int progress_percent
        string update_text
    }

    RESOURCE {
        int id PK
        string title
        string link
        string description
    }

    MENTOR ||--o{ MENTORSHIP : mentors
    MENTEE ||--o{ MENTORSHIP : learns_in
    MENTORSHIP ||--o{ GOAL : has
    GOAL ||--o{ PROGRESS_LOG : tracks
    MENTORSHIP }o--o{ RESOURCE : recommends
    GOAL }o--o{ RESOURCE : supports
```

### Pairing Rule Note

- A `Mentorship` can be created only when:
  - `Mentor.department == Mentee.department`
  - `Mentor.skills` and `Mentee.skills` have at least one overlapping value

This rule is application logic enforced during mentorship creation. It does not require a separate matching table in the current design.

## Flow Diagram

```mermaid
flowchart TD
    A["Create Mentor Profile"] --> C["Store Mentor Department and Skills"]
    B["Create Mentee Profile"] --> D["Store Mentee Department and Skills"]
    C --> E["Try Mentorship Creation"]
    D --> E
    E --> F{"Same Department?"}
    F -- "No" --> X["Reject Pairing"]
    F -- "Yes" --> G{"At Least One Shared Skill?"}
    G -- "No" --> X
    G -- "Yes" --> H["Create Mentorship"]
    H --> I["Create Goal"]
    H --> J["Attach General Resource to Mentorship"]
    I --> K["Attach Goal-Specific Resource"]
    I --> L["Add Progress Log"]
    L --> M["Track Goal Progress"]
    J --> N["Continuous Improvement Support"]
    K --> O["Focused Goal Learning"]
    M --> P["Mentor Reviews Growth"]
    N --> P
    O --> P
```

## Demo Explanation

- `Mentorship -> Resource` means a general recommendation for ongoing improvement.
- `Goal -> Resource` means a targeted learning resource for one specific goal.
- `ProgressLog` shows how the mentee is moving toward a goal over time.
- `Mentorship` is created only if mentor and mentee match on department and share at least one skill.

Example:

- Mentorship resource: `PPT Design Basics`
- Goal: `Learn FastAPI`
- Goal resource: `FastAPI Tutorial`
