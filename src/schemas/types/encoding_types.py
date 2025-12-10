from typing import Literal, TypedDict

# Enums untuk categorical features (sebelum di-encode)
CodeModule = Literal["AAA", "BBB", "CCC", "DDD", "EEE", "FFF", "GGG"]
CodePresentation = Literal["2013B", "2013J", "2014B", "2014J"]
Gender = Literal["F", "M"]
Region = Literal[
    "East Anglian Region",
    "East Midlands Region", 
    "Ireland",
    "London Region",
    "North Region",
    "North Western Region",
    "Scotland",
    "South East Region",
    "South Region",
    "South West Region",
    "Wales",
    "West Midlands Region",
    "Yorkshire Region"
]
HighestEducation = Literal[
    "A Level or Equivalent",
    "HE Qualification",
    "Lower Than A Level",
    "No Formal quals",
    "Post Graduate Qualification"
]
IMDBand = Literal[
    "0-10%",
    "10-20",
    "20-30%",
    "30-40%",
    "40-50%",
    "50-60%",
    "60-70%",
    "70-80%",
    "80-90%",
    "90-100%",
    "Unknown"
]
AgeBand = Literal["0-35", "35-55", "55<="]
Disability = Literal["N", "Y"]
FinalResult = Literal["Distinction", "Fail", "Pass", "Withdrawn"]

# Raw input types (belum di-encode)
class DropoutFeatures:
    """Features untuk dropout prediction (sebelum encoding)"""
    code_module: CodeModule
    code_presentation: CodePresentation
    gender: Gender
    region: Region
    highest_education: HighestEducation
    imd_band: IMDBand
    age_band: AgeBand
    num_of_prev_attempts: int
    studied_credits: int
    disability: Disability

class FinalResultFeatures:
    """Features untuk final result prediction (sebelum encoding)"""
    gender: Gender
    highest_education: HighestEducation
    imd_band: IMDBand
    age_band: AgeBand
    num_of_prev_attempts: int
    studied_credits: int
    disability: Disability
    avg_assessment_score: float
    total_clicks: int

class DropoutEncodingFeature(TypedDict):
    pass

class FinalResultEncodingFeature(TypedDict):
    pass
