from pydantic_settings import BaseSettings  # Changed import
from pydantic import Field  # Optional: For field configurations

class Settings(BaseSettings):
    # Individual database components
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_HOSTNAME: str 
    DATABASE_PORT: str = "5432"
    DATABASE_NAME: str
    
    # Auth
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Storage
    UPLOAD_DIR: str = "uploads"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()