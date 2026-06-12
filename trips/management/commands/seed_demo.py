"""
Commande de génération de données de démonstration.

Usage :  python manage.py seed_demo

Crée des AgroTrips passés et à venir avec photos (Unsplash), témoignages
et un compte administrateur pour la CEO Yacine.
"""
import datetime

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from trips.models import (
    AgroTrip, TripPhoto, Testimonial,
    APropos, Initiateur, Partenaire,
)


# Photos agricoles libres de droits (Unsplash)
IMG = {
    "ferme": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=1200&q=80",
    "champ": "https://images.unsplash.com/photo-1574943320219-553eb213f72d?w=1200&q=80",
    "recolte": "https://images.unsplash.com/photo-1464226184884-fa280b87c399?w=1200&q=80",
    "maraichage": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=1200&q=80",
    "elevage": "https://images.unsplash.com/photo-1516467508483-a7212febe31a?w=1200&q=80",
    "vigne": "https://images.unsplash.com/photo-1474440692490-2e83ae13ba29?w=1200&q=80",
    "serre": "https://images.unsplash.com/photo-1530836369250-ef72a3f5cda8?w=1200&q=80",
    "verger": "https://images.unsplash.com/photo-1445264918150-66a2371142a2?w=1200&q=80",
    "tracteur": "https://images.unsplash.com/photo-1530267981375-f0de937f5f13?w=1200&q=80",
    "miel": "https://images.unsplash.com/photo-1587049352846-4a222e784d38?w=1200&q=80",
    "riz": "https://images.unsplash.com/photo-1536431311719-398b6704d4cc?w=1200&q=80",
    "marche": "https://images.unsplash.com/photo-1488459716781-31db52582fe9?w=1200&q=80",
}


