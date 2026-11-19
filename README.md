# Projet Django du groupe

Projet Django regroupant les chapitres 1 à 13 du cours : pages, formulaires, authentification,
administration, fichiers statiques, blog et déploiement.

## Lancer le projet en développement

Par défaut, `DEBUG` est désactivé. Pour développer en local, activez-le dans le terminal avant de lancer Django.

Windows (PowerShell) :

    $env:DJANGO_DEBUG="True"
    python manage.py runserver

Windows (invite de commandes) :

    set DJANGO_DEBUG=True
    python manage.py runserver

Sans cette variable, Django demande `DJANGO_SECRET_KEY` et refuse de démarrer.

## Pages principales

| URL | Contenu |
|---|---|
| `/` | Accueil (pages) |
| `/messages/` | Messages de contact non traités (connexion requise) |
| `/contact/` | Formulaire de contact |
| `/comptes/login/` | Connexion |
| `/inscription/` | Inscription |
| `/admin/` | Administration Django |
| `/blog/` | Blog : liste paginée des articles |

## Blog

- Les utilisateurs connectés peuvent créer, modifier et supprimer leurs articles.
- Tout le monde peut lire les articles et voir le profil des auteurs (`/blog/profil/<nom>/`).
- Un utilisateur connecté peut commenter les articles des autres, mais pas les siens.
- Le fichier `blogapp/signals.py` affiche dans la console chaque création, modification ou suppression d'article.

## Tests

    $env:DJANGO_DEBUG="True"
    python manage.py test

## Déploiement

Voir `DEPLOIEMENT.md`.
