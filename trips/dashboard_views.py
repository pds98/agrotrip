"""
Tableau de bord simplifié pour la CEO Yacine.

Interface claire en français (séparée de l'admin Django) permettant de gérer
seule : AgroTrips, inscriptions, page « Pourquoi AgroTrip », initiateurs et
partenaires. Toutes les vues sont protégées par connexion (staff requis).
"""
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import (
    AgroTripForm, InitiateurForm, PartenaireForm, AProposForm,
    TripPhotoForm, TripVideoForm,
)
from .models import (
    AgroTrip, Registration, APropos, Initiateur, Partenaire,
    TripPhoto, TripVideo,
)


# Seuls les membres du staff (dont les super-utilisateurs) accèdent au dashboard.
def _staff(user):
    return user.is_active and user.is_staff


staff_requis = user_passes_test(_staff, login_url="trips:gestion_connexion")


# --------------------------------------------------------------------------
# CONNEXION / DÉCONNEXION
# --------------------------------------------------------------------------
def connexion(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("trips:gestion_accueil")
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        if user.is_staff:
            login(request, user)
            return redirect("trips:gestion_accueil")
        messages.error(request, "Ce compte n'a pas accès à la gestion.")
    return render(request, "gestion/connexion.html", {"form": form})


def deconnexion(request):
    logout(request)
    return redirect("trips:gestion_connexion")


# --------------------------------------------------------------------------
# ACCUEIL DU TABLEAU DE BORD
# --------------------------------------------------------------------------
@staff_requis
def accueil(request):
    today = timezone.localdate()
    context = {
        "nb_a_venir": AgroTrip.objects.filter(date_debut__gte=today).count(),
        "nb_passes": AgroTrip.objects.filter(date_debut__lt=today).count(),
        "nb_inscriptions": Registration.objects.count(),
        "nb_nouvelles": Registration.objects.filter(lu=False).count(),
        "dernieres": Registration.objects.all()[:8],
        "prochains": AgroTrip.objects.filter(date_debut__gte=today).order_by("date_debut")[:5],
        "rubrique": "accueil",
    }
    return render(request, "gestion/accueil.html", context)


# --------------------------------------------------------------------------
# AGROTRIPS
# --------------------------------------------------------------------------
@staff_requis
def agrotrips(request):
    return render(request, "gestion/agrotrips.html", {
        "agrotrips": AgroTrip.objects.all(),
        "rubrique": "agrotrips",
    })


@staff_requis
def agrotrip_ajouter(request):
    form = AgroTripForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        trip = form.save()
        messages.success(request, f"L'AgroTrip « {trip.titre} » a été créé.")
        return redirect("trips:gestion_agrotrips")
    return render(request, "gestion/agrotrip_form.html", {
        "form": form, "titre_page": "Ajouter un AgroTrip", "rubrique": "agrotrips",
    })


@staff_requis
def agrotrip_modifier(request, pk):
    trip = get_object_or_404(AgroTrip, pk=pk)
    form = AgroTripForm(request.POST or None, request.FILES or None, instance=trip)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"L'AgroTrip « {trip.titre} » a été modifié.")
        return redirect("trips:gestion_agrotrips")
    return render(request, "gestion/agrotrip_form.html", {
        "form": form, "titre_page": f"Modifier : {trip.titre}", "objet": trip,
        "rubrique": "agrotrips",
        "photo_form": TripPhotoForm(),
        "video_form": TripVideoForm(),
        "photos": trip.photos.all(),
        "videos": trip.videos.all(),
    })


# ----- Photos d'un AgroTrip -----
@staff_requis
def photo_ajouter(request, pk):
    trip = get_object_or_404(AgroTrip, pk=pk)
    if request.method == "POST":
        form = TripPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.agrotrip = trip
            photo.save()
            messages.success(request, "Photo ajoutée.")
    return redirect("trips:gestion_agrotrip_modifier", pk=trip.pk)


@staff_requis
def photo_supprimer(request, pk):
    photo = get_object_or_404(TripPhoto, pk=pk)
    trip_pk = photo.agrotrip.pk
    photo.delete()
    messages.success(request, "Photo supprimée.")
    return redirect("trips:gestion_agrotrip_modifier", pk=trip_pk)


# ----- Vidéos d'un AgroTrip -----
@staff_requis
def video_ajouter(request, pk):
    trip = get_object_or_404(AgroTrip, pk=pk)
    if request.method == "POST":
        form = TripVideoForm(request.POST)
        if form.is_valid():
            video = form.save(commit=False)
            video.agrotrip = trip
            video.save()
            messages.success(request, "Vidéo ajoutée.")
        else:
            messages.error(request, "Lien de vidéo invalide.")
    return redirect("trips:gestion_agrotrip_modifier", pk=trip.pk)


