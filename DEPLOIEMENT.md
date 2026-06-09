# 🚀 Mettre AgroTrip en ligne (Render) + domaine agrotrip.sn

Ce guide vous emmène, étape par étape, d'un projet sur votre ordinateur à un
site accessible sur Internet, puis sur votre propre adresse **agrotrip.sn**.

Aucune connaissance avancée n'est nécessaire. Comptez environ **1 heure** la
première fois. Tout est **gratuit** pour l'hébergement ; seul le domaine `.sn`
est payant (≈ 10 000 FCFA HT/an).

---

## 🗺️ Vue d'ensemble

```
Votre PC  →  GitHub (stocke le code)  →  Render (héberge le site)  →  agrotrip.sn
```

1. **Partie A** — Mettre le code sur GitHub
2. **Partie B** — Déployer sur Render (site en ligne, adresse gratuite)
3. **Partie C** — Créer le compte admin de Yacine en ligne
4. **Partie D** — Acheter et connecter le domaine **agrotrip.sn**
5. **Partie E** — Activer les vrais emails (facultatif)

---

## 📋 Partie A — Mettre le code sur GitHub

GitHub est un site gratuit qui stocke votre code. Render ira le chercher là-bas.

### 1. Créer un compte
Allez sur **https://github.com** → **Sign up** → suivez les étapes (gratuit).

### 2. Créer un dépôt (repository)
- Cliquez sur le **+** en haut à droite → **New repository**.
- Nom : `agrotrip`
- Laissez **Public** (ou Private), ne cochez rien d'autre → **Create repository**.

