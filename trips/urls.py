"""URLs de l'application trips."""
from django.urls import path

from . import views
from . import dashboard_views as dash

app_name = "trips"

urlpatterns = [
    # ---------- Site public ----------
    path("", views.home, name="home"),
    path("pourquoi-agrotrip/", views.pourquoi, name="pourquoi"),
    path("agrotrips/", views.tous_les_agrotrips, name="liste"),
    path("agrotrip/<slug:slug>/", views.agrotrip_detail, name="detail"),
    path("agrotrip/<slug:slug>/succes/", views.inscription_succes, name="inscription_succes"),

    # ---------- Tableau de bord (gestion) ----------
    path("gestion/connexion/", dash.connexion, name="gestion_connexion"),
    path("gestion/deconnexion/", dash.deconnexion, name="gestion_deconnexion"),
    path("gestion/", dash.accueil, name="gestion_accueil"),

    path("gestion/agrotrips/", dash.agrotrips, name="gestion_agrotrips"),
    path("gestion/agrotrips/ajouter/", dash.agrotrip_ajouter, name="gestion_agrotrip_ajouter"),
    path("gestion/agrotrips/<int:pk>/modifier/", dash.agrotrip_modifier, name="gestion_agrotrip_modifier"),
    path("gestion/agrotrips/<int:pk>/supprimer/", dash.agrotrip_supprimer, name="gestion_agrotrip_supprimer"),

    path("gestion/inscriptions/", dash.inscriptions, name="gestion_inscriptions"),
    path("gestion/inscriptions/<int:pk>/", dash.inscription_detail, name="gestion_inscription_detail"),

    path("gestion/pourquoi/", dash.pourquoi, name="gestion_pourquoi"),
    path("gestion/initiateurs/ajouter/", dash.initiateur_ajouter, name="gestion_initiateur_ajouter"),
    path("gestion/initiateurs/<int:pk>/modifier/", dash.initiateur_modifier, name="gestion_initiateur_modifier"),
    path("gestion/initiateurs/<int:pk>/supprimer/", dash.initiateur_supprimer, name="gestion_initiateur_supprimer"),
    path("gestion/partenaires/ajouter/", dash.partenaire_ajouter, name="gestion_partenaire_ajouter"),
    path("gestion/partenaires/<int:pk>/modifier/", dash.partenaire_modifier, name="gestion_partenaire_modifier"),
    path("gestion/partenaires/<int:pk>/supprimer/", dash.partenaire_supprimer, name="gestion_partenaire_supprimer"),
]
