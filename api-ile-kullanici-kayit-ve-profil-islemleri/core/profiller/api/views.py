from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from profiller.models import Profil, ProfilDurum
from profiller.api.serializers import ProfilSerializer, ProfilDurumSerializer, ProfilFotoSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from profiller.api.permissions import KendiProfiliYadaReadOnly, DurumSahibiYadaReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from profiller.api.filters import ProfilFilter, ProfilDurumFilter, ProfilFilterBackend, ProfilDurumFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
import logging


logger = logging.getLogger("django")

class ProfilViewSet(ModelViewSet):  
    serializer_class = ProfilSerializer
    permission_classes = [IsAuthenticated]    
    #filter_backends = [ProfilFilterBackend]
    #search_fields = ["sehir", "bio"]
    #ordering_fields = ["id"]
    #filterset_class = ProfilFilter
    filterset_fields = ["sehir", "bio", "user"]
    #authentication_classes = [TokenAuthentication]

    def list(self, request, *args, **kwargs):
        logger.info(f"User {request.user.username} retrieved their profile.")
        return super().list(request, *args, **kwargs)
    

    def create(self, request, *args, **kwargs):
        logger.info(f"User {request.user.username} created a new profile.")
        return super().create(request, *args, **kwargs)
    
    
    def get_queryset(self):
        sorgu_kümesi = Profil.objects.all()
        
        # Şehir filtresi
        sehir_adi = self.request.query_params.get("city", None)
        if sehir_adi is not None:
            sorgu_kümesi = sorgu_kümesi.filter(sehir__icontains = sehir_adi)
        
        # Biyografi filtresi
        bio_icerik = self.request.query_params.get("biography", None)
        if bio_icerik is not None:
            sorgu_kümesi = sorgu_kümesi.filter(bio__icontains = bio_icerik)

        return sorgu_kümesi
        
    


class ProfilDurumViewSet(ModelViewSet):     
    serializer_class = ProfilDurumSerializer
    permission_classes = [IsAuthenticated, DurumSahibiYadaReadOnly]
    filter_backends = [DjangoFilterBackend]
    #search_fields = ["user_profil__user__username", "durum_mesaji"]
    #ordering_fields = ["yaratilma_zamani"]
    #filterset_class = ProfilDurumFilter
    filterset_fields = ["id", "user_profil__user__username"]

    
    def get_queryset(self):
        sorgu_kümesi = ProfilDurum.objects.all()
        kullanici_adi = self.request.query_params.get("username", None)
        if kullanici_adi is not None:
            sorgu_kümesi = sorgu_kümesi.filter(user_profil__user__username = kullanici_adi) 
        return sorgu_kümesi

    
    def perform_create(self, serializer):
        kullanici_profili = self.request.user.profil
        serializer.save(user_profil=kullanici_profili)




class ProfilFotoUpdateView(generics.UpdateAPIView):   
    serializer_class = ProfilFotoSerializer
    permission_classes = [IsAuthenticated]


    def get_object(self):
        profil_nesnesi = self.request.user.profil
        return profil_nesnesi

