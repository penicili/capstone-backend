import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
ML_DIR = BASE_DIR / "assets" / "models"

# Model paths
FINAL_GRADE_MODEL_PATH = ML_DIR / "final_grade_model.pkl"
DROPOUT_MODEL_PATH = ML_DIR / "dropout_model.pkl"
LABEL_ENCODER_FINALGRADE_PATH = ML_DIR / "label_encoder_finalgrade.pkl"
LABEL_ENCODER_DROPOUT_PATH = ML_DIR / "label_encoder_dropout.pkl"
