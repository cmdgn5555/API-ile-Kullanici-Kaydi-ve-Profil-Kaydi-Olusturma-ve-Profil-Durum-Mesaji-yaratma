from django.test import TestCase
from django.contrib.auth.models import User
from profiller.models import Profil, ProfilDurum
from django.core.exceptions import ValidationError
import os


class ProfilPostSaveSignalTestCase(TestCase):

    def test_profil_olusturma(self):
        # Post_save sinyali sayesinde yeni bir User nesnesi oluşturulduğunda, otomatik olarak bir Profil nesnesi oluşturulmalı
        
        # Kullanıcı oluşturuyoruz
        kullanici = User.objects.create(username="testuser")
        
        # Kullanıcının profilinin olup olmadığını kontrol ediyoruz
        profil_var_mi = Profil.objects.filter(user=kullanici).exists()
        
        # Profil otomatik oluşturulmuş mu ?
        self.assertTrue(profil_var_mi, msg="Kullanıcı oluşturulduğunda profil otomatik olarak oluşturulmadı!")
    
    
    
    def test_profil_tekrar_olusturulmuyor(self):
        # Var olan bir User nesnesi güncellendiğinde, yeni bir Profil nesnesi oluşturulmamalı

        # Kullanıcı oluşturuyoruz
        kullanici = User.objects.create(username="testuser")

        # Kullanıcı adını güncelleyeliyoruz
        kullanici.username = "updated_user"
        kullanici.save() # post_save tekrar çalışacak ama created = False olduğu için yeni profil eklememeli

        # Kullanıcının hala sadece 1 profil kaydı olmalı
        profil_sayisi = Profil.objects.filter(user=kullanici).count()

        self.assertEqual(profil_sayisi, 1, msg="Kullanıcı güncellendiğinde yeni bir profil oluşturulmamalı!")        





class ProfilPreSaveSignalTestCase(TestCase):

    def test_profil_varsayilan_sehir_ve_bio(self):
        # Yeni bir kullanıcı oluşturduğumuzda pre_save sinyali sehir ve bio alanlarını boş ise otomatik olarak doldurmalı

        # Yeni bir kullanıcı oluşturuyoruz
        kullanici = User.objects.create(username="testuser2")

        # Kullanıcı oluşturulduğu için otomatik bir Profil kaydı da oluşturulacak
        profil = Profil.objects.get(user=kullanici) # Profil'i çekiyoruz

        # pre_save sinyali sayesinde sehir ve bio alanları boş olmamalı
        self.assertEqual(profil.sehir, "Ankara", msg="Profil kaydedildiğinde varsayılan şehir Ankara olmalıdır!")
        self.assertEqual(profil.bio, "Bu testuser2 adlı kullanıcının biyografisidir", msg="Profil kaydedildiğinde varsayılan bio atanmalı!")
       
    
    
    def test_profil_sehir_ve_bio_dolu_gelirse(self):
        # Kullanıcı profili oluşturulurken sehir ve bio önceden ayarlanmışsa pre_save sinyali bunları değiştirmemeli

        # Kullanıcıyı oluşturuyoruz
        kullanici = User.objects.create(username="testuser3")
        
        # Kullanıcının mevcut profilini alıyoruz
        profil = Profil.objects.get(user=kullanici)
        
        # Kullanıcıyı oluşturduğumuz anda o kullanıcı ile ilgili Profil modelinden bir profil kaydı
        # otomatik olarak oluşturulduğu için başlangıçta sehir ve bio alanları boş olarak geliyo
        # bu alanlar boş olarak geldiği için pre_save sinyali sayesinde sehir alanına Ankara 
        # bio alanına da Bu ... adlı kullanıcının biyografisidir şeklinde atamalar yapılıyo
        # Sehir ve bio alanlarını manuel olarak değiştiriyoruz
        profil.sehir = "İstanbul"
        profil.bio = "Bu özel bir biyografidir"
        profil.save() # Kaydediyoruz (pre_save burada tekrar çalışacak)
        
        # Pre_save sinyali, dolu olan sehir ve bio alanlarını değiştirmemeli
        self.assertEqual(profil.sehir, "İstanbul", msg="Önceden ayarlanmış şehir değişmemeli")
        self.assertEqual(profil.bio, "Bu özel bir biyografidir", msg="Önceden ayarlanmış bio değişmemeli")





class ProfilPreDeleteSignalTestCase(TestCase):

    def test_kullanici_profili_varken_silinmemeli(self):
        
        # Kullanıcı oluşturuyoruz
        kullanici = User.objects.create(username="testuser4")
        
        # Kullanıcıya ait profil otomatik olarak oluşturuluyor mu ? Kontrol ediyoruz
        profil = Profil.objects.get(user=kullanici)
        self.assertIsNotNone(profil, msg="Kullanıcı oluşturulduğunda profil de oluşturulmalıdır!")
        
        # Kullanıcıyı silmeye çalış ve hata almasını bekle
        with self.assertRaises(ValidationError) as hata:
            kullanici.delete()
        print(f"hata = {hata.exception}")
        
        # Dönen hata mesajını kontrol ediyoruz
        self.assertIn("testuser4 adlı kullanıcı silinemedi", str(hata.exception), msg="Hata mesajı doğru olmalıdır!")
        




