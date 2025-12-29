import os
from pathlib import Path
from dotenv import load_dotenv

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env file dari src directory (jangan override env vars dari Docker)
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path, override=False)

# ML Directory
ML_DIR = BASE_DIR / os.getenv("ML_DIR", "assets/models")

# Model paths
FINAL_GRADE_MODEL_PATH = ML_DIR / os.getenv("FINAL_GRADE_MODEL_PATH", "final_grade_model.pkl")
DROPOUT_MODEL_PATH = ML_DIR / os.getenv("DROPOUT_MODEL_PATH", "dropout_model.pkl")
LABEL_ENCODER_FINALGRADE_PATH = ML_DIR / os.getenv("LABEL_ENCODER_FINALGRADE_PATH", "label_encoder_finalgrade.pkl")
LABEL_ENCODER_DROPOUT_PATH = ML_DIR / os.getenv("LABEL_ENCODER_DROPOUT_PATH", "label_encoder_dropout.pkl")

# API Settings
API_VERSION = os.getenv("API_VERSION", "1.0.0")
API_TITLE = os.getenv("API_TITLE", "Capstone KPI & ML API")
API_DESCRIPTION = os.getenv("API_DESCRIPTION", "Backend API for KPI dashboard and ML predictions")

# Server Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = BASE_DIR / "logs" / os.getenv("LOG_FILE", "app.log")

# Database Configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3006"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "capstone_kpi")

# Database Pool Configuration
DB_POOL_MIN_CACHED = int(os.getenv("DB_POOL_MIN_CACHED", "2"))
DB_POOL_MAX_CACHED = int(os.getenv("DB_POOL_MAX_CACHED", "5"))
DB_POOL_MAX_CONNECTIONS = int(os.getenv("DB_POOL_MAX_CONNECTIONS", "10"))

# Redis Configuration
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")

# KPI Cache Configuration
KPI_CACHE_TTL_SECONDS = int(os.getenv("KPI_CACHE_TTL_SECONDS", "300"))  # Default: 5 menit

# Sample Size buat dimasukin model
SAMPLE_SIZE = float(os.getenv("SAMPLE_SIZE", "0.2"))  