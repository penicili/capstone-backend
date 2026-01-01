"""
Docstring for services.predictor_service
predictor service untuk handling prediksi ML models
"""
from services.model_service import model_service
from schemas.types import DropoutFeaturesEncoded, FinalResultFeaturesEncoded
from core.logging import logger

class PredictorService:
    def __init__(self):
        # Use global model_service instance
        models = model_service.get_models()
        self.final_grade_model = models.get("final_grade_model")
        self.dropout_model = models.get("dropout_model")
        
    def predict_final_grade(self, features: FinalResultFeaturesEncoded):
        """Predict Final Result berdasarkan input data"""
        if not self.final_grade_model:
            logger.exception("Final Result model is not loaded")
            raise Exception("Final Result model is not loaded")
        
        # Convert features dict to list with correct order
        feature_list = [
            features['gender'],
            features['age_band'],
            features['studied_credits'],
            features['num_of_prev_attempts'],
            features['total_clicks'],
            features['avg_assessment_score']
        ]
        
        prediction = self.final_grade_model.predict([feature_list])
        return prediction[0]
    
    def predict_dropout(self, features: DropoutFeaturesEncoded):
        """Predict dropout berdasarkan input data"""
        if not self.dropout_model:
            logger.exception("Dropout model is not loaded")
            raise Exception("Dropout model is not loaded")
        
        # Convert features dict to list with correct order (same as final_grade)
        feature_list = [
            features['avg_assessment_score'],
            features['total_clicks'],
            features['studied_credits'],
            features['num_of_prev_attempts'],
            features['gender'],
            features['age_band']
        ]
        
        prediction = self.dropout_model.predict([feature_list])
        return int(prediction[0])