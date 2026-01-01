"""
Docstring for services.encoder_service
encoder service untuk mengelola label encoders
"""
from services.model_service import model_service
from schemas.types import DropoutFeaturesEncoded, FinalResultFeaturesEncoded, DropoutFeatures, FinalResultFeatures
from core.logging import logger

class EncoderService:
    def __init__(self):
        # Use global model_service instance
        encoders = model_service.get_encoders()
        self.label_encoder_finalgrade = encoders.get("label_encoder_finalgrade")
        self.label_encoder_dropout = encoders.get("label_encoder_dropout")
        
    def encode_finalgrade(self, data: FinalResultFeatures) -> FinalResultFeaturesEncoded:
        """Encode fitur untuk Final Result prediction"""
        if not self.label_encoder_finalgrade:
            logger.exception("Final Result label encoder is not loaded") 
            raise Exception("Final Result label encoder is not loaded")
        return {
            "gender": self.label_encoder_finalgrade['gender'].transform([data["gender"]])[0],
            "age_band": self.label_encoder_finalgrade['age_band'].transform([data["age_band"]])[0],
            "studied_credits": data["studied_credits"],
            "num_of_prev_attempts": data["num_of_prev_attempts"],
            "total_clicks": data["total_clicks"],
            "avg_assessment_score": data["avg_assessment_score"]
        }
    
    def encode_dropout(self, data: DropoutFeatures) -> DropoutFeaturesEncoded:
        """Encode fitur untuk dropout prediction (same as Final Result)"""
        if not self.label_encoder_finalgrade:
            logger.exception("Dropout encoders not loaded") 
            raise Exception("Dropout encoders not loaded")
        
        # Use same encoding as finalgrade (same features)
        return {
            "gender": int(self.label_encoder_finalgrade['gender'].transform([data["gender"]])[0]),
            "age_band": int(self.label_encoder_finalgrade['age_band'].transform([data["age_band"]])[0]),
            "studied_credits": data["studied_credits"],
            "num_of_prev_attempts": data["num_of_prev_attempts"],
            "total_clicks": data["total_clicks"],
            "avg_assessment_score": data["avg_assessment_score"]
        }