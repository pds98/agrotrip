"""Variables disponibles dans tous les templates du tableau de bord."""
from django.conf import settings

from .models import Registration


def gestion(request):
    """Infos communes au tableau de bord : badge de notifications + délai d'inactivité."""
    if request.user.is_authenticated and request.user.is_staff:
        return {
            "nb_nouvelles_global": Registration.objects.filter(lu=False).count(),
            "gestion_timeout_minutes": getattr(
                settings, "GESTION_TIMEOUT_MINUTES", 30
            ),
        }
    return {}
