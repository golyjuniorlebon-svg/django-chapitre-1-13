from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView

from .forms import ContactModelForm
from .models import ContactMessage


class HomePageView(TemplateView):
    """Page d'accueil (CBV) : rend home.html avec un contexte."""
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Accueil (CBV)'
        context['nom_utilisateur'] = 'Loi'
        context['age'] = 25
        context['couleurs_preferees'] = ['Bleu', 'Gris', 'Aquamaria']
        context['est_connecte'] = True
        return context


class MessageListView(LoginRequiredMixin, ListView):
    """Liste des messages non traités (CBV), réservée aux utilisateurs connectés."""
    model = ContactMessage
    template_name = 'message_list.html'
    context_object_name = 'message_list'

    def get_queryset(self):
        return ContactMessage.objects.filter(is_treated=False).order_by('created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Liste des Messages (Protégé)'
        return context


def contact_view(request):
    """Formulaire de contact (FBV) : GET affiche, POST valide et enregistre."""
    if request.method == 'POST':
        form = ContactModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Message envoyé avec succès !')
            return redirect('home')  # Pattern PRG : Post/Redirect/Get
    else:
        form = ContactModelForm()

    context = {
        'form': form,
        'page_title': 'Contactez-nous',
    }
    return render(request, 'contact.html', context)


class SignUpView(CreateView):
    """Inscription (CBV) : crée un compte avec UserCreationForm."""
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
