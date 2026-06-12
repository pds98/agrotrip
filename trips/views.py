"""Vues du site AgroTrip."""
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import RegistrationForm
from .models import AgroTrip, Registration, APropos, Initiateur, Partenaire


def home(request):
    """Page d'accueil : slider, AgroTrips passés, AgroTrips à venir."""
    today = timezone.localdate()
    publies = AgroTrip.objects.filter(statut=AgroTrip.STATUT_PUBLIE)

    slides = publies.filter(a_la_une=True)
    if not slides:
        # Repli : on met les AgroTrips à venir dans le slider
        slides = publies.filter(date_debut__gte=today)[:4]

    passes = publies.filter(date_debut__lt=today).order_by("-date_debut")
    a_venir = publies.filter(date_debut__gte=today).order_by("date_debut")[:5]

    context = {
        "slides": slides,
        "agrotrips_passes": passes,
        "agrotrips_a_venir": a_venir,
    }
    return render(request, "trips/home.html", context)


def pourquoi(request):
    """Page « Pourquoi AgroTrip » : explication, mission, initiateurs, partenaires."""
    context = {
        "apropos": APropos.charger(),
        "initiateurs": Initiateur.objects.all(),
        "partenaires": Partenaire.objects.all(),
    }
    return render(request, "trips/pourquoi.html", context)


def agrotrip_detail(request, slug):
    """Page détaillée d'un AgroTrip + formulaire d'inscription si à venir."""
    agrotrip = get_object_or_404(AgroTrip, slug=slug)

    form = None
    if agrotrip.est_a_venir and not agrotrip.complet:
        if request.method == "POST":
            form = RegistrationForm(request.POST, agrotrip=agrotrip)
            if form.is_valid():
                inscription = form.save(commit=False)
                inscription.agrotrip = agrotrip
                inscription.save()
                _envoyer_emails(inscription)
                messages.success(
                    request,
                    "Votre inscription a bien été enregistrée. "
                    "Un email de confirmation vous a été envoyé.",
                )
                return redirect("trips:inscription_succes", slug=agrotrip.slug)
        else:
            form = RegistrationForm(agrotrip=agrotrip)

    context = {
        "agrotrip": agrotrip,
        "form": form,
    }
    return render(request, "trips/agrotrip_detail.html", context)


def inscription_succes(request, slug):
    """Page de confirmation après inscription."""
    agrotrip = get_object_or_404(AgroTrip, slug=slug)
    return render(request, "trips/inscription_succes.html", {"agrotrip": agrotrip})


def tous_les_agrotrips(request):
    """Liste complète des AgroTrips (passés et à venir)."""
    today = timezone.localdate()
    publies = AgroTrip.objects.filter(statut=AgroTrip.STATUT_PUBLIE)
    context = {
        "a_venir": publies.filter(date_debut__gte=today).order_by("date_debut"),
        "passes": publies.filter(date_debut__lt=today).order_by("-date_debut"),
    }
    return render(request, "trips/liste.html", context)


# --------------------------------------------------------------------------
# Utilitaire d'envoi d'emails (client + notification CEO)
# --------------------------------------------------------------------------
def _envoyer_emails(inscription):
    """Envoie l'email de confirmation au client et notifie la CEO."""
    trip = inscription.agrotrip

    # 1) Email de confirmation au client
    sujet_client = f"Confirmation de votre inscription — {trip.titre}"
    corps_client = (
        f"Bonjour {inscription.prenom},\n\n"
        f"Merci pour votre inscription à l'AgroTrip « {trip.titre} » !\n\n"
        f"Récapitulatif :\n"
        f"  • Lieu : {trip.lieu}\n"
        f"  • Date : {trip.date_debut:%d/%m/%Y}\n"
        f"  • Nombre de places : {inscription.nombre_places}\n"
        f"  • Prix : {trip.prix:,.0f} FCFA / place\n\n"
        f"Notre équipe vous contactera bientôt pour finaliser les détails.\n\n"
        f"À très vite,\n"
        f"L'équipe AgroTrip — L'agriculture en immersion"
    ).replace(",", " ")

    # 2) Notification à la CEO Yacine
    sujet_admin = f"🔔 Nouvelle inscription — {trip.titre}"
    corps_admin = (
        f"Nouvelle inscription reçue :\n\n"
        f"  • Client : {inscription.nom_complet}\n"
        f"  • Téléphone : {inscription.telephone}\n"
        f"  • Email : {inscription.email}\n"
        f"  • AgroTrip : {trip.titre}\n"
        f"  • Places : {inscription.nombre_places}\n"
        f"  • Message : {inscription.message or '(aucun)'}\n\n"
        f"Connectez-vous à l'administration pour gérer cette inscription."
    )

    try:
        send_mail(
            sujet_client, corps_client,
            settings.DEFAULT_FROM_EMAIL, [inscription.email],
            fail_silently=True,
        )
        send_mail(
            sujet_admin, corps_admin,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_NOTIFICATION_EMAIL],
            fail_silently=True,
        )
    except Exception:
        # On n'interrompt jamais l'inscription si l'email échoue.
        pass
