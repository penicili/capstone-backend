"""
Docstring for services.encoder_service
encoder service untuk mengelola label encoders
"""
from services import ModelService
from schemas.types import DropoutFeaturesEncoded, FinalResultFeaturesEncoded, DropoutFeatures, FinalResultFeatures
from core.logging import logger

class EncoderService:
    def __init__(self):
        self.ModelService = ModelService()
        encoders = self.ModelService.get_encoders()
        self.label_encoder_finalgrade = encoders.get("label_encoder_finalgrade")
        self.label_encoder_dropout = encoders.get("label_encoder_dropout")
        
    def encode_finalgrade(self, data: FinalResultFeatures) -> FinalResultFeaturesEncoded:
        """Encode fitur untuk final grade prediction"""
        if not self.label_encoder_finalgrade:
            logger.exception("Final grade label encoder is not loaded") 
            raise Exception("Final grade label encoder is not loaded")
        return {
            "gender": self.label_encoder_finalgrade.transform([data["gender"]])[0],
            "age_band": self.label_encoder_finalgrade.transform([data["age_band"]])[0],
            "studied_credits": data["studied_credits"],
            "num_of_prev_attempts": data["num_of_prev_attempts"],
            "total_clicks": data["total_clicks"],
            "avg_assessment_score": data["avg_assessment_score"]
        }
    
    def encode_dropout(self, data: DropoutFeatures) -> DropoutFeaturesEncoded:
        """Encode fitur untuk dropout prediction"""
        if not self.label_encoder_dropout:
            logger.exception("Dropout label encoder is not loaded") 
            raise Exception("Dropout label encoder is not loaded")
        return {
            "code_module": self.label_encoder_dropout.transform([data["code_module"]])[0],
            "code_presentation": self.label_encoder_dropout.transform([data["code_presentation"]])[0],
            "gender": self.label_encoder_dropout.transform([data["gender"]])[0],
            "region": self.label_encoder_dropout.transform([data["region"]])[0],
            "highest_education": self.label_encoder_dropout.transform([data["highest_education"]])[0],
            "imd_band": self.label_encoder_dropout.transform([data["imd_band"]])[0],
            "age_band": self.label_encoder_dropout.transform([data["age_band"]])[0],
            "num_of_prev_attempts": data["num_of_prev_attempts"],
            "studied_credits": data["studied_credits"],
            "disability": self.label_encoder_dropout.transform([data["disability"]])[0]
        }


# Global instance
encoder_service = EncoderService()