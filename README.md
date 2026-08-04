# QA Test Playground

A full-stack web application designed as a **QA testing playground**, exposing **23 realistic REST APIs** with complete CRUD, JWT authentication, OpenAPI documentation, validation, and predictable workflows.

## Quick Start

### Backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 9000
```

- **API**: http://localhost:9000
- **Swagger UI**: http://localhost:9000/docs
- **OpenAPI JSON**: http://localhost:9000/openapi.json

### Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

- **UI**: http://localhost:5173

### Default Credentials

```
Email:    admin@test.com
Password: password123
```

## API Summary

| Module         | Endpoints | Prefix        |
|----------------|-----------|---------------|
| Authentication | 3         | `/auth`       |
| Students       | 5         | `/students`   |
| Courses        | 5         | `/courses`    |
| Attendance     | 5         | `/attendance` |
| Notices        | 5         | `/notices`    |
| **Total**      | **23**    |               |

## Seed Data

On first run, the database is automatically seeded with:
- 1 admin user
- 10 students
- 5 courses
- 20 attendance records
- 5 notices

## Testing Scenarios

This playground is designed for:
- Manual API Testing (Postman, Bruno, Insomnia, curl)
- API Automation (Pytest, REST Assured)
- UI Automation (Playwright, Selenium)
- Regression Testing
- Load Testing
- OpenAPI-based API Discovery
- Schema Validation
- Negative Testing

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, SQLite, Pydantic, PyJWT
- **Frontend**: React 18, Vite, Axios, React Router v6
