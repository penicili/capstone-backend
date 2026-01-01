# Capstone Backend API

FastAPI backend for student performance prediction and KPI dashboard analytics.

## Overview

This API provides two main functionalities:
1. **Machine Learning Predictions**: Predict student final results and dropout probability
2. **KPI Dashboard**: OLAP queries for student performance analytics

## Tech Stack

- **Framework**: FastAPI
- **Database**: MySQL with PyMySQL
- **ML**: scikit-learn (RandomForest models)
- **Testing**: pytest, requests
- **Logging**: loguru

## Project Structure

```
src/
├── api/                    # API endpoints
│   ├── router.py          # Prediction endpoints
│   └── kpi_router.py      # KPI dashboard endpoints
├── services/              # Business logic
│   ├── model_service.py   # ML model loading
│   ├── encoder_service.py # Feature encoding
│   ├── predictor_service.py # Prediction logic
│   └── kpi_service.py     # KPI queries
├── schemas/               # Request/response models
│   ├── requests/          # Pydantic request schemas
│   ├── responses/         # Pydantic response schemas
│   └── types/             # TypedDict definitions
├── core/                  # Core utilities
│   ├── database.py        # Database connection
│   └── logging.py         # Logger setup
├── config/                # Configuration
│   └── settings.py        # App settings
└── app.py                 # FastAPI application
```

## Installation

### Prerequisites

- Python 3.12+
- MySQL Server
- Virtual environment (recommended)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd capstone-backend
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
# Windows
.\.venv\Scripts\Activate.ps1
# Linux/Mac
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure database in `src/config/settings.py`:
```python
DB_CONFIG = {
    "host": "localhost",
    "port": 3308,
    "user": "root",
    "password": "",
    "database": "capstone_kpi"
}
```

5. Place trained models in `src/ml/` directory:
- `dropout_model.pkl`
- `final_grade_model.pkl`
- `label_encoder_dropout.pkl`
- `label_encoder_finalgrade.pkl`

## Running the Application

Start the server:
```bash
python src/app.py
```

Server will be available at: `http://localhost:8000`

API Documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

## API Endpoints

### Health Check

**GET /** - Root endpoint  
**GET /health** - Health status with model readiness

### Prediction Endpoints

**POST /api/predict/final-result** - Predict student Final Result
```json
{
  "gender": "M",
  "age_band": "35-55",
  "studied_credits": 120,
  "num_of_prev_attempts": 0,
  "total_clicks": 1500,
  "avg_assessment_score": 75.5
}
```

**POST /api/predict/dropout** - Predict dropout probability
```json
{
  "gender": "F",
  "age_band": "0-35",
  "studied_credits": 60,
  "num_of_prev_attempts": 0,
  "total_clicks": 1500,
  "avg_assessment_score": 75.5
}
```

**GET /api/models/status** - Check model loading status

### KPI Dashboard Endpoints

**GET /api/kpi/overview** - Complete dashboard overview  
**GET /api/kpi/student-performance** - Student performance summary  
**GET /api/kpi/module-statistics** - Module-level statistics  
**GET /api/kpi/vle-engagement** - VLE engagement metrics  
**GET /api/kpi/assessment-summary** - Assessment score summary

## Machine Learning Models

### Feature Requirements

Both models use the same 6 features:
- `gender`: "M" or "F"
- `age_band`: "0-35", "35-55", or "55<="
- `studied_credits`: Integer
- `num_of_prev_attempts`: Integer
- `total_clicks`: Integer
- `avg_assessment_score`: Float

### Model Architecture

- **Algorithm**: RandomForestClassifier
- **Training**: scikit-learn 1.1.3
- **Runtime**: scikit-learn 1.5.2 (compatible)

### Feature Order

**Final Result Model:**
```python
[gender, age_band, studied_credits, num_of_prev_attempts, total_clicks, avg_assessment_score]
```

**Dropout Model:**
```python
[avg_assessment_score, total_clicks, studied_credits, num_of_prev_attempts, gender, age_band]
```

## Database Schema

Required tables in `capstone_kpi` database:
- `studentinfo` - Student demographics
- `studentassessment` - Assessment scores
- `assessments` - Assessment metadata
- `studentvle` - VLE interaction logs
- `vle` - VLE resources
- `courses` - Course information
- `studentregistration` - Registration data

## Testing

### Run All Tests
```bash
pytest
```

### HTTP Integration Tests
Ensure server is running, then:
```bash
python src/tests/http_request_test.py
```

### Debug Scripts
```bash
python src/tests/debug_encoders.py
python src/tests/debug_dropout.py
```

## Development

### Service Architecture

1. **ModelService**: Loads pickle files at startup
2. **EncoderService**: Encodes categorical features using LabelEncoders
3. **PredictorService**: Makes predictions with encoded features
4. **KPIService**: Executes OLAP queries without ORM

### Dependency Injection

Services are initialized in FastAPI lifespan and stored in `app.state`:
```python
app.state.model_service
app.state.encoder_service
app.state.predictor_service
app.state.kpi_service
```

### Error Handling

All endpoints return consistent error responses:
```json
{
  "success": false,
  "error": "Error message",
  "detail": "Additional details"
}
```

## CORS Configuration

CORS is enabled for all origins (development mode):
```python
allow_origins=["*"]
allow_methods=["*"]
allow_headers=["*"]
```

For production, restrict to specific origins.

## Export OpenAPI Schema

### Method 1: Download from running server
```bash
python download_openapi.py
```

### Method 2: Via curl
```bash
curl http://localhost:8000/openapi.json -o openapi.json
```

### Method 3: Browser
Navigate to `http://localhost:8000/openapi.json` and save the file.

## Troubleshooting

### Models not loading
- Check file paths in `src/services/model_service.py`
- Verify pickle files exist in `src/ml/`
- Check scikit-learn version compatibility

### Database connection failed
- Verify MySQL is running
- Check port and credentials in `src/config/settings.py`
- Ensure database `capstone_kpi` exists

### 404 on KPI endpoints
- Endpoints are at `/api/kpi/*` not `/kpi/*`
- Check router prefix configuration

### JSON serialization errors
- Ensure numpy types are converted to Python natives
- Check `int()` wrapping in encoder/predictor services

## Data Source

Dataset: [Student Demographics in Online Education (OULAD)](https://www.kaggle.com/datasets/anlgrbz/student-demographics-online-education-dataoulad/data)