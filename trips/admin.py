"""
Administration AgroTrip — tableau de bord de la CEO Yacine.

Admin Django amélioré : aperçu des images, badges de statut, compteur de
notifications de nouvelles inscriptions, actions groupées, etc.
"""
from django.contrib import admin
from django.utils.html import format_html

from .models import (
    AgroTrip, TripPhoto, TripVideo, Testimonial, Registration,
    APropos, Initiateur, Partenaire,
)


class TripPhotoInline(admin.TabularInline):
    model = TripPhoto
    extra = 1
    fields = ("image", "image_url", "legende")


class TripVideoInline(admin.TabularInline):
    model = TripVideo
    extra = 1
    fields = ("video_url", "titre", "ordre")


class TestimonialInline(admin.StackedInline):
    model = Testimonial
    extra = 1
    fields = ("auteur", "note", "texte")


@admin.register(AgroTrip)
class AgroTripAdmin(admin.ModelAdmin):
    list_display = (
        "apercu", "titre", "lieu", "date_debut",
        "prix_affiche", "periode_badge", "statut", "a_la_une",
    )
    list_display_links = ("apercu", "titre")
    list_filter = ("statut", "a_la_une", "date_debut")
    search_fields = ("titre", "lieu", "description_courte")
    list_editable = ("statut", "a_la_une")
    prepopulated_fields = {"slug": ("titre",)}
    date_hierarchy = "date_debut"
    inlines = [TripPhotoInline, TripVideoInline, TestimonialInline]
    save_on_top = True

    fieldsets = (
        ("Informations principales", {
            "fields": ("titre", "slug", "lieu",
                       ("date_debut", "date_fin"), "prix"),
        }),
        ("Descriptions", {
            "fields": ("description_courte", "description_complete", "activites"),
        }),
        ("Image principale", {
            "fields": ("image", "image_url"),
            "description": "Uploadez une image OU collez un lien web.",
        }),
        ("Participants & places", {
            "fields": ("nombre_participants", "places_disponibles"),
        }),
        ("Publication", {
            "fields": ("statut", "a_la_une"),
        }),
    )

    @admin.display(description="Aperçu")
    def apercu(self, obj):
        if obj.cover:
            return format_html(
                '<img src="{}" style="width:70px;height:48px;'
                'object-fit:cover;border-radius:6px;" />',
                obj.cover,
            )
        return "—"

    @admin.display(description="Prix")
    def prix_affiche(self, obj):
        return f"{obj.prix:,.0f} FCFA".replace(",", " ")

    @admin.display(description="Période")
    def periode_badge(self, obj):
        if obj.est_a_venir:
            color, label = "#2e7d32", "À venir"
        else:
            color, label = "#9e9e9e", "Passé"
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 10px;'
            'border-radius:12px;font-size:11px;">{}</span>',
            color, label,
        )


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = (
        "badge_lu", "nom_complet", "agrotrip", "telephone",
        "email", "nombre_places", "statut_badge", "cree_le",
    )
    list_display_links = ("nom_complet",)
    list_filter = ("statut", "lu", "agrotrip", "cree_le")
    search_fields = ("prenom", "nom", "email", "telephone")
    readonly_fields = ("cree_le",)
    list_per_page = 30
    actions = ["marquer_confirmee", "marquer_annulee", "marquer_lue"]

    fieldsets = (
        ("Client", {
            "fields": (("prenom", "nom"), ("telephone", "email")),
        }),
        ("Inscription", {
            "fields": ("agrotrip", "nombre_places", "message"),
        }),
        ("Suivi", {
            "fields": ("statut", "lu", "cree_le"),
        }),
    )

    @admin.display(description="")
    def badge_lu(self, obj):
        if not obj.lu:
            return format_html(
                '<span title="Nouvelle inscription" style="display:inline-block;'
                'width:10px;height:10px;background:#e53935;border-radius:50%;"></span>'
            )
        return ""

    @admin.display(description="Statut")
    def statut_badge(self, obj):
        couleurs = {
            obj.STATUT_NOUVELLE: "#fb8c00",
            obj.STATUT_CONFIRMEE: "#2e7d32",
            obj.STATUT_ANNULEE: "#9e9e9e",
        }
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 10px;'
            'border-radius:12px;font-size:11px;">{}</span>',
            couleurs.get(obj.statut, "#607d8b"),
            obj.get_statut_display(),
        )

    @admin.action(description="✅ Marquer comme confirmée(s)")
    def marquer_confirmee(self, request, queryset):
        n = queryset.update(statut=Registration.STATUT_CONFIRMEE, lu=True)
        self.message_user(request, f"{n} inscription(s) confirmée(s).")

    @admin.action(description="🚫 Marquer comme annulée(s)")
    def marquer_annulee(self, request, queryset):
        n = queryset.update(statut=Registration.STATUT_ANNULEE, lu=True)
        self.message_user(request, f"{n} inscription(s) annulée(s).")

    @admin.action(description="👁 Marquer comme lue(s)")
    def marquer_lue(self, request, queryset):
        n = queryset.update(lu=True)
        self.message_user(request, f"{n} notification(s) marquée(s) comme lue(s).")

    def changelist_view(self, request, extra_context=None):
        """Affiche le nombre de nouvelles inscriptions non lues en haut de liste."""
        extra_context = extra_context or {}
        non_lues = Registration.objects.filter(lu=False).count()
        if non_lues:
            self.message_user(
                request,
                f"🔔 Vous avez {non_lues} nouvelle(s) inscription(s) non lue(s).",
            )
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("auteur", "agrotrip", "note")
    list_filter = ("note", "agrotrip")
    search_fields = ("auteur", "texte")


