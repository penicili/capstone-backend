"""
KPI Router untuk dashboard endpoints
"""
from fastapi import APIRouter, HTTPException, Request
from schemas.responses import (
    DashboardOverviewResponse,
    KPIResponse,
    ModuleStatisticsResponse,
    AssessmentSummaryResponse,
    ErrorResponse
)
from core.logging import logger

router = APIRouter(prefix="/api/kpi", tags=["kpi"])


@router.get("/overview", response_model=DashboardOverviewResponse, responses={500: {"model": ErrorResponse}})
async def get_dashboard_overview(request: Request):
    """Get complete dashboard overview dengan semua KPI metrics"""
    try:
        kpi_service = request.app.state.kpi_service
        overview = kpi_service.get_dashboard_overview()
        return DashboardOverviewResponse(
            success=True,
            data=overview
        )
    except Exception as e:
        logger.exception(f"Error getting dashboard overview: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/student-performance", response_model=KPIResponse, responses={500: {"model": ErrorResponse}})
async def get_student_performance(request: Request):
    """Get summary performa mahasiswa"""
    try:
        kpi_service = request.app.state.kpi_service
        data = kpi_service.get_student_performance_summary()
        return KPIResponse(
            success=True,
            data=data
        )
    except Exception as e:
        logger.exception(f"Error getting student performance: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/module-statistics", response_model=ModuleStatisticsResponse, responses={500: {"model": ErrorResponse}})
async def get_module_statistics(request: Request):
    """Get statistik per modul"""
    try:
        kpi_service = request.app.state.kpi_service
        data = kpi_service.get_module_statistics()
        return ModuleStatisticsResponse(
            success=True,
            data=data
        )
    except Exception as e:
        logger.exception(f"Error getting module statistics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/vle-engagement", response_model=KPIResponse, responses={500: {"model": ErrorResponse}})
async def get_vle_engagement(request: Request):
    """Get summary VLE engagement"""
    try:
        kpi_service = request.app.state.kpi_service
        data = kpi_service.get_vle_engagement_summary()
        return KPIResponse(
            success=True,
            data=data
        )
    except Exception as e:
        logger.exception(f"Error getting VLE engagement: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/assessment-summary", response_model=AssessmentSummaryResponse, responses={500: {"model": ErrorResponse}})
async def get_assessment_summary(request: Request):
    """Get summary assessment scores"""
    try:
        kpi_service = request.app.state.kpi_service
        data = kpi_service.get_assessment_summary()
        return AssessmentSummaryResponse(
            success=True,
            data=data
        )
    except Exception as e:
        logger.exception(f"Error getting assessment summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))
