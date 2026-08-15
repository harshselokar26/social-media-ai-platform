from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# backend/app/.env
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):

    PROJECT_NAME: str = "AI Social Media Automation Platform"

    API_V1_STR: str = "/api/v1"

    DATABASE_URL: str

    JWT_SECRET: str

    JWT_ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    OPENAI_API_KEY: str = ""

    CLOUDINARY_NAME: str = ""

    CLOUDINARY_API_KEY: str = ""

    CLOUDINARY_API_SECRET: str = ""

    AYRSHARE_API_KEY: str = ""

    # ============================================================
    # META / FACEBOOK
    # ============================================================

    META_APP_ID: str = ""

    META_APP_SECRET: str = ""

    META_REDIRECT_URI: str = ""

    # ============================================================
    # INSTAGRAM
    # ============================================================

    INSTAGRAM_APP_ID: str = ""

    INSTAGRAM_APP_SECRET: str = ""

    INSTAGRAM_REDIRECT_URI: str = ""

    # ============================================================
    # ENVIRONMENT
    # ============================================================

    ENVIRONMENT: str = "development"

    # ============================================================
    # FACEBOOK DEVELOPMENT SAFETY
    # ============================================================

    FACEBOOK_TEST_PAGE_ID: str = ""

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()