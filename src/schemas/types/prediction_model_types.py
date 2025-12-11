from typing import TypedDict

# Encoded types (sudah di-encode jadi numerik untuk model)
class DropoutFeaturesEncoded(TypedDict):
    """Features untuk dropout prediction (setelah encoding) - same as FinalResultFeaturesEncoded"""
    gender: int  # 0-1
    age_band: int  # 0-2
    studied_credits: int
    num_of_prev_attempts: int
    total_clicks: int
    avg_assessment_score: float

class FinalResultFeaturesEncoded(TypedDict):
    """Features untuk final result prediction (setelah encoding)"""
    gender: int  # 0-1
    age_band: int  # 0-2
    studied_credits: int
    num_of_prev_attempts: int
    total_clicks: int
    avg_assessment_score: float