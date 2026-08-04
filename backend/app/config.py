"""
Application configuration settings.
"""

SECRET_KEY = "qa-test-playground-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

DATABASE_URL = "sqlite:///./qa_playground.db"