class Command(BaseCommand):
    help = "Génère des données de démonstration pour AgroTrip."

    def handle(self, *args, **options):
        today = timezone.localdate()

        # -------- Compte CEO --------
        User = get_user_model()
        if not User.objects.filter(username="yacine").exists():
            User.objects.create_superuser(
                username="yacine",
                email="yacine@agrotrip.com",
                password="AgroTrip2026",
            )
            self.stdout.write(self.style.SUCCESS(
                "✅ Compte admin créé : yacine / AgroTrip2026"
            ))

        # -------- Page « Pourquoi AgroTrip » (mission, initiateurs, partenaires) --------
        apropos = APropos.charger()
        if not apropos.pourquoi_texte:
            apropos.pourquoi_titre = "Pourquoi AgroTrip ?"
            apropos.pourquoi_texte = (
                "AgroTrip est né d'une conviction simple : l'agriculture se comprend "
                "mieux en la vivant. Trop de personnes sont aujourd'hui déconnectées de "
                "la terre et des métiers qui les nourrissent.\n\n"
                "Nous créons des expériences immersives — les « AgroTrips » — qui "
                "reconnectent les participants à la nature, aux fermes et aux savoir-faire "
                "agricoles, dans une ambiance conviviale et formatrice."
            )
            apropos.mission_texte = (
                "Rendre l'agriculture accessible, attractive et inspirante.\n\n"
                "Nous transmettons des techniques concrètes, nous valorisons les acteurs "
                "du monde agricole et nous faisons naître des vocations grâce à des camps "
                "et ateliers pratiques ouverts à tous."
            )
            apropos.save()

        if not Initiateur.objects.exists():
            Initiateur.objects.create(
                nom="Yacine", role="Fondatrice & CEO", ordre=1,
                photo_url="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=600&q=80",
                presentation="Passionnée d'agriculture et d'entrepreneuriat, Yacine a "
                             "fondé AgroTrip pour rapprocher les jeunes du monde agricole.",
            )
            Initiateur.objects.create(
                nom="Initiateur 2", role="Co-fondateur", ordre=2,
                photo_url="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600&q=80",
                presentation="Expert agronome, il conçoit les programmes pédagogiques "
                             "des AgroTrips et accompagne les participants sur le terrain.",
            )

        if not Partenaire.objects.exists():
            Partenaire.objects.create(
                nom="Ferme partenaire", ordre=1,
                logo_url="https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=300&q=80",
            )
            Partenaire.objects.create(
                nom="Coopérative agricole", ordre=2,
                logo_url="https://images.unsplash.com/photo-1574943320219-553eb213f72d?w=300&q=80",
            )

        if AgroTrip.objects.exists():
            self.stdout.write(self.style.WARNING(
                "Des AgroTrips existent déjà — création des AgroTrips ignorée."
            ))
            return

        # ================= AGROTRIPS PASSÉS =================
        passes = [
            {
                "titre": "Camp Maraîchage Bio de Thiès",
                "lieu": "Thiès, Sénégal",
                "jours_avant": 90, "duree": 3, "prix": 45000,
                "img": IMG["maraichage"], "participants": 24,
                "courte": "Trois jours immersifs dans le maraîchage biologique : semis, arrosage et récolte.",
                "complete": "Un camp de trois jours au cœur des fermes maraîchères de Thiès. "
                            "Les participants ont appris les techniques de culture biologique, "
                            "la préparation des sols, le compostage et la gestion de l'eau. "
                            "Une expérience riche en partage et en apprentissage pratique.",
                "activites": "Préparation des planches de culture\nSemis et repiquage\nFabrication de compost naturel\nRécolte de légumes de saison\nAtelier de conservation",
                "galerie": ["champ", "recolte", "serre"],
                "temoins": [
                    ("Awa Ndiaye", 5, "Une expérience incroyable ! J'ai appris énormément sur le maraîchage bio."),
                    ("Cheikh Fall", 5, "Très bien organisé, les formateurs étaient passionnés et pédagogues."),
                ],
            },
            {
                "titre": "Atelier Apiculture & Miel",
                "lieu": "Ziguinchor, Casamance",
                "jours_avant": 150, "duree": 2, "prix": 35000,
                "img": IMG["miel"], "participants": 16,
                "courte": "Découverte du monde des abeilles et de la production de miel artisanal.",
                "complete": "Pendant deux jours, les participants ont plongé dans l'univers fascinant "
                            "de l'apiculture. De l'installation des ruches à la récolte du miel, "
                            "chaque étape a été expliquée et pratiquée sur le terrain en Casamance.",
                "activites": "Visite d'un rucher\nManipulation des cadres\nExtraction du miel\nDégustation de produits de la ruche",
                "galerie": ["verger", "marche"],
                "temoins": [
                    ("Fatou Sow", 5, "Magique de voir comment le miel est produit. À refaire absolument !"),
                ],
            },
            {
                "titre": "Immersion Riziculture du Delta",
                "lieu": "Saint-Louis, Sénégal",
                "jours_avant": 220, "duree": 4, "prix": 55000,
                "img": IMG["riz"], "participants": 30,
                "courte": "Quatre jours dans les rizières du delta du fleuve Sénégal.",
                "complete": "Une immersion complète dans la riziculture irriguée du delta. "
                            "Les participants ont découvert tout le cycle du riz, de la mise en eau "
                            "des parcelles jusqu'à la transformation, aux côtés de producteurs locaux.",
                "activites": "Mise en eau des rizières\nRepiquage du riz\nGestion de l'irrigation\nVisite d'une unité de transformation\nRencontre avec les coopératives",
                "galerie": ["champ", "tracteur", "marche"],
                "temoins": [
                    ("Mamadou Ba", 4, "Très instructif sur toute la chaîne de production du riz."),
                    ("Aïssatou Diop", 5, "Un séjour authentique au contact des vrais producteurs."),
                ],
            },
            {
                "titre": "Camp Élevage & Pastoralisme",
                "lieu": "Louga, Sénégal",
                "jours_avant": 300, "duree": 3, "prix": 48000,
                "img": IMG["elevage"], "participants": 20,
                "courte": "À la rencontre des éleveurs et du pastoralisme traditionnel.",
                "complete": "Trois jours pour comprendre l'élevage et le pastoralisme au Sénégal. "
                            "Soins aux animaux, traite, production laitière et gestion des troupeaux "
                            "ont rythmé ce camp au plus près des éleveurs.",
                "activites": "Soins et alimentation du bétail\nTraite et transformation du lait\nGestion des pâturages\nFabrication de fromage local",
                "galerie": ["elevage", "ferme"],
                "temoins": [
                    ("Ousmane Sarr", 5, "Une belle découverte du monde de l'élevage, très immersif."),
                ],
            },
        ]

        for d in passes:
            self._creer_trip(today, d, a_la_une=False)

        # ================= AGROTRIPS À VENIR =================
        a_venir = [
            {
                "titre": "AgroTrip Permaculture de Mbour",
                "lieu": "Mbour, Sénégal",
                "jours_avant": -12, "duree": 3, "prix": 50000,
                "img": IMG["ferme"], "places": 25,
                "courte": "Concevez et cultivez votre propre jardin en permaculture pendant 3 jours.",
                "complete": "Un AgroTrip dédié à la permaculture : apprenez à concevoir un écosystème "
                            "agricole durable, autonome et productif. Design de jardin, associations "
                            "de plantes, gestion de l'eau et techniques régénératives au programme.",
                "activites": "Design en permaculture\nAssociations de cultures\nButtes et paillage\nRécupération d'eau de pluie\nCréation d'un mandala potager",
                "galerie": ["serre", "maraichage"],
            },
            {
                "titre": "Camp Vendanges & Vigne",
                "lieu": "Dakar (domaine viticole)",
                "jours_avant": -25, "duree": 2, "prix": 60000,
                "img": IMG["vigne"], "places": 20,
                "courte": "Participez aux vendanges et découvrez le travail de la vigne.",
                "complete": "Deux jours au cœur d'un domaine viticole pour vivre les vendanges. "
                            "De la taille à la récolte des grappes, découvrez le savoir-faire de la "
                            "viticulture sous le soleil sénégalais.",
                "activites": "Taille de la vigne\nVendanges manuelles\nDécouverte des cépages\nVisite du chai",
                "galerie": ["vigne", "verger"],
            },
            {
                "titre": "AgroTrip Serres & Hydroponie",
                "lieu": "Rufisque, Sénégal",
                "jours_avant": -40, "duree": 3, "prix": 65000,
                "img": IMG["serre"], "places": 18,
                "courte": "L'agriculture du futur : cultures sous serre et hydroponie.",
                "complete": "Découvrez les techniques modernes de production sous serre et la culture "
                            "hors-sol (hydroponie). Un AgroTrip tourné vers l'innovation agricole et "
                            "l'agriculture intelligente face au climat.",
                "activites": "Installation d'un système hydroponique\nGestion du climat sous serre\nNutrition des plantes\nSuivi de croissance\nAutomatisation de l'arrosage",
                "galerie": ["serre", "maraichage"],
            },
            {
                "titre": "Immersion Verger & Arboriculture",
                "lieu": "Kolda, Sénégal",
                "jours_avant": -60, "duree": 4, "prix": 58000,
                "img": IMG["verger"], "places": 22,
                "courte": "Plantez, greffez et entretenez des arbres fruitiers pendant 4 jours.",
                "complete": "Un AgroTrip dédié à l'arboriculture fruitière : manguiers, agrumes et "
                            "anacardiers. Apprenez la plantation, la greffe, la taille et l'entretien "
                            "d'un verger productif et durable.",
                "activites": "Plantation d'arbres fruitiers\nTechniques de greffage\nTaille de formation\nLutte biologique\nRécolte et conservation des fruits",
                "galerie": ["verger", "recolte"],
            },
            {
                "titre": "Camp Agroécologie & Compost",
                "lieu": "Fatick, Sénégal",
                "jours_avant": -85, "duree": 3, "prix": 47000,
                "img": IMG["champ"], "places": 30,
                "courte": "Régénérez les sols grâce à l'agroécologie et au compostage.",
                "complete": "Un AgroTrip centré sur la santé des sols et l'agroécologie. Apprenez à "
                            "produire un compost de qualité, à fabriquer des engrais naturels et à "
                            "régénérer des terres dégradées pour une agriculture durable.",
                "activites": "Fabrication de compost et lombricompost\nEngrais verts et bio-fertilisants\nRotation et associations de cultures\nAnalyse simple des sols\nReboisement et haies vives",
                "galerie": ["champ", "tracteur"],
            },
        ]

        for d in a_venir:
            self._creer_trip(today, d, a_la_une=True)

        self.stdout.write(self.style.SUCCESS(
            f"✅ {AgroTrip.objects.count()} AgroTrips de démo créés "
            f"({len(passes)} passés, {len(a_venir)} à venir)."
        ))

    # ------------------------------------------------------------------
    def _creer_trip(self, today, d, a_la_une):
        date_debut = today - datetime.timedelta(days=d["jours_avant"])
        date_fin = date_debut + datetime.timedelta(days=d["duree"] - 1)

        trip = AgroTrip.objects.create(
            titre=d["titre"],
            lieu=d["lieu"],
            date_debut=date_debut,
            date_fin=date_fin,
            prix=d["prix"],
            description_courte=d["courte"],
            description_complete=d["complete"],
            activites=d["activites"],
            image_url=d["img"],
            nombre_participants=d.get("participants", 0),
            places_disponibles=d.get("places", 20),
            statut=AgroTrip.STATUT_PUBLIE,
            a_la_une=a_la_une,
        )

        for key in d.get("galerie", []):
            TripPhoto.objects.create(
                agrotrip=trip, image_url=IMG[key], legende=trip.titre
            )

        for auteur, note, texte in d.get("temoins", []):
            Testimonial.objects.create(
                agrotrip=trip, auteur=auteur, note=note, texte=texte
            )
