import requests
import unittest
import json
import sys

class CurelyAPITester(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(CurelyAPITester, self).__init__(*args, **kwargs)
        self.base_url = "https://8c7b67e8-9b06-44cc-ab9d-e7ace48c64ff.preview.emergentagent.com/api"
        self.tests_run = 0
        self.tests_passed = 0

    def setUp(self):
        """Setup before each test"""
        self.tests_run += 1
        print(f"\n🔍 Running test: {self._testMethodName}")

    def test_01_health_check(self):
        """Test the API health check endpoint"""
        response = requests.get(f"{self.base_url}/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("message", data)
        self.assertIn("status", data)
        self.assertEqual(data["status"], "active")
        print("✅ Health check endpoint is working")

    def test_02_predict_disease(self):
        """Test the disease prediction endpoint with sample symptoms"""
        test_symptoms = ["fever", "headache", "cough", "fatigue"]
        response = requests.post(
            f"{self.base_url}/predict-disease",
            json={"symptoms": test_symptoms}
        )
        self.assertEqual(response.status_code, 200)
        predictions = response.json()
        self.assertIsInstance(predictions, list)
        
        if len(predictions) > 0:
            # Check structure of first prediction
            first_prediction = predictions[0]
            self.assertIn("id", first_prediction)
            self.assertIn("disease", first_prediction)
            self.assertIn("confidence", first_prediction)
            self.assertIn("matching_symptoms", first_prediction)
            self.assertIn("total_symptoms", first_prediction)
            self.assertIn("description", first_prediction)
            self.assertIn("precautions", first_prediction)
            self.assertIn("medicines", first_prediction)
            
            # Verify predictions are sorted by confidence
            for i in range(len(predictions) - 1):
                self.assertGreaterEqual(
                    predictions[i]["confidence"],
                    predictions[i + 1]["confidence"]
                )
            
            print(f"✅ Disease prediction returned {len(predictions)} results")
            print(f"   Top prediction: {predictions[0]['disease']} with {predictions[0]['confidence']}% confidence")
        else:
            print("⚠️ No predictions returned for the test symptoms")

    def test_03_empty_symptoms(self):
        """Test the disease prediction endpoint with empty symptoms"""
        response = requests.post(
            f"{self.base_url}/predict-disease",
            json={"symptoms": []}
        )
        self.assertEqual(response.status_code, 400)
        print("✅ Empty symptoms correctly return 400 error")

    def test_04_get_all_diseases(self):
        """Test the endpoint to get all diseases"""
        response = requests.get(f"{self.base_url}/diseases")
        self.assertEqual(response.status_code, 200)
        diseases = response.json()
        self.assertIsInstance(diseases, list)
        self.assertGreater(len(diseases), 0)
        
        # Check structure of first disease
        first_disease = diseases[0]
        self.assertIn("id", first_disease)
        self.assertIn("disease", first_disease)
        self.assertIn("symptoms", first_disease)
        
        print(f"✅ Retrieved {len(diseases)} diseases from the directory")

    def test_05_get_disease_details(self):
        """Test getting details for a specific disease"""
        # First get all diseases to get a valid ID
        response = requests.get(f"{self.base_url}/diseases")
        diseases = response.json()
        
        if len(diseases) > 0:
            disease_id = diseases[0]["id"]
            response = requests.get(f"{self.base_url}/disease/{disease_id}")
            self.assertEqual(response.status_code, 200)
            disease_details = response.json()
            
            self.assertEqual(disease_details["id"], disease_id)
            self.assertIn("disease", disease_details)
            self.assertIn("symptoms", disease_details)
            self.assertIn("description", disease_details)
            self.assertIn("precautions", disease_details)
            self.assertIn("medicines", disease_details)
            
            print(f"✅ Successfully retrieved details for disease: {disease_details['disease']}")
        else:
            self.fail("No diseases available to test details endpoint")

    def test_06_invalid_disease_id(self):
        """Test getting details for an invalid disease ID"""
        response = requests.get(f"{self.base_url}/disease/invalid-id")
        self.assertEqual(response.status_code, 404)
        print("✅ Invalid disease ID correctly returns 404 error")

    def test_07_search_diseases(self):
        """Test searching for diseases by name"""
        # First get all diseases to find a search term
        response = requests.get(f"{self.base_url}/diseases")
        diseases = response.json()
        
        if len(diseases) > 0:
            # Use the first few letters of a disease name as search term
            search_term = diseases[0]["disease"][:4]
            response = requests.get(f"{self.base_url}/search-diseases?query={search_term}")
            self.assertEqual(response.status_code, 200)
            search_results = response.json()
            
            self.assertIsInstance(search_results, list)
            if len(search_results) > 0:
                # Verify search results contain the search term
                for result in search_results:
                    self.assertIn(search_term.lower(), result["disease"].lower())
                
                print(f"✅ Search for '{search_term}' returned {len(search_results)} results")
            else:
                print(f"⚠️ Search for '{search_term}' returned no results")
        else:
            self.fail("No diseases available to test search endpoint")

    def test_08_empty_search(self):
        """Test searching with an empty query"""
        response = requests.get(f"{self.base_url}/search-diseases?query=")
        self.assertEqual(response.status_code, 200)
        results = response.json()
        self.assertIsInstance(results, list)
        
        # Empty search should return all diseases
        all_diseases_response = requests.get(f"{self.base_url}/diseases")
        all_diseases = all_diseases_response.json()
        
        self.assertEqual(len(results), len(all_diseases))
        print(f"✅ Empty search correctly returns all {len(results)} diseases")

    def test_09_confidence_calculation(self):
        """Test confidence calculation with specific symptoms"""
        # Test with symptoms that should match a specific disease
        test_cases = [
            {
                "disease": "Common Cold",
                "symptoms": ["continuous_sneezing", "chills", "fatigue", "cough"]
            },
            {
                "disease": "Diabetes",
                "symptoms": ["fatigue", "weight_loss", "restlessness", "excessive_hunger"]
            }
        ]
        
        for test_case in test_cases:
            response = requests.post(
                f"{self.base_url}/predict-disease",
                json={"symptoms": test_case["symptoms"]}
            )
            self.assertEqual(response.status_code, 200)
            predictions = response.json()
            
            # Check if the expected disease is in the top results
            disease_found = False
            for prediction in predictions:
                if prediction["disease"] == test_case["disease"]:
                    disease_found = True
                    print(f"✅ Found {test_case['disease']} with {prediction['confidence']}% confidence")
                    break
            
            if not disease_found:
                print(f"⚠️ Expected disease {test_case['disease']} not found in top predictions")
                print(f"   Top prediction was: {predictions[0]['disease']} with {predictions[0]['confidence']}% confidence")

def run_tests():
    """Run all the API tests"""
    test_suite = unittest.TestLoader().loadTestsFromTestCase(CurelyAPITester)
    test_result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    
    print("\n📊 Test Summary:")
    print(f"   Tests run: {test_result.testsRun}")
    print(f"   Tests passed: {test_result.testsRun - len(test_result.failures) - len(test_result.errors)}")
    print(f"   Tests failed: {len(test_result.failures)}")
    print(f"   Test errors: {len(test_result.errors)}")
    
    return len(test_result.failures) + len(test_result.errors)

if __name__ == "__main__":
    sys.exit(run_tests())
