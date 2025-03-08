import django_filters
from django.test import TestCase
from profiller.models import Profil, ProfilDurum
from profiller.api.filters import ProfilFilter, ProfilDurumFilter, ProfilFilterBackend, ProfilDurumFilterBackend
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory


class ProfilFilterTests(TestCase):
    
    def setUp(self):
        # Testler için örnek veriler oluşturuyoruz
        self.kullanici1 = User.objects.create(username="Ahmet")
        self.kullanici2 = User.objects.create(username="Mehmet")
        self.profili1 = Profil.objects.create(user=self.kullanici1, bio="Python developer", sehir="Bursa")
        self.profili2 = Profil.objects.create(user=self.kullanici2, bio="Java developer", sehir="Samsun")
    
    
    def test_bio_filter(self): 
        # Bio içeriğine göre filtreleme test edilir
        sorgu_kümesi = Profil.objects.all()
        filtre = ProfilFilter(data={"bio__icontains": "java"}, queryset=sorgu_kümesi)
        self.assertEqual(filtre.qs.count(), 1)
        self.assertEqual(filtre.qs.first(), self.profili2)
    

    def test_sehir_filter_1(self):
        # Şehir adına göre istartswith ile filtreleme test edilir
        sorgu_kümesi = Profil.objects.all()
        filtre = ProfilFilter(data={"sehir__istartswith": "B"}, queryset=sorgu_kümesi)
        self.assertEqual(filtre.qs.count(), 1)
        self.assertEqual(filtre.qs.first(), self.profili1)
    

    def test_sehir_filter_2(self):
        # Şehir adına göre iendswith ile filtreleme test edilir
        sorgu_kümesi = Profil.objects.all() 
        filtre = ProfilFilter(data={"sehir__iendswith": "N"}, queryset=sorgu_kümesi)
        self.assertEqual(filtre.qs.count(), 1)
        self.assertEqual(filtre.qs.first(), self.profili2)


class ProfilDurumFilterTests(TestCase):

    def setUp(self):
        # Test verilerini oluşturuyoruz
        self.kullanici1 = User.objects.create(username="admin")
        self.kullanici2 = User.objects.create(username="ahmet")
        self.profili1 = Profil.objects.create(user=self.kullanici1, bio="Admin bio", sehir="Denizli")
        self.profili2 = Profil.objects.create(user=self.kullanici2, bio="Ahmet bio", sehir="Konya")
        self.durumu1 = ProfilDurum.objects.create(user_profil=self.profili1, durum_mesaji="Admin kullanıcısının ilk durum mesajıdır")
        self.durumu2 = ProfilDurum.objects.create(user_profil=self.profili2, durum_mesaji="Ahmet kullanıcısının yeni durum mesajıdır")
    

    def test_durum_mesaji_filter_1(self):
        # Durum mesajına göre filtreleme test edilir
        sorgu_kümesi = ProfilDurum.objects.all()
        filtre = ProfilDurumFilter(data={"durum_mesaji__icontains": "ilk"}, queryset=sorgu_kümesi)
        self.assertEqual(filtre.qs.count(), 1)
        self.assertEqual(filtre.qs.first(), self.durumu1)
    

    def test_durum_mesaji_filter_2(self):
        # Durum mesajına göre filtreleme test edilir
        sorgu_kümesi = ProfilDurum.objects.all()
        filtre = ProfilDurumFilter(data={"durum_mesaji__icontains": "Yeni"}, queryset=sorgu_kümesi)
        self.assertEqual(filtre.qs.count(), 1)
        self.assertEqual(filtre.qs.first(), self.durumu2)


class ProfilFilterBackendTests(TestCase):

    def setUp(self):
        # Test verilerini hazırlıyoruz
        self.kullanici1 = User.objects.create(username="admin")
        self.kullanici2 = User.objects.create(username="ahmet")
        self.kullanici3 = User.objects.create(username="ali")
        self.profili1 = Profil.objects.create(user=self.kullanici1, bio="Developer", sehir="Bursa")
        self.profili2 = Profil.objects.create(user=self.kullanici2, bio="Designer", sehir="Samsun")
        self.profili3 = Profil.objects.create(user=self.kullanici3, bio="Engineer", sehir="Ordu")
        self.factory = APIRequestFactory()


    def test_profil_filter_backend(self):
        # Özel ProfilFilterBackend filtreleme testi
        sorgu_kümesi = Profil.objects.all()
        istek = self.factory.get("/fake-url/")
        backend = ProfilFilterBackend()

        filtrelenmis_sorgu_kümesi = backend.filter_queryset(istek, sorgu_kümesi, None)
        #print(filtrelenmis_sorgu_kümesi)
        
        self.assertTrue(all("u" in p.sehir.lower() for p in filtrelenmis_sorgu_kümesi))
        self.assertTrue(all(p.bio.lower().endswith("r") for p in filtrelenmis_sorgu_kümesi))
        self.assertTrue(all(p.user.username.lower().startswith("a") for p in filtrelenmis_sorgu_kümesi))
        self.assertGreater(len(filtrelenmis_sorgu_kümesi), 0, msg="Filtreleme sonucu boş döndü! Test verilerini gözden geçirin.")


class ProfilDurumFilterBackendTests(TestCase):

    def setUp(self):
        # Test verilerini hazırlıyoruz
        self.kullanici1 = User.objects.create(username="admin")
        self.kullanici2 = User.objects.create(username="testuser")
        self.profili1 = Profil.objects.create(user=self.kullanici1, bio="Admin bio")
        self.profili2 = Profil.objects.create(user=self.kullanici2, bio="Test user bio")
        self.durumu1 = ProfilDurum.objects.create(user_profil=self.profili1, durum_mesaji="Admin adlı kullanıcının durum mesajı")
        self.durumu2 = ProfilDurum.objects.create(user_profil=self.profili2, durum_mesaji="Test user durum mesajıdır")
        self.factory = APIRequestFactory()

    
    def test_profil_durum_filter_backend(self):
        # Özel ProfilDurumFilterBackend filtreleme testi
        sorgu_kümesi = ProfilDurum.objects.all()
        istek = self.factory.get("/fake-url/")
        backend = ProfilDurumFilterBackend()
    
        filtrelenmis_sorgu_kümesi = backend.filter_queryset(istek, sorgu_kümesi, None)
        print(f"filtrelenmiş sorgu kümesi = {filtrelenmis_sorgu_kümesi}")

        self.assertGreater(len(filtrelenmis_sorgu_kümesi), 0, msg="Filtreleme sonucu boş döndü! Test verilerini gözden geçirin.")

        # Kullanıcı adı admin mi ?
        self.assertTrue(all(d.user_profil.user.username == "testuser" for d in filtrelenmis_sorgu_kümesi))

        # Durum mesajı içinde adlı kelimesi var mı ? 
        self.assertTrue(all("mesajıdır" in d.durum_mesaji for d in filtrelenmis_sorgu_kümesi))
        

        
        
        



        
