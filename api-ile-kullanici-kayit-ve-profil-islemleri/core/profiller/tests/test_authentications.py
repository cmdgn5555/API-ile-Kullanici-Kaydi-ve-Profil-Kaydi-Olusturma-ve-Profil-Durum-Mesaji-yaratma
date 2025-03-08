from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.contrib.auth import get_user_model

'''
class TestBasicAuthentication(APITestCase):

    def setUp(self):
        # Test kullanıcısını oluştur
        self.user = User.objects.create_user(username="test_user_1", password="testpassword123")
        self.url = "/api/kullanici-profilleri/"
    
    
    def test_authenticated_user_can_access_profiles(self):
        # Doğru kimlik bilgileriyle giriş yapıldığında erişim başarılı olmalı
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    

    def test_wrong_credentials_cannot_access_profiles(self):
        # Yanlış kimlik bilgileriyle giriş yapıldığında erişim reddedilmeli
        self.client.login(username="wrong_user", password="wrong_password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    

    def test_no_credentials_cannot_access_profiles(self):
        # Kimlik bilgisi olmadan giriş yapıldığında erişim reddedilmeli
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)




class TestSessionAuthentication(APITestCase):

    def setUp(self):
        # Test kullanıcısı oluşturuyoruz ve giriş yapıyoruz
        self.user = User.objects.create_user(username="test_user_2", password="testpassword123")
        self.client.login(username="test_user_2", password="testpassword123")
    

    def test_authenticated_user_can_access_profiles(self): 
        # Oturum açmış kullanıcı profillere erişebiliyor mu ?
        response = self.client.get("/api/kullanici-profilleri/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    

    def test_unauthenticated_user_cannot_access_profiles(self): 
        # Oturum açmamış kullanıcı 403 hatası alıyor mu ?
        self.client.logout()
        response = self.client.get("/api/kullanici-profilleri/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

'''



class TestTokenAuthenticationLogin(APITestCase):

    def setUp(self):
        # Test için kullanıcı oluşturuyoruz
        self.user = User.objects.create_user(username="test_user_3", password="testpassword123")
        self.login_url = "/api/dj-rest-auth/login/"
    
    
    def test_valid_login_returns_token(self):
        # Geçerli bilgilerle giriş yapıldığında token dönmeli
        credentials = {
            "username": "test_user_3",
            "password": "testpassword123"
        }

        response = self.client.post(path=self.login_url, data=credentials)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("key", response.data) # Gelen veride token(key) olmalı
    

    def test_invalid_login_fails(self):
        # Yanlış bilgilerle giriş başarısız olmalı ve token dönmemeli
        credentials = {
            "username": "yanlis_kullanici",
            "password": "yanlis_sifre"
        }

        response = self.client.post(path=self.login_url, data=credentials)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("key", response.data) # Hatalı girişte token(key) dönmemeli
    

    def test_missing_credentials_fails(self):
        # Eksik bilgilerle giriş başarısız olmalı
        credentials = {
            "username": "test_user_3" # Burda şifre eksik
        }

        response = self.client.post(path=self.login_url, data=credentials)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data) # Eksik alan hakkında hata mesajı olmalı




class TestTokenAuthenticationRequest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="test_user_4", password="testpassword123")
        self.token = Token.objects.create(user=self.user)
        self.url = "/api/kullanici-profilleri/" # Test edilecek API endpoint
        

    def test_valid_token_authentication(self):
        # Doğru token ile yetkilendirme başarılı olmalı
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}") 
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    

    def test_invalid_token_authentication(self):
        # Yanlış token ile yetkilendirme başarısız olmalı
        self.client.credentials(HTTP_AUTHORIZATION="Token yanlis_token")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    

    def test_no_token_provided(self):
        # Token olmadan yetkilendirme başarısız olmalı
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    

    def test_invalid_header_format(self):
        # Hatalı header formatı ile yetkilendirme başlığını ayarla
        self.client.credentials(HTTP_AUTHORIZATION="Bearer 095e5c2df86fceeda46c66a9d565588aa5bfd5634439")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)




