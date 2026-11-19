from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from .models import Article


@receiver(post_save, sender=Article)
def log_article_sauvegarde(sender, instance, created, **kwargs):
    if created:
        print(f"ARTICLE CRÉÉ : '{instance.titre}' par {instance.auteur.username}")
    else:
        print(f"ARTICLE MIS À JOUR : '{instance.titre}'")


@receiver(pre_delete, sender=Article)
def log_avant_suppression_article(sender, instance, **kwargs):
    print(f"ATTENTION SUPPRESSION : L'article '{instance.titre}' (ID: {instance.id}) va être supprimé.")
