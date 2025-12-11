"""
Response schemas untuk KPI endpoints
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class StudentPerformanceResponse(BaseModel):
    """Response untuk student performance summary"""
    total_students: int = Field(..., description="Total jumlah mahasiswa")
    avg_credits: float = Field(..., description="Rata-rata kredit yang diambil")
    total_pass: int = Field(..., description="Total mahasiswa Pass")
    total_fail: int = Field(..., description="Total mahasiswa Fail")
    total_withdrawn: int = Field(..., description="Total mahasiswa Withdrawn")
    total_distinction: int = Field(..., description="Total mahasiswa Distinction")

    class Config:
        json_schema_extra = {
            "example": {
                "total_students": 1000,
                "avg_credits": 45.5,
                "total_pass": 450,
                "total_fail": 200,
                "total_withdrawn": 250,
                "total_distinction": 100
            }
        }


class ModuleStatisticsItem(BaseModel):
    """Item untuk module statistics"""
    code_module: str = Field(..., description="Kode modul")
    code_presentation: str = Field(..., description="Kode presentasi")
    total_students: int = Field(..., description="Total mahasiswa di modul ini")
    passed_students: int = Field(..., description="Total mahasiswa yang lulus")
    pass_rate: float = Field(..., description="Persentase kelulusan")

    class Config:
        json_schema_extra = {
            "example": {
                "code_module": "AAA",
                "code_presentation": "2013J",
                "total_students": 100,
                "passed_students": 75,
                "pass_rate": 75.0
            }
        }


class ModuleStatisticsResponse(BaseModel):
    """Response untuk module statistics"""
    success: bool = Field(default=True, description="Status keberhasilan")
    data: List[ModuleStatisticsItem] = Field(..., description="List statistik per modul")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "data": [
                    {
                        "code_module": "AAA",
                        "code_presentation": "2013J",
                        "total_students": 100,
                        "passed_students": 75,
                        "pass_rate": 75.0
                    }
                ]
            }
        }


class VLEEngagementResponse(BaseModel):
    """Response untuk VLE engagement summary"""
    total_active_students: int = Field(..., description="Total mahasiswa aktif di VLE")
    total_clicks: int = Field(..., description="Total clicks di VLE")
    avg_clicks_per_student: float = Field(..., description="Rata-rata clicks per mahasiswa")
    max_clicks: int = Field(..., description="Maksimum clicks")
    min_clicks: int = Field(..., description="Minimum clicks")

    class Config:
        json_schema_extra = {
            "example": {
                "total_active_students": 1000,
                "total_clicks": 500000,
                "avg_clicks_per_student": 500.0,
                "max_clicks": 5000,
                "min_clicks": 10
            }
        }


class AssessmentSummaryItem(BaseModel):
    """Item untuk assessment summary"""
    code_module: str = Field(..., description="Kode modul")
    code_presentation: str = Field(..., description="Kode presentasi")
    total_students: int = Field(..., description="Total mahasiswa yang mengerjakan assessment")
    avg_score: float = Field(..., description="Rata-rata nilai assessment")
    min_score: float = Field(..., description="Nilai minimum")
    max_score: float = Field(..., description="Nilai maksimum")

    class Config:
        json_schema_extra = {
            "example": {
                "code_module": "AAA",
                "code_presentation": "2013J",
                "total_students": 95,
                "avg_score": 75.5,
                "min_score": 20.0,
                "max_score": 100.0
            }
        }


class AssessmentSummaryResponse(BaseModel):
    """Response untuk assessment summary"""
    success: bool = Field(default=True, description="Status keberhasilan")
    data: List[AssessmentSummaryItem] = Field(..., description="List summary assessment per modul")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "data": [
                    {
                        "code_module": "AAA",
                        "code_presentation": "2013J",
                        "total_students": 95,
                        "avg_score": 75.5,
                        "min_score": 20.0,
                        "max_score": 100.0
                    }
                ]
            }
        }


class DashboardOverviewResponse(BaseModel):
    """Response untuk dashboard overview"""
    success: bool = Field(default=True, description="Status keberhasilan")
    data: Dict[str, Any] = Field(..., description="Dashboard data dengan semua metrics")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "data": {
                    "student_performance": {
                        "total_students": 1000,
                        "avg_credits": 45.5,
                        "total_pass": 450,
                        "total_fail": 200,
                        "total_withdrawn": 250,
                        "total_distinction": 100
                    },
                    "vle_engagement": {
                        "total_active_students": 1000,
                        "total_clicks": 500000,
                        "avg_clicks_per_student": 500.0,
                        "max_clicks": 5000,
                        "min_clicks": 10
                    },
                    "module_statistics": [],
                    "assessment_summary": []
                }
            }
        }


class KPIResponse(BaseModel):
    """Generic response untuk KPI endpoints"""
    success: bool = Field(default=True, description="Status keberhasilan")
    data: Any = Field(..., description="Data KPI")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "data": {}
            }
        }
