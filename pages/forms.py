from django import forms
from .models import ContactMessage


class ContactForm(forms.Form):
    """
    Formulaire simple (forms.Form) : nom, email et message.
    Conservé pour référence ; la vue utilise ContactModelForm.
    """
    name = forms.CharField(
        label="Votre Nom",
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Entrez votre nom'}),
    )
    email = forms.EmailField(
        label="Votre Email",
        widget=forms.EmailInput(attrs={'placeholder': 'nom@example.com'}),
    )
    message = forms.CharField(
        label="Votre Message",
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Votre message ici...'}),
        help_text="Soyez aussi précis que possible.",
    )


class ContactModelForm(forms.ModelForm):
    """
    Formulaire généré automatiquement à partir du modèle ContactMessage.
    """
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Votre nom ici'}),
            'email': forms.EmailInput(attrs={'placeholder': 'email@example.com'}),
            'message': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Laissez votre message...'}),
        }
        labels = {
            'name': 'Nom Complet',
            'email': 'Adresse Courriel',
        }
        help_texts = {
            'message': "Essayez d'être clair.",
        }
        error_messages = {
            'name': {
                'max_length': "Le nom est trop long.",
            },
        }
