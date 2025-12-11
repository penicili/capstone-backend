"""
KPI Service untuk dashboard analytics
OLAP queries untuk KPI metrics
"""
from typing import List, Dict, Any, Optional
from core.database import db
from core.logging import logger


class KPIService:
    """Service untuk KPI dashboard queries"""
    
    def get_all_kpis(self) -> List[Dict[str, Any]]:
        """
        Get semua KPI metrics overview
        
        Returns:
            List of KPI data dengan metrics
        """
        query = """
            SELECT 
                kpi_id,
                nama_kpi,
                deskripsi,
                tipe_kpi,
                satuan,
                target_value,
                current_value,
                persentase_tercapai,
                status,
                last_updated
            FROM kpi_metrics
            ORDER BY kpi_id
        """
        try:
            results = db.execute_query(query)
            logger.info(f"Retrieved {len(results)} KPIs")
            return results
        except Exception as e:
            logger.exception(f"Error getting KPIs: {e}")
            return []
    
    def get_student_performance_summary(self) -> Dict[str, Any]:
        """
        Get summary performa mahasiswa
        
        Returns:
            Dictionary dengan total students, avg score, dropout rate, dll
        """
        query = """
            SELECT 
                COUNT(*) as total_students,
                AVG(studied_credits) as avg_credits,
                SUM(CASE WHEN final_result = 'Pass' THEN 1 ELSE 0 END) as total_pass,
                SUM(CASE WHEN final_result = 'Fail' THEN 1 ELSE 0 END) as total_fail,
                SUM(CASE WHEN final_result = 'Withdrawn' THEN 1 ELSE 0 END) as total_withdrawn,
                SUM(CASE WHEN final_result = 'Distinction' THEN 1 ELSE 0 END) as total_distinction
            FROM studentinfo
        """
        try:
            result = db.execute_one(query)
            logger.info("Retrieved student performance summary")
            return result or {}
        except Exception as e:
            logger.exception(f"Error getting student performance: {e}")
            return {}
    
    def get_module_statistics(self) -> List[Dict[str, Any]]:
        """
        Get statistik per modul
        
        Returns:
            List of module stats (total students, avg score, pass rate per module)
        """
        query = """
            SELECT 
                code_module,
                code_presentation,
                COUNT(*) as total_students,
                SUM(CASE WHEN final_result IN ('Pass', 'Distinction') THEN 1 ELSE 0 END) as passed_students,
                ROUND(
                    (SUM(CASE WHEN final_result IN ('Pass', 'Distinction') THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 
                    2
                ) as pass_rate
            FROM studentinfo
            GROUP BY code_module, code_presentation
            ORDER BY code_module, code_presentation
        """
        try:
            results = db.execute_query(query)
            logger.info(f"Retrieved statistics for {len(results)} modules")
            return results
        except Exception as e:
            logger.exception(f"Error getting module statistics: {e}")
            return []
    
    def get_assessment_summary(self) -> List[Dict[str, Any]]:
        """
        Get summary assessment scores
        
        Returns:
            List of assessment averages per module
        """
        query = """
            SELECT 
                sa.code_module,
                sa.code_presentation,
                COUNT(DISTINCT sa.id_student) as total_students,
                AVG(sa.score) as avg_score,
                MIN(sa.score) as min_score,
                MAX(sa.score) as max_score
            FROM studentassessment sa
            GROUP BY sa.code_module, sa.code_presentation
            ORDER BY sa.code_module, sa.code_presentation
        """
        try:
            results = db.execute_query(query)
            logger.info(f"Retrieved assessment summary for {len(results)} modules")
            return results
        except Exception as e:
            logger.exception(f"Error getting assessment summary: {e}")
            return []
    
    def get_vle_engagement_summary(self) -> Dict[str, Any]:
        """
        Get summary engagement VLE (total clicks, avg clicks per student)
        
        Returns:
            Dictionary dengan VLE engagement metrics
        """
        query = """
            SELECT 
                COUNT(DISTINCT id_student) as total_active_students,
                SUM(sum_click) as total_clicks,
                AVG(sum_click) as avg_clicks_per_student,
                MAX(sum_click) as max_clicks,
                MIN(sum_click) as min_clicks
            FROM studentvle
        """
        try:
            result = db.execute_one(query)
            logger.info("Retrieved VLE engagement summary")
            return result or {}
        except Exception as e:
            logger.exception(f"Error getting VLE engagement: {e}")
            return {}
    
    def get_dashboard_overview(self) -> Dict[str, Any]:
        """
        Get complete dashboard overview dengan semua KPI metrics
        
        Returns:
            Dictionary dengan semua metrics untuk dashboard
        """
        try:
            overview = {
                "student_performance": self.get_student_performance_summary(),
                "vle_engagement": self.get_vle_engagement_summary(),
                "module_statistics": self.get_module_statistics(),
                "assessment_summary": self.get_assessment_summary()
            }
            logger.info("Retrieved complete dashboard overview")
            return overview
        except Exception as e:
            logger.exception(f"Error getting dashboard overview: {e}")
            return {}


# Global instance
kpi_service = KPIService()