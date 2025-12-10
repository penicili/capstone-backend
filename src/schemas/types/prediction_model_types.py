from typing import TypedDict

# Encoded types (sudah di-encode jadi numerik untuk model)
class DropoutFeaturesEncoded(TypedDict):
    """Features untuk dropout prediction (setelah encoding)"""
    code_module: int  # 0-6
    code_presentation: int  # 0-3
    gender: int  # 0-1
    region: int  # 0-12
    highest_education: int  # 0-4
    imd_band: int  # 0-10
    age_band: int  # 0-2
    num_of_prev_attempts: int
    studied_credits: int
    disability: int  # 0-1

class FinalResultFeaturesEncoded(TypedDict):
    """Features untuk final result prediction (setelah encoding)"""
    gender: int  # 0-1
    age_band: int  # 0-2
    studied_credits: int
    num_of_prev_attempts: int
    total_clicks: int
    avg_assessment_score: float