class TestUserRegistration(APITestCase):

    def setUp(self):
        self.registration_url = "/api/dj-rest-auth/registration/"
    

    def test_valid_registration_returns_201_and_token(self):
        # Geçerli bilgilerle kayıt olunduğunda 201 Created ve token dönmeli ve kullanıcı otomatik olarak giriş yapmalı
        credentials = {
            "username": "test_user_kayit",
            "email": "testuserkayit@gmail.com",
            "password1": "testpassword123",
            "password2": "testpassword123"
        }

        response = self.client.post(path=self.registration_url, data=credentials)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("key", response.data) # Başarılı kayıt sonrası token olmalı
        

    def test_missing_fields_returns_400(self):
        # Eksik bilgilerle kayıt olunmaz, 400 Bad request dönmeli
        credentials = {
            "username": "test_user_kayit", # e-posta ve şifreler eksik
        }

        response = self.client.post(path=self.registration_url, data=credentials)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertIn("password1", response.data)
        self.assertIn("password2", response.data)
    

    def test_password_mismatch_returns_400(self):
        # Şifreler eşleşmezse kayıt başarısız olmalı ve 400 dönmeli
        credentials = {
            "username": "test_user_kayit",
            "email": "testuserkayit@gmail.com",
            "password1": "testpassword123",
            "password2": "yanlis_sifre"
        }

        response = self.client.post(path=self.registration_url, data=credentials)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data) # Şifreler eşleşmediği için hata olmalı
    

    def test_invalid_email_format_returns_400(self):
        # Geçersiz e-posta formatıyla kayıt denemesi yapılırsa,
        # API 400 Bad request dönmeli ve email alanında hata içermeli
        credentials = {
            "username": "test_user_kayit",
            "email": "yanlis_email_format",
            "password1": "testpassword123",
            "password2": "testpassword123"
        }

        response = self.client.post(path=self.registration_url, data=credentials)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
    

    def test_duplicate_username_fails(self):
        # Aynı kullanıcı adıyla ikinci kez kayıt olunamaz, 400 dönmeli
        User.objects.create_user(username="test_user_kayit", email="testuserkayit@gmail.com", password="testpassword123")

        credentials = {
            "username": "test_user_kayit",
            "email": "testuserkayit@gmail.com",
            "password1": "testpassword123",
            "password2": "testpassword123"
        }

        response = self.client.post(path=self.registration_url, data=credentials)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data) # Kullanıcı adı zaten daha önceden alındığı için hata dönmeli
        

        

