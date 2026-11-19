# Déploiement (chapitre 13)

## 1. Variables d'environnement à définir sur le serveur

| Variable | Rôle | Exemple |
|---|---|---|
| `DJANGO_DEBUG` | Doit rester `False` en production | `False` |
| `DJANGO_SECRET_KEY` | Clé secrète, obligatoire quand `DEBUG` est désactivé | une longue chaîne aléatoire |
| `DJANGO_ALLOWED_HOSTS` | Noms de domaine autorisés | `monsite.com,www.monsite.com` |
| `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` | Base PostgreSQL (facultatif) | `monblog`, `...` |

Générer une clé secrète :

    python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"

## 2. Installation sur le serveur

    git clone <url-du-depot> projet && cd projet
    python -m venv env
    source env/bin/activate           # Windows : env\Scripts\activate
    pip install -r requirements.txt

## 3. Base de données et fichiers statiques

    python manage.py migrate
    python manage.py createsuperuser
    python manage.py collectstatic --noinput

`collectstatic` copie les fichiers statiques dans le dossier `staticfiles/` (`STATIC_ROOT`).

## 4. Lancer l'application avec Gunicorn

    gunicorn config.wsgi --bind 127.0.0.1:8000

Sur une plateforme PaaS (Heroku, Render…), le fichier `Procfile` indique la commande de démarrage.

## 5. Serveur web (VPS)

Nginx écoute sur les ports 80/443 :
- les requêtes `/static/` sont servies directement depuis `staticfiles/` ;
- les autres requêtes sont transmises à Gunicorn (`proxy_pass http://127.0.0.1:8000;`).

HTTPS : un certificat Let's Encrypt configuré sur Nginx. Les PaaS gèrent souvent le HTTPS automatiquement.

## 6. Vérifications de sécurité

    python manage.py check --deploy

Une fois le site servi en HTTPS, ajoutez dans `settings.py` les réglages que cette commande
demande (`SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, `SECURE_HSTS_SECONDS`).
Ils ne doivent pas être activés tant que le HTTPS n'est pas en place, sinon le site devient inaccessible.
