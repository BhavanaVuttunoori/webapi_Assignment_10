# User Management API

A secure FastAPI application with user authentication, SQLAlchemy ORM, Pydantic validation, and comprehensive testing.

[![CI/CD Pipeline](https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/ci-cd.yml)

## 🚀 Features

- **Secure User Model**: SQLAlchemy-based User model with hashed passwords using bcrypt
- **Pydantic Validation**: Request/response validation with email and password constraints
- **RESTful API**: Full CRUD operations for user management
- **Comprehensive Testing**: Unit and integration tests with pytest
- **CI/CD Pipeline**: Automated testing and Docker image deployment via GitHub Actions
- **Docker Support**: Containerized application ready for deployment
- **Database Support**: PostgreSQL with SQLAlchemy ORM

## 📋 Requirements

- Python 3.11+
- PostgreSQL 15+
- Docker (optional, for containerized deployment)

## 🛠️ Installation

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
   cd YOUR_REPO
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   DATABASE_URL=postgresql://postgres:postgres@localhost:5432/userdb
   DEBUG=False
   ```

5. **Set up PostgreSQL database**
   ```bash
   # Create database
   createdb userdb
   
   # Or using psql
   psql -U postgres -c "CREATE DATABASE userdb;"
   ```

### Docker Setup

1. **Build the Docker image**
   ```bash
   docker build -t user-management-api .
   ```

2. **Run with Docker Compose** (recommended)
   
   Create a `docker-compose.yml` file:
   ```yaml
   version: '3.8'
   
   services:
     db:
       image: postgres:15
       environment:
         POSTGRES_USER: postgres
         POSTGRES_PASSWORD: postgres
         POSTGRES_DB: userdb
       ports:
         - "5432:5432"
       volumes:
         - postgres_data:/var/lib/postgresql/data
     
     api:
       build: .
       ports:
         - "8000:8000"
       environment:
         DATABASE_URL: postgresql://postgres:postgres@db:5432/userdb
       depends_on:
         - db
   
   volumes:
     postgres_data:
   ```
   
   Then run:
   ```bash
   docker-compose up
   ```

## 🏃 Running the Application

### Local Development

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Access the API at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Docker

```bash
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://postgres:postgres@host.docker.internal:5432/userdb \
  user-management-api
```

## 🧪 Testing

### Run All Tests

```bash
pytest -v
```

### Run Specific Test Files

```bash
# Unit tests (password hashing)
pytest tests/test_auth.py -v

# Integration tests (API endpoints)
pytest tests/test_api.py -v
```

### Run Tests with Coverage

```bash
pytest --cov=app --cov-report=html
```

View coverage report by opening `htmlcov/index.html` in your browser.

### Test with PostgreSQL (like CI)

```bash
# Ensure PostgreSQL is running
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/testdb

# Run tests
pytest -v
```

## 📚 API Endpoints

### Root & Health

- `GET /` - Welcome message
- `GET /health` - Health check

### Users

- `POST /users/` - Create a new user
  ```json
  {
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword123"
  }
  ```

- `GET /users/` - Get all users (with pagination)
  - Query params: `skip` (default: 0), `limit` (default: 100)

- `GET /users/{user_id}` - Get user by ID

## 🔒 Security Features

1. **Password Hashing**: Bcrypt algorithm with automatic salt generation
2. **Unique Constraints**: Enforced at database level for username and email
3. **Input Validation**: Pydantic schemas validate all inputs
4. **No Password Exposure**: Password hashes never returned in API responses

## 🐳 Docker Hub

The Docker image is automatically built and pushed to Docker Hub on every successful commit to the main branch.

**Docker Hub Repository**: [https://hub.docker.com/r/YOUR_USERNAME/user-management-api](https://hub.docker.com/r/YOUR_USERNAME/user-management-api)

### Pull and Run the Image

```bash
# Pull latest image
docker pull YOUR_USERNAME/user-management-api:latest

# Run the container
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://postgres:postgres@localhost:5432/userdb \
  YOUR_USERNAME/user-management-api:latest
```

## 🔄 CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment:

1. **Testing Stage**:
   - Sets up Python 3.11 environment
   - Spins up PostgreSQL service container
   - Runs unit tests (`test_auth.py`)
   - Runs integration tests (`test_api.py`)

2. **Build & Deploy Stage** (on successful tests):
   - Builds Docker image
   - Pushes to Docker Hub with tags:
     - `latest`
     - `{branch}-{sha}`

### Setting Up CI/CD

Add the following secrets to your GitHub repository:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Add the following repository secrets:
   - `DOCKER_USERNAME`: Your Docker Hub username
   - `DOCKER_PASSWORD`: Your Docker Hub password or access token

## 📁 Project Structure

```
.
├── app/
│   ├── __init__.py          # Package initialization
│   ├── auth.py              # Password hashing utilities
│   ├── config.py            # Application configuration
│   ├── database.py          # Database setup and session management
│   ├── main.py              # FastAPI application and routes
│   ├── models.py            # SQLAlchemy models
│   └── schemas.py           # Pydantic schemas
├── tests/
│   ├── conftest.py          # Pytest fixtures
│   ├── test_api.py          # Integration tests
│   └── test_auth.py         # Unit tests
├── .github/
│   └── workflows/
│       └── ci-cd.yml        # GitHub Actions workflow
├── Dockerfile               # Docker image configuration
├── docker-compose.yml       # Docker Compose setup
├── requirements.txt         # Python dependencies
├── pytest.ini               # Pytest configuration
└── README.md                # This file
```

## 🧩 Technologies Used

- **FastAPI**: Modern web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation using Python type annotations
- **PostgreSQL**: Relational database
- **Bcrypt/Passlib**: Password hashing
- **Pytest**: Testing framework
- **Docker**: Containerization
- **GitHub Actions**: CI/CD automation

## 📝 Learning Outcomes Demonstrated

- ✅ **CLO3**: Python applications with automated testing (pytest, fixtures, unit & integration tests)
- ✅ **CLO4**: GitHub Actions CI/CD with automated tests and Docker builds
- ✅ **CLO9**: Application containerization using Docker
- ✅ **CLO11**: Python-SQL database integration with SQLAlchemy
- ✅ **CLO12**: JSON serialization/validation with Pydantic
- ✅ **CLO13**: Security best practices (password hashing, encryption)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is part of an academic assignment and is available for educational purposes.

## 👤 Author

**Your Name**
- GitHub: [@YOUR_USERNAME](https://github.com/YOUR_USERNAME)
- Email: your.email@example.com

## 🙏 Acknowledgments

- Course: Web API Development
- Institution: [Your Institution]
- Assignment: Module 10 - Secure User Model, Pydantic Validation, Database Testing, and Docker Deployment
