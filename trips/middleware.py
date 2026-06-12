"""Middlewares personnalisés du site AgroTrip."""
import time

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse


class InactiviteMiddleware:
    """
    Déconnecte automatiquement un utilisateur du tableau de bord après une
    période d'inactivité (sécurité). Ne concerne que les pages /gestion/.
    Durée configurable via GESTION_TIMEOUT_MINUTES dans settings.py.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        chemin = request.path
        connexion_url = reverse("trips:gestion_connexion")

        if (
            request.user.is_authenticated
            and request.user.is_staff
            and chemin.startswith("/gestion/")
            and chemin != connexion_url
        ):
            timeout = getattr(settings, "GESTION_TIMEOUT_MINUTES", 30) * 60
            maintenant = time.time()
            derniere = request.session.get("derniere_activite")

            if derniere and (maintenant - derniere) > timeout:
                logout(request)
                messages.error(
                    request,
                    "Vous avez été déconnecté(e) pour cause d'inactivité. "
                    "Merci de vous reconnecter.",
                )
                return redirect("trips:gestion_connexion")

            request.session["derniere_activite"] = maintenant

        return self.get_response(request)