@staff_requis
def video_supprimer(request, pk):
    video = get_object_or_404(TripVideo, pk=pk)
    trip_pk = video.agrotrip.pk
    video.delete()
    messages.success(request, "Vidéo supprimée.")
    return redirect("trips:gestion_agrotrip_modifier", pk=trip_pk)


@staff_requis
def agrotrip_supprimer(request, pk):
    trip = get_object_or_404(AgroTrip, pk=pk)
    if request.method == "POST":
        nom = trip.titre
        trip.delete()
        messages.success(request, f"L'AgroTrip « {nom} » a été supprimé.")
        return redirect("trips:gestion_agrotrips")
    return render(request, "gestion/confirmer_suppression.html", {
        "objet": trip, "type": "l'AgroTrip", "retour": "trips:gestion_agrotrips",
        "rubrique": "agrotrips",
    })


# --------------------------------------------------------------------------
# INSCRIPTIONS
# --------------------------------------------------------------------------
@staff_requis
def inscriptions(request):
    return render(request, "gestion/inscriptions.html", {
        "inscriptions": Registration.objects.select_related("agrotrip").all(),
        "rubrique": "inscriptions",
    })


@staff_requis
def inscription_detail(request, pk):
    insc = get_object_or_404(Registration, pk=pk)
    if not insc.lu:
        insc.lu = True
        insc.save(update_fields=["lu"])
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "confirmer":
            insc.statut = Registration.STATUT_CONFIRMEE
            insc.save()
            messages.success(request, "Inscription confirmée.")
        elif action == "annuler":
            insc.statut = Registration.STATUT_ANNULEE
            insc.save()
            messages.success(request, "Inscription annulée.")
        elif action == "supprimer":
            insc.delete()
            messages.success(request, "Inscription supprimée.")
            return redirect("trips:gestion_inscriptions")
        return redirect("trips:gestion_inscription_detail", pk=insc.pk)
    return render(request, "gestion/inscription_detail.html", {
        "insc": insc, "rubrique": "inscriptions",
    })


# --------------------------------------------------------------------------
# PAGE « POURQUOI AGROTRIP »
# --------------------------------------------------------------------------
@staff_requis
def pourquoi(request):
    apropos = APropos.charger()
    form = AProposForm(request.POST or None, instance=apropos)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Le contenu de la page a été enregistré.")
        return redirect("trips:gestion_pourquoi")
    return render(request, "gestion/pourquoi.html", {
        "form": form,
        "initiateurs": Initiateur.objects.all(),
        "partenaires": Partenaire.objects.all(),
        "rubrique": "pourquoi",
    })


# ----- Initiateurs -----
@staff_requis
def initiateur_ajouter(request):
    form = InitiateurForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Initiateur ajouté.")
        return redirect("trips:gestion_pourquoi")
    return render(request, "gestion/objet_form.html", {
        "form": form, "titre_page": "Ajouter un initiateur",
        "retour": "trips:gestion_pourquoi", "rubrique": "pourquoi",
    })


@staff_requis
def initiateur_modifier(request, pk):
    obj = get_object_or_404(Initiateur, pk=pk)
    form = InitiateurForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Initiateur modifié.")
        return redirect("trips:gestion_pourquoi")
    return render(request, "gestion/objet_form.html", {
        "form": form, "titre_page": f"Modifier : {obj.nom}",
        "retour": "trips:gestion_pourquoi", "rubrique": "pourquoi",
    })


@staff_requis
def initiateur_supprimer(request, pk):
    obj = get_object_or_404(Initiateur, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Initiateur supprimé.")
        return redirect("trips:gestion_pourquoi")
    return render(request, "gestion/confirmer_suppression.html", {
        "objet": obj, "type": "l'initiateur", "retour": "trips:gestion_pourquoi",
    })


# ----- Partenaires -----
@staff_requis
def partenaire_ajouter(request):
    form = PartenaireForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Partenaire ajouté.")
        return redirect("trips:gestion_pourquoi")
    return render(request, "gestion/objet_form.html", {
        "form": form, "titre_page": "Ajouter un partenaire",
        "retour": "trips:gestion_pourquoi", "rubrique": "pourquoi",
    })


@staff_requis
def partenaire_modifier(request, pk):
    obj = get_object_or_404(Partenaire, pk=pk)
    form = PartenaireForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Partenaire modifié.")
        return redirect("trips:gestion_pourquoi")
    return render(request, "gestion/objet_form.html", {
        "form": form, "titre_page": f"Modifier : {obj.nom}",
        "retour": "trips:gestion_pourquoi", "rubrique": "pourquoi",
    })


@staff_requis
def partenaire_supprimer(request, pk):
    obj = get_object_or_404(Partenaire, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Partenaire supprimé.")
        return redirect("trips:gestion_pourquoi")
    return render(request, "gestion/confirmer_suppression.html", {
        "objet": obj, "type": "le partenaire", "retour": "trips:gestion_pourquoi",
    })
