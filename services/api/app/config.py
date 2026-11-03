import os


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./unbuilt.db")
APP_ENV = os.getenv("APP_ENV", "development")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
