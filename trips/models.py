"""
Modèles de données du site AgroTrip.

- AgroTrip   : un camp / atelier agricole (passé ou à venir)
- TripPhoto  : photos supplémentaires d'un AgroTrip (galerie)
- Testimonial: témoignage d'un participant
- Registration: inscription d'un client à un AgroTrip à venir
"""
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class AgroTrip(models.Model):
    """Un camp ou atelier agricole proposé par AgroTrip."""

    STATUT_BROUILLON = "brouillon"
    STATUT_PUBLIE = "publie"
    STATUT_CHOICES = [
        (STATUT_BROUILLON, "Brouillon"),
        (STATUT_PUBLIE, "Publié"),
    ]

    titre = models.CharField("Titre", max_length=200)
    slug = models.SlugField(
        "Slug (URL)",
        max_length=220,
        unique=True,
        blank=True,
        help_text="Laissez vide : il sera généré automatiquement à partir du titre.",
    )
    lieu = models.CharField("Lieu", max_length=200)
    date_debut = models.DateField("Date de début")
    date_fin = models.DateField("Date de fin", blank=True, null=True)
    prix = models.DecimalField(
        "Prix (FCFA)", max_digits=10, decimal_places=0, default=0
    )

    description_courte = models.CharField(
        "Description courte",
        max_length=300,
        help_text="Affichée sur les cartes de la page d'accueil.",
    )
    description_complete = models.TextField("Description complète")
    activites = models.TextField(
        "Activités réalisées",
        blank=True,
        help_text="Une activité par ligne.",
    )

    # Image principale : upload OU adresse web (les deux fonctionnent)
    image = models.ImageField(
        "Image principale (upload)", upload_to="agrotrips/", blank=True, null=True
    )
    image_url = models.URLField(
        "Image principale (lien web)",
        blank=True,
        help_text="Utilisé si aucune image n'est uploadée.",
    )

    nombre_participants = models.PositiveIntegerField(
        "Nombre de participants", default=0
    )
    places_disponibles = models.PositiveIntegerField(
        "Places disponibles", default=20,
        help_text="Pour les AgroTrips à venir.",
    )

    statut = models.CharField(
        "Statut de publication",
        max_length=20,
        choices=STATUT_CHOICES,
        default=STATUT_PUBLIE,
    )
    a_la_une = models.BooleanField(
        "Mettre dans le slider d'accueil", default=False
    )

    cree_le = models.DateTimeField("Créé le", auto_now_add=True)
    modifie_le = models.DateTimeField("Modifié le", auto_now=True)

    class Meta:
        verbose_name = "AgroTrip"
        verbose_name_plural = "AgroTrips"
        ordering = ["-date_debut"]

    def __str__(self):
        return self.titre

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.titre)
            slug = base
            n = 1
            while AgroTrip.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                n += 1
                slug = f"{base}-{n}"
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("trips:detail", kwargs={"slug": self.slug})

    @property
    def est_a_venir(self):
        """True si l'AgroTrip n'a pas encore commencé."""
        return self.date_debut >= timezone.localdate()

    @property
    def cover(self):
        """Retourne l'image à afficher (upload prioritaire, sinon lien web)."""
        if self.image:
            return self.image.url
        return self.image_url

    @property
    def liste_activites(self):
        """Les activités sous forme de liste (une par ligne)."""
        return [a.strip() for a in self.activites.splitlines() if a.strip()]

    @property
    def places_restantes(self):
        prises = sum(
            r.nombre_places
            for r in self.inscriptions.filter(
                statut__in=[Registration.STATUT_NOUVELLE, Registration.STATUT_CONFIRMEE]
            )
        )
        return max(self.places_disponibles - prises, 0)

    @property
    def complet(self):
        return self.est_a_venir and self.places_restantes <= 0


class TripPhoto(models.Model):
    """Photo supplémentaire d'un AgroTrip (galerie)."""

    agrotrip = models.ForeignKey(
        AgroTrip, on_delete=models.CASCADE, related_name="photos"
    )
    image = models.ImageField("Image (upload)", upload_to="galerie/", blank=True, null=True)
    image_url = models.URLField("Image (lien web)", blank=True)
    legende = models.CharField("Légende", max_length=200, blank=True)

    class Meta:
        verbose_name = "Photo de galerie"
        verbose_name_plural = "Photos de galerie"

    def __str__(self):
        return f"Photo — {self.agrotrip.titre}"

    @property
    def cover(self):
        if self.image:
            return self.image.url
        return self.image_url


class Testimonial(models.Model):
    """Témoignage d'un participant à un AgroTrip."""

    agrotrip = models.ForeignKey(
        AgroTrip, on_delete=models.CASCADE, related_name="temoignages"
    )
    auteur = models.CharField("Nom du participant", max_length=120)
    texte = models.TextField("Témoignage")
    note = models.PositiveSmallIntegerField(
        "Note (sur 5)", default=5,
        help_text="De 1 à 5 étoiles.",
    )

    class Meta:
        verbose_name = "Témoignage"
        verbose_name_plural = "Témoignages"

    def __str__(self):
        return f"{self.auteur} — {self.agrotrip.titre}"

    @property
    def etoiles(self):
        return range(self.note)


class Registration(models.Model):
    """Inscription d'un client à un AgroTrip à venir."""

    STATUT_NOUVELLE = "nouvelle"
    STATUT_CONFIRMEE = "confirmee"
    STATUT_ANNULEE = "annulee"
    STATUT_CHOICES = [
        (STATUT_NOUVELLE, "Nouvelle"),
        (STATUT_CONFIRMEE, "Confirmée"),
        (STATUT_ANNULEE, "Annulée"),
    ]

    agrotrip = models.ForeignKey(
        AgroTrip, on_delete=models.CASCADE,
        related_name="inscriptions", verbose_name="AgroTrip choisi"
    )
    prenom = models.CharField("Prénom", max_length=80)
    nom = models.CharField("Nom", max_length=80)
    telephone = models.CharField("Téléphone", max_length=30)
    email = models.EmailField("Email")
    nombre_places = models.PositiveSmallIntegerField("Nombre de places", default=1)
    message = models.TextField("Message / besoin particulier", blank=True)

    statut = models.CharField(
        "Statut", max_length=20, choices=STATUT_CHOICES, default=STATUT_NOUVELLE
    )
    lu = models.BooleanField("Notification lue", default=False)
    cree_le = models.DateTimeField("Date d'inscription", auto_now_add=True)

    class Meta:
        verbose_name = "Inscription"
        verbose_name_plural = "Inscriptions"
        ordering = ["-cree_le"]

    def __str__(self):
        return f"{self.prenom} {self.nom} — {self.agrotrip.titre}"

    @property
    def nom_complet(self):
        return f"{self.prenom} {self.nom}"
