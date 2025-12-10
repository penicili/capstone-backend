from typing import TypedDict, Literal
from datetime import date


# belom fix, tipedatanya masih ngasal, nunggu info dari yang buat model
# TODO: Update Types dengan Literal enum yang sesuai dengan kolom model dan tipe data yang sesuai

# TODO: anu encoder
class DropoutFeatures(TypedDict):
    code_module: str
    code_presentation: str
    gender: Literal['M', 'F']
    region: str
    highest_education: str
    imd_band: str
    age_band: str
    num_of_prev_attempts: int
    studied_credits: int
    disability: Literal['Y', 'N']
    avg_assessment_score: float
    total_clicks: int
    date_registration: date
    has_unregistered: Literal[0, 1]
    
class FinalResultFeatures(TypedDict):
    gender: Literal['M', 'F']
    highest_education: str
    imd_band: str
    age_band: str
    num_of_prev_attempts: int
    studied_credits: int
    disability: Literal['Y', 'N']
    avg_assessment_score: float
    total_clicks: int
    
