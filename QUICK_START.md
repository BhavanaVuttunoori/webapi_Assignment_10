# Quick Start Guide

## 🚀 Running the Application

### Option 1: Local Development (Without Docker)

1. **Install PostgreSQL** (if not already installed)

2. **Create database**:
   ```powershell
   # Using psql
   psql -U postgres
   CREATE DATABASE userdb;
   \q
   ```

3. **Set up environment**:
   ```powershell
   # Create .env file
   Copy-Item .env.example .env
   
   # Edit .env if needed (default works for local PostgreSQL)
   ```

4. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

5. **Run the application**:
   ```powershell
   uvicorn app.main:app --reload
   ```

6. **Access the API**:
   - API: http://localhost:8000
   - Interactive Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Option 2: Docker Compose (Recommended)

1. **Start everything**:
   ```powershell
   docker-compose up -d
   ```

2. **Check status**:
   ```powershell
   docker-compose ps
   ```

3. **View logs**:
   ```powershell
   docker-compose logs -f api
   ```

4. **Stop everything**:
   ```powershell
   docker-compose down
   ```

## 🧪 Testing

### Run All Tests:
```powershell
pytest -v
```

### Run Specific Test File:
```powershell
pytest tests/test_auth.py -v
pytest tests/test_api.py -v
```

### Run Single Test:
```powershell
pytest tests/test_auth.py::TestPasswordHashing::test_hash_password_format -v
```

### Run with Coverage:
```powershell
pytest --cov=app --cov-report=html
# Open htmlcov/index.html in browser
```

## 📊 API Examples

### Create a User:
```powershell
curl -X POST http://localhost:8000/users/ `
  -H "Content-Type: application/json" `
  -d '{"username":"john_doe","email":"john@example.com","password":"securepass123"}'
```

### Get All Users:
```powershell
curl http://localhost:8000/users/
```

### Get User by ID:
```powershell
curl http://localhost:8000/users/1
```

### Health Check:
```powershell
curl http://localhost:8000/health
```

## 🐳 Docker Commands

### Build Image:
```powershell
docker build -t user-management-api .
```

### Run Container:
```powershell
docker run -p 8000:8000 `
  -e DATABASE_URL=postgresql://postgres:postgres@host.docker.internal:5432/userdb `
  user-management-api
```

### Pull from Docker Hub:
```powershell
docker pull YOUR_USERNAME/user-management-api:latest
docker run -p 8000:8000 YOUR_USERNAME/user-management-api:latest
```

## 🔧 Troubleshooting

### Tests failing locally?
```powershell
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Database connection error?
```powershell
# Check PostgreSQL is running
Get-Service postgresql*

# If not running, start it
Start-Service postgresql-x64-15  # Adjust version number
```

### Port already in use?
```powershell
# Find process using port 8000
Get-NetTCPConnection -LocalPort 8000 | Select-Object -Property OwningProcess | Get-Unique

# Kill the process (replace PID with actual process ID)
Stop-Process -Id PID
```

### Docker issues?
```powershell
# Clean up Docker
docker-compose down -v
docker system prune -f

# Rebuild from scratch
docker-compose up --build
```

## 📝 Development Workflow

1. **Make changes** to code
2. **Run tests** to verify:
   ```powershell
   pytest -v
   ```
3. **Test locally** with uvicorn:
   ```powershell
   uvicorn app.main:app --reload
   ```
4. **Commit and push**:
   ```powershell
   git add .
   git commit -m "Description of changes"
   git push
   ```
5. **Check GitHub Actions** for CI/CD status

## 🌐 Interactive API Documentation

Once the application is running, visit:
- **Swagger UI**: http://localhost:8000/docs
  - Try out endpoints directly from browser
  - See request/response schemas
  - Test authentication

- **ReDoc**: http://localhost:8000/redoc
  - Alternative documentation format
  - Easier to read and navigate

## 📊 Monitoring

### Check Application Logs:
```powershell
# Docker Compose
docker-compose logs -f api

# Docker
docker logs <container-id> -f
```

### Database Access:
```powershell
# Connect to PostgreSQL container
docker-compose exec db psql -U postgres -d userdb

# List tables
\dt

# Query users
SELECT * FROM users;

# Exit
\q
```

## 🔐 Security Notes

- Never commit `.env` file (already in `.gitignore`)
- Use strong passwords in production
- Change default database credentials
- Use HTTPS in production
- Set proper CORS settings for production
- Keep dependencies updated

## 📚 Additional Resources

- FastAPI Docs: https://fastapi.tiangolo.com/
- SQLAlchemy Docs: https://docs.sqlalchemy.org/
- Pydantic Docs: https://docs.pydantic.dev/
- Docker Docs: https://docs.docker.com/
- PostgreSQL Docs: https://www.postgresql.org/docs/
