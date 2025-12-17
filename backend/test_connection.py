import requests
import time

def test_backend():
    url = "http://127.0.0.1:8001/"
    print(f"Testing connection to {url}")

    try:
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        print(f"Headers: {response.headers}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

    # Test API endpoint
    api_url = "http://127.0.0.1:8001/docs"
    print(f"\nTesting API endpoint: {api_url}")

    try:
        response = requests.get(api_url, timeout=10)
        print(f"API Status Code: {response.status_code}")
        print(f"API Response length: {len(response.text)}")
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")

if __name__ == "__main__":
    test_backend()