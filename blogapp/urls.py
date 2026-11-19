from django.urls import path
from . import views

app_name = 'blogapp'

urlpatterns = [
    path('', views.accueil_view, name='accueil'),
    path('article/creer/', views.creer_article_view, name='creer_article'),
    path('article/<int:pk>/', views.detail_article_view, name='detail_article'),
    path('article/<int:pk>/modifier/', views.modifier_article_view, name='modifier_article'),
    path('article/<int:pk>/supprimer/', views.supprimer_article_view, name='supprimer_article'),
    path('article/<int:article_pk>/ajouter_commentaire/', views.ajouter_commentaire_view,
         name='ajouter_commentaire'),
    path('profil/<str:username>/', views.profil_utilisateur_view, name='profil_utilisateur'),
]
