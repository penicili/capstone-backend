"""
KPI Router untuk dashboard endpoints
"""
from fastapi import APIRouter, HTTPException, Request
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from core.logging import logger

router = APIRouter(prefix="/api/kpi", tags=["kpi"])


class KPIListResponse(BaseModel):
    """Response untuk list semua KPI"""
    success: bool = Field(..., description="Status keberhasilan")
    data: List[Dict[str, Any]] = Field(..., description="List of all KPI metrics")
    total_kpis: int = Field(..., description="Total jumlah KPI")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "data": [
                    {
                        "kpi_id": 1,
                        "name": "Login Frequency",
                        "definition": "Jumlah login dalam periode tertentu",
                        "value": 1500,
                        "unit": "logins",
                        "category": "engagement"
                    }
                ],
                "total_kpis": 12
            }
        }


class ErrorResponse(BaseModel):
    """Response untuk error"""
    success: bool = Field(default=False)
    error: str = Field(..., description="Pesan error")


@router.get("/metrics", response_model=KPIListResponse, responses={500: {"model": ErrorResponse}})
async def get_all_kpi_metrics(request: Request, refresh: bool = False):
    """
    Get all KPI metrics with caching support
    
    Query Parameters:
        - refresh: Force refresh cache (default: False)
    
    Returns list of 12 KPIs grouped by category:
    - engagement: Login Frequency, Active Learning Time, Material Access Rate, Course Engagement Score, Attendance Consistency
    - academic: Task Completion Ratio, Assignment Timeliness, Quiz Participation Rate, Grade Performance Index
    - risk: Low Activity Alert Index, Predicted Dropout Risk
    
    Frontend can iterate through the list with foreach and group by category
    
    Cache is automatically refreshed every 5 minutes, or can be manually refreshed with ?refresh=true
    """
    try:
        kpi_service = request.app.state.kpi_service
        kpis = kpi_service.get_all_kpis(force_refresh=refresh)
        
        return KPIListResponse(
            success=True,
            data=kpis,
            total_kpis=len(kpis)
        )
    except Exception as e:
        logger.exception(f"Error getting KPI metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cache/info")
async def get_cache_info(request: Request):
    """
    Get informasi status cache KPI
    
    Returns cache status: valid, timestamp, expiry, dll
    """
    try:
        kpi_service = request.app.state.kpi_service
        cache_info = kpi_service.get_cache_info()
        return {"success": True, "data": cache_info}
    except Exception as e:
        logger.exception(f"Error getting cache info: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cache/clear")
async def clear_cache(request: Request):
    """
    Manually clear KPI cache
    
    Use this to force refresh on next request
    """
    try:
        kpi_service = request.app.state.kpi_service
        kpi_service.clear_cache()
        return {"success": True, "message": "Cache cleared successfully"}
    except Exception as e:
        logger.exception(f"Error clearing cache: {e}")
        raise HTTPException(status_code=500, detail=str(e))
