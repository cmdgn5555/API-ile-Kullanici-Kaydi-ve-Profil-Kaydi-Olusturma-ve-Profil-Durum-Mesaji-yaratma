from django.contrib.auth.models import User
from django.test import TestCase
from profiller.models import Profil, ProfilDurum
from profiller.api.serializers import ProfilSerializer, ProfilFotoSerializer, ProfilDurumSerializer
from dateutil.parser import parse


class ProfilSerializerTest(TestCase):

    def setUp(self):
        # Testlerden önce çalışacak ayarlar
        print("ProfilSerializerTest setUp çalıştı")
        self.kullanici = User.objects.create_user(username="software_developer", password="testpassword")
        self.profili = Profil.objects.create(user=self.kullanici, bio="Test biyografi", sehir="Ankara")

    
    def test_profil_serializer(self):
        # ProfilSerializer'ın doğru çalışıp çalışmadığını test ediyoruz
        serializer = ProfilSerializer(instance=self.profili)

        # Beklenen veri
        expected_data = {
            "kullanici": self.kullanici.username,
            "biyografi": "Test biyografi",
            "sehir_adi": "Ankara",
        }

        # expected_data ile serializer verisini karşılaştıralım
        self.assertEqual(serializer.data["user"], expected_data["kullanici"])
        self.assertEqual(serializer.data["bio"], expected_data["biyografi"])
        self.assertEqual(serializer.data["sehir"], expected_data["sehir_adi"])




class ProfilFotoSerializerTest(TestCase):

    def setUp(self):
        # Testlerden önce çalışacak ayarlar
        print("ProfilFotoSerializerTest setUp çalıştı")
        self.kullanici = User.objects.create_user(username="software_developer", password="testpassword")
        self.profili = Profil.objects.create(user=self.kullanici)
    

    def test_profil_foto_serializer(self):
        # ProfilFotoSerializer sadece foto alanını içermeli
        serializer = ProfilFotoSerializer(instance=self.profili)
        
        # Beklenen alan
        self.assertEqual(serializer.data, {"foto": serializer.data["foto"]})




class ProfilDurumSerializerTest(TestCase):

    def setUp(self):
        # Testlerden önce çalışacak ayarlar
        print("ProfilDurumSerializerTest setUp çalıştı")
        self.kullanici = User.objects.create_user(username="software_developer", password="testpassword")
        self.profili = Profil.objects.create(user=self.kullanici)
        self.durumu = ProfilDurum.objects.create(user_profil=self.profili, durum_mesaji="Test mesajı")
    

    def test_profil_durum_serializer(self):  
        # ProfilDurumSerializer'ın doğru çalışıp çalışmadığını test ediyoruz
        serializer = ProfilDurumSerializer(instance=self.durumu)
        
        # Beklenen veri
        expected_data = {
            "kullanici_profili": self.kullanici.username,
            "durum_mesaji_bilgisi": "Test mesajı",
            "yaratilma_zamani_bilgisi": self.durumu.yaratilma_zamani.isoformat(), 
            "guncellenme_zamani_bilgisi": self.durumu.guncellenme_zamani.isoformat() 
        }

        # expected_data ile serializer verisini karşılaştıralım
        self.assertEqual(serializer.data["user_profil"], expected_data["kullanici_profili"]) 
        self.assertEqual(serializer.data["durum_mesaji"], expected_data["durum_mesaji_bilgisi"])
        self.assertEqual(parse(serializer.data["yaratilma_zamani"]), parse(expected_data["yaratilma_zamani_bilgisi"]))
        self.assertEqual(parse(serializer.data["guncellenme_zamani"]), parse(expected_data["guncellenme_zamani_bilgisi"]))
        
        
        
        

        

        