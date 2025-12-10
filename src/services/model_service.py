"""
Model service buat loading model dan encoding
"""
import pickle
from pathlib import Path
from config import settings
from core.logging import logger

class ModelService:
    """Service untuk mengelola ML models dan predictions"""
    
    def __init__(self):
        """Initialize model service"""
        self.dropout_model = None
        self.final_grade_model = None
        self.label_encoder_dropout = None
        self.label_encoder_finalgrade = None
        
    def load_models(self):
        """Load semua ML models"""
        try:
            with open(settings.DROPOUT_MODEL_PATH, 'rb') as f:
                self.dropout_model = pickle.load(f)
            with open(settings.FINAL_GRADE_MODEL_PATH, 'rb') as f:
                self.final_grade_model = pickle.load(f)
                
            # encoder models
            with open(settings.LABEL_ENCODER_DROPOUT_PATH, 'rb') as f:
                self.label_encoder_dropout = pickle.load(f)
            with open(settings.LABEL_ENCODER_FINALGRADE_PATH, 'rb') as f:
                self.label_encoder_finalgrade = pickle.load(f)
                
        except Exception as e:
            logger.exception("error loading models")
            raise
    
    def is_ready(self):
        """Check apakah models sudah di-load"""
        return self.dropout_model is not None and self.final_grade_model is not None
    
    def get_models(self):
        """Get loaded models"""
        return {
            "dropout_model": self.dropout_model,
            "final_grade_model": self.final_grade_model,
        }
    def get_encoders(self):
        """Get loaded label encoders"""
        return {
            "label_encoder_dropout": self.label_encoder_dropout,
            "label_encoder_finalgrade": self.label_encoder_finalgrade,
        }

# Global instance
model_service = ModelService()