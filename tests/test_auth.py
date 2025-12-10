"""
Unit tests for authentication utilities and password hashing.
"""
import pytest
from app.auth import hash_password, verify_password


class TestPasswordHashing:
    """
    Unit tests for password hashing and verification.
    """
    
    def test_hash_password_returns_different_hash(self):
        """Test that hashing the same password twice returns different hashes."""
        password = "testpassword123"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        
        assert hash1 != hash2  # Bcrypt uses salt, so hashes should differ
        assert hash1 != password  # Hash should not be the same as plain text
    
    def test_hash_password_format(self):
        """Test that hashed password has correct bcrypt format."""
        password = "testpassword123"
        hashed = hash_password(password)
        
        assert hashed.startswith("$2b$")  # Bcrypt format
        assert len(hashed) == 60  # Bcrypt hash length
    
    def test_verify_password_correct(self):
        """Test that verify_password returns True for correct password."""
        password = "testpassword123"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) is True
    
    def test_verify_password_incorrect(self):
        """Test that verify_password returns False for incorrect password."""
        password = "testpassword123"
        wrong_password = "wrongpassword"
        hashed = hash_password(password)
        
        assert verify_password(wrong_password, hashed) is False
    
    def test_verify_password_empty_string(self):
        """Test that verify_password handles empty passwords."""
        password = "testpassword123"
        hashed = hash_password(password)
        
        assert verify_password("", hashed) is False
    
    def test_hash_special_characters(self):
        """Test that password with special characters is hashed correctly."""
        password = "P@ssw0rd!#$%^&*()"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) is True
        assert verify_password("P@ssw0rd!#$%^&*", hashed) is False
    
    def test_hash_unicode_characters(self):
        """Test that password with unicode characters is hashed correctly."""
        password = "密码测试123"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) is True
        assert verify_password("密码测试12", hashed) is False
