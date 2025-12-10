from fastapi import APIRouter, HTTPException, Request
from typing import Optional, Any

from schemas.requests import FinalResultRequest, DropoutRequest
from schemas.responses import PredictionResponse, ErrorResponse, ModelStatusResponse
from core.logging import logger


# Create router
router = APIRouter(prefix="/api", tags=["predictions"])



@router.post("/predict/final-result", response_model=PredictionResponse, responses={500: {"model": ErrorResponse}})
async def predict_final_result(body: FinalResultRequest, request: Request):
    """
    Predict final result mahasiswa
    
    - **gender**: F atau M
    - **age_band**: 0-35, 35-55, atau 55<=
    - **studied_credits**: Jumlah kredit yang diambil
    - **num_of_prev_attempts**: Jumlah percobaan sebelumnya
    - **total_clicks**: Total clicks di VLE
    - **avg_assessment_score**: Rata-rata nilai assessment (0-100)
    """
    try:
        
        # Convert to dict for encoding (Pydantic model to dict)
        features = body.model_dump()
        
        # Encode features
        encoded_features = request.app.state.encoder_service.encode_finalgrade(features)
        
        # Predict
        prediction = request.app.state.predictor_service.predict_final_grade(encoded_features)
        
        return PredictionResponse(
            success=True,
            prediction=prediction,
            message="Final result predicted successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error predicting final result: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/predict/dropout", response_model=PredictionResponse, responses={500: {"model": ErrorResponse}})
async def predict_dropout(body: DropoutRequest, request: Request):
    """
    Predict apakah mahasiswa akan dropout
    
    - **code_module**: Kode modul (AAA-GGG)
    - **code_presentation**: Kode presentasi (2013B, 2013J, 2014B, 2014J)
    - **gender**: F atau M
    - **region**: Region mahasiswa
    - **highest_education**: Pendidikan tertinggi
    - **imd_band**: IMD band
    - **age_band**: 0-35, 35-55, atau 55<=
    - **num_of_prev_attempts**: Jumlah percobaan sebelumnya
    - **studied_credits**: Jumlah kredit yang diambil
    - **disability**: N atau Y
    """
    try:
        # Convert to dict for encoding (Pydantic model to dict)
        features = body.model_dump()
        
        # Encode features
        encoded_features = request.app.state.encoder_service.encode_dropout(features)
        
        # Predict
        prediction = request.app.state.predictor_service.predict_dropout(encoded_features)
        
        return PredictionResponse(
            success=True,
            prediction=prediction,
            message="Dropout predicted successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error predicting dropout: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/models/status", response_model=ModelStatusResponse)
async def get_models_status(request: Request):
    """Get status dari loaded models"""
    model_service = request.app.state.model_service
    
    return ModelStatusResponse(
        models_ready=model_service.dropout_model is not None and model_service.final_grade_model is not None,
        dropout_model_loaded=model_service.dropout_model is not None,
        final_grade_model_loaded=model_service.final_grade_model is not None,
        dropout_encoder_loaded=model_service.label_encoder_dropout is not None,
        finalgrade_encoder_loaded=model_service.label_encoder_finalgrade is not None,
    )
