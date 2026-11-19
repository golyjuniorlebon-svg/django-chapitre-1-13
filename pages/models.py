from django.db import models


class ContactMessage(models.Model):
    """
    Représente un message envoyé via un formulaire de contact.
    """
    name = models.CharField(max_length=100, verbose_name="Nom")
    email = models.EmailField(verbose_name="Adresse Email")
    message = models.TextField(verbose_name="Message")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    is_treated = models.BooleanField(default=False, verbose_name="Traité ?")

    def __str__(self):
        return f"Message de {self.name}"
