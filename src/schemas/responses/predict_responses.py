"""
Response schemas untuk prediction endpoints
"""
from pydantic import BaseModel, Field
from typing import Any, Optional, Dict


class PredictionResponse(BaseModel):
    """Response untuk prediction"""
    success: bool = Field(..., description="Status keberhasilan prediksi")
    prediction: Any = Field(..., description="Hasil prediksi")
    message: str = Field(default="", description="Pesan tambahan")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "prediction": "Pass",
                "message": "Prediction completed successfully"
            }
        }


class ErrorResponse(BaseModel):
    """Response untuk error"""
    success: bool = Field(default=False, description="Status keberhasilan (selalu false untuk error)")
    error: str = Field(..., description="Pesan error")
    detail: Optional[str] = Field(None, description="Detail error tambahan")

    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "error": "Model not loaded",
                "detail": "Please ensure all models are loaded before making predictions"
            }
        }


class ModelStatusResponse(BaseModel):
    """Response untuk model status"""
    models_ready: bool = Field(..., description="Apakah semua model sudah ready")
    dropout_model_loaded: bool = Field(..., description="Status dropout model")
    final_grade_model_loaded: bool = Field(..., description="Status final grade model")
    dropout_encoder_loaded: bool = Field(..., description="Status dropout label encoder")
    finalgrade_encoder_loaded: bool = Field(..., description="Status final grade label encoder")

    class Config:
        json_schema_extra = {
            "example": {
                "models_ready": True,
                "dropout_model_loaded": True,
                "final_grade_model_loaded": True,
                "dropout_encoder_loaded": True,
                "finalgrade_encoder_loaded": True
            }
        }
