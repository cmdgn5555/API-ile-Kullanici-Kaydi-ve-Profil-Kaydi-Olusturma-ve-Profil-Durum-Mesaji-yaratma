import requests
from pprint import pprint

def client():
    session_id = "kygz8l3yzwunmvcf9ebjxpoy04u3d1u8"

    cookies = {
        'sessionid': session_id
    }

    response = requests.get(
        url = 'http://127.0.0.1:8000/api/kullanici-profilleri/',
        cookies = cookies
    )

    print("Status Code:", response.status_code)

    response_data = response.json()
    pprint(response_data)
    

if __name__ == "__main__":
    client()