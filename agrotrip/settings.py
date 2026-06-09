"""
Paramètres Django pour le projet AgroTrip.
Site de camps agricoles et d'ateliers d'agriculture immersifs.

Cette configuration fonctionne :
  • EN LOCAL  : sans aucune variable d'environnement (valeurs par défaut).
  • EN LIGNE  : en lisant des variables d'environnement (Render, etc.).
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(nom, defaut):
    """Lit une variable d'environnement booléenne ('1', 'true', 'on')."""
    valeur = os.environ.get(nom)
    if valeur is None:
        return defaut
    return valeur.strip().lower() in ("1", "true", "yes", "on")


# --------------------------------------------------------------------------
# SÉCURITÉ
# --------------------------------------------------------------------------
# En production, définissez la variable d'environnement SECRET_KEY.
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-agrotrip-cle-de-developpement-uniquement",
)

# DEBUG=True en local par défaut. En production, mettez DJANGO_DEBUG=False.
DEBUG = env_bool("DJANGO_DEBUG", True)

# Hôtes autorisés : "localhost,127.0.0.1" + votre domaine en production.
ALLOWED_HOSTS = [
    h.strip() for h in os.environ.get(
        "ALLOWED_HOSTS", "127.0.0.1,localhost"
    ).split(",") if h.strip()
]

# Render fournit automatiquement le nom d'hôte de l'app dans cette variable.
RENDER_HOST = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_HOST:
    ALLOWED_HOSTS.append(RENDER_HOST)

# Origines de confiance pour les formulaires (CSRF) en HTTPS.
CSRF_TRUSTED_ORIGINS = [
    o.strip() for o in os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",")
    if o.strip()
]
if RENDER_HOST:
    CSRF_TRUSTED_ORIGINS.append(f"https://{RENDER_HOST}")

# --------------------------------------------------------------------------
# APPLICATIONS
# --------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    # Application du projet
    "trips",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise sert les fichiers statiques en production (juste après Security).
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "agrotrip.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "agrotrip.wsgi.application"

# --------------------------------------------------------------------------
# BASE DE DONNÉES
# --------------------------------------------------------------------------
# En local : SQLite (aucune configuration).
# En production : si la variable DATABASE_URL existe (PostgreSQL fourni par
# Render), elle est utilisée automatiquement.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    import dj_database_url
    DATABASES["default"] = dj_database_url.parse(
        DATABASE_URL, conn_max_age=600, ssl_require=True
    )

# --------------------------------------------------------------------------
# VALIDATION DES MOTS DE PASSE
# --------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --------------------------------------------------------------------------
# INTERNATIONALISATION (français)
# --------------------------------------------------------------------------
LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "Africa/Dakar"
USE_I18N = True
USE_TZ = True

# --------------------------------------------------------------------------
# FICHIERS STATIQUES ET MÉDIAS
# --------------------------------------------------------------------------
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# WhiteNoise : compression + cache des fichiers statiques en production.
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
    },
}

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --------------------------------------------------------------------------
# SÉCURITÉ EN PRODUCTION (activée automatiquement quand DEBUG = False)
# --------------------------------------------------------------------------
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = env_bool("SECURE_SSL_REDIRECT", True)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 60 * 60 * 24 * 30  # 30 jours
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True

# --------------------------------------------------------------------------
# PERSONNALISATION DE L'ADMIN
# --------------------------------------------------------------------------
# Adresse email qui reçoit les notifications de nouvelles inscriptions.
ADMIN_NOTIFICATION_EMAIL = os.environ.get(
    "ADMIN_NOTIFICATION_EMAIL", "yacine@agrotrip.com"
)

# --------------------------------------------------------------------------
# ENVOI D'EMAILS
# --------------------------------------------------------------------------
# Par défaut : affichage dans la console (aucune configuration requise).
# Pour de VRAIS emails, définissez les variables EMAIL_* en production
# (le backend SMTP s'active automatiquement si EMAIL_HOST_USER est fourni).
if os.environ.get("EMAIL_HOST_USER"):
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
    EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
    EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS", True)
    EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
    DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    DEFAULT_FROM_EMAIL = "AgroTrip <no-reply@agrotrip.com>"
