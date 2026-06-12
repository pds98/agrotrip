"""Formulaires du site AgroTrip."""
from django import forms

from .models import (
    Registration, AgroTrip, Initiateur, Partenaire, APropos,
)


# Petit utilitaire : applique la classe CSS "form-control" à tous les champs.
def _styler(form, classe="form-control"):
    for champ in form.fields.values():
        widget = champ.widget
        if isinstance(widget, (forms.CheckboxInput,)):
            widget.attrs.setdefault("class", "form-check")
        else:
            existing = widget.attrs.get("class", "")
            widget.attrs["class"] = (existing + " " + classe).strip()


class RegistrationForm(forms.ModelForm):
    """Formulaire d'inscription à un AgroTrip à venir."""

    class Meta:
        model = Registration
        fields = [
            "prenom", "nom", "telephone", "email",
            "nombre_places", "message",
        ]
        widgets = {
            "prenom": forms.TextInput(
                attrs={"placeholder": "Votre prénom", "class": "form-control"}
            ),
            "nom": forms.TextInput(
                attrs={"placeholder": "Votre nom", "class": "form-control"}
            ),
            "telephone": forms.TextInput(
                attrs={"placeholder": "+221 ...", "class": "form-control"}
            ),
            "email": forms.EmailInput(
                attrs={"placeholder": "vous@email.com", "class": "form-control"}
            ),
            "nombre_places": forms.NumberInput(
                attrs={"min": 1, "value": 1, "class": "form-control"}
            ),
            "message": forms.Textarea(
                attrs={
                    "placeholder": "Un besoin particulier ? (facultatif)",
                    "rows": 4,
                    "class": "form-control",
                }
            ),
        }

    def __init__(self, *args, agrotrip=None, **kwargs):
        self.agrotrip = agrotrip
        super().__init__(*args, **kwargs)

    def clean_nombre_places(self):
        places = self.cleaned_data["nombre_places"]
        if places < 1:
            raise forms.ValidationError("Le nombre de places doit être au moins 1.")
        if self.agrotrip and places > self.agrotrip.places_restantes:
            raise forms.ValidationError(
                f"Il ne reste que {self.agrotrip.places_restantes} place(s) "
                "disponible(s) pour cet AgroTrip."
            )
        return places


# ==========================================================================
#  FORMULAIRES DU TABLEAU DE BORD (gestion par Yacine)
# ==========================================================================
class AgroTripForm(forms.ModelForm):
    """Ajouter / modifier un AgroTrip depuis le tableau de bord."""

    class Meta:
        model = AgroTrip
        fields = [
            "titre", "lieu", "date_debut", "date_fin", "prix",
            "description_courte", "description_complete", "activites",
            "image", "image_url",
            "nombre_participants", "places_disponibles",
            "statut", "a_la_une",
        ]
        widgets = {
            "date_debut": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "date_fin": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "description_courte": forms.Textarea(attrs={"rows": 2}),
            "description_complete": forms.Textarea(attrs={"rows": 6}),
            "activites": forms.Textarea(attrs={"rows": 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Les champs date acceptent le format du calendrier HTML.
        self.fields["date_debut"].input_formats = ["%Y-%m-%d"]
        self.fields["date_fin"].input_formats = ["%Y-%m-%d"]
        _styler(self)


class InitiateurForm(forms.ModelForm):
    class Meta:
        model = Initiateur
        fields = ["nom", "role", "photo", "photo_url", "presentation", "ordre"]
        widgets = {"presentation": forms.Textarea(attrs={"rows": 4})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _styler(self)


class PartenaireForm(forms.ModelForm):
    class Meta:
        model = Partenaire
        fields = ["nom", "logo", "logo_url", "site_web", "ordre"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _styler(self)


class AProposForm(forms.ModelForm):
    class Meta:
        model = APropos
        fields = ["pourquoi_titre", "pourquoi_texte", "mission_texte"]
        widgets = {
            "pourquoi_texte": forms.Textarea(attrs={"rows": 6}),
            "mission_texte": forms.Textarea(attrs={"rows": 6}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _styler(self)
