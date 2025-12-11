"""
Request schemas untuk prediction endpoints
"""
from pydantic import BaseModel, Field


class FinalResultRequest(BaseModel):
    """Request body untuk final result prediction"""
    gender: str = Field(..., description="Gender mahasiswa (F/M)", pattern="^(F|M)$")
    age_band: str = Field(..., description="Kelompok umur", pattern="^(0-35|35-55|55<=)$")
    studied_credits: int = Field(..., ge=0, description="Jumlah kredit yang diambil")
    num_of_prev_attempts: int = Field(..., ge=0, description="Jumlah percobaan sebelumnya")
    total_clicks: int = Field(..., ge=0, description="Total clicks di VLE")
    avg_assessment_score: float = Field(..., ge=0, le=100, description="Rata-rata nilai assessment")

    class Config:
        json_schema_extra = {
            "example": {
                "gender": "M",
                "age_band": "35-55",
                "studied_credits": 120,
                "num_of_prev_attempts": 0,
                "total_clicks": 1500,
                "avg_assessment_score": 75.5
            }
        }


class DropoutRequest(BaseModel):
    """Request body untuk dropout prediction (uses same 6 features as final_result)"""
    gender: str = Field(..., description="Gender mahasiswa (F/M)", pattern="^(F|M)$")
    age_band: str = Field(..., description="Kelompok umur", pattern="^(0-35|35-55|55<=)$")
    studied_credits: int = Field(..., ge=0, description="Jumlah kredit yang diambil")
    num_of_prev_attempts: int = Field(..., ge=0, description="Jumlah percobaan sebelumnya")
    total_clicks: int = Field(..., ge=0, description="Total clicks di VLE")
    avg_assessment_score: float = Field(..., ge=0, le=100, description="Rata-rata nilai assessment")

    class Config:
        json_schema_extra = {
            "example": {
                "gender": "F",
                "age_band": "0-35",
                "studied_credits": 60,
                "num_of_prev_attempts": 0,
                "total_clicks": 1200,
                "avg_assessment_score": 65.0
            }
        }
