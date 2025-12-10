"""
Pytest configuration and fixtures for testing.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.models import User


# Create in-memory SQLite database for testing
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """
    Create a fresh database session for each test.
    
    Yields:
        Session: SQLAlchemy database session.
    """
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """
    Create a test client with overridden database dependency.
    
    Args:
        db_session: Database session fixture.
        
    Yields:
        TestClient: FastAPI test client.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def sample_user(db_session):
    """
    Create a sample user in the database.
    
    Args:
        db_session: Database session fixture.
        
    Returns:
        User: Created user object.
    """
    from app.auth import hash_password
    
    user = User(
        username="sampleuser",
        email="sample@example.com",
        password_hash=hash_password("samplepassword123")
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def multiple_users(db_session):
    """
    Create multiple sample users in the database.
    
    Args:
        db_session: Database session fixture.
        
    Returns:
        List[User]: List of created user objects.
    """
    from app.auth import hash_password
    
    users = []
    for i in range(3):
        user = User(
            username=f"user{i}",
            email=f"user{i}@example.com",
            password_hash=hash_password("password123")
        )
        db_session.add(user)
        users.append(user)
    
    db_session.commit()
    
    for user in users:
        db_session.refresh(user)
    
    return users
