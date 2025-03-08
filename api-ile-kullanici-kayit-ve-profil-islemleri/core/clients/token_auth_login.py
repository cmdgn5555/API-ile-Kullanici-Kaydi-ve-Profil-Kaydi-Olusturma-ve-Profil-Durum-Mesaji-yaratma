import requests
from pprint import pprint

# {'key': 'fae77af382bf67916d3f6ee6d39137250a107bad'} test_user_20 için
# {'key': 'a863776a74f876753d83eb1683ee8facfe55678e'} test_user_21 için
# {'key': 'cb9160a46ac3c62b48e58c0ef7eb530d551ada34'} test_user_22 için
# {'key': '75d1a2a5d5d142ebf3488827ab67614765f742c2'} test_user_24 için


def client():
    credentials = {
        "username": "test_user_35",
        "password": "testpassword123"
    }

    response = requests.post(  
        url = 'http://127.0.0.1:8000/api/dj-rest-auth/login/',
        data = credentials
    )

    print("Status Code:", response.status_code)

    response_data = response.json()
    pprint(response_data)

if __name__ == "__main__":
    client()