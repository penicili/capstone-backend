"""
Debug script untuk check struktur encoder files
"""
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

import pickle
from config import settings

print("="*70)
print("ENCODER FILES DEBUG")
print("="*70)

print(f"\nFinal Grade Encoder Path: {settings.LABEL_ENCODER_FINALGRADE_PATH}")
print(f"Dropout Encoder Path: {settings.LABEL_ENCODER_DROPOUT_PATH}")

# Load final grade encoder
print("\n" + "="*70)
print("FINAL GRADE ENCODER")
print("="*70)
with open(settings.LABEL_ENCODER_FINALGRADE_PATH, 'rb') as f:
    finalgrade_encoder = pickle.load(f)
    print(f"Type: {type(finalgrade_encoder)}")
    print(f"Value: {finalgrade_encoder}")
    
    if isinstance(finalgrade_encoder, dict):
        print("\n✓ It's a DICTIONARY!")
        print(f"Keys: {list(finalgrade_encoder.keys())}")
        for key, value in finalgrade_encoder.items():
            print(f"  {key}: {type(value)}")
            if hasattr(value, 'classes_'):
                print(f"    Classes: {value.classes_[:5]}...")  # First 5 classes
    else:
        print("\n✓ It's a single object")
        if hasattr(finalgrade_encoder, 'classes_'):
            print(f"Classes: {finalgrade_encoder.classes_}")

# Load dropout encoder
print("\n" + "="*70)
print("DROPOUT ENCODER")
print("="*70)
with open(settings.LABEL_ENCODER_DROPOUT_PATH, 'rb') as f:
    dropout_encoder = pickle.load(f)
    print(f"Type: {type(dropout_encoder)}")
    print(f"Value: {dropout_encoder}")
    
    if isinstance(dropout_encoder, dict):
        print("\n✓ It's a DICTIONARY!")
        print(f"Keys: {list(dropout_encoder.keys())}")
        for key, value in dropout_encoder.items():
            print(f"  {key}: {type(value)}")
            if hasattr(value, 'classes_'):
                print(f"    Classes: {value.classes_[:10]}...")  # First 10 classes
    else:
        print("\n✓ It's a single object")
        if hasattr(dropout_encoder, 'classes_'):
            print(f"Classes: {dropout_encoder.classes_}")

print("\n" + "="*70)
