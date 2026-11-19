from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Ajoute toutes les URLs définies dans pages/urls.py à la racine du site ('')
    path('', include('pages.urls')),
    # URLs d'authentification de Django : login, logout, password_change, password_reset...
    path('comptes/', include('django.contrib.auth.urls')),
    # Blog (chapitre 12) : toutes ses URLs commencent par /blog/
    path('blog/', include('blogapp.urls')),
]
