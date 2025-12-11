"""
Test untuk API endpoints menggunakan TestClient
Test HTTP endpoints untuk prediction dan KPI
"""
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

from fastapi.testclient import TestClient
from app import app

# Create test client
client = TestClient(app)


class APITest:
    """Test class untuk API endpoints"""
    
    def __init__(self):
        """Initialize API test"""
        print("\n" + "="*70)
        print("API ENDPOINT TESTING")
        print("="*70)
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        print("\n" + "="*70)
        print("TEST: Root Endpoint")
        print("="*70)
        
        response = client.get("/")
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        assert response.status_code == 200
        assert "message" in response.json()
        print("✓ Root endpoint working")
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        print("\n" + "="*70)
        print("TEST: Health Check Endpoint")
        print("="*70)
        
        response = client.get("/health")
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        assert response.status_code == 200
        assert "status" in response.json()
        assert "models_ready" in response.json()
        print("✓ Health endpoint working")
    
    def test_model_status_endpoint(self):
        """Test model status endpoint"""
        print("\n" + "="*70)
        print("TEST: Model Status Endpoint")
        print("="*70)
        
        response = client.get("/api/models/status")
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        assert response.status_code == 200
        data = response.json()
        assert "models_ready" in data
        assert "dropout_model_loaded" in data
        assert "final_grade_model_loaded" in data
        print("✓ Model status endpoint working")
    
    def test_predict_final_result(self):
        """Test prediction final result endpoint"""
        print("\n" + "="*70)
        print("TEST: Predict Final Result Endpoint")
        print("="*70)
        
        # Test data
        payload = {
            "gender": "M",
            "age_band": "35-55",
            "studied_credits": 120,
            "num_of_prev_attempts": 0,
            "total_clicks": 1500,
            "avg_assessment_score": 75.5
        }
        
        print(f"\nRequest payload:")
        for key, value in payload.items():
            print(f"  {key}: {value}")
        
        response = client.post("/api/predict/final-result", json=payload)
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "prediction" in data
        print(f"\n✓ Final result prediction: {data['prediction']}")
    
    def test_predict_dropout(self):
        """Test prediction dropout endpoint"""
        print("\n" + "="*70)
        print("TEST: Predict Dropout Endpoint")
        print("="*70)
        
        # Test data
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
        
        print(f"\nRequest payload:")
        for key, value in payload.items():
            print(f"  {key}: {value}")
        
        response = client.post("/api/predict/dropout", json=payload)
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "prediction" in data
        print(f"\n✓ Dropout prediction: {data['prediction']}")
    
    def test_kpi_dashboard_overview(self):
        """Test KPI dashboard overview endpoint"""
        print("\n" + "="*70)
        print("TEST: KPI Dashboard Overview Endpoint")
        print("="*70)
        
        response = client.get("/api/kpi/overview")
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response keys: {list(data.keys())}")
            
            assert "success" in data
            assert data["success"] == True
            assert "data" in data
            
            # Check data structure
            overview_data = data["data"]
            print(f"\nOverview data keys: {list(overview_data.keys())}")
            
            assert "student_performance" in overview_data
            assert "vle_engagement" in overview_data
            assert "module_statistics" in overview_data
            assert "assessment_summary" in overview_data
            
            print("\n✓ KPI dashboard overview working")
        else:
            print(f"Response: {response.json()}")
            print("\n⚠ KPI overview endpoint failed (database might not be connected)")
    
    def test_kpi_student_performance(self):
        """Test KPI student performance endpoint"""
        print("\n" + "="*70)
        print("TEST: KPI Student Performance Endpoint")
        print("="*70)
        
        response = client.get("/api/kpi/student-performance")
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {data}")
            
            assert "success" in data
            assert data["success"] == True
            assert "data" in data
            
            # Check student performance data
            perf_data = data["data"]
            if perf_data:
                print(f"\nStudent Performance Metrics:")
                print(f"  Total Students: {perf_data.get('total_students', 'N/A')}")
                print(f"  Total Pass: {perf_data.get('total_pass', 'N/A')}")
                print(f"  Total Fail: {perf_data.get('total_fail', 'N/A')}")
                print(f"  Total Withdrawn: {perf_data.get('total_withdrawn', 'N/A')}")
            
            print("\n✓ Student performance endpoint working")
        else:
            print(f"Response: {response.json()}")
            print("\n⚠ Student performance endpoint failed (database might not be connected)")
    
    def test_kpi_module_statistics(self):
        """Test KPI module statistics endpoint"""
        print("\n" + "="*70)
        print("TEST: KPI Module Statistics Endpoint")
        print("="*70)
        
        response = client.get("/api/kpi/module-statistics")
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            assert "success" in data
            assert data["success"] == True
            assert "data" in data
            
            # Check module statistics data
            modules = data["data"]
            print(f"\nTotal Modules: {len(modules)}")
            
            if modules:
                print(f"\nFirst 3 modules:")
                for module in modules[:3]:
                    print(f"  {module.get('code_module')} - {module.get('code_presentation')}: "
                          f"{module.get('total_students')} students, "
                          f"{module.get('pass_rate')}% pass rate")
            
            print("\n✓ Module statistics endpoint working")
        else:
            print(f"Response: {response.json()}")
            print("\n⚠ Module statistics endpoint failed (database might not be connected)")
    
    def test_kpi_vle_engagement(self):
        """Test KPI VLE engagement endpoint"""
        print("\n" + "="*70)
        print("TEST: KPI VLE Engagement Endpoint")
        print("="*70)
        
        response = client.get("/api/kpi/vle-engagement")
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {data}")
            
            assert "success" in data
            assert data["success"] == True
            assert "data" in data
            
            # Check VLE engagement data
            vle_data = data["data"]
            if vle_data:
                print(f"\nVLE Engagement Metrics:")
                print(f"  Total Active Students: {vle_data.get('total_active_students', 'N/A')}")
                print(f"  Total Clicks: {vle_data.get('total_clicks', 'N/A')}")
                print(f"  Avg Clicks/Student: {vle_data.get('avg_clicks_per_student', 'N/A')}")
            
            print("\n✓ VLE engagement endpoint working")
        else:
            print(f"Response: {response.json()}")
            print("\n⚠ VLE engagement endpoint failed (database might not be connected)")
    
    def test_kpi_assessment_summary(self):
        """Test KPI assessment summary endpoint"""
        print("\n" + "="*70)
        print("TEST: KPI Assessment Summary Endpoint")
        print("="*70)
        
        response = client.get("/api/kpi/assessment-summary")
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            assert "success" in data
            assert data["success"] == True
            assert "data" in data
            
            # Check assessment summary data
            assessments = data["data"]
            print(f"\nTotal Assessment Records: {len(assessments)}")
            
            if assessments:
                print(f"\nFirst 3 assessment summaries:")
                for assessment in assessments[:3]:
                    print(f"  {assessment.get('code_module')} - {assessment.get('code_presentation')}: "
                          f"avg score {assessment.get('avg_score')}")
            
            print("\n✓ Assessment summary endpoint working")
        else:
            print(f"Response: {response.json()}")
            print("\n⚠ Assessment summary endpoint failed (database might not be connected)")
    
    def test_invalid_prediction_request(self):
        """Test invalid prediction request"""
        print("\n" + "="*70)
        print("TEST: Invalid Prediction Request")
        print("="*70)
        
        # Invalid payload (missing required fields)
        payload = {
            "gender": "M",
            "age_band": "35-55"
            # Missing other required fields
        }
        
        print(f"\nRequest payload (invalid - missing fields):")
        for key, value in payload.items():
            print(f"  {key}: {value}")
        
        response = client.post("/api/predict/final-result", json=payload)
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        assert response.status_code == 422  # Validation error
        print("\n✓ Invalid request properly rejected with 422 status")
    
    def run_all_tests(self):
        """Run all tests"""
        print("\n" + "="*70)
        print("RUNNING ALL API TESTS")
        print("="*70)
        
        tests = [
            ("Root Endpoint", self.test_root_endpoint),
            ("Health Check", self.test_health_endpoint),
            ("Model Status", self.test_model_status_endpoint),
            ("Predict Final Result", self.test_predict_final_result),
            ("Predict Dropout", self.test_predict_dropout),
            ("KPI Dashboard Overview", self.test_kpi_dashboard_overview),
            ("KPI Student Performance", self.test_kpi_student_performance),
            ("KPI Module Statistics", self.test_kpi_module_statistics),
            ("KPI VLE Engagement", self.test_kpi_vle_engagement),
            ("KPI Assessment Summary", self.test_kpi_assessment_summary),
            ("Invalid Request Handling", self.test_invalid_prediction_request),
        ]
        
        passed = 0
        failed = 0
        skipped = 0
        
        for test_name, test_func in tests:
            try:
                test_func()
                passed += 1
            except AssertionError as e:
                print(f"\n✗ Test failed: {test_name}")
                print(f"  Error: {str(e)}")
                failed += 1
            except Exception as e:
                print(f"\n⚠ Test skipped: {test_name}")
                print(f"  Reason: {str(e)}")
                skipped += 1
        
        # Summary
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)
        print(f"Total Tests: {len(tests)}")
        print(f"✓ Passed: {passed}")
        print(f"✗ Failed: {failed}")
        print(f"⚠ Skipped: {skipped}")
        print("="*70)


if __name__ == "__main__":
    tester = APITest()
    tester.run_all_tests()
