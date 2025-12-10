"""
Docstring for services.predictor_service
predictor service untuk handling prediksi ML models
"""
from model_service import model_service
from schemas.types import DropoutFeaturesEncoded, FinalResultFeaturesEncoded
from core.logging import logger

class PredictorService:
    def __init__(self):
        models = model_service.get_models()
        self.final_grade_model = models.get("final_grade_model")
        self.dropout_model = models.get("dropout_model")
        
    def predict_final_grade(self, features: FinalResultFeaturesEncoded):
        """Predict final grade berdasarkan input data"""
        if not self.final_grade_model:
            logger.exception("Final grade model is not loaded")
            raise Exception("Final grade model is not loaded")
        prediction = self.final_grade_model.predict([features])
        return prediction[0]
    
    def predict_dropout(self, features: DropoutFeaturesEncoded):
        """Predict dropout berdasarkan input data"""
        if not self.dropout_model:
            logger.exception("Dropout model is not loaded")
            raise Exception("Dropout model is not loaded")
        prediction = self.dropout_model.predict([features])
        return prediction[0]
    

# Global instance
predictor_service = PredictorService()   