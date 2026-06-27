# CloudBoard Database Schema

## Entities

User
- has many Projects

Project
- belongs to User
- has many Tasks

Task
- belongs to Project


## Table

`users`

| Column | Data Type | Constraints | Description |
|---|---|---|---|
| id | Integer | Primary Key | User identifier |
| email | VARCHAR | Required, Unique | User email address |
| hashed_password | VARCHAR | Required | Encrypted user password |
| role | VARCHAR/ENUM | Required, Default: user | User permission level |
| created_at | Timestamp | Required | Account creation time |
| updated_at | Timestamp | Required | Last update time |


## Table

`projects`

| Column | Data Type | Constraints | Description |
|---|---|---|---|
| id | Integer | Primary Key | Project identifier |
| title | VARCHAR | Required | Project name |
| description | TEXT | Optional | Project details |
| owner_id | Integer | Foreign Key → users.id, Required | User who owns the project |
| created_at | Timestamp | Required | Project creation time |
| updated_at | Timestamp | Required | Last update time |


## Table

`tasks`

| Column | Data Type | Constraints | Description |
|---|---|---|---|
| id | Integer | Primary Key | Task identifier |
| title | VARCHAR | Required | Task name |
| description | TEXT | Optional | Task details |
| status | VARCHAR/ENUM | Required, Default: todo | Current state |
| priority | VARCHAR/ENUM | Required, Default: normal | Task priority |
| due_date | Timestamp | Optional | Deadline |
| project_id | Integer | Foreign Key → projects.id, Required | Parent project |
| created_at | Timestamp | Required | Creation time |
| updated_at | Timestamp | Required | Last update time |


## Decisions

- Project deletion deletes tasks.
- Task cannot exist without project.
- User owns projects.


### Polish it later if needed, this is a copy pasted basic schema from AI (for time constraints)
### I reviewed it though