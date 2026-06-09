"""URLs principales du projet AgroTrip."""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

# Personnalisation des en-têtes de l'administration
admin.site.site_header = "AgroTrip — Administration"
admin.site.site_title = "AgroTrip Admin"
admin.site.index_title = "Tableau de bord de Yacine"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("trips.urls")),
]

# Servir les fichiers médias (photos uploadées) en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
