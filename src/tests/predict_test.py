"""
Test untuk prediction service
Test langsung lewat service tanpa API
"""
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

from services.model_service import model_service
from services.encoder_service import EncoderService
from services.predictor_service import PredictorService
from schemas.types.encoding_types import DropoutFeatures, FinalResultFeatures


class PredictionTest:
    """Test class untuk prediction services"""
    
    def __init__(self):
        """Initialize test dengan load models dan services"""
        print("\n" + "="*60)
        print("INITIALIZING PREDICTION TEST")
        print("="*60)
        
        # Load models
        print("\n1. Loading models...")
        model_service.load_models()
        print("✓ Models loaded")
        
        # Initialize services
        print("\n2. Initializing services...")
        self.encoder_service = EncoderService()
        self.predictor_service = PredictorService()
        print("✓ Services initialized")
    
    def test_final_result_prediction(self):
        """Test prediksi final result"""
        print("\n" + "="*60)
        print("TEST FINAL RESULT PREDICTION")
        print("="*60)
        
        # Prepare test data
        print("\n1. Preparing test data...")
        test_data: FinalResultFeatures = {
            "gender": "M",
            "age_band": "35-55",
            "studied_credits": 120,
            "num_of_prev_attempts": 0,
            "total_clicks": 1500,
            "avg_assessment_score": 75.5
        }
        print(f"Test data: {test_data}")
        
        # Encode features
        print("\n2. Encoding features...")
        encoded_data = self.encoder_service.encode_finalgrade(test_data)
        print(f"Encoded data: {encoded_data}")
        
        # Predict
        print("\n3. Predicting...")
        result = self.predictor_service.predict_final_grade(encoded_data)
        print(f"Prediction result: {result}")
        
        print("\n✓ Final result prediction test completed!")
        return result
    
    def test_dropout_prediction(self):
        """Test prediksi dropout"""
        print("\n" + "="*60)
        print("TEST DROPOUT PREDICTION")
        print("="*60)
        
        # Prepare test data
        print("\n1. Preparing test data...")
        test_data: DropoutFeatures = {
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
        print(f"Test data: {test_data}")
        
        # Encode features
        print("\n2. Encoding features...")
        encoded_data = self.encoder_service.encode_dropout(test_data)
        print(f"Encoded data: {encoded_data}")
        
        # Predict
        print("\n3. Predicting...")
        result = self.predictor_service.predict_dropout(encoded_data)
        print(f"Prediction result: {result}")
        
        print("\n✓ Dropout prediction test completed!")
        return result
    
    def run_all_tests(self):
        """Run semua test"""
        print("\n" + "="*60)
        print("RUNNING ALL PREDICTION TESTS")
        print("="*60)
        
        try:
            # Test 1: Final Result
            final_result = self.test_final_result_prediction()
            
            # Test 2: Dropout
            dropout_result = self.test_dropout_prediction()
            
            # Summary
            print("\n" + "="*60)
            print("TEST SUMMARY")
            print("="*60)
            print(f"✓ Final Result Prediction: {final_result}")
            print(f"✓ Dropout Prediction: {dropout_result}")
            print("="*60)
            
            return True
            
        except Exception as e:
            print(f"\n✗ TEST FAILED: {str(e)}")
            import traceback
            traceback.print_exc()
            return False


if __name__ == "__main__":
    test = PredictionTest()
    success = test.run_all_tests()
    sys.exit(0 if success else 1)