'''

class TestJWTAuthenticationLogin(APITestCase):

    def setUp(self):
        # Test için kullanıcı oluşturuyoruz
        self.user = User.objects.create_user(username="test_user_5", password="testpassword123")
        self.token_url = "/api/token/"
    

    def test_valid_credentials(self):
        # Geçerli kullanıcı adı ve şifre ile token alınabilmeli
        credentials = {
            "username": "test_user_5",
            "password": "testpassword123"
        }

        response = self.client.post(path=self.token_url, data=credentials)  

        self.assertEqual(response.status_code, status.HTTP_200_OK) # Status code 200 olmalı
        self.assertIn("access", response.data) # access token dönmeli
        self.assertIn("refresh", response.data) # refresh token dönmeli
    

    def test_invalid_credentials(self):
        # Yanlış kullanıcı adı veya şifre ile giriş başarısız olmalı
        credentials = {
            "username": "wrong_user",
            "password": "wrong_password"
        }

        response = self.client.post(path=self.token_url, data=credentials)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) # Status code 401 olmalı
        self.assertIn("detail", response.data) # Hata mesajı içermeli
    

    def test_missing_username(self):
        # Eksik kullanıcı adı ile giriş başarısız olmalı
        credentials = {
            "password": "testpassword123",
        }

        response = self.client.post(path=self.token_url, data=credentials)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) # Status code 400 olmalı
        self.assertIn("username", response.data) # Eksik alan bildirimi olmalı
    

    def test_missing_password(self):
        # Eksik şifre ile giriş başarısız olmalı
        credentials = {
            "username": "test_user_5"
        }

        response = self.client.post(path=self.token_url, data=credentials)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) # Status code 400 olmalı
        self.assertIn("password", response.data) # Eksik alan bildirimi olmalı
        



class TestJWTAuthenticationRequest(APITestCase):

    def setUp(self):
        # Testler için bir kullanıcı oluşturalım ve JWT access token alalım
        self.user= User.objects.create_user(username="test_user_6", password="testpassword123")
        self.profile_url = "/api/kullanici-profilleri/"
        self.access_token = str(AccessToken.for_user(self.user)) # Kullanıcı için geçerli bir access token oluşturuyoruz
        
    
    def test_valid_access_token(self):
        # Geçerli bir access token ile erişim başarılı olmalı
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        response = self.client.get(path=self.profile_url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK) # Yetkilendirme başarılı olmalı
        
    
    def test_missing_token(self):
        # Token olmadan erişim reddedilmeli
        response = self.client.get(path=self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) # Kimlik doğrulama hatası
    

    def test_invalid_token(self):
        # Geçersiz token ile erişim reddedilmeli
        headers = {
            "Authorization": "Bearer yanlis_token"
        }

        response = self.client.get(path=self.profile_url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) # Token geçersiz
        
        
    def test_expired_token(self):
        # Süresi dolmuş bir token kullanılırsa erişim reddedilmeli
        expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQxMTAxNjY1LCJpYXQiOjE3NDExMDE0ODUsImp0aSI6ImFjMTNhNTAwODUxNjRmNTI4MjVjZmI4NmE5MTFiYjBmIiwidXNlcl9pZCI6MX0.ce3SN6ezaWklgNki8XfMkPgTKTP2gBkOgq-52uPfmXE"
        headers = {
            "Authorization": f"Bearer {expired_token}"
        }

        response = self.client.get(path=self.profile_url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) # Token süresi dolmuş olmalı
       
        
    def test_wrong_token_format(self):
        # Bearer yerine yanlış formatta token kullanılırsa hata alınmalı
        headers = {
            "Authorization": f"WrongPrefix {self.access_token}"
        }

        response = self.client.get(path=self.profile_url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) # Yanlış format hatası
    

    def test_empty_token(self):
        # Boş token kullanıldığında hata alınmalı
        headers = {
            "Authorization": "Bearer "
        }

        response = self.client.get(path=self.profile_url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        



class TestJWTRefreshToken(APITestCase):

    def setUp(self):
        # Test için kullanıcı oluşturuyoruz
        self.user = User.objects.create_user(username="test_user_refresh", password="testpassword123")
        self.refresh_url = "/api/token/refresh/"
        self.refresh_token = str(RefreshToken.for_user(self.user)) # Kullanıcı için refresh token oluşturuyoruz
    
    
    def test_valid_refresh_token(self):
        # Geçerli refresh token ile yeni access token alınmalı
        response = self.client.post(self.refresh_url, data={"refresh": self.refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data) # Yeni access token dönmeli
        
        
    def test_invalid_resfresh_token(self):
        # Geçersiz refresh token ile yenileme başarısız olmalı
        response = self.client.post(self.refresh_url, data={"refresh": "invalid_refresh_token"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) # Yetkisiz erişim hatası
        self.assertIn("detail", response.data) # Hata mesajı içermeli
    

    def test_expired_refresh_token(self):
        # Süresi dolmuş refresh token ile yenileme başarısız olmalı
        expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTE4MTU0NywiaWF0IjoxNzQxMTgwOTQ3LCJqdGkiOiI3YjRiOTIyMDE0OWM0YTRiYmY4NTY3NGMyMTBlNzU5OSIsInVzZXJfaWQiOjF9.Nj7Pfwf1n297WL4WQZSCB9o0GpF3oQ8NGPLPF9dga4s"
        response = self.client.post(self.refresh_url, data={"refresh": expired_token})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) # Yetkisiz hata dönmeli
    

    def test_missing_refresh_token(self):
        # Eksik refresh token ile yenileme başarısız olmalı
        response = self.client.post(self.refresh_url, data={}) # Refresh token hiç gönderilmiyor
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) # Eksik parametre hatası
        self.assertIn("refresh", response.data) # Hata mesajı refresh alanı ile ilgili olmalı
        

    def test_empty_refresh_token(self):
        # Boş refresh token ile yenileme başarısız olmalı
        response = self.client.post(self.refresh_url, data={"refresh": ""})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("refresh", response.data)

'''
        

