import requests
from requests.auth import HTTPBasicAuth
from pprint import pprint

def client():
    auth = HTTPBasicAuth("test_user_35", "testpassword123")

    response = requests.get(
        url = 'http://127.0.0.1:8000/api/kullanici-profilleri/',
        auth = auth
    )
    
    print("Status Code:", response.status_code)
    response_data = response.json()
    pprint(response_data)
 
if __name__ == "__main__":   
    client()