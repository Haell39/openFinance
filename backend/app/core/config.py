from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "OpenFinance Map"
    API_V1_STR: str = "/api/v1"
    
    # Use SQLite for local dev, Postgres for production
    USE_SQLITE: bool = True
    DATABASE_URL: str = ""
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]

    def model_post_init(self, __context):
        if not self.DATABASE_URL:
            if self.USE_SQLITE:
                db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "openfinance.db")
                self.DATABASE_URL = f"sqlite:///{db_path}"
            else:
                self.DATABASE_URL = "postgresql://postgres:postgres@db/openfinance"

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
