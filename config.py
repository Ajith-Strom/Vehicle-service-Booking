import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Flask configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'vehicle-service-secret-key-2024')
    
    # Database configuration
    if os.getenv('DATABASE_URL'):  # For PostgreSQL (Render)
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL').replace('postgres://', 'postgresql://')
    else:  # For MySQL (local development)
        SQLALCHEMY_DATABASE_URI = (
            f"mysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@"
            f"{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DB')}"
        )
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False 