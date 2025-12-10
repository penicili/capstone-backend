"""
Model service buat loading model dan encoding
"""


class ModelService:
    """Service untuk mengelola ML models dan predictions"""
    
    def __init__(self):
        """Initialize model service"""
        self.models = {}
        
    def load_models(self):
        """Load semua ML models"""
        pass
    
    def is_ready(self):
        """Check apakah models sudah di-load"""
        return False


# Global instance
model_service = ModelService()