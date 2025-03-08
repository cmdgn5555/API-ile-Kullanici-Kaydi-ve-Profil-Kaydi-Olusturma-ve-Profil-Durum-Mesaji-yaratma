from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.


class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profil")
    bio = models.CharField(max_length=500, blank=True, null=True)
    sehir = models.CharField(max_length=100, blank=True, null=True)
    foto = models.ImageField(null=True, blank=True, upload_to="profil_fotolari/%Y/%m/")

    def __str__(self):
        return self.user.username
    
    
    class Meta:
        verbose_name_plural = "Profiller"
    

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Eğer resim mevcutsa resmi boyutlandırıyoruz
        if self.foto:
            img = Image.open(self.foto.path)
            if img.height > 600 or img.width > 600:
                output_size = (600, 600)
                img.thumbnail(output_size) 
                img.save(self.foto.path)



class ProfilDurum(models.Model):
    user_profil = models.ForeignKey(Profil, on_delete=models.CASCADE)
    durum_mesaji = models.CharField(max_length=250)
    yaratilma_zamani = models.DateTimeField(auto_now_add=True)
    guncellenme_zamani = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user_profil.user.username)
    
    
    class Meta:
        verbose_name_plural = "Profil Mesajları"