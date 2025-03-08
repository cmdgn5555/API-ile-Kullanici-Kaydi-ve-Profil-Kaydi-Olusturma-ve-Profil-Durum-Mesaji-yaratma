from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from rest_framework.permissions import SAFE_METHODS
from profiller.api.permissions import KendiProfiliYadaReadOnly, DurumSahibiYadaReadOnly
from profiller.models import Profil, ProfilDurum


class KendiProfiliYadaReadOnlyTest(TestCase):

    def setUp(self):
        # Test için iki kullanıcı ve profillerini oluşturuyoruz
        self.kullanici1 = User.objects.create_user(username="user1", password="pass1")
        self.kullanici2 = User.objects.create_user(username="user2", password="pass2")
        self.profili1 = Profil.objects.create(user=self.kullanici1)
        self.profili2 = Profil.objects.create(user=self.kullanici2)
        self.izin = KendiProfiliYadaReadOnly()
        self.factory = APIRequestFactory()
    

    def test_read_only_permission(self):
        # Get gibi güvenli metodlarda herkes erişebiliyor mu ?
        istek = self.factory.get("/fake-url/")
        istek.user = self.kullanici2 # Farklı bir kullanıcı
        self.assertTrue(self.izin.has_object_permission(istek, None, self.profili1))


    def test_user_can_edit_own_profile(self):
        # Kullanıcı kendi profilini düzenleyebilir mi ?
        istek = self.factory.put("/fake-url/")
        istek.user = self.kullanici1 # Kendi profili
        self.assertTrue(self.izin.has_object_permission(istek, None, self.profili1))
        
    
    def test_user_cannot_edit_other_profiles(self):
        # Kullanıcı başka birinin profilini düzenleyebilir mi ?
        istek = self.factory.put("/fake-url/")
        istek.user = self.kullanici2 # Farklı kullanıcı
        self.assertFalse(self.izin.has_object_permission(istek, None, self.profili1))
    

    def test_user_can_create_own_profile(self):
        # Kullanıcı kendi adına profil oluşturabilir mi ?
        istek = self.factory.post("/fake-url/")
        istek.user = self.kullanici1
        self.assertTrue(self.izin.has_object_permission(istek, None, self.profili1))
    

    def test_user_cannot_create_profile_for_other(self):
        # Kullanıcı başka biri adına profil oluşturabilir mi ?
        istek = self.factory.post("/fake-url/")
        istek.user = self.kullanici2 # Farklı kullanıcı
        self.assertFalse(self.izin.has_object_permission(istek, None, self.profili1))
    

    def test_user_can_delete_own_profile(self):
        # Kullanıcı kendi profilini silebilir mi ?
        istek = self.factory.delete("/fake-url/")
        istek.user = self.kullanici1 # Kendi profili
        self.assertTrue(self.izin.has_object_permission(istek, None, self.profili1))
    

    def test_user_cannot_delete_other_profile(self):
        # Kullanıcı başkasının profilini silebilir mi ?
        istek = self.factory.delete("/fake-url/")
        istek.user = self.kullanici2 # Farklı kullanıcı
        self.assertFalse(self.izin.has_object_permission(istek, None, self.profili1))




class DurumSahibiYadaReadOnlyTest(TestCase):

    def setUp(self):
        # Test için iki kullanıcıyı profillerini ve durumlarını oluşturuyoruz
        self.kullanici1 = User.objects.create_user(username="user1", password="pass1")
        self.kullanici2 = User.objects.create_user(username="user2", password="pass2")
        self.profili1 = Profil.objects.create(user=self.kullanici1)
        self.profili2 = Profil.objects.create(user=self.kullanici2)
        self.durumu1 = ProfilDurum.objects.create(user_profil=self.profili1, durum_mesaji="İlk Durum")
        self.durumu2 = ProfilDurum.objects.create(user_profil=self.profili2, durum_mesaji="Başka Durum")
        self.izin = DurumSahibiYadaReadOnly()
        self.factory = APIRequestFactory()
    

    def test_read_only_permission(self):
        # Herkes bir başkasının durumunu görüntüleyebilir mi ?
        istek = self.factory.get("/fake-url/")
        istek.user = self.kullanici2 # Farklı bir kullanıcı
        self.assertTrue(self.izin.has_object_permission(istek, None, self.durumu1))
    

    def test_user_can_edit_own_status(self):
        # Kullanıcı kendi durumunu düzenleyebilir mi ?
        istek = self.factory.put("/fake-url/")
        istek.user = self.kullanici1
        self.assertTrue(self.izin.has_object_permission(istek, None, self.durumu1))


    def test_user_cannot_edit_other_status(self):
        # Kullanıcı bir başkasının durumunu düzenleyebilir mi ?
        istek = self.factory.put("/fake-url/")
        istek.user = self.kullanici2 # Farklı bir kullanıcı
        self.assertFalse(self.izin.has_object_permission(istek, None, self.durumu1))


    def test_user_can_delete_own_status(self):
        # Kullanıcı kendi durumunu silebilir mi ?
        istek = self.factory.delete("/fake-url/")
        istek.user = self.kullanici1
        self.assertTrue(self.izin.has_object_permission(istek, None, self.durumu1))
    

    def test_user_cannot_delete_other_status(self):
        # Kullanıcı başka birinin durumunu silebilir mi ?
        istek = self.factory.delete("/fake-url/")
        istek.user = self.kullanici2 # Farklı bir kullanıcı
        self.assertFalse(self.izin.has_object_permission(istek, None, self.durumu1))
    

    def test_user_can_create_status(self):
        # Kullanıcı kendi adına yeni bir durum oluşturabilir mi ?
        istek = self.factory.post("/fake-url/")
        istek.user = self.kullanici1
        self.assertTrue(self.izin.has_object_permission(istek, None, ProfilDurum(user_profil=self.profili1, durum_mesaji="Yeni durum")))


    def test_user_cannot_create_status_for_other(self):
        # Kullanıcı başkası adına yeni bir durum oluşturabilir mi ?
        istek = self.factory.post("/fake-url/")
        istek.user = self.kullanici2
        self.assertFalse(self.izin.has_object_permission(istek, None, ProfilDurum(user_profil=self.profili1, durum_mesaji="Başkası için yeni durum")))