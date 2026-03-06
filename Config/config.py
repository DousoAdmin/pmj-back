import os
from dotenv import load_dotenv

# Carga las variables desde el archivo .env
load_dotenv()

class Settings:
    # App info
    APP_NAME: str = os.getenv("APP_NAME", "FastAPI App")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    APP_DESCRIPTION: str = os.getenv("APP_DESCRIPTION", "")
    APP_ENV: str = os.getenv("APP_ENV", "development")
    APP_HOST: str = os.getenv("APP_HOST", "127.0.0.1")
    APP_PORT: int = int(os.getenv("APP_PORT", 8000))

    # Database
    DB_ENGINE: str = os.getenv("DB_ENGINE", "mysql")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "3306")
    DB_DATABASE: str = os.getenv("DB_DATABASE", "test")
    DB_USERNAME: str = os.getenv("DB_USERNAME", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    
    # Construir DATABASE_URL para MySQL
    @property
    def DATABASE_URL(self) -> str:
        return f"mysql+pymysql://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_DATABASE}"

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

settings = Settings()