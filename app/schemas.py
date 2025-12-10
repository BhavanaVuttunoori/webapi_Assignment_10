"""
Pydantic schemas for request and response validation.
"""
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    """
    Schema for creating a new user.
    
    Attributes:
        username: Username for the new user (3-50 characters).
        email: Valid email address for the user.
        password: Password for the user (minimum 8 characters).
    """
    
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Username must be between 3 and 50 characters"
    )
    email: EmailStr = Field(
        ...,
        description="Valid email address"
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="Password must be at least 8 characters"
    )
    
    @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        """Validate that username contains only alphanumeric characters and underscores."""
        if not v.replace('_', '').isalnum():
            raise ValueError('Username must contain only alphanumeric characters and underscores')
        return v
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "john_doe",
                    "email": "john@example.com",
                    "password": "securepassword123"
                }
            ]
        }
    }


class UserRead(BaseModel):
    """
    Schema for reading user data.
    
    Attributes:
        id: Unique identifier for the user.
        username: Username of the user.
        email: Email address of the user.
        created_at: Timestamp when the user was created.
    """
    
    id: int
    username: str
    email: str
    created_at: datetime
    
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "username": "john_doe",
                    "email": "john@example.com",
                    "created_at": "2024-01-01T12:00:00Z"
                }
            ]
        }
    }


class UserUpdate(BaseModel):
    """
    Schema for updating user data.
    
    Attributes:
        email: Optional new email address.
        password: Optional new password.
    """
    
    email: EmailStr | None = None
    password: str | None = Field(None, min_length=8, max_length=100)
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "newemail@example.com",
                    "password": "newsecurepassword123"
                }
            ]
        }
    }
