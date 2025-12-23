from fastapi import APIRouter, HTTPException, Request
from typing import Optional, Any

from schemas.requests import FinalResultRequest, DropoutRequest
from schemas.responses import PredictionResponse, ErrorResponse, ModelStatusResponse
from core.logging import logger
from core.database import db


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


@router.post("/predict/dropout/{id}", response_model=PredictionResponse, responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def predict_dropout_by_student_id(id: int, request: Request):
    """
    Predict dropout berdasarkan ID mahasiswa dari database
    
    - **id**: ID mahasiswa (id_student) di database
    """
    try:
        # Query student data dari database
        query = """
            SELECT 
                si.code_module,
                si.code_presentation,
                si.gender,
                si.region,
                si.highest_education,
                si.imd_band,
                si.age_band,
                si.num_of_prev_attempts,
                si.studied_credits,
                si.disability
            FROM studentinfo si
            WHERE si.id_student = %s
            LIMIT 1
        """
        
        student_data = db.execute_one(query, (id,))
        
        if not student_data:
            raise HTTPException(
                status_code=404, 
                detail=f"Student with ID {id} not found in database"
            )
        
        logger.info(f"Fetched student data for ID {id}: {student_data}")
        
        # Convert disability dari integer ke string (N/Y)
        disability = 'Y' if student_data['disability'] == 1 else 'N'
        
        # Prepare features untuk prediction
        features = {
            "code_module": student_data['code_module'],
            "code_presentation": student_data['code_presentation'],
            "gender": student_data['gender'],
            "region": student_data['region'],
            "highest_education": student_data['highest_education'],
            "imd_band": student_data['imd_band'],
            "age_band": student_data['age_band'],
            "num_of_prev_attempts": int(student_data['num_of_prev_attempts']),
            "studied_credits": int(student_data['studied_credits']),
            "disability": disability
        }
        
        # Encode features
        encoded_features = request.app.state.encoder_service.encode_dropout(features)
        
        # Predict
        prediction = request.app.state.predictor_service.predict_dropout(encoded_features)
        
        return PredictionResponse(
            success=True,
            prediction=prediction,
            message=f"Dropout prediction for student ID {id} completed successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error predicting dropout for student ID {id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/predict/final-result/{id}", response_model=PredictionResponse, responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def predict_final_result_by_student_id(id: int, request: Request):
    """
    Predict final result berdasarkan ID mahasiswa dari database
    
    - **id**: ID mahasiswa (id_student) di database
    """
    try:
        # Query student data dan agregasi dari database
        query = """
            SELECT 
                si.gender,
                si.age_band,
                si.studied_credits,
                si.num_of_prev_attempts,
                COALESCE(SUM(sv.sum_click), 0) as total_clicks,
                COALESCE(AVG(sa.score), 0) as avg_assessment_score
            FROM studentinfo si
            LEFT JOIN studentvle sv ON si.id_student = sv.id_student 
                AND si.code_module = sv.code_module 
                AND si.code_presentation = sv.code_presentation
            LEFT JOIN studentassessment sa ON si.id_student = sa.id_student
            WHERE si.id_student = %s
            GROUP BY si.id_student, si.gender, si.age_band, si.studied_credits, si.num_of_prev_attempts
            LIMIT 1
        """
        
        student_data = db.execute_one(query, (id,))
        
        if not student_data:
            raise HTTPException(
                status_code=404, 
                detail=f"Student with ID {id} not found in database"
            )
        
        logger.info(f"Fetched student data for ID {id}: {student_data}")
        
        # Prepare features untuk prediction
        features = {
            "gender": student_data['gender'],
            "age_band": student_data['age_band'],
            "studied_credits": int(student_data['studied_credits']),
            "num_of_prev_attempts": int(student_data['num_of_prev_attempts']),
            "total_clicks": int(student_data['total_clicks']),
            "avg_assessment_score": float(student_data['avg_assessment_score'])
        }
        
        # Encode features
        encoded_features = request.app.state.encoder_service.encode_finalgrade(features)
        
        # Predict
        prediction = request.app.state.predictor_service.predict_final_grade(encoded_features)
        
        return PredictionResponse(
            success=True,
            prediction=prediction,
            message=f"Final result prediction for student ID {id} completed successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error predicting final result for student ID {id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))