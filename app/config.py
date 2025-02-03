import os

class Config(object):
    # Database connection string; can be set via environment variable
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or "sqlite:///copiloto-py.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # DeepSeek API configuration
    DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
    DEEPSEEK_BASE_URL = os.environ.get("DEEPSEEK_BASE_URL") or "https://api.deepseek.com" 