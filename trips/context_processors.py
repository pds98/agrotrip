"""Variables disponibles dans tous les templates du tableau de bord."""
from .models import Registration


def gestion(request):
    """Nombre d'inscriptions non lues, pour le badge de la barre latérale."""
    if request.user.is_authenticated and request.user.is_staff:
        return {
            "nb_nouvelles_global": Registration.objects.filter(lu=False).count(),
        }
    return {}
