from django.urls import path, include
from profiller.api.views import ProfilViewSet, ProfilDurumViewSet, ProfilFotoUpdateView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'kullanici-profilleri', ProfilViewSet, basename="profiller")    
router.register(r'durum', ProfilDurumViewSet, basename="profil-durum")

# profil_list = ProfilViewSet.as_view({"get": "list"}) # get isteği gelirse tüm kayıtları listele
# profil_detay = ProfilViewSet.as_view({"get": "retrieve"}) # get isteği gelirse tek bir kaydı getir

urlpatterns = [
    # path("kullanici-profilleri/", profil_list, name="profiller"),    # "http://127.0.0.1:8000/api/kullanici-profilleri/" endpoint'ine get isteği yapınca tüm kayıtları listeler
    # path("kullanici-profilleri/<int:pk>", profil_detay, name="profil-detay")   # "http://127.0.0.1:8000/api/kullanici-profilleri/3" endpoint'ine get isteği yapınca id si 3 olan kaydı getirir

    path("", include(router.urls)),
    path("profil_foto/", ProfilFotoUpdateView.as_view(), name="profil-foto")
] 
