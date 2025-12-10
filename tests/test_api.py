import pytest
from fastapi import status

class TestRootEndpoint:
    """
    Tests for the root endpoint.
    """
    
    def test_root_endpoint(self, client):
        """Test that root endpoint returns welcome message."""
        response = client.get("/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "message" in data
        assert "version" in data

class TestHealthCheck:
    """
    Tests for the health check endpoint.
    """
    
    def test_health_check(self, client):
        """Test that health check endpoint returns healthy status."""
        response = client.get("/health")
        
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"status": "healthy"}

class TestCreateUser:
    """
    Integration tests for user creation endpoint.
    """
    
    def test_create_user_success(self, client):
        """Test successful user creation."""
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
        
        response = client.post("/users/", json=user_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
        assert "id" in data
        assert "created_at" in data
        assert "password" not in data
        assert "password_hash" not in data
    
    def test_create_user_duplicate_username(self, client):
        """Test that creating user with duplicate username fails."""
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
        
        # Create first user
        response1 = client.post("/users/", json=user_data)
        assert response1.status_code == status.HTTP_201_CREATED
        
        # Try to create second user with same username but different email
        user_data2 = {
            "username": "testuser",
            "email": "different@example.com",
            "password": "password123"
        }
        response2 = client.post("/users/", json=user_data2)
        
        assert response2.status_code == status.HTTP_400_BAD_REQUEST
        assert "username" in response2.json()["detail"].lower()
    
    def test_create_user_duplicate_email(self, client):
        """Test that creating user with duplicate email fails."""
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
        
        # Create first user
        response1 = client.post("/users/", json=user_data)
        assert response1.status_code == status.HTTP_201_CREATED
        
        # Try to create second user with different username but same email
        user_data2 = {
            "username": "differentuser",
            "email": "test@example.com",
            "password": "password123"
        }
        response2 = client.post("/users/", json=user_data2)
        
        assert response2.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response2.json()["detail"].lower()
    
    def test_create_user_invalid_email(self, client):
        """Test that creating user with invalid email fails validation."""
        user_data = {
            "username": "testuser",
            "email": "invalidemail",
            "password": "password123"
        }
        
        response = client.post("/users/", json=user_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_create_user_short_password(self, client):
        """Test that creating user with short password fails validation."""
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "pass"
        }
        
        response = client.post("/users/", json=user_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_create_user_short_username(self, client):
        """Test that creating user with short username fails validation."""
        user_data = {
            "username": "ab",
            "email": "test@example.com",
            "password": "password123"
        }
        
        response = client.post("/users/", json=user_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_password_is_hashed(self, client, db_session):
        """Test that password is properly hashed in database."""
        from app.models import User
        
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
        
        response = client.post("/users/", json=user_data)
        assert response.status_code == status.HTTP_201_CREATED
        
        # Query database directly
        db_user = db_session.query(User).filter(User.username == "testuser").first()
        
        assert db_user is not None
        assert db_user.password_hash != "password123"  # Password should be hashed
        assert db_user.password_hash.startswith("$2b$")  # Bcrypt hash format

class TestGetUsers:
    """
    Integration tests for getting users.
    """
    
    def test_get_empty_users_list(self, client):
        """Test getting users when database is empty."""
        response = client.get("/users/")
        
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []
    
    def test_get_users_list(self, client):
        """Test getting list of users."""
        # Create multiple users
        users = [
            {"username": "user1", "email": "user1@example.com", "password": "password123"},
            {"username": "user2", "email": "user2@example.com", "password": "password123"},
            {"username": "user3", "email": "user3@example.com", "password": "password123"}
        ]
        
        for user_data in users:
            response = client.post("/users/", json=user_data)
            assert response.status_code == status.HTTP_201_CREATED
        
        # Get all users
        response = client.get("/users/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3
        assert all("password" not in user for user in data)
        assert all("password_hash" not in user for user in data)
    
    def test_get_users_pagination(self, client):
        """Test pagination with skip and limit parameters."""
        # Create multiple users
        for i in range(5):
            user_data = {
                "username": f"user{i}",
                "email": f"user{i}@example.com",
                "password": "password123"
            }
            client.post("/users/", json=user_data)
        
        # Test skip parameter
        response = client.get("/users/?skip=2&limit=2")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2

class TestGetUser:
    """
    Integration tests for getting a specific user.
    """
    
    def test_get_user_by_id(self, client):
        """Test getting a specific user by ID."""
        # Create a user
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
        create_response = client.post("/users/", json=user_data)
        user_id = create_response.json()["id"]
        
        # Get the user
        response = client.get(f"/users/{user_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == user_id
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
        assert "password" not in data
        assert "password_hash" not in data
    
    def test_get_nonexistent_user(self, client):
        """Test getting a user that doesn't exist."""
        response = client.get("/users/99999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"].lower()
