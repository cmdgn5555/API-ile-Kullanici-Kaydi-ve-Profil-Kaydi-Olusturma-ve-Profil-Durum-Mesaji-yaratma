import requests
from pprint import pprint


def client():
    # jwt_login.py dosyası içinde aldığımız access token'ı burda kullanıyoruz
    token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQxMTE2NjI4LCJpYXQiOjE3NDExMTYzODEsImp0aSI6ImNmODgzMTY3YTZhZjRjOGM4NTA4OWM3OWJiYzk2MjI3IiwidXNlcl9pZCI6Mjh9.JoU9qN6Uqvhj_OKuzlJ0UUJTF4SNlc9M_z07hG906ag"

    headers = {
        "Authorization": token
    }

    response = requests.get(
        url = "http://127.0.0.1:8000/api/kullanici-profilleri/", 
        headers = headers
    )

    print("Status Code:", response.status_code)

    response_data = response.json()
    pprint(response_data)

if __name__ == "__main__":
    client()