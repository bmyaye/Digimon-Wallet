from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SQLDB_URL: str
    ECRET_KEY: str = "secret"

    # model_config = SettingsConfigDict(env_file=".env")

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 5 * 60  # 5 minutes
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 7 * 24 * 60  # 7 days

    model_config = SettingsConfigDict(
        env_file=".env", validate_assignment=True, extra="allow"
    )


def get_settings():
    return Settings()