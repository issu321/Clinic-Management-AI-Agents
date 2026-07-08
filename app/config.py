import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clinic-dev-secret-key-change-in-production'

    # Database - SQLite for production-ready portability
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{os.path.join(basedir, "..", "instance", "clinic.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # File uploads
    UPLOAD_FOLDER = os.path.join(basedir, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

    # App settings
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours
