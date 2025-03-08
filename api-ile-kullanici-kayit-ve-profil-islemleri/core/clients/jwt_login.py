import requests
from pprint import pprint

# test_user_32 için
# 'access': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM4MTc5NzQ0LCJpYXQiOjE3MzgxNzkxNDQsImp0aSI6IjE3NGIxODZmMDAzNjQ4ZGM4NTM5ZWJkZGU4OWZlZjRjIiwidXNlcl9pZCI6NDF9.aqevRU-Kjma8xMLltBubAT5ZtCDvJDHOSDkct2taQqs'
# 'refresh': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczODI2NTU0NCwiaWF0IjoxNzM4MTc5MTQ0LCJqdGkiOiIzM2IwNzU1N2UwZGQ0NzgyODk4N2NhMTY2NjA4ZGE1NCIsInVzZXJfaWQiOjQxfQ.27oF6JwEGgpCRHMXHnpgwLPiattHT0tUcBxD48FY668'

# Access token: Kullanıcının yetkilendirilmiş API istekleri yapması için kullanılır.
# Refresh token: Access token süresi dolduğunda yeni bir access token almak için kullanılır.

def client():
    credentials = {
        "username": "test_user_10",
        "password": "testpassword123"
    }

    response = requests.post(
        url = 'http://127.0.0.1:8000/api/token/',
        data = credentials
    )

    print("Status Code:", response.status_code)

    response_data = response.json()
    pprint(response_data)

if __name__ == "__main__": 
    client()