from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 33333

    # Database
    MYSQL_HOST: str
    MYSQL_PORT: int = 3306
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DATABASE: str

    # Redis
    REDIS_HOST: str
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = ""

    # CORS
    CORS_ALLOWED_FRONTEND_URL: str

    # OAuth - Google
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = ""

    # OAuth - Kakao (future)
    KAKAO_CLIENT_ID: str = ""
    KAKAO_CLIENT_SECRET: str = ""
    KAKAO_REDIRECT_URI: str = ""

    # OAuth - Naver (future)
    NAVER_CLIENT_ID: str = ""
    NAVER_CLIENT_SECRET: str = ""
    NAVER_REDIRECT_URI: str = ""

    # Security
    CSRF_SECRET_KEY: str
    COOKIE_SECURE: bool = False  # Set True in production (HTTPS)
    COOKIE_SAMESITE: str = "lax"

    # Session
    SESSION_TTL_SECONDS: int = 86400  # 24 hours

    # Frontend URL for redirects after OAuth
    FRONTEND_URL: str

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra env vars like MYSQL_ROOT_PASSWORD


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