@admin.register(TripPhoto)
class TripPhotoAdmin(admin.ModelAdmin):
    list_display = ("agrotrip", "legende")
    list_filter = ("agrotrip",)


# ---------------------- PAGE « POURQUOI AGROTRIP » ----------------------
@admin.register(APropos)
class AProposAdmin(admin.ModelAdmin):
    """Contenu de la page Pourquoi AgroTrip (une seule fiche)."""

    def has_add_permission(self, request):
        # Empêche de créer plusieurs fiches : il n'y en a qu'une.
        return not APropos.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Initiateur)
class InitiateurAdmin(admin.ModelAdmin):
    list_display = ("apercu", "nom", "role", "ordre")
    list_display_links = ("apercu", "nom")
    list_editable = ("ordre",)
    search_fields = ("nom", "role")
    fieldsets = (
        ("Identité", {"fields": ("nom", "role", "ordre")}),
        ("Photo", {"fields": ("photo", "photo_url"),
                   "description": "Uploadez une photo OU collez un lien web."}),
        ("Présentation", {"fields": ("presentation",)}),
    )

    @admin.display(description="Photo")
    def apercu(self, obj):
        if obj.cover:
            return format_html(
                '<img src="{}" style="width:52px;height:52px;object-fit:cover;'
                'border-radius:50%;" />', obj.cover,
            )
        return "—"


@admin.register(Partenaire)
class PartenaireAdmin(admin.ModelAdmin):
    list_display = ("apercu", "nom", "site_web", "ordre")
    list_display_links = ("apercu", "nom")
    list_editable = ("ordre",)
    search_fields = ("nom",)
    fieldsets = (
        ("Partenaire", {"fields": ("nom", "site_web", "ordre")}),
        ("Logo", {"fields": ("logo", "logo_url"),
                  "description": "Uploadez un logo OU collez un lien web."}),
    )

    @admin.display(description="Logo")
    def apercu(self, obj):
        if obj.cover:
            return format_html(
                '<img src="{}" style="width:70px;height:44px;object-fit:contain;" />',
                obj.cover,
            )
        return "—"
