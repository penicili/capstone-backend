"""
KPI Service untuk dashboard analytics
OLAP queries untuk KPI metrics
"""
from typing import List, Dict, Any, Optional
from core.database import db
from core.logging import logger


class KPIService:
    """Service untuk KPI dashboard queries"""
    
    def _calculate_login_frequency(self) -> Dict[str, Any]:
        """KPI 1: Login Frequency - Jumlah login dalam periode tertentu"""
        query = """
            SELECT 
                COUNT(DISTINCT id_student) as total_active_students,
                COUNT(*) as total_logins,
                ROUND(COUNT(*) * 1.0 / COUNT(DISTINCT id_student), 2) as avg_login_per_student
            FROM studentvle
        """
        try:
            result = db.execute_one(query)
            return {
                "kpi_id": 1,
                "name": "Login Frequency",
                "definition": "Jumlah login dalam periode tertentu",
                "value": result.get('total_logins', 0) if result else 0,
                "avg_per_student": result.get('avg_login_per_student', 0) if result else 0,
                "unit": "logins",
                "category": "engagement"
            }
        except Exception as e:
            logger.exception(f"Error calculating login frequency: {e}")
            return {"kpi_id": 1, "name": "Login Frequency", "value": 0, "unit": "logins", "category": "engagement"}
    
    def _calculate_active_learning_time(self) -> Dict[str, Any]:
        """KPI 2: Active Learning Time - Total durasi mahasiswa aktif di LMS"""
        query = """
            SELECT 
                COUNT(DISTINCT id_student) as total_students,
                SUM(sum_click) as total_clicks,
                ROUND(AVG(sum_click), 2) as avg_clicks_per_student
            FROM studentvle
        """
        try:
            result = db.execute_one(query)
            # Estimasi: 1 click ≈ 2 menit waktu aktif
            total_minutes = (result.get('total_clicks', 0) * 2) if result else 0
            return {
                "kpi_id": 2,
                "name": "Active Learning Time",
                "definition": "Total durasi mahasiswa aktif di LMS",
                "value": total_minutes,
                "avg_per_student": round(total_minutes / result.get('total_students', 1), 2) if result and result.get('total_students') else 0,
                "unit": "minutes",
                "category": "engagement"
            }
        except Exception as e:
            logger.exception(f"Error calculating active learning time: {e}")
            return {"kpi_id": 2, "name": "Active Learning Time", "value": 0, "unit": "minutes", "category": "engagement"}
    
    def _calculate_material_access_rate(self) -> Dict[str, Any]:
        """KPI 3: Material Access Rate - Persentase materi yang diakses"""
        query = """
            SELECT 
                COUNT(DISTINCT CONCAT(sv.id_student, '-', sv.id_site)) as materials_accessed,
                COUNT(DISTINCT sv.id_site) as total_materials,
                COUNT(DISTINCT sv.id_student) as active_students
            FROM studentvle sv
        """
        try:
            result = db.execute_one(query)
            materials_accessed = result.get('materials_accessed', 0) if result else 0
            total_materials = result.get('total_materials', 1) if result else 1
            access_rate = round((materials_accessed / total_materials) * 100, 2) if total_materials > 0 else 0
            return {
                "kpi_id": 3,
                "name": "Material Access Rate",
                "definition": "Persentase materi yang diakses",
                "value": access_rate,
                "materials_accessed": materials_accessed,
                "total_materials": total_materials,
                "unit": "percent",
                "category": "engagement"
            }
        except Exception as e:
            logger.exception(f"Error calculating material access rate: {e}")
            return {"kpi_id": 3, "name": "Material Access Rate", "value": 0, "unit": "percent", "category": "engagement"}
    
    def _calculate_task_completion_ratio(self) -> Dict[str, Any]:
        """KPI 5: Task Completion Ratio - Persentase tugas yang diselesaikan"""
        query = """
            SELECT 
                COUNT(DISTINCT CASE WHEN sa.score IS NOT NULL THEN CONCAT(sa.id_student, '-', sa.id_assessment) END) as completed_tasks,
                COUNT(DISTINCT a.id_assessment) * COUNT(DISTINCT sa.id_student) as total_possible_tasks,
                COUNT(DISTINCT sa.id_student) as participating_students
            FROM studentassessment sa
            JOIN assessments a ON sa.id_assessment = a.id_assessment
            WHERE a.assessment_type IN ('TMA', 'CMA')
        """
        try:
            result = db.execute_one(query)
            completed = result.get('completed_tasks', 0) if result else 0
            total = result.get('total_possible_tasks', 1) if result else 1
            completion_rate = round((completed / total) * 100, 2) if total > 0 else 0
            return {
                "kpi_id": 5,
                "name": "Task Completion Ratio",
                "definition": "Persentase tugas yang diselesaikan",
                "value": completion_rate,
                "completed_tasks": completed,
                "total_tasks": total,
                "unit": "percent",
                "category": "academic"
            }
        except Exception as e:
            logger.exception(f"Error calculating task completion ratio: {e}")
            return {"kpi_id": 5, "name": "Task Completion Ratio", "value": 0, "unit": "percent", "category": "academic"}
    
    def _calculate_assignment_timeliness(self) -> Dict[str, Any]:
        """KPI 6: Assignment Timeliness - Persentase tugas tepat waktu"""
        query = """
            SELECT 
                COUNT(CASE WHEN sa.date_submitted <= a.date THEN 1 END) as on_time_submissions,
                COUNT(*) as total_submissions
            FROM studentassessment sa
            JOIN assessments a ON sa.id_assessment = a.id_assessment
            WHERE sa.date_submitted IS NOT NULL AND a.date IS NOT NULL
        """
        try:
            result = db.execute_one(query)
            on_time = result.get('on_time_submissions', 0) if result else 0
            total = result.get('total_submissions', 1) if result else 1
            timeliness_rate = round((on_time / total) * 100, 2) if total > 0 else 0
            return {
                "kpi_id": 6,
                "name": "Assignment Timeliness",
                "definition": "Persentase tugas tepat waktu",
                "value": timeliness_rate,
                "on_time_submissions": on_time,
                "total_submissions": total,
                "unit": "percent",
                "category": "academic"
            }
        except Exception as e:
            logger.exception(f"Error calculating assignment timeliness: {e}")
            return {"kpi_id": 6, "name": "Assignment Timeliness", "value": 0, "unit": "percent", "category": "academic"}
    
    def _calculate_quiz_participation_rate(self) -> Dict[str, Any]:
        """KPI 7: Quiz/Exam Participation Rate - Partisipasi kuis/ujian"""
        query = """
            SELECT 
                COUNT(DISTINCT CASE WHEN sa.score IS NOT NULL THEN CONCAT(sa.id_student, '-', sa.id_assessment) END) as participated,
                COUNT(DISTINCT a.id_assessment) * COUNT(DISTINCT sa.id_student) as total_possible,
                COUNT(DISTINCT sa.id_student) as total_students
            FROM studentassessment sa
            JOIN assessments a ON sa.id_assessment = a.id_assessment
            WHERE a.assessment_type = 'Exam'
        """
        try:
            result = db.execute_one(query)
            participated = result.get('participated', 0) if result else 0
            total = result.get('total_possible', 1) if result else 1
            participation_rate = round((participated / total) * 100, 2) if total > 0 else 0
            return {
                "kpi_id": 7,
                "name": "Quiz/Exam Participation Rate",
                "definition": "Partisipasi kuis/ujian",
                "value": participation_rate,
                "participated": participated,
                "total_possible": total,
                "unit": "percent",
                "category": "academic"
            }
        except Exception as e:
            logger.exception(f"Error calculating quiz participation rate: {e}")
            return {"kpi_id": 7, "name": "Quiz/Exam Participation Rate", "value": 0, "unit": "percent", "category": "academic"}
    
    def _calculate_grade_performance_index(self) -> Dict[str, Any]:
        """KPI 8: Grade Performance Index - Rata-rata nilai tugas & kuis"""
        query = """
            SELECT 
                AVG(sa.score) as avg_score,
                MIN(sa.score) as min_score,
                MAX(sa.score) as max_score,
                COUNT(DISTINCT sa.id_student) as total_students,
                COUNT(*) as total_assessments
            FROM studentassessment sa
            WHERE sa.score IS NOT NULL
        """
        try:
            result = db.execute_one(query)
            avg_score = round(result.get('avg_score', 0), 2) if result else 0
            return {
                "kpi_id": 8,
                "name": "Grade Performance Index",
                "definition": "Rata-rata nilai tugas & kuis",
                "value": avg_score,
                "min_score": result.get('min_score', 0) if result else 0,
                "max_score": result.get('max_score', 0) if result else 0,
                "total_assessments": result.get('total_assessments', 0) if result else 0,
                "unit": "score",
                "category": "academic"
            }
        except Exception as e:
            logger.exception(f"Error calculating grade performance index: {e}")
            return {"kpi_id": 8, "name": "Grade Performance Index", "value": 0, "unit": "score", "category": "academic"}
    
    def _calculate_course_engagement_score(self) -> Dict[str, Any]:
        """KPI 9: Course Engagement Score - Skor gabungan aktivitas mahasiswa"""
        # Gabungkan berbagai metrik: VLE clicks, assessment participation, material access
        query_vle = "SELECT AVG(sum_click) as avg_clicks FROM studentvle"
        query_assessment = "SELECT COUNT(*) * 100.0 / (SELECT COUNT(DISTINCT id_student) FROM studentinfo) as participation FROM studentassessment"
        
        try:
            vle_result = db.execute_one(query_vle)
            assessment_result = db.execute_one(query_assessment)
            
            # Weighted score: 40% VLE, 60% Assessment
            avg_clicks = float(vle_result.get('avg_clicks', 0)) if vle_result else 0
            vle_score = avg_clicks / 10  # Normalize clicks
            assessment_score = float(assessment_result.get('participation', 0)) if assessment_result else 0
            
            engagement_score = round((vle_score * 0.4 + assessment_score * 0.6), 2)
            
            return {
                "kpi_id": 9,
                "name": "Course Engagement Score",
                "definition": "Skor gabungan aktivitas mahasiswa",
                "value": engagement_score,
                "vle_component": round(vle_score, 2),
                "assessment_component": round(assessment_score, 2),
                "unit": "score",
                "category": "engagement"
            }
        except Exception as e:
            logger.exception(f"Error calculating course engagement score: {e}")
            return {"kpi_id": 9, "name": "Course Engagement Score", "value": 0, "unit": "score", "category": "engagement"}
    
    def _calculate_low_activity_alert_index(self) -> Dict[str, Any]:
        """KPI 10: Low Activity Alert Index - Indeks risiko aktivitas rendah"""
        query = """
            SELECT 
                COUNT(CASE WHEN total_clicks < avg_clicks * 0.5 THEN 1 END) as low_activity_students,
                COUNT(*) as total_students,
                AVG(total_clicks) as avg_clicks
            FROM (
                SELECT 
                    sv.id_student,
                    SUM(sv.sum_click) as total_clicks,
                    (SELECT AVG(sum_click_total) FROM (
                        SELECT SUM(sum_click) as sum_click_total 
                        FROM studentvle 
                        GROUP BY id_student
                    ) as student_totals) as avg_clicks
                FROM studentvle sv
                GROUP BY sv.id_student
            ) student_activity
        """
        try:
            result = db.execute_one(query)
            low_activity = result.get('low_activity_students', 0) if result else 0
            total = result.get('total_students', 1) if result else 1
            alert_index = round((low_activity / total) * 100, 2) if total > 0 else 0
            
            return {
                "kpi_id": 10,
                "name": "Low Activity Alert Index",
                "definition": "Indeks risiko aktivitas rendah",
                "value": alert_index,
                "low_activity_students": low_activity,
                "total_students": total,
                "unit": "percent",
                "category": "risk"
            }
        except Exception as e:
            logger.exception(f"Error calculating low activity alert index: {e}")
            return {"kpi_id": 10, "name": "Low Activity Alert Index", "value": 0, "unit": "percent", "category": "risk"}
    
    def _calculate_predicted_dropout_risk(self) -> Dict[str, Any]:
        """KPI 11: Predicted Dropout Risk - Prediksi risiko dropout"""
        query = """
            SELECT 
                COUNT(CASE WHEN final_result = 'Withdrawn' THEN 1 END) as withdrawn_students,
                COUNT(*) as total_students
            FROM studentinfo
        """
        try:
            result = db.execute_one(query)
            withdrawn = result.get('withdrawn_students', 0) if result else 0
            total = result.get('total_students', 1) if result else 1
            dropout_rate = round((withdrawn / total) * 100, 2) if total > 0 else 0
            
            return {
                "kpi_id": 11,
                "name": "Predicted Dropout Risk",
                "definition": "Prediksi risiko dropout",
                "value": dropout_rate,
                "withdrawn_students": withdrawn,
                "total_students": total,
                "unit": "percent",
                "category": "risk"
            }
        except Exception as e:
            logger.exception(f"Error calculating predicted dropout risk: {e}")
            return {"kpi_id": 11, "name": "Predicted Dropout Risk", "value": 0, "unit": "percent", "category": "risk"}
    
    def _calculate_attendance_consistency_score(self) -> Dict[str, Any]:
        """KPI 12: Attendance Consistency Score - Konsistensi login mingguan"""
        query = """
            SELECT 
                id_student,
                COUNT(DISTINCT CONCAT(code_module, '-', code_presentation, '-', date)) as distinct_days,
                SUM(sum_click) as total_clicks
            FROM studentvle
            GROUP BY id_student
        """
        try:
            results = db.execute_query(query)
            if not results:
                return {"kpi_id": 12, "name": "Attendance Consistency Score", "value": 0, "unit": "score", "category": "engagement"}
            
            # Calculate variance/consistency (lower variance = higher consistency)
            days_list = [r.get('distinct_days', 0) for r in results]
            avg_days = sum(days_list) / len(days_list) if days_list else 0
            consistency_score = round(avg_days, 2)
            
            return {
                "kpi_id": 12,
                "name": "Attendance Consistency Score",
                "definition": "Konsistensi login mingguan",
                "value": consistency_score,
                "avg_active_days": consistency_score,
                "total_students": len(results),
                "unit": "days",
                "category": "engagement"
            }
        except Exception as e:
            logger.exception(f"Error calculating attendance consistency score: {e}")
            return {"kpi_id": 12, "name": "Attendance Consistency Score", "value": 0, "unit": "days", "category": "engagement"}
    
    def get_all_kpis(self) -> List[Dict[str, Any]]:
        """
        Get semua KPI metrics dalam satu endpoint
        
        Returns:
            List of all 12 KPI metrics
        """
        try:
            kpis = [
                self._calculate_login_frequency(),
                self._calculate_active_learning_time(),
                self._calculate_material_access_rate(),
                self._calculate_task_completion_ratio(),
                self._calculate_assignment_timeliness(),
                self._calculate_quiz_participation_rate(),
                self._calculate_grade_performance_index(),
                self._calculate_course_engagement_score(),
                self._calculate_low_activity_alert_index(),
                self._calculate_predicted_dropout_risk(),
                self._calculate_attendance_consistency_score()
            ]
            logger.info(f"Retrieved {len(kpis)} KPIs")
            return kpis
        except Exception as e:
            logger.exception(f"Error getting all KPIs: {e}")
            return []


# Global instance
kpi_service = KPIService()