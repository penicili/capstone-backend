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
    """Request body untuk dropout prediction"""
    code_module: str = Field(..., description="Kode modul (AAA-GGG)", pattern="^(AAA|BBB|CCC|DDD|EEE|FFF|GGG)$")
    code_presentation: str = Field(..., description="Kode presentasi", pattern="^(2013B|2013J|2014B|2014J)$")
    gender: str = Field(..., description="Gender mahasiswa (F/M)", pattern="^(F|M)$")
    region: str = Field(..., description="Region mahasiswa")
    highest_education: str = Field(..., description="Pendidikan tertinggi")
    imd_band: str = Field(..., description="IMD band")
    age_band: str = Field(..., description="Kelompok umur", pattern="^(0-35|35-55|55<=)$")
    num_of_prev_attempts: int = Field(..., ge=0, description="Jumlah percobaan sebelumnya")
    studied_credits: int = Field(..., ge=0, description="Jumlah kredit yang diambil")
    disability: str = Field(..., description="Status disabilitas (N/Y)", pattern="^(N|Y)$")

    class Config:
        json_schema_extra = {
            "example": {
                "code_module": "AAA",
                "code_presentation": "2013J",
                "gender": "F",
                "region": "East Anglian Region",
                "highest_education": "A Level or Equivalent",
                "imd_band": "30-40%",
                "age_band": "0-35",
                "num_of_prev_attempts": 0,
                "studied_credits": 60,
                "disability": "N"
            }
        }
