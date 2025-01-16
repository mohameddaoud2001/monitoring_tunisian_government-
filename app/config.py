import os
from datetime import timedelta

class Config:
    # Base configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:15985212@localhost/government_monitoring')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default-jwt-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

class DevelopmentConfig(Config):
    # Development-specific configuration
    DEBUG = True

class TestingConfig(Config):
    # Testing-specific configuration
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL', 'postgresql://postgres:15985212@localhost/government_monitoring_test')
    JWT_ACCESS_TOKEN_EXPIRES = False  # Disable token expiration for testing