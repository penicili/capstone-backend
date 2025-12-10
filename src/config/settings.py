import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
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