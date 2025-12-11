"""
Debug dropout prediction
"""
import sys
sys.path.insert(0, 'src')

from services.model_service import model_service
from services.encoder_service import EncoderService
from services.predictor_service import PredictorService

# Load models
print("Loading models...")
model_service.load_models()
print("Models loaded!")

# Create services
encoder_service = EncoderService()
predictor_service = PredictorService()

# Test data
test_data = {
    "gender": "F",
    "age_band": "0-35",
    "studied_credits": 60,
    "num_of_prev_attempts": 0,
    "total_clicks": 1500,
    "avg_assessment_score": 75.5
}

print("\n" + "="*70)
print("Testing Dropout Prediction")
print("="*70)
print(f"Input: {test_data}")

try:
    # Encode
    print("\nEncoding features...")
    encoded = encoder_service.encode_dropout(test_data)
    print(f"Encoded: {encoded}")
    
    # Predict
    print("\nPredicting...")
    prediction = predictor_service.predict_dropout(encoded)
    print(f"Prediction: {prediction}")
    print("✓ Success!")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
