# User Management API - Assignment 10

The Assignment 10 deliverable is a fully tested FastAPI user management service with secure authentication, database integration, and CI/CD. This README documents how the project is structured, what was implemented, and how to reproduce the results.

## Project Highlights

Built with FastAPI and SQLAlchemy to manage users through REST endpoints with secure password hashing.
Robust security implementation using bcrypt for password hashing with automatic salt generation.
Comprehensive automated test suite covering unit tests for authentication and integration tests for API endpoints (21 tests total).
Pydantic schemas with custom validators for username, email, and password validation.
Continuous Integration and Deployment via GitHub Actions to test, build, and deploy Docker images.
Containerized delivery: public Docker image available at bhavanavuttunoori/user-management-api.
PostgreSQL database integration with SQLAlchemy ORM for production use.

## Requirements

Python 3.11 or higher
PostgreSQL 15 or higher
Docker (optional, for containerized deployment)

## Getting Started

### 1. Setup Environment

```bash
git clone https://github.com/BhavanaVuttunoori/webapi_Assignment_10.git
cd webapi_Assignment_10
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Database

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/userdb
DEBUG=False
```

Set up PostgreSQL database:

```bash
createdb userdb
```

Or using psql:

```bash
psql -U postgres -c "CREATE DATABASE userdb;"
```

### 3. Run the Application Locally

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Navigate to:
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Docker Usage

### Build Locally (optional)

```bash
docker build -t user-management-api .
```

### Pull Prebuilt Image

```bash
docker pull bhavanavuttunoori/user-management-api:latest
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://postgres:postgres@localhost:5432/userdb \
  bhavanavuttunoori/user-management-api:latest
```

### Docker Compose (Recommended)

```bash
docker-compose up -d
```

This starts both the API and PostgreSQL database containers.

## Testing Strategy

Unit Tests (tests/test_auth.py): Verify password hashing functions with bcrypt.
Integration Tests (tests/test_api.py): Exercise each API endpoint through FastAPI's test client with SQLite in-memory database.
Tests cover user creation, duplicate detection, validation, pagination, and password security.

Run the full suite:

```bash
pytest -v
```

Run specific test files:

```bash
pytest tests/test_auth.py -v      # Unit tests only
pytest tests/test_api.py -v       # Integration tests only
```

Run with coverage:

```bash
pytest --cov=app --cov-report=html
```

## API Endpoints

### Root and Health

GET / - Welcome message
GET /health - Health check

### Users

POST /users/ - Create a new user
  Request body: {"username": "john_doe", "email": "john@example.com", "password": "securepassword123"}
  
GET /users/ - List all users (with pagination)
  Query params: skip (default: 0), limit (default: 100)
  
GET /users/{user_id} - Get user by ID

## Security Features

Password Hashing: Bcrypt algorithm with automatic salt generation
Unique Constraints: Enforced at database level for username and email
Input Validation: Pydantic schemas validate all inputs
No Password Exposure: Password hashes never returned in API responses
Username Validation: Alphanumeric characters and underscores only
Email Validation: Valid email format required
Password Requirements: Minimum 8 characters

## Logging

app/main.py configures FastAPI with structured error handling. Each endpoint:

Logs startup and request lifecycle events through FastAPI.
Returns validation errors via FastAPI's automatic exception handlers.
Provides detailed error messages when operations fail (e.g., duplicate username/email).
Log statements appear in the console, Docker container logs, and GitHub Actions output.

## Continuous Integration and Deployment

The repository includes a GitHub Actions workflow that runs on every push to main:

Set up Python 3.11 environment.
Spin up PostgreSQL service container for integration tests.
Install dependencies and the application package.
Execute unit tests (test_auth.py).
Execute integration tests (test_api.py).
Build Docker image on successful tests.
Push Docker image to Docker Hub with tags (latest and branch-sha).

GitHub Actions workflow file: .github/workflows/ci-cd.yml

## Assignment Instructions and Deliverables

Objective: Implement a secure FastAPI user management system with SQLAlchemy, Pydantic validation, password hashing, automated tests, and CI/CD pipeline.

### Implementation Checklist

