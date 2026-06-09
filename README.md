# 🌱 AgroTrip — L'agriculture en immersion

Site web professionnel de camps agricoles et d'ateliers pratiques d'agriculture
(« AgroTrips »), développé avec **Django**. Le site permet aux visiteurs de
découvrir les AgroTrips passés et à venir, de s'inscrire en ligne, et offre à la
CEO **Yacine** un espace d'administration complet.

---

## ✨ Fonctionnalités

- **Slider d'accueil** professionnel avec défilement automatique, flèches et points
  de navigation, titre, texte et bouton d'appel à l'action.
- **Cartes des AgroTrips réalisés** (image, nom, lieu, date, description) menant à
  une page détaillée (description, galerie photos, activités, participants, témoignages).
- **Section « AgroTrips à venir »** avec ~5 cartes et **compte à rebours** en temps réel
  jusqu'au début de chaque événement.
- **Système d'inscription** : formulaire (prénom, nom, téléphone, email, places,
  message), message de confirmation à l'écran **et** email de confirmation au client.
- **Notification automatique par email** à la CEO à chaque nouvelle inscription.
- **Espace administrateur sécurisé** (Django Admin personnalisé) : gestion complète
  des AgroTrips (ajouter, modifier, photos, prix, lieu, date, supprimer) et suivi des
  inscriptions (nom, téléphone, email, AgroTrip, date, places, statut, notifications).
- **100 % responsive** : téléphone, tablette, ordinateur.

---

## 🚀 Installation et lancement

```bash
# 1. (Recommandé) Créer un environnement virtuel
python -m venv venv
source venv/bin/activate        # Windows : venv\Scripts\activate

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Créer la base de données
python manage.py migrate

# 4. (Optionnel) Charger des données de démonstration
#    -> crée 9 AgroTrips (4 passés, 5 à venir) + le compte de Yacine
python manage.py seed_demo

# 5. Lancer le serveur
python manage.py runserver
```

Le site est alors accessible sur **http://127.0.0.1:8000/**

---

## 🔑 Accès administrateur (CEO Yacine)

Après `python manage.py seed_demo`, un compte est créé automatiquement :

| Identifiant | Mot de passe   |
|-------------|----------------|
| `yacine`    | `AgroTrip2026` |

Connexion : **http://127.0.0.1:8000/admin/**

> ⚠️ Changez ce mot de passe en production : `python manage.py changepassword yacine`

Pour créer un autre administrateur :
```bash
python manage.py createsuperuser
```

Dans le tableau de bord, Yacine peut :
- voir un **rappel des nouvelles inscriptions non lues** (point rouge + message),
- consulter et filtrer les inscriptions, changer leur statut (nouvelle / confirmée / annulée),
- **ajouter, modifier ou supprimer** des AgroTrips, gérer photos, prix, lieu et dates,
- cocher « Mettre dans le slider d'accueil » pour mettre un AgroTrip en avant.

---

## 📧 Configuration des emails

Par défaut, les emails s'affichent **dans la console** (aucune configuration requise,
idéal pour tester). Pour envoyer de **vrais emails**, ouvrez `agrotrip/settings.py`,
commentez le backend console et complétez le bloc SMTP (un exemple Gmail est fourni) :

```python
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "votre.adresse@gmail.com"
EMAIL_HOST_PASSWORD = "mot-de-passe-application-gmail"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```

> Pour Gmail, utilisez un **mot de passe d'application** (pas votre mot de passe habituel).

L'adresse qui reçoit les notifications de la CEO se règle via `ADMIN_NOTIFICATION_EMAIL`
dans `settings.py`.

---

## 🖼️ Images

Les images de démonstration proviennent d'**Unsplash** (libres de droits). Chaque
AgroTrip accepte soit une **image uploadée**, soit un **lien web** (`image_url`).
Yacine peut remplacer les images depuis l'administration.

---

## 📁 Structure du projet

```
agrotrip/
├── manage.py
├── requirements.txt
├── agrotrip/              # Configuration du projet
│   ├── settings.py        # Paramètres (BDD, emails, langue FR...)
│   └── urls.py
└── trips/                 # Application principale
    ├── models.py          # AgroTrip, TripPhoto, Testimonial, Registration
    ├── views.py           # Accueil, détail, inscription, succès
    ├── forms.py           # Formulaire d'inscription
    ├── admin.py           # Tableau de bord de la CEO (admin personnalisé)
    ├── urls.py
    ├── templates/         # (dans /templates) base, accueil, détail...
    ├── static/            # CSS + JS (slider, compte à rebours)
    └── management/commands/seed_demo.py   # Données de démonstration
```

---

## ⚙️ Notes pour la mise en production

- Mettre `DEBUG = False` et renseigner `ALLOWED_HOSTS` dans `settings.py`.
- Changer `SECRET_KEY` (la garder secrète, via variable d'environnement).
- Lancer `python manage.py collectstatic` et servir les fichiers statiques/médias.
- Envisager PostgreSQL à la place de SQLite pour un trafic important.
```
```
