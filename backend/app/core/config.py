from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List
import os


class Settings(BaseSettings):
    PROJECT_NAME: str = "OpenFinance Map"
    API_V1_STR: str = "/api/v1"

    # Database
    USE_SQLITE: bool = False
    DATABASE_URL: str = ""

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, value):
        if isinstance(value, str):
            # Accept comma separated env var values
            if value.startswith("["):
                return value
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    def model_post_init(self, __context):
        if not self.DATABASE_URL:
            if self.USE_SQLITE:
                db_path = os.path.join(
                    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                    "openfinance.db",
                )
                self.DATABASE_URL = f"sqlite:///{db_path}"
            else:
                self.DATABASE_URL = "postgresql://postgres:postgres@db/openfinance"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
