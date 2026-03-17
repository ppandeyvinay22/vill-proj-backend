from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Village Food Platform"

    # Database — works with both local MongoDB and Atlas SRV
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "village_food"

    # Auth
    SECRET_KEY: str = "a_very_secret_key_for_development_change_in_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 * 24 * 60  # 30 days

    # Razorpay (optional — mock is used when not set)
    RAZORPAY_KEY_ID: Optional[str] = None
    RAZORPAY_KEY_SECRET: Optional[str] = None

    # Shiprocket (optional — mock is used when not set)
    SHIPROCKET_EMAIL: Optional[str] = None
    SHIPROCKET_PASSWORD: Optional[str] = None

    # Environment
    ENV: str = "development"

    @property
    def is_production(self) -> bool:
        return self.ENV == "production"

    @property
    def use_real_payments(self) -> bool:
        return self.RAZORPAY_KEY_ID is not None and self.RAZORPAY_KEY_SECRET is not None

    @property
    def use_real_logistics(self) -> bool:
        return self.SHIPROCKET_EMAIL is not None and self.SHIPROCKET_PASSWORD is not None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
