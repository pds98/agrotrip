"""URLs de l'application trips."""
from django.urls import path

from . import views

app_name = "trips"

urlpatterns = [
    path("", views.home, name="home"),
    path("agrotrips/", views.tous_les_agrotrips, name="liste"),
    path("agrotrip/<slug:slug>/", views.agrotrip_detail, name="detail"),
    path("agrotrip/<slug:slug>/succes/", views.inscription_succes, name="inscription_succes"),
]
