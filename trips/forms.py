"""Formulaires du site AgroTrip."""
from django import forms

from .models import Registration


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
