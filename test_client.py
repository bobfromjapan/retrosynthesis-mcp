import requests
import json

BASE_URL = "http://localhost:8000"

def test_health_check():
    print("\n--- Testing GET / ---")
    try:
        response = requests.get(f"{BASE_URL}/")
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Is the server running?")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def test_retrosynthesis():
    print("\n--- Testing POST /retrosynthesis ---")
    test_smiles = "CCO"
    headers = {"Content-Type": "application/json"}
    data = {"smiles": test_smiles}

    try:
        response = requests.post(f"{BASE_URL}/retrosynthesis", headers=headers, data=json.dumps(data))
        response.raise_for_status()
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Is the server running?")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_health_check()
    test_retrosynthesis()
