from django.contrib import admin
from .models import ContactMessage


class ContactMessageAdmin(admin.ModelAdmin):
    # Colonnes affichées dans la liste des messages
    list_display = ('name', 'email', 'created_at', 'is_treated')
    # Barre latérale de filtres
    list_filter = ('is_treated', 'created_at')
    # Barre de recherche
    search_fields = ('name', 'email', 'message')


admin.site.register(ContactMessage, ContactMessageAdmin)
