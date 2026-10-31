# Course Management API — Flask, JWT & Role-Based Access

A REST API for managing users and courses, built with **Flask** following a layered architecture (routes → services → data). Authentication uses **JWT** tokens, passwords are hashed with **bcrypt**, and data is stored in **SQLite**. This is a software-architecture mini-project.

## Roles

| Role | Permissions |
|---|---|
| `gerant` (manager) | Manage users (list, update, delete) and courses |
| `enseignant` (teacher) | Create, update and delete courses |
| `etudiant` (student, default) | Read courses |

## Project structure

```
.
├── app.py                  # Flask entry point, registers blueprints
├── auth/auth_handler.py    # JWT encode / decode
├── models/                 # User and Course models
├── outils/validator.py     # Input validation helpers
├── routes/                 # HTTP layer (auth_routes, course_routes)
├── services/               # Business logic + SQLite access
└── database.db             # SQLite database (users, courses)
```

## Getting started

### Prerequisites

- Python 3.9+

### Install and run

```bash
git clone <your-repo-url>
cd "mini projet"
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install flask flask-bcrypt pyjwt
python app.py
```

The API runs on http://127.0.0.1:5000.

## API

### Authentication (`/auth`)

| Method | Endpoint | Access | Description |
|---|---|---|---|
| POST | `/auth/register` | public | Create an account (`role` optional, default `etudiant`) |
| POST | `/auth/login` | public | Returns a JWT and the role |
| GET | `/auth/users` | gerant | List users |
| PUT | `/auth/users/<id>` | token | Update a user |
| DELETE | `/auth/users/<id>` | token | Delete a user |

### Courses (`/courses`)

| Method | Endpoint | Access | Description |
|---|---|---|---|
| GET | `/courses/` | public | List courses |
| POST | `/courses/` | gerant, enseignant | Create a course |
| PUT | `/courses/<id>` | gerant, enseignant | Update a course |
| DELETE | `/courses/<id>` | gerant, enseignant | Delete a course |

Protected endpoints expect the header `Authorization: Bearer <token>`.

### Example

```bash
# Register
curl -X POST http://127.0.0.1:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"sara","password":"secret","role":"enseignant"}'

# Login
curl -X POST http://127.0.0.1:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"sara","password":"secret"}'

# Create a course
curl -X POST http://127.0.0.1:5000/courses/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"title":"Software Architecture","instructor":"Sara","description":"Layered design"}'
```

## Database schema

```sql
users   (id INTEGER PK AUTOINCREMENT, username TEXT UNIQUE, password TEXT, role TEXT)
courses (id INTEGER PK AUTOINCREMENT, title TEXT, instructor TEXT, description TEXT)
```

## Known limitations

- The JWT `SECRET_KEY` is hard-coded in `auth/auth_handler.py`; load it from an environment variable before publishing.
- `/auth/register` lets anyone choose any role, including `gerant`. In production, restrict role assignment.
- `database.db` is committed and contains whatever accounts you created; consider git-ignoring it and creating it at start-up.
- `app.run(debug=True)` is for development only.
