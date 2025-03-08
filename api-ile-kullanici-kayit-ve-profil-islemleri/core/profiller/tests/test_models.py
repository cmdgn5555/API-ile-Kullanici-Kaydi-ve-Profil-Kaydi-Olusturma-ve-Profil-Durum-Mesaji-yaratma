from django.test import TestCase
from django.contrib.auth import get_user_model
from profiller.models import Profil, ProfilDurum
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io


User = get_user_model()


class ProfilModelTest(TestCase):  
    
    def setUp(self):
        # Testler başlamadan önce çalışacak kod
        print("ProfilModelTest setUp çalıştı")
        self.kullanici = User.objects.create_user(username="software_developer", password="testpassword")
        self.profili = Profil.objects.create(user=self.kullanici, bio="Test biyografi", sehir="Ankara")

    
    def test_profil_olusturuldu_mu(self):
        # Profil modeli başarıyla oluşturuluyor mu ?
        self.assertEqual(self.profili.user.username, "software_developer", msg="Kullanıcı adı beklenen değeri karşılamıyor!")
        self.assertEqual(self.profili.bio, "Test biyografi", msg="Biyografi tanımı beklenen değeri karşılamıyor!")
        self.assertEqual(self.profili.sehir, "Ankara", msg="Şehir adı beklenen değeri karşılamıyor!")
    
    
    def test_profil_str_metodu(self):
        # Profil metodunun __str__ metodu doğru çalışıyor mu ?
        self.assertEqual(str(self.profili), "software_developer", msg="str metodu beklenen değeri karşılamıyor!")




class ProfilFotoResizeTest(TestCase):

    def setUp(self): 
        # Testler başlamadan önce çalışacak kod
        print("ProfilFotoResizeTest setUp çalıştı") 
        self.kullanici = User.objects.create_user(username="software_developer", password="testpassword")

    def test_profil_foto_resize(self): 
        image = Image.new("RGB", (1000, 1000), "pink") # 1000x1000 px sahte bir resim oluşturuyoruz
        image_io = io.BytesIO() # Bellekte sanal bir dosya açıyoruz
        image.save(image_io, format="JPEG")  # Resmi buraya kaydediyoruz
        image_io.seek(0) # Dosyanın başına giderek okuma işlemi için hazırlıyoruz
        
        # Sahte resmi Django'nun SimpleUploadedFile ile yükle
        uploaded_image = SimpleUploadedFile(name="testdeneme.jpg", content=image_io.getvalue(), content_type="image/jpeg")

        # Profili oluştur ve kaydet
        profil = Profil.objects.create(user=self.kullanici, foto=uploaded_image)

        # Fotoğrafı tekrar aç ve boyutlarını kontrol et
        img = Image.open(profil.foto.path)

        # Boyutun 600x600 olup olmadığını test et
        self.assertEqual(img.size, (600, 600))
        

        


class ProfilDurumModelTest(TestCase):
    
    def setUp(self):
        # Testler başlamadan önce çalışacak kod
        print("ProfilDurumModelTest setUp çalıştı")
        self.kullanici = User.objects.create_user(username="software_developer", password="testpassword")
        self.profili = Profil.objects.create(user=self.kullanici)
        self.durumu = ProfilDurum.objects.create(user_profil=self.profili, durum_mesaji="Test mesajı")
    
    
    def test_durum_mesaji_kaydediliyor_mu(self):
        # Profil durum mesajı başarıyla kaydediliyor mu ?
        self.assertEqual(self.durumu.durum_mesaji, "Test mesajı")
    
    
    def test_durum_str_metodu(self):
        # ProfilDurum modelinin __str__ metodu doğru çalışıyor mu ?
        self.assertEqual(str(self.durumu), "software_developer")