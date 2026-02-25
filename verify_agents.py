import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_agent(endpoint, message):
    url = f"{BASE_URL}/agent/{endpoint}"
    payload = {
        "message": message,
        "patient_id": "test_patient_001",
        "patient_info": {"name": "Test User"}
    }
    print(f"Testing [{endpoint}] Agent...")
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"SUCCESS! Response: {data.get('response')[:100]}...")
            if data.get('worker_results'):
                print(f"   Results: {data.get('worker_results')}")
        else:
            print(f"FAILED! Status Code: {response.status_code}")
    except Exception as e:
        print(f"ERROR: {e}")
    print("-" * 50)

def run_all_tests():
    print(f"ADHILAXMI Hospital Agent Verification\n")
    
    # 1. Receptionist
    test_agent("receptionist", "I want to schedule a visit")
    
    # 2. Appointment
    test_agent("appointment", "Book a slot for tomorrow")
    
    # 3. Lab Analyst
    test_agent("lab_analyst", "My blood report says hemoglobin is 10")
    
    # 4. Specialist
    test_agent("specialist", "I have a red rash on my hand")
    
    # 5. Wellness
    test_agent("wellness", "I need a recovery plan for stress")
    
    # 6. Prescription
    test_agent("prescription", "Can I take aspirin with warfarin?")
    
    # 7. Admin
    test_agent("admin", "Give me my bill")

if __name__ == "__main__":
    # Ensure backend is running before starting this
    try:
        requests.get(BASE_URL)
        run_all_tests()
    except:
        print(f"❌ Backend not found at {BASE_URL}. Please run 'uvicorn backend.main:app --reload' first.")
