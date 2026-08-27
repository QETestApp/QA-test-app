# QA Test Playground

A full-stack web application designed as a **QA testing playground**, exposing **23 realistic REST APIs** with complete CRUD, JWT authentication, OpenAPI documentation, validation, and predictable workflows.

## Quick Start((

### Backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt
copy .env.example .env  # Windows PowerShell: Copy-Item .env.example .env
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **OpenAPI JSON**: http://localhost:8000/openapi.json
- **Health**: http://localhost:8000/health

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

## Environment Setup

### Backend

Create a backend environment file from the example:

```bash
cd backend
copy .env.example .env
```

Required variables:

```env
APP_NAME=QA Test Playground API
APP_ENV=development
HOST=0.0.0.0
PORT=8000
API_PREFIX=/api/v1
DATABASE_URL=sqlite:///./qa_playground.db
JWT_SECRET=change-me-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
ALLOW_CREDENTIALS=true
ALLOWED_METHODS=*
ALLOWED_HEADERS=*
```

### Frontend

The Vite frontend uses environment files:

```env
# frontend/.env.development
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

```env
# frontend/.env.production
VITE_API_BASE_URL=https://your-production-backend.example.com/api/v1
```

To change the backend URL, update the Vite environment variable and rebuild the frontend.

## Local Development

1. Start the backend from the backend folder.
2. Start the frontend from the frontend folder.
3. The frontend will call the backend via the configured VITE_API_BASE_URL.

## Production Deployment

- Set production values in backend/.env or the deployment platform's secret manager.
- Ensure JWT_SECRET is set to a strong secret value.
- Configure CORS_ORIGINS to include the deployed frontend origin.
- Build the frontend with `npm run build`.
- Serve the backend with an environment-aware process manager such as Docker, systemd, or a PaaS.

## Build Frontend

```bash
cd frontend
npm run build
```

## Deployment Notes

- Keep .env files out of version control.
- Only commit .env.example.
- The application reads configuration from environment variables so local, staging, and production deployments only require environment changes.

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
