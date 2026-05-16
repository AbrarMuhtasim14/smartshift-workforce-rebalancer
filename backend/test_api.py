"""
Quick test script for SmartShift API
Run this to verify the backend is working correctly.
"""
import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint."""
    print("\n🔍 Testing health check...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_get_workers():
    """Test getting all workers."""
    print("\n🔍 Testing get all workers...")
    response = requests.get(f"{BASE_URL}/api/workers")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        workers = response.json()
        print(f"Total workers: {len(workers)}")
        print(f"First worker: {json.dumps(workers[0], indent=2)}")
    return response.status_code == 200

def test_get_zone_stats():
    """Test getting zone statistics."""
    print("\n🔍 Testing zone statistics...")
    response = requests.get(f"{BASE_URL}/api/zones/Zone A")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_search_workers():
    """Test searching for workers."""
    print("\n🔍 Testing worker search...")
    payload = {
        "query": "forklift operator",
        "exclude_zone": "Zone A"
    }
    response = requests.post(f"{BASE_URL}/api/search", json=payload)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")
    else:
        print(f"Error: {response.text}")
    return response.status_code == 200

def test_recommendations():
    """Test getting AI recommendations."""
    print("\n🔍 Testing AI recommendations...")
    payload = {
        "manager_input": "Zone A dispatch is overloaded, need forklift help"
    }
    response = requests.post(f"{BASE_URL}/api/recommendations", json=payload)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Status: {result['status']}")
        print(f"Recommendations preview: {result['recommendations'][:200]}...")
    return response.status_code == 200

def main():
    """Run all tests."""
    print("=" * 60)
    print("SmartShift API Test Suite")
    print("=" * 60)
    
    tests = [
        ("Health Check", test_health_check),
        ("Get Workers", test_get_workers),
        ("Zone Statistics", test_get_zone_stats),
        ("Search Workers", test_search_workers),
        ("AI Recommendations", test_recommendations),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, "✅ PASS" if success else "❌ FAIL"))
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            results.append((name, "❌ ERROR"))
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    for name, result in results:
        print(f"{name}: {result}")
    
    passed = sum(1 for _, r in results if "✅" in r)
    total = len(results)
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! API is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the output above.")

if __name__ == "__main__":
    main()

# Made with Bob