SQLAlchemy User model with username, email, password_hash, and created_at timestamp.
Unique constraints on username and email fields.
Pydantic schemas (UserCreate, UserRead) with custom validators.
Password hashing implementation using bcrypt.
Unit tests covering password hashing functions (7 tests).
Integration tests covering all API endpoints (14 tests).
FastAPI application with CRUD operations for users.
GitHub Actions CI/CD workflow with PostgreSQL service.
Docker containerization with Dockerfile and docker-compose.yml.
Comprehensive documentation in README.

### Submission Package

GitHub repository: https://github.com/BhavanaVuttunoori/webapi_Assignment_10
Docker Hub image: https://hub.docker.com/r/bhavanavuttunoori/user-management-api
Screenshots demonstrating:
  - Successful GitHub Actions workflow run
  - Docker Hub deployment with image tags
  - Application running locally or in Docker

### Grading Guidelines

Criterion | Details
--- | ---
Submission Completeness (50 points) | Repository accessible, all files present, screenshots provided, documentation complete
Functionality and Testing (50 points) | User model correct, schemas validate properly, all tests pass in CI/CD, Docker image functional

### Learning Outcomes

CLO3: Create Python applications with automated testing
CLO4: Set up GitHub Actions for Continuous Integration (CI) with automated tests and Docker builds
CLO9: Apply containerization techniques using Docker
CLO11: Integrate Python programs with SQL databases
CLO12: Serialize, deserialize, and validate JSON using Pydantic
CLO13: Implement secure authentication with encryption, hashing, and encoding

## Project Structure

```
.
├── app/
│   ├── __init__.py          # Package initialization
│   ├── auth.py              # Password hashing utilities (bcrypt)
│   ├── config.py            # Application configuration
│   ├── database.py          # Database setup and session management
│   ├── main.py              # FastAPI application and routes
│   ├── models.py            # SQLAlchemy User model
│   └── schemas.py           # Pydantic validation schemas
├── tests/
│   ├── conftest.py          # Pytest fixtures and configuration
│   ├── test_api.py          # Integration tests (14 tests)
│   └── test_auth.py         # Unit tests (7 tests)
├── .github/
│   └── workflows/
│       └── ci-cd.yml        # GitHub Actions CI/CD workflow
├── Dockerfile               # Docker image configuration
├── docker-compose.yml       # Docker Compose setup with PostgreSQL
├── setup.py                 # Python package setup
├── requirements.txt         # Python dependencies
├── pytest.ini               # Pytest configuration
└── README.md                # This file
```

## Helpful Commands

Task | Command
--- | ---
Run all tests | `pytest -v`
Run unit tests only | `pytest tests/test_auth.py -v`
Run integration tests only | `pytest tests/test_api.py -v`
Run with coverage | `pytest --cov=app --cov-report=html`
Start application locally | `uvicorn app.main:app --reload`
Build Docker image | `docker build -t user-management-api .`
Run Docker container | `docker run -p 8000:8000 user-management-api`
Start with Docker Compose | `docker-compose up -d`
Stop Docker Compose | `docker-compose down`
View Docker logs | `docker logs -f <container_name>`
Push code to GitHub | `git add . && git commit -m "message" && git push`

## Submission Tips

Commit frequently with meaningful messages describing what was implemented.
Keep .env file out of version control (use .env.example instead).
Ensure all tests pass locally before pushing to GitHub.
Wait for GitHub Actions workflow to complete successfully.
Verify Docker image is available on Docker Hub.
Capture required screenshots after successful deployment.
Update README with your actual GitHub and Docker Hub usernames.

## Technologies Used

FastAPI: Modern web framework for building APIs
SQLAlchemy: SQL toolkit and Object-Relational Mapping (ORM)
Pydantic: Data validation using Python type annotations
PostgreSQL: Relational database management system
Bcrypt/Passlib: Password hashing and verification
Pytest: Testing framework for Python
Docker: Containerization platform
GitHub Actions: CI/CD automation

## Author

Bhavana Vuttunoori
GitHub: @BhavanaVuttunoori
Repository: webapi_Assignment_10

## Quick Links

Repository: https://github.com/BhavanaVuttunoori/webapi_Assignment_10
Docker Hub: https://hub.docker.com/r/bhavanavuttunoori/user-management-api
GitHub Actions: https://github.com/BhavanaVuttunoori/webapi_Assignment_10/actions
