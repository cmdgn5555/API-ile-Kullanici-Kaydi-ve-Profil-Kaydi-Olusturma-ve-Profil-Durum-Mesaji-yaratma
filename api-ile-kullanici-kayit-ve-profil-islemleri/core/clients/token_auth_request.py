import requests
from pprint import pprint

# {'key': 'a863776a74f876753d83eb1683ee8facfe55678e'} test_user_21 için
# {'key': 'fae77af382bf67916d3f6ee6d39137250a107bad'} test_user_20 için
# {'key': '75d1a2a5d5d142ebf3488827ab67614765f742c2'} test_user_24 için


def client():
    token = 'Token 6fcddfdbe859e91439984c9a2f88c4613c8f0ba1'

    headers = {
        'Authorization': token
    }

    response = requests.get( 
        url = 'http://127.0.0.1:8000/api/kullanici-profilleri/',
        headers = headers
    )

    print("Status Code:", response.status_code)

    response_data = response.json()
    pprint(response_data)

if __name__ == "__main__":
    client()