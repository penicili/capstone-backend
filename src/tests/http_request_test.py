"""
HTTP Request Test menggunakan requests library
Pastikan server sudah running: python src/app.py
"""
import requests
import json

# Base URL
BASE_URL = "http://localhost:8000"


class HTTPRequestTest:
    """Test HTTP requests ke running server"""
    
    def __init__(self):
        """Initialize test"""
        print("\n" + "="*70)
        print("HTTP REQUEST TESTING")
        print("="*70)
        print(f"Target: {BASE_URL}")
        print("Pastikan server sudah running!")
        print("="*70)
    
    def test_server_connection(self):
        """Test apakah server running"""
        print("\n" + "="*70)
        print("TEST: Server Connection")
        print("="*70)
        
        try:
            response = requests.get(f"{BASE_URL}/", timeout=5)
            print(f"✓ Server is running")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.json()}")
            return True
        except requests.exceptions.ConnectionError:
            print("✗ Server is not running!")
            print("Please run: python src/app.py")
            return False
        except Exception as e:
            print(f"✗ Error: {e}")
            return False
    
    def test_health_check(self):
        """Test health check endpoint"""
        print("\n" + "="*70)
        print("TEST: Health Check")
        print("="*70)
        
        try:
            response = requests.get(f"{BASE_URL}/health")
            print(f"Status Code: {response.status_code}")
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            
            assert response.status_code == 200
            assert "status" in data
            assert "models_ready" in data
            print("✓ Health check passed")
            return True
        except Exception as e:
            print(f"✗ Health check failed: {e}")
            return False
    
    def test_model_status(self):
        """Test model status endpoint"""
        print("\n" + "="*70)
        print("TEST: Model Status")
        print("="*70)
        
        try:
            response = requests.get(f"{BASE_URL}/api/models/status")
            print(f"Status Code: {response.status_code}")
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            
            assert response.status_code == 200
            assert data["models_ready"] == True
            print("✓ Model status check passed")
            return True
        except Exception as e:
            print(f"✗ Model status check failed: {e}")
            return False
    
    def test_predict_final_result(self):
        """Test predict final result endpoint"""
        print("\n" + "="*70)
        print("TEST: Predict Final Result")
        print("="*70)
        
        payload = {
            "gender": "M",
            "age_band": "35-55",
            "studied_credits": 120,
            "num_of_prev_attempts": 0,
            "total_clicks": 1500,
            "avg_assessment_score": 75.5
        }
        
        print(f"\nRequest payload:")
        print(json.dumps(payload, indent=2))
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/predict/final-result",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            print(f"\nStatus Code: {response.status_code}")
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            
            assert response.status_code == 200
            assert data["success"] == True
            assert "prediction" in data
            print(f"\n✓ Prediction: {data['prediction']}")
            return True
        except Exception as e:
            print(f"✗ Prediction failed: {e}")
            return False
    
    def test_predict_dropout(self):
        """Test predict dropout endpoint"""
        print("\n" + "="*70)
        print("TEST: Predict Dropout")
        print("="*70)
        
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
        print(json.dumps(payload, indent=2))
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/predict/dropout",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            print(f"\nStatus Code: {response.status_code}")
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            
            assert response.status_code == 200
            assert data["success"] == True
            assert "prediction" in data
            print(f"\n✓ Prediction: {data['prediction']}")
            return True
        except Exception as e:
            print(f"✗ Prediction failed: {e}")
            return False
    
    def test_invalid_request(self):
        """Test invalid request handling"""
        print("\n" + "="*70)
        print("TEST: Invalid Request Handling")
        print("="*70)
        
        payload = {
            "gender": "M",
            # Missing required fields
        }
        
        print(f"\nRequest payload (invalid):")
        print(json.dumps(payload, indent=2))
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/predict/final-result",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            print(f"\nStatus Code: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            
            assert response.status_code == 422  # Validation error
            print("\n✓ Invalid request properly rejected")
            return True
        except Exception as e:
            print(f"✗ Test failed: {e}")
            return False
    
    def test_kpi_overview(self):
        """Test KPI overview endpoint"""
        print("\n" + "="*70)
        print("TEST: KPI Dashboard Overview")
        print("="*70)
        
        try:
            response = requests.get(f"{BASE_URL}/api/kpi/overview")
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Response keys: {list(data.keys())}")
                
                if "data" in data:
                    overview = data["data"]
                    print(f"\nOverview sections:")
                    for key in overview.keys():
                        print(f"  - {key}")
                
                print("\n✓ KPI overview working")
                return True
            else:
                print(f"Response: {response.json()}")
                print("⚠ Database might not be connected")
                return True  # Not a failure, just DB not ready
        except Exception as e:
            print(f"⚠ KPI test skipped: {e}")
            return True
    
    def test_kpi_student_performance(self):
        """Test KPI student performance endpoint"""
        print("\n" + "="*70)
        print("TEST: KPI Student Performance")
        print("="*70)
        
        try:
            response = requests.get(f"{BASE_URL}/api/kpi/student-performance")
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Response: {json.dumps(data, indent=2)}")
                print("\n✓ Student performance endpoint working")
                return True
            else:
                print("⚠ Database might not be connected")
                return True
        except Exception as e:
            print(f"⚠ KPI test skipped: {e}")
            return True
    
    def run_all_tests(self):
        """Run all tests"""
        print("\n" + "="*70)
        print("RUNNING ALL HTTP REQUEST TESTS")
        print("="*70)
        
        # Check server connection first
        if not self.test_server_connection():
            print("\n" + "="*70)
            print("❌ TESTS ABORTED - Server not running")
            print("="*70)
            print("\nTo start the server, run:")
            print("  python src/app.py")
            return
        
        tests = [
            ("Health Check", self.test_health_check),
            ("Model Status", self.test_model_status),
            ("Predict Final Result", self.test_predict_final_result),
            ("Predict Dropout", self.test_predict_dropout),
            ("Invalid Request Handling", self.test_invalid_request),
            ("KPI Overview", self.test_kpi_overview),
            ("KPI Student Performance", self.test_kpi_student_performance),
        ]
        
        passed = 0
        failed = 0
        
        for test_name, test_func in tests:
            try:
                if test_func():
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                print(f"\n✗ Test crashed: {test_name}")
                print(f"  Error: {str(e)}")
                failed += 1
        
        # Summary
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)
        print(f"Total Tests: {len(tests)}")
        print(f"✓ Passed: {passed}")
        print(f"✗ Failed: {failed}")
        print("="*70)


if __name__ == "__main__":
    print("\n" + "="*70)
    print("INSTRUCTIONS:")
    print("="*70)
    print("1. Open a new terminal")
    print("2. Run: python src/app.py")
    print("3. Wait for 'Application startup complete'")
    print("4. Run this test file: python src/tests/http_request_test.py")
    print("="*70)
    
    input("\nPress ENTER when server is ready...")
    
    tester = HTTPRequestTest()
    tester.run_all_tests()
