"""
Database connection management untuk MySQL
Menggunakan PyMySQL tanpa ORM
"""
import pymysql
from contextlib import contextmanager
from typing import Dict, List, Any, Optional
from config import settings
from core.logging import logger


class DatabaseConnection:
    """Database connection manager untuk MySQL"""
    
    def __init__(self):
        """Initialize database configuration"""
        self.config = {
            'host': settings.DB_HOST,
            'port': settings.DB_PORT,
            'user': settings.DB_USER,
            'password': settings.DB_PASSWORD,
            'database': settings.DB_NAME,
            'cursorclass': pymysql.cursors.DictCursor,
            'autocommit': True
        }
        logger.info(f"Database config initialized: {settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")
    
    @contextmanager
    def get_connection(self):
        """
        Context manager untuk mendapatkan database connection
        
        Usage:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM table")
        """
        connection = None
        try:
            connection = pymysql.connect(**self.config)
            logger.debug("Database connection opened")
            yield connection
        except pymysql.Error as e:
            logger.exception(f"Database connection error: {e}")
            raise
        finally:
            if connection:
                connection.close()
                logger.debug("Database connection closed")
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """
        Execute SELECT query dan return results
        
        Args:
            query: SQL query string
            params: Query parameters (optional)
            
        Returns:
            List of dictionaries (rows)
        """
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params or ())
                results = cursor.fetchall()
                logger.debug(f"Query executed: {cursor.rowcount} rows returned")
                return results
    
    def execute_one(self, query: str, params: Optional[tuple] = None) -> Optional[Dict[str, Any]]:
        """
        Execute SELECT query dan return single result
        
        Args:
            query: SQL query string
            params: Query parameters (optional)
            
        Returns:
            Single dictionary (row) or None
        """
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params or ())
                result = cursor.fetchone()
                logger.debug(f"Query executed: {'1 row' if result else 'no rows'} returned")
                return result
    
    def execute_write(self, query: str, params: Optional[tuple] = None) -> int:
        """
        Execute INSERT/UPDATE/DELETE query
        
        Args:
            query: SQL query string
            params: Query parameters (optional)
            
        Returns:
            Number of affected rows
        """
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params or ())
                conn.commit()
                affected_rows = cursor.rowcount
                logger.debug(f"Write query executed: {affected_rows} rows affected")
                return affected_rows
    
    def test_connection(self) -> bool:
        """
        Test database connection
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    result = cursor.fetchone()
                    logger.success("Database connection test successful")
                    return result is not None
        except Exception as e:
            logger.exception(f"Database connection test failed: {e}")
            return False


# Global instance
db = DatabaseConnection()