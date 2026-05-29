import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Konfigurasi aplikasi Flask."""

    # Flask
    SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default-secret-key")

    # Database MySQL / SQLite Fallback
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "stress_detection_db")

    # Uji apakah MySQL aktif di host/port yang ditentukan. Jika tidak, gunakan SQLite.
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        s.connect((DB_HOST, int(DB_PORT)))
        s.close()
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
        print("[CONFIG] MySQL aktif terdeteksi. Menggunakan MySQL.")
    except Exception:
        db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "stress_detection.db")
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_path}"
        print(f"[CONFIG] MySQL tidak terdeteksi pada {DB_HOST}:{DB_PORT}. Menggunakan SQLite fallback: {SQLALCHEMY_DATABASE_URI}")

    SQLALCHEMY_TRACK_MODIFICATIONS = False


    # JWT
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default-secret-key")
    JWT_ACCESS_TOKEN_EXPIRES = 86400  # 24 jam (dalam detik)