class ProfilPostDeleteSignalTestCase(TestCase):

    def setUp(self):
        # Test için bir kullanıcı oluşturuyoruz o kullanıcıya bağlı profil modelinden 
        # bir profil nesnesi zaten post_save sinyali sayesinde otomatik olarak oluşturuluyor
        self.kullanici = User.objects.create(username="testuser5")
        self.profili = Profil.objects.get(user=self.kullanici) # Profil modelinden kullanıcının profil kaydını çekiyoruz
        
    
    
    def test_profil_silindiginde_dosya_guncellenmeli(self):
        # Profil silindiğinde bilgilerin dosyaya yazıldığını doğrular
        dosya_yolu = "silinen_profiller.txt"
        
        # Test başlamadan önce dosya varsa içeriğini temizleyelim
        if os.path.exists(dosya_yolu):
            open(dosya_yolu, "w").close()
        
        # Profili silelim bu aşamada post_delete sinyalimiz tetikleniyo
        self.profili.delete()

        # Dosyanın gerçekten güncellenip güncellenmediğini kontrol edelim
        self.assertTrue(os.path.exists(dosya_yolu), msg="Dosya oluşturulmuş olmalıdır")
        
        # Dosyanın içeriğini okuyalım
        with open(dosya_yolu, "r", encoding="utf-8") as file:
            icerik = file.read()
            
        # İçeriğin doğru formatta olup olmadığını kontrol edelim
        self.assertIn("Profil nesnesi silindi - ID: 1", icerik, msg="Dosyada silinen profil bilgisi bulunmalıdır!")
        self.assertIn("Kullanıcı: testuser5", icerik, msg="Silinen profilin kullanıcı adı dosyada bulunmalıdır!")





class ProfilDurumPostSaveSignalTestCase(TestCase):

    def test_profil_olusturuldugunda_profil_durum_olusturuluyor(self):
        # Bir profil oluşturulduğunda, otomatik olarak bir ProfilDurum nesnesi oluşturulmalı

        # Kullanıcı oluşturuyoruz
        kullanici = User.objects.create(username="testuser6")

        # Kullanıcı için otomatik oluşturulan profili alalım
        profil = Profil.objects.get(user=kullanici)

        # ProfilDurum nesnesi oluşmuş mu ?
        profil_durum_var_mi = ProfilDurum.objects.filter(user_profil=profil).exists()

        self.assertTrue(profil_durum_var_mi, msg="Profil oluşturulduğunda otomatik olarak ProfilDurum oluşturulmadı!")
    

    
    def test_profil_guncellendiginde_yeni_profil_durum_olusturulmuyor(self):
        # Mevcut bir profil güncellendiğinde, yeni bir ProfilDurum nesnesi oluşturulmamalı

        # Kullanıcı oluşturuyoruz
        kullanici = User.objects.create(username="testuser6")

        # Kullanıcı için otomatik oluşturulan profili alalım
        profil = Profil.objects.get(user=kullanici)
        
        # ProfilDurum nesnesi ilk kez oluşturulduğunda kayıt sayısını alalım
        ilk_profil_durum_sayisi = ProfilDurum.objects.filter(user_profil=profil).count()
        
        # Profili güncelleyelim
        profil.save() # post_save tekrar çalışır ama created = False olduğu için yeni bir durum eklenmemeli

       # Güncelleme sonrası profil durumlarının sayısını tekrar kontrol edelim
        son_profil_durum_sayisi = ProfilDurum.objects.filter(user_profil=profil).count()

        self.assertEqual(ilk_profil_durum_sayisi, son_profil_durum_sayisi, msg="Profil güncellendiğinde yeni bir ProfilDurum nesnesi oluşturulmamalı!")
    


    def test_profil_durum_mesaji_dogru_olusturuluyor(self):
        # ProfilDurum nesnesinin durum mesajı doğru bir şekilde oluşturulmalı

        # Kullanıcı oluşturuyoruz
        kullanici = User.objects.create(username="testuser6")

        # Kullanıcının profilini alalım
        profil = Profil.objects.get(user=kullanici)

        # Kullanıcıya ait ProfilDurum nesnesini alalım
        profil_durum = ProfilDurum.objects.get(user_profil=profil)
        
        # Beklenen mesajı oluştur
        beklenen_mesaj = f"{kullanici.username} için durum mesajı oluşturuldu"

        self.assertEqual(profil_durum.durum_mesaji, beklenen_mesaj, msg="Oluşturulan ProfilDurum mesajı hatalı!")