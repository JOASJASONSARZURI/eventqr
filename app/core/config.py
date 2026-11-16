import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", os.getenv("APP_TITLE", "QRManager"))
    STORAGE_SECRET: str = os.getenv("STORAGE_SECRET", "default_secret")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./qrmanager.db")
    PORT: int = int(os.getenv("PORT", os.getenv("APP_PORT", 8080)))

settings = Settings()