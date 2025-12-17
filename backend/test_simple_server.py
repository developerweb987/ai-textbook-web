import requests
import time

def test_connection():
    print("Testing connection to simple server...")
    try:
        response = requests.get("http://127.0.0.1:8001/", timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        print("SUCCESS: Simple server is responding!")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    time.sleep(3)  # Wait for server to be ready
    test_connection()