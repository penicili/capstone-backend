"""
KPI Service untuk dashboard analytics
OLAP queries untuk KPI metrics dengan Redis caching
"""
from typing import List, Dict, Any, Optional
from core.database import db
from core.logging import logger
from core.cache import cache
from config import settings
from schemas.types import DropoutFeatures
from fastapi import Request
from services.predictor_service import PredictorService
from services.encoder_service import EncoderService


class KPIService:
    """Service untuk KPI dashboard queries dengan Redis caching"""
    
    CACHE_KEY_ALL_KPIS = "kpi:all_metrics"
    
    def __init__(self, cache_ttl_seconds: int = 300, encoder_service: Optional[EncoderService] = None, predictor_service: Optional[PredictorService] = None):
        """
        Initialize KPI Service dengan cache configuration
        
        Args:
            cache_ttl_seconds: Cache Time To Live dalam detik (default: 300 = 5 menit)
            encoder_service: EncoderService instance (optional)
            predictor_service: PredictorService instance (optional)
        """
        self._cache_ttl = cache_ttl_seconds
        self._encoder_service = encoder_service
        self._predictor_service = predictor_service
        logger.info(f"KPIService initialized with cache TTL: {cache_ttl_seconds} seconds")
    
    @property
    def encoder_service(self) -> Optional[EncoderService]:
        """Lazy access to encoder_service."""
        return self._encoder_service
    
    @encoder_service.setter
    def encoder_service(self, value: Optional[EncoderService]):
        """Set encoder_service."""
        self._encoder_service = value
    
    @property
    def predictor_service(self) -> Optional[PredictorService]:
        """Lazy access to predictor_service."""
        return self._predictor_service
    
    @predictor_service.setter
    def predictor_service(self, value: Optional[PredictorService]):
        """Set predictor_service."""
        self._predictor_service = value
    
    def clear_cache(self) -> None:
        """Manually clear cache (untuk force refresh)"""
        cache.delete(self.CACHE_KEY_ALL_KPIS)
        logger.info("KPI cache cleared manually")
    
    def _calculate_forum_participation_score(self) -> Dict[str, Any]:
        """KPI 1: Forum Participation Score - Skor aktivitas diskusi"""
        logger.info("Calculating Forum Participation Score KPI")
        query = """
            SELECT 
                SUM(sv.sum_click) as total_forum_clicks,
                COUNT(DISTINCT sv.id_student) as active_students,
                ROUND(AVG(sv.sum_click), 2) as avg_clicks_per_activity
            FROM studentvle sv
        """
        try:
            result = db.execute_one(query)
            total_clicks = result.get('total_forum_clicks', 0) if result else 0
            active_students = result.get('active_students', 0) if result else 0
            
            return {
                "kpi_id": 1,
                "name": "Forum Participation Score",
                "definition": "Skor aktivitas diskusi",
                "value": total_clicks,
                "active_students": active_students,
                "avg_clicks_per_activity": result.get('avg_clicks_per_activity', 0) if result else 0,
                "unit": "clicks",
                "category": "engagement"
            }
        except Exception as e:
            logger.exception(f"Error calculating forum participation score: {e}")
            return {"kpi_id": 1, "name": "Forum Participation Score", "value": 0, "unit": "clicks", "category": "engagement"}
    
    def _calculate_task_completion_ratio(self) -> Dict[str, Any]:
        logger.info("Calculating Task Completion Ratio KPI")
        """KPI 2: Task Completion Ratio - Persentase assessment yang diselesaikan (score > 50)"""
        query = """
            SELECT 
                COUNT(CASE WHEN sa.score > 50 THEN 1 END) as completed_tasks,
                COUNT(*) as total_submissions,
                COUNT(DISTINCT sa.id_student) as participating_students
            FROM studentassessment sa
            WHERE sa.score IS NOT NULL
        """
        try:
            result = db.execute_one(query)
            completed = result.get('completed_tasks', 0) if result else 0
            total = result.get('total_submissions', 1) if result else 1
            completion_rate = round((completed / total) * 100, 2) if total > 0 else 0
            
            return {
                "kpi_id": 2,
                "name": "Task Completion Ratio",
                "definition": "Persentase assessment yang diselesaikan (>50)",
                "value": completion_rate,
                "completed_tasks": completed,
                "total_submissions": total,
                "participating_students": result.get('participating_students', 0) if result else 0,
                "unit": "percent",
                "category": "academic"
            }
        except Exception as e:
            logger.exception(f"Error calculating task completion ratio: {e}")
            return {"kpi_id": 2, "name": "Task Completion Ratio", "value": 0, "unit": "percent", "category": "academic"}
    
    def _calculate_assignment_timeliness(self) -> Dict[str, Any]:
        """KPI 3: Assignment Timeliness - Persentase tugas tepat waktu"""
        logger.info("Calculating Assignment Timeliness KPI")
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
                "kpi_id": 3,
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
            return {"kpi_id": 3, "name": "Assignment Timeliness", "value": 0, "unit": "percent", "category": "academic"}
    
    def _calculate_grade_performance_index(self) -> Dict[str, Any]:
        """KPI 4: Grade Performance Index - Rata-rata nilai tugas & kuis"""
        logger.info("Calculating Grade Performance Index KPI")
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
                "kpi_id": 4,
                "name": "Grade Performance Index",
                "definition": "Rata-rata nilai tugas & kuis",
                "value": avg_score,
                "min_score": result.get('min_score', 0) if result else 0,
                "max_score": result.get('max_score', 0) if result else 0,
                "total_students": result.get('total_students', 0) if result else 0,
                "total_assessments": result.get('total_assessments', 0) if result else 0,
                "unit": "score",
                "category": "academic"
            }
        except Exception as e:
            logger.exception(f"Error calculating grade performance index: {e}")
            return {"kpi_id": 4, "name": "Grade Performance Index", "value": 0, "unit": "score", "category": "academic"}
    
    def _calculate_low_activity_alert_index(self) -> Dict[str, Any]:
        """KPI 5: Low Activity Alert Index - Indeks risiko aktivitas rendah"""
        logger.info("Calculating Low Activity Alert Index KPI") 
        query = """
            SELECT 
                COUNT(CASE WHEN total_clicks < avg_clicks * 0.5 THEN 1 END) as low_activity_students,
                COUNT(*) as total_students,
                ROUND(AVG(total_clicks), 2) as avg_clicks
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
                "kpi_id": 5,
                "name": "Low Activity Alert Index",
                "definition": "Indeks risiko aktivitas rendah",
                "value": alert_index,
                "low_activity_students": low_activity,
                "total_students": total,
                "avg_clicks_threshold": result.get('avg_clicks', 0) if result else 0,
                "unit": "percent",
                "category": "risk"
            }
        except Exception as e:
            logger.exception(f"Error calculating low activity alert index: {e}")
            return {"kpi_id": 5, "name": "Low Activity Alert Index", "value": 0, "unit": "percent", "category": "risk"}
    
    def _calculate_predicted_dropout_risk(self) -> Dict[str, Any]:
        """KPI 6: Predicted Dropout Risk - Prediksi risiko dropout menggunakan ML model"""
        logger.info("Calculating Predicted Dropout Risk KPI using ML model")
        try:
            # 1. Ambil total student untuk sampling
            count_query = "SELECT COUNT(*) as total FROM studentinfo"
            count_result = db.execute_one(count_query)
            total_students = count_result.get('total', 0) if count_result else 0
            
            if total_students == 0:
                return {
                    "kpi_id": 6,
                    "name": "Predicted Dropout Risk",
                    "definition": "Prediksi risiko dropout menggunakan ML",
                    "value": 0,
                    "predicted_dropouts": 0,
                    "sampled_students": 0,
                    "unit": "percent",
                    "category": "risk"
                }
            
            # 2. Hitung jumlah sampel berdasarkan SAMPLE_SIZE
            sample_size = max(1, int(total_students * settings.SAMPLE_SIZE))
            logger.info(f"Getting sample size for dropout prediction: {sample_size}")
            
            # 3. Query untuk mengambil sample data student dengan fitur yang diperlukan
            # Menggunakan subquery untuk menghindari cartesian product
            sample_query = f"""
                SELECT 
                    si.id_student,
                    si.gender,
                    si.age_band,
                    si.studied_credits,
                    si.num_of_prev_attempts,
                    COALESCE(vle.total_clicks, 0) as total_clicks,
                    COALESCE(assess.avg_score, 0) as avg_assessment_score
                FROM studentinfo si
                LEFT JOIN (
                    SELECT id_student, SUM(sum_click) as total_clicks
                    FROM studentvle
                    GROUP BY id_student
                ) vle ON si.id_student = vle.id_student
                LEFT JOIN (
                    SELECT id_student, AVG(score) as avg_score
                    FROM studentassessment
                    WHERE score IS NOT NULL
                    GROUP BY id_student
                ) assess ON si.id_student = assess.id_student
                ORDER BY RAND()
                LIMIT {sample_size}
            """
            
            sample_data = db.execute_query(sample_query)
            logger.info(f"Sample data retrieved for dropout prediction: {len(sample_data)} students")
            
            if not sample_data:
                logger.warning("No sample data retrieved for dropout prediction")
                return {
                    "kpi_id": 6,
                    "name": "Predicted Dropout Risk",
                    "definition": "Prediksi risiko dropout menggunakan ML",
                    "value": 0,
                    "predicted_dropouts": 0,
                    "sampled_students": 0,
                    "unit": "percent",
                    "category": "risk"
                }
            
            
            # 5. Prediksi untuk setiap student dalam sample
            dropout_predictions = []
            logger.info(f"Predicting dropout risk for {len(sample_data)} students")
            
            # Check service availability
            if self.encoder_service is None or self.predictor_service is None:
                logger.error("EncoderService or PredictorService not available")
                return {
                    "kpi_id": 6,
                    "name": "Predicted Dropout Risk",
                    "definition": "Prediksi risiko dropout menggunakan ML",
                    "value": 0,
                    "predicted_dropouts": 0,
                    "sampled_students": 0,
                    "unit": "percent",
                    "category": "risk",
                    "error": "Services not available"
                }
            
            for student in sample_data:
                try:
                    # Prepare raw features (sama seperti di router.py)
                    raw_features: DropoutFeatures = {
                        'gender': student.get('gender', 'M'),
                        'age_band': student.get('age_band', '0-35'),
                        'studied_credits': int(student.get('studied_credits', 0)),
                        'num_of_prev_attempts': int(student.get('num_of_prev_attempts', 0)),
                        'total_clicks': int(student.get('total_clicks', 0)),
                        'avg_assessment_score': float(student.get('avg_assessment_score', 0))
                    }
                    
                    # Encode features (sama seperti di router.py)
                    encoded_features = self.encoder_service.encode_dropout(raw_features)
                    
                    # Predict (sama seperti di router.py)
                    prediction = self.predictor_service.predict_dropout(encoded_features)
                    dropout_predictions.append(prediction)
                    
                except Exception as e:
                    logger.warning(f"Error predicting for student {student.get('id_student')}: {e}")
                    continue
            
            # 6. Hitung persentase dropout (prediction = 1)
            if len(dropout_predictions) == 0:
                dropout_percentage = 0
                predicted_dropouts = 0
            else:
                predicted_dropouts = sum(1 for pred in dropout_predictions if pred == 1)
                dropout_percentage = round((predicted_dropouts / len(dropout_predictions)) * 100, 2)
            
            return {
                "kpi_id": 6,
                "name": "Predicted Dropout Risk",
                "definition": "Prediksi risiko dropout menggunakan ML",
                "value": dropout_percentage,
                "predicted_dropouts": predicted_dropouts,
                "sampled_students": len(dropout_predictions),
                "total_students": total_students,
                "sample_percentage": round((sample_size / total_students) * 100, 2),
                "unit": "percent",
                "category": "risk"
            }
            
        except Exception as e:
            logger.exception(f"Error calculating predicted dropout risk: {e}")
            return {
                "kpi_id": 6,
                "name": "Predicted Dropout Risk",
                "definition": "Prediksi risiko dropout menggunakan ML",
                "value": 0,
                "predicted_dropouts": 0,
                "sampled_students": 0,
                "unit": "percent",
                "category": "risk"
            }
    
    # KPI ini gak jelas, dibiarin aja tunggu pada nge fiks, gausah di serve ke API
    def _calculate_attendance_consistency_score(self) -> Dict[str, Any]:
        """KPI 7: Attendance Consistency Score - Konsistensi login mingguan"""
        logger.info("Calculating Attendance Consistency Score KPI")
        query = """
            SELECT 
                COUNT(DISTINCT id_student) as total_students,
                AVG(distinct_days) as avg_active_days,
                ROUND(STDDEV(distinct_days), 2) as std_deviation
            FROM (
                SELECT 
                    id_student,
                    COUNT(DISTINCT date) as distinct_days
                FROM studentvle
                GROUP BY id_student
            ) student_activity
        """
        try:
            result = db.execute_one(query)
            avg_days = round(result.get('avg_active_days', 0), 2) if result else 0
            std_dev = result.get('std_deviation', 0) if result else 0
            
            # Consistency score: semakin tinggi avg_days dan semakin rendah std_dev, semakin baik
            # Score normalisasi: avg_days / (1 + std_dev)
            consistency_score = round(avg_days / (1 + std_dev), 2) if std_dev is not None else avg_days
            
            return {
                "kpi_id": 7,
                "name": "Attendance Consistency Score",
                "definition": "Konsistensi login mingguan",
                "value": consistency_score,
                "avg_active_days": avg_days,
                "std_deviation": std_dev,
                "total_students": result.get('total_students', 0) if result else 0,
                "unit": "score",
                "category": "engagement"
            }
        except Exception as e:
            logger.exception(f"Error calculating attendance consistency score: {e}")
            return {"kpi_id": 7, "name": "Attendance Consistency Score", "value": 0, "unit": "score", "category": "engagement"}
    
    
    def get_all_kpis(self, force_refresh: bool = False) -> List[Dict[str, Any]]:
        """
        Get semua KPI metrics dengan Redis caching
        
        Args:
            force_refresh: Force refresh cache (ignore cache dan query database)
        
        Returns:
            List of 6 active KPI metrics (KPI 6 uses ML prediction)
        """
        # Check cache first (unless force_refresh)
        if not force_refresh:
            cached_kpis = cache.get(self.CACHE_KEY_ALL_KPIS)
            if cached_kpis is not None:
                logger.info("Returning KPIs from Redis cache")
                return cached_kpis
        
        # Cache miss atau force refresh - query database
        logger.info("Cache miss or force refresh - querying database for KPIs")
        try:
            kpis = [
                self._calculate_forum_participation_score(),
                self._calculate_task_completion_ratio(),
                self._calculate_assignment_timeliness(),
                self._calculate_grade_performance_index(),
                self._calculate_low_activity_alert_index(),
                self._calculate_predicted_dropout_risk(),
            ]
            
            # Store in Redis cache
            cache.set(self.CACHE_KEY_ALL_KPIS, kpis, self._cache_ttl)
            logger.info(f"Retrieved and cached {len(kpis)} KPIs with TTL {self._cache_ttl}s")
            return kpis
        except Exception as e:
            logger.exception(f"Error getting all KPIs: {e}")
            # Try to return stale cache if available
            cached_kpis = cache.get(self.CACHE_KEY_ALL_KPIS)
            if cached_kpis is not None:
                logger.warning("Database error, returning stale cache")
                return cached_kpis
            return []
    
    def get_cache_info(self) -> Dict[str, Any]:
        """Get informasi tentang status cache"""
        stats = cache.get_stats()
        return {
            **stats,
            "cache_ttl_seconds": self._cache_ttl,
            "cache_key": self.CACHE_KEY_ALL_KPIS,
        }