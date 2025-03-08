import requests
from pprint import pprint


def refresh_token():
    # Eğer access token'ın süresi dolmuş ise burda daha önceden almış olduğumuz refresh token'ı kullanarak yeni bir access token alıyoruz
    # Tabi ki burda refresh token'ın süresi de dolmamış olmalı geçerli bir refresh token olmalı
    refresh_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTExNzI0MiwiaWF0IjoxNzQxMTE2NjQyLCJqdGkiOiIwMzUzNzZjYzEyYjQ0ZDI3OTNiOWVjZDYwZTRmMDI3MyIsInVzZXJfaWQiOjI4fQ.a9lKdhVoTsF1r-tKolV0wQGE2wFS-7Cn_v0jtaoWNIE"

    response = requests.post(
        url = "http://127.0.0.1:8000/api/token/refresh/",
        data = {"refresh": refresh_token}
    )

    print("Status Code:", response.status_code)

    response_data = response.json() 
    pprint(response_data)

if __name__ == "__main__":
    refresh_token()