### 3. Envoyer votre code
Ouvrez le terminal **dans le dossier qui contient `manage.py`** et tapez
(remplacez `VOTRE-NOM` par votre nom d'utilisateur GitHub) :

```bash
git init
git add .
git commit -m "Premier dépôt AgroTrip"
git branch -M main
git remote add origin https://github.com/VOTRE-NOM/agrotrip.git
git push -u origin main
```

> Git vous demandera de vous connecter à GitHub la première fois.
> Si `git` n'est pas installé : `xcode-select --install` (sur Mac).

Rechargez la page GitHub : vos fichiers doivent apparaître. ✅

---

## 🌐 Partie B — Déployer sur Render

### 1. Créer un compte
Allez sur **https://render.com** → **Get Started** → connectez-vous **avec GitHub**
(bouton « GitHub »). C'est le plus simple.

### 2. Créer le service web
Deux méthodes — la **méthode Blueprint** est la plus automatique :

**Méthode 1 — Blueprint (recommandée, tout automatique)**
- Tableau de bord Render → **New +** → **Blueprint**.
- Sélectionnez votre dépôt `agrotrip`.
- Render lit le fichier `render.yaml` fourni et crée **le site + la base de
  données PostgreSQL** automatiquement. Cliquez **Apply**.

**Méthode 2 — Manuelle (si vous préférez)**
- **New +** → **Web Service** → choisissez le dépôt `agrotrip`.
- Renseignez :
  - **Build Command** : `./build.sh`
  - **Start Command** : `gunicorn agrotrip.wsgi:application`
  - **Instance Type** : `Free`
- Dans **Environment**, ajoutez les variables :
  | Clé              | Valeur                          |
  |------------------|---------------------------------|
  | `SECRET_KEY`     | (cliquez « Generate »)          |
  | `DJANGO_DEBUG`   | `False`                         |
  | `PYTHON_VERSION` | `3.12.4`                        |
- Créez aussi une base : **New +** → **PostgreSQL** (plan Free), puis copiez son
  **Internal Database URL** dans une variable `DATABASE_URL` du service web.

### 3. Attendre le déploiement
Render installe tout et lance le site (quelques minutes). Quand le statut passe
à **Live**, cliquez sur l'URL en haut : `https://agrotrip.onrender.com`
(ou similaire). **Votre site est en ligne !** 🎉

> ℹ️ Sur le plan gratuit, le site « s'endort » après 15 min d'inactivité et met
> ~30 s à se réveiller à la première visite. Normal. Un plan payant (~7 $/mois)
> supprime ce délai.

---

## 👩‍💼 Partie C — Créer le compte admin de Yacine en ligne

La base en ligne est vide au départ. Créez le compte admin et (si vous voulez)
les données de démo via le terminal intégré de Render :

- Sur la page de votre service Render → onglet **Shell** (menu de gauche).
- Tapez :

```bash
python manage.py seed_demo
```

Cela crée le compte **yacine / AgroTrip2026** + les AgroTrips de démonstration.

> 🔒 **Changez immédiatement le mot de passe** :
> ```bash
> python manage.py changepassword yacine
> ```

Admin en ligne : `https://votre-site.onrender.com/admin/`

---

## 🏷️ Partie D — Acheter et connecter le domaine agrotrip.sn

### Ce qu'il faut savoir sur le .sn
- Le `.sn` est géré par **NIC Sénégal**. Il est **réservé aux personnes/entités
  ayant un lien avec le Sénégal**.
- **Pièces demandées** : copie de votre **carte d'identité** et/ou **registre de
  commerce** (ou certificat de marque) de l'entreprise.
- **Prix officiel** : **10 000 FCFA HT/an** pour `agrotrip.sn`
  (ou 5 000 FCFA HT/an pour un `agrotrip.com.sn`).

### 1. Acheter le domaine
Passez par un **bureau d'enregistrement (registrar)** accrédité. Options :
- **NIC Sénégal** directement : https://www.nic.sn
- Registrars internationaux qui gèrent le `.sn` : **LWS**, **Netim**, etc.

Créez un compte, recherchez `agrotrip.sn`, ajoutez au panier, fournissez les
pièces justificatives et payez.

### 2. Déclarer le domaine sur Render
- Page de votre service Render → **Settings** → **Custom Domains** → **Add Custom
  Domain**.
- Ajoutez `agrotrip.sn` **et** `www.agrotrip.sn`.
- Render affiche les **enregistrements DNS** à créer (gardez cette page ouverte).

### 3. Configurer le DNS chez votre registrar
Dans l'espace de gestion DNS de votre domaine (chez NIC/LWS/Netim), créez :

| Type    | Nom / Hôte | Valeur (fournie par Render)              |
|---------|------------|------------------------------------------|
| `A`     | `@`        | l'adresse IP indiquée par Render         |
| `CNAME` | `www`      | `votre-site.onrender.com`                |

> Les valeurs exactes sont **celles affichées par Render** — recopiez-les
> précisément. Le `@` représente le domaine « nu » (agrotrip.sn).

### 4. Attendre la propagation
La mise à jour DNS prend de **quelques minutes à 24-48 h**. Render vérifie
automatiquement et installe un **certificat HTTPS gratuit**. Quand tout est vert,
**https://agrotrip.sn** affiche votre site. ✅

### 5. Important après la connexion du domaine
Sur Render, ajoutez/complétez ces variables d'environnement, puis redéployez :

| Clé                   | Valeur                                  |
|-----------------------|-----------------------------------------|
| `ALLOWED_HOSTS`       | `agrotrip.sn,www.agrotrip.sn`           |
| `CSRF_TRUSTED_ORIGINS`| `https://agrotrip.sn,https://www.agrotrip.sn` |

---

## 📧 Partie E — Activer les vrais emails (facultatif)

Par défaut, les emails de confirmation s'affichent dans les logs Render. Pour
les **envoyer réellement** (ex. via Gmail), ajoutez ces variables sur Render :

| Clé                   | Valeur                                   |
|-----------------------|------------------------------------------|
| `EMAIL_HOST_USER`     | votre.adresse@gmail.com                  |
| `EMAIL_HOST_PASSWORD` | mot de passe **d'application** Gmail     |
| `ADMIN_NOTIFICATION_EMAIL` | l'email où Yacine reçoit les alertes |
| `DEFAULT_FROM_EMAIL`  | votre.adresse@gmail.com                  |

> Pour Gmail : activez la validation en 2 étapes, puis créez un
> « mot de passe d'application » dans les paramètres de sécurité Google.
> Le code bascule automatiquement en envoi réel dès que `EMAIL_HOST_USER` existe.

---

## 🔁 Mettre à jour le site plus tard

À chaque modification de votre code :

```bash
git add .
git commit -m "Description de la modification"
git push
```

Render redéploie **automatiquement** la nouvelle version. C'est tout.

---

## ❓ Problèmes fréquents

- **« Bad Request (400) »** après avoir branché le domaine → ajoutez bien
  `ALLOWED_HOSTS` (Partie D, étape 5) et redéployez.
- **Les images/CSS ne s'affichent pas** → vérifiez que `build.sh` s'est bien
  exécuté (il lance `collectstatic`). WhiteNoise est déjà configuré.
- **Le site est lent au premier chargement** → c'est le « réveil » du plan
  gratuit (~30 s). Passez à un plan payant pour l'éviter.
- **Données perdues après un déploiement** → assurez-vous d'utiliser la base
  **PostgreSQL** (variable `DATABASE_URL` présente), pas SQLite.

Bonne mise en ligne ! 🌱
