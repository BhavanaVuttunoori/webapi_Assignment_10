# Submission Checklist for Module 10 Assignment

## ✅ Before Submitting

### 1. Code Implementation
- [x] SQLAlchemy User model with username, email, password_hash, and created_at
- [x] Unique constraints on username and email
- [x] Pydantic schemas (UserCreate, UserRead) with proper validation
- [x] Password hashing with bcrypt (hash_password and verify_password functions)
- [x] FastAPI endpoints: /, /health, POST /users/, GET /users/, GET /users/{id}
- [x] All tests passing locally (21 tests total)

### 2. Testing
- [x] Unit tests for password hashing (7 tests in test_auth.py)
- [x] Integration tests for API endpoints (14 tests in test_api.py)
- [x] Tests cover:
  - User creation with validation
  - Duplicate username/email handling
  - Invalid email format
  - Short password/username validation
  - Password hashing verification
  - User retrieval and pagination

### 3. GitHub Repository Setup

#### Required Files Checklist:
- [x] `app/` directory with all application code
  - [x] `__init__.py`
  - [x] `main.py`
  - [x] `models.py`
  - [x] `schemas.py`
  - [x] `database.py`
  - [x] `config.py`
  - [x] `auth.py`
- [x] `tests/` directory
  - [x] `conftest.py`
  - [x] `test_api.py`
  - [x] `test_auth.py`
- [x] `.github/workflows/ci-cd.yml`
- [x] `Dockerfile`
- [x] `docker-compose.yml`
- [x] `requirements.txt`
- [x] `pytest.ini`
- [x] `README.md`
- [x] `.env.example`
- [x] `.gitignore`

#### Repository Configuration:
1. Create a new repository on GitHub (do not fork instructor's repo)
2. Initialize git and push code:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Module 10 assignment"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

### 4. GitHub Actions Secrets

Add these secrets to your repository:
1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Add **Repository secrets**:
   - `DOCKER_USERNAME`: Your Docker Hub username
   - `DOCKER_PASSWORD`: Your Docker Hub password or access token

To create a Docker Hub access token:
1. Log in to Docker Hub
2. Go to **Account Settings** → **Security**
3. Click **New Access Token**
4. Give it a name and copy the token
5. Use this token as `DOCKER_PASSWORD`

### 5. Docker Hub Repository

1. Create Docker Hub account at https://hub.docker.com
2. Create a repository (can be done automatically on first push)
3. Update README.md with your Docker Hub username/repository name

### 6. Screenshots Required

Take screenshots of:

#### A. GitHub Actions Workflow Success
- Go to **Actions** tab in your GitHub repository
- Click on the latest workflow run
- Take screenshot showing:
  - All jobs (test, build-and-push) completed successfully
  - Green checkmarks
  - Build details

#### B. Docker Hub Deployment
- Go to your Docker Hub repository page
- Take screenshot showing:
  - Repository name
  - Image tags (latest, branch-sha)
  - Last pushed timestamp
  - Image size

### 7. Documentation

Update README.md with:
- [x] Your GitHub username in URLs
- [x] Your Docker Hub username
- [x] Link to Docker Hub repository
- [x] Instructions for running tests locally
- [x] Instructions for running with Docker

### 8. Final Verification

Run these commands locally to verify:

```bash
# 1. Run all tests
pytest -v

# 2. Build Docker image
docker build -t user-management-api .

# 3. Test Docker image (with docker-compose)
docker-compose up -d
docker-compose ps
docker-compose down

# 4. Check git status
git status  # Should show no uncommitted changes

# 5. Verify all files are tracked
git ls-files
```

## 📤 Submission

### What to Submit:
1. **GitHub Repository URL** (must be your own repository)
2. **Screenshot**: GitHub Actions workflow success
3. **Screenshot**: Docker Hub image deployment
4. **Reflection Document** (if required by your instructor)

### Canvas Submission Format:
Create a text file or document with:
```
Student Name: [Your Name]
GitHub Repository: https://github.com/YOUR_USERNAME/YOUR_REPO
Docker Hub Repository: https://hub.docker.com/r/YOUR_USERNAME/user-management-api

GitHub Actions Screenshot: [Attach image]
Docker Hub Screenshot: [Attach image]
```

## 🎯 Grading Rubric Reference

### Submission Completeness (50 Points)
- GitHub repository link provided and accessible
- All necessary files present
- GitHub Actions workflow screenshot showing success
- Docker Hub screenshot showing deployed image
- README with local testing instructions
- README with Docker Hub links

### Functionality (50 Points)
- User model with hashed passwords and constraints
- Pydantic schemas validate correctly
- All tests pass in GitHub Actions
- CI/CD pipeline builds and deploys Docker image
- Docker image is functional and can be pulled

## 📝 Common Issues and Solutions

### Issue: Tests fail in GitHub Actions but pass locally
**Solution**: Check that `requirements.txt` includes all dependencies and versions match

### Issue: Docker build fails
**Solution**: Ensure `Dockerfile` has correct Python version and all dependencies are in `requirements.txt`

### Issue: GitHub Actions can't push to Docker Hub
**Solution**: Verify `DOCKER_USERNAME` and `DOCKER_PASSWORD` secrets are set correctly

### Issue: PostgreSQL connection fails in tests
**Solution**: Tests use SQLite in-memory database, not PostgreSQL. Check `conftest.py` fixtures

## 🚀 After Submission

1. Keep the repository public for grading
2. Do not modify code until after grading
3. Tag the submission commit:
   ```bash
   git tag -a v1.0-submission -m "Module 10 assignment submission"
   git push origin v1.0-submission
   ```

Good luck! 🎓
