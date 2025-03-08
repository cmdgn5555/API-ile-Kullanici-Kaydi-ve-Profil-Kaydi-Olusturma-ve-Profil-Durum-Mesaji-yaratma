import django_filters
from profiller.models import Profil, ProfilDurum
from rest_framework import filters



class ProfilFilter(django_filters.FilterSet): 
    
    class Meta:
        model = Profil
        fields = {
            "bio": ["icontains"],
            "sehir": ["istartswith", "iendswith"]
        }



class ProfilDurumFilter(django_filters.FilterSet):

    class Meta:
        model = ProfilDurum
        fields = {
            "durum_mesaji": ["icontains"],
            "id": ["exact", "lt", "lte", "gt", "gte", "range"],
            "yaratilma_zamani": ["lt", "gt", "range"]
        }



class ProfilFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(sehir__icontains="u", bio__iendswith="r", user__username__istartswith="a")



class ProfilDurumFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(yaratilma_zamani__gte="2025-02-05T10:00:00.194485Z", user_profil__user__username="testuser", durum_mesaji__icontains="mesajıdır")