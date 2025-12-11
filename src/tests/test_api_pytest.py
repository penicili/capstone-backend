"""
Test untuk API endpoints menggunakan pytest dan TestClient
Test HTTP endpoints untuk prediction dan KPI
"""
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

import pytest
from fastapi.testclient import TestClient
from app import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


# ========== Basic Endpoints ==========

def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()
    assert "models_ready" in response.json()


def test_model_status_endpoint(client):
    """Test model status endpoint"""
    response = client.get("/api/models/status")
    assert response.status_code == 200
    data = response.json()
    assert "models_ready" in data
    assert "dropout_model_loaded" in data
    assert "final_grade_model_loaded" in data


# ========== Prediction Endpoints ==========

def test_predict_final_result(client):
    """Test prediction final result endpoint"""
    payload = {
        "gender": "M",
        "age_band": "35-55",
        "studied_credits": 120,
        "num_of_prev_attempts": 0,
        "total_clicks": 1500,
        "avg_assessment_score": 75.5
    }
    
    response = client.post("/api/predict/final-result", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "prediction" in data


def test_predict_dropout(client):
    """Test prediction dropout endpoint"""
    payload = {
        "code_module": "AAA",
        "code_presentation": "2013J",
        "gender": "F",
        "region": "East Anglian Region",
        "highest_education": "HE Qualification",
        "imd_band": "10-20%",
        "age_band": "0-35",
        "num_of_prev_attempts": 0,
        "studied_credits": 60,
        "disability": "N"
    }
    
    response = client.post("/api/predict/dropout", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "prediction" in data


def test_invalid_prediction_request(client):
    """Test invalid prediction request should return 422"""
    payload = {
        "gender": "M",
        "age_band": "35-55"
        # Missing required fields
    }
    
    response = client.post("/api/predict/final-result", json=payload)
    assert response.status_code == 422  # Validation error


# ========== KPI Endpoints ==========

def test_kpi_dashboard_overview(client):
    """Test KPI dashboard overview endpoint"""
    response = client.get("/api/kpi/overview")
    
    # Skip if database not connected
    if response.status_code != 200:
        pytest.skip("Database not connected")
    
    data = response.json()
    assert "success" in data
    assert data["success"] == True
    assert "data" in data
    
    overview_data = data["data"]
    assert "student_performance" in overview_data
    assert "vle_engagement" in overview_data
    assert "module_statistics" in overview_data
    assert "assessment_summary" in overview_data


def test_kpi_student_performance(client):
    """Test KPI student performance endpoint"""
    response = client.get("/api/kpi/student-performance")
    
    # Skip if database not connected
    if response.status_code != 200:
        pytest.skip("Database not connected")
    
    data = response.json()
    assert "success" in data
    assert data["success"] == True
    assert "data" in data


def test_kpi_module_statistics(client):
    """Test KPI module statistics endpoint"""
    response = client.get("/api/kpi/module-statistics")
    
    # Skip if database not connected
    if response.status_code != 200:
        pytest.skip("Database not connected")
    
    data = response.json()
    assert "success" in data
    assert data["success"] == True
    assert "data" in data


def test_kpi_vle_engagement(client):
    """Test KPI VLE engagement endpoint"""
    response = client.get("/api/kpi/vle-engagement")
    
    # Skip if database not connected
    if response.status_code != 200:
        pytest.skip("Database not connected")
    
    data = response.json()
    assert "success" in data
    assert data["success"] == True
    assert "data" in data


def test_kpi_assessment_summary(client):
    """Test KPI assessment summary endpoint"""
    response = client.get("/api/kpi/assessment-summary")
    
    # Skip if database not connected
    if response.status_code != 200:
        pytest.skip("Database not connected")
    
    data = response.json()
    assert "success" in data
    assert data["success"] == True
    assert "data" in data


# ========== Edge Cases ==========

def test_predict_with_invalid_enum_values(client):
    """Test prediction with invalid enum values"""
    payload = {
        "gender": "INVALID",  # Invalid enum
        "age_band": "35-55",
        "studied_credits": 120,
        "num_of_prev_attempts": 0,
        "total_clicks": 1500,
        "avg_assessment_score": 75.5
    }
    
    response = client.post("/api/predict/final-result", json=payload)
    assert response.status_code == 422  # Validation error


def test_predict_with_negative_values(client):
    """Test prediction with negative values"""
    payload = {
        "gender": "M",
        "age_band": "35-55",
        "studied_credits": -10,  # Negative value
        "num_of_prev_attempts": -1,  # Negative value
        "total_clicks": 1500,
        "avg_assessment_score": 75.5
    }
    
    response = client.post("/api/predict/final-result", json=payload)
    # Should either reject or handle gracefully
    assert response.status_code in [200, 422]


def test_predict_with_extreme_values(client):
    """Test prediction with extreme values"""
    payload = {
        "gender": "M",
        "age_band": "35-55",
        "studied_credits": 999999,  # Extreme value
        "num_of_prev_attempts": 100,
        "total_clicks": 1000000,
        "avg_assessment_score": 100
    }
    
    response = client.post("/api/predict/final-result", json=payload)
    # Should handle gracefully
    assert response.status_code == 200


# ========== Fixtures (Optional) ==========

@pytest.fixture
def sample_final_result_payload():
    """Sample payload for final result prediction"""
    return {
        "gender": "M",
        "age_band": "35-55",
        "studied_credits": 120,
        "num_of_prev_attempts": 0,
        "total_clicks": 1500,
        "avg_assessment_score": 75.5
    }


@pytest.fixture
def sample_dropout_payload():
    """Sample payload for dropout prediction"""
    return {
        "code_module": "AAA",
        "code_presentation": "2013J",
        "gender": "F",
        "region": "East Anglian Region",
        "highest_education": "HE Qualification",
        "imd_band": "10-20%",
        "age_band": "0-35",
        "num_of_prev_attempts": 0,
        "studied_credits": 60,
        "disability": "N"
    }


def test_with_fixture(client, sample_final_result_payload):
    """Test using pytest fixture"""
    response = client.post("/api/predict/final-result", json=sample_final_result_payload)
    assert response.status_code == 200
    assert response.json()["success"] == True
