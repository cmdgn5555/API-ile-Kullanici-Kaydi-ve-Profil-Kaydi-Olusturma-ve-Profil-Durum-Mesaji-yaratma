from django.contrib.auth.models import User
from profiller.models import Profil, ProfilDurum
from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError


# Burda post_save sinyalini kullanarak bir kullanıcı kaydı
# oluşturduktan hemen sonra o kullanıcı ile ilgili bir 
# profil kaydı oluşturuyoruz

@receiver(post_save, sender=User)
def create_profil(sender, instance, created, **kwargs):
    print(instance.username, "__Created: ", created)    
    if created:
        Profil.objects.create(user=instance)



# Burda pre_save sinyalini kullanarak yukarıda User modelinde oluşturduğumuz
# kullanıcı kaydının akabinde Profil modelinde ilgili kullanıcı için oluşturulacak 
# profil kaydı için Profil modelindeki sehir ve bio alanlarını kontrol ediyoruz 
# eğer sehir alanı ve bio alanı boş ise yani User modelinde yeni bir kullanıcı kaydı 
# oluşturulurken bu alanlar manuel olarak doldurulmadıysa bu iki alan için sabit değerler atıyoruz 
# ve Profil modelinde ilgili kullanıcı için profil kaydını oluşturuyoruz


@receiver(pre_save, sender=Profil)
def assign_city_bio(sender, instance, **kwargs):
    if not instance.sehir:
        instance.sehir = "Ankara"
    if not instance.bio:
        instance.bio = f"Bu {instance.user.username} adlı kullanıcının biyografisidir"



# Burda pre_delete sinyalini kullanarak User modelinden silmek istediğimiz bir kullanıcı kaydı için
# silme işlemini gerçekleştirmeden önce ilgili kullanıcının Profil modelinde bir profil kaydı 
# olup olmadığını kontrol ediyoruz ve eğer User modelinden silmek istediğimiz kullanıcının 
# Profil modelinde mevcut bir profil kaydı var ise kullanıcının User modelinden silinmesini engelleyerek
# bir hata fırlatıyoruz ancak eğer kullanıcının Profil modelinde mevcut bir profil kaydı yoksa 
# ilgili kullanıcının kaydını User modelinden başarıyla siliyoruz


@receiver(pre_delete, sender=User)
def prevent_user_deletion_if_profile_exists(sender, instance, **kwargs):
    # Kullanıcıya bağlı bir profil var mı diye kontrol ediyoruz
    print(f"pre_delete sinyali çalıştı! Kullanıcı: {instance.username}")
    if Profil.objects.filter(user=instance).exists():
        print("Kullanıcı silinemez çünkü profili var!")
        # Hata fırlatarak silme işlemini iptal ediyoruz
        raise ValidationError(f"{instance.username} adlı kullanıcı silinemedi çünkü ilgili kullanıcıya ait bir profil kaydı mevcut!")



# Burda post_delete sinyalini kullanarak Profil modelinden bir kaydı sildikten sonra 
# ilgili silinen kaydın bio, sehir ve foto alanlarının boş olup olmadığını kontrol ediyoruz 
# eğer bio, sehir ve foto alanları boş ise bu alanlara
# Bio alanı boştu, Şehir alanı boştu, Foto alanı boştu şeklinde sabit string ifadelerini atıyoruz
# eğer bio, sehir ve foto alanları dolu ise mevcut değerlerini koruyoruz
# ve silinen Profil modeli kaydını txt dosyasına yazdırıyoruz


@receiver(post_delete, sender=Profil)
def check_bio_sehir_foto(sender, instance, **kwargs):

    # Yazılacak içerik
    content = (
        f"Profil nesnesi silindi - ID: {instance.id}, "
        f"Kullanıcı: {instance.user.username}, "
        f"Bio: {instance.bio if instance.bio else 'Bio alanı boştu'}, "
        f"Şehir: {instance.sehir if instance.sehir else 'Şehir alanı boştu'}, "
        f"Foto: {instance.foto if instance.foto else 'Foto alanı boştu'}\n"
    )

    # Dosyaya yazma işlemi
    with open("silinen_profiller.txt", "a", encoding="utf-8") as file: 
        file.write(content)


# Burda da yine post_save sinyalini kullanarak daha önceki post_save sinyalini kullandığımız senaryomuzda
# User modelinde oluşturduğumuz bir kullanıcı için Profil modelinde o kullanıcı için bir profil kaydı oluşturuyoduk 
# Şimdi de Profil modelinde oluşturulan profil kaydı için ProfilDurum modelini tetikliyoruz ve
# User modelinde oluşturulan kullanıcı için Profil modelinde oluşturulan profil kaydı nesnesi üzerinden 
# ProfilDurum modelinde bulunan durum mesajı alanına oluşturulan kullanıcının kullanıcı adını belirterek 
# bir durum mesajı string ifadesi belirliyoruz


@receiver(post_save, sender=Profil)
def create_ilk_durum_mesaji(sender, instance, created, **kwargs): 
    if created:
        ProfilDurum.objects.create(
            user_profil = instance,
            durum_mesaji = f"{instance.user.username} için durum mesajı oluşturuldu"
        )


    






