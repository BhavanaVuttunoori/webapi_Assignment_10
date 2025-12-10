"""
FastAPI application with user management endpoints.
"""
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from app.config import settings
from app.database import get_db, init_db
from app.models import User
from app.schemas import UserCreate, UserRead
from app.auth import hash_password

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="A secure user management API with SQLAlchemy and Pydantic validation"
)


@app.on_event("startup")
def on_startup():
    """Initialize database on application startup."""
    try:
        init_db()
    except Exception:
        # Skip if database is not available (e.g., during testing with mocked DB)
        pass


@app.get("/", tags=["Root"])
def read_root():
    """
    Root endpoint returning welcome message.
    
    Returns:
        dict: Welcome message with API information.
    """
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version
    }


@app.get("/health", tags=["Health"])
def health_check():
    """
    Health check endpoint.
    
    Returns:
        dict: Health status of the application.
    """
    return {"status": "healthy"}


@app.post("/users/", response_model=UserRead, status_code=status.HTTP_201_CREATED, tags=["Users"])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.
    
    Args:
        user: User data from request body.
        db: Database session.
        
    Returns:
        UserRead: Created user data.
        
    Raises:
        HTTPException: If username or email already exists.
    """
    # Check if username exists
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email exists
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password and create user
    hashed_password = hash_password(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password
    )
    
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User creation failed due to database constraint"
        )


@app.get("/users/", response_model=List[UserRead], tags=["Users"])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get list of users with pagination.
    
    Args:
        skip: Number of users to skip.
        limit: Maximum number of users to return.
        db: Database session.
        
    Returns:
        List[UserRead]: List of users.
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@app.get("/users/{user_id}", response_model=UserRead, tags=["Users"])
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get a specific user by ID.
    
    Args:
        user_id: ID of the user to retrieve.
        db: Database session.
        
    Returns:
        UserRead: User data.
        
    Raises:
        HTTPException: If user not found.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user
