import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Konfigurasi aplikasi Flask."""

    # Flask
    SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default-secret-key")

    # Database MySQL
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "stress_detection_db")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default-secret-key")
    JWT_ACCESS_TOKEN_EXPIRES = 86400  # 24 jam (dalam detik)
