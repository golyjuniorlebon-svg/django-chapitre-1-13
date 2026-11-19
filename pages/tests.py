from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.views.generic import ListView, TemplateView

from .models import ContactMessage
from .views import HomePageView, MessageListView

PASSWORD = 'MotDePasse-Solide-2026'


class HomePageTests(TestCase):
    def test_home_utilise_template_et_contexte(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertContains(response, 'Bonjour, LOI !')
        self.assertContains(response, 'Vous êtes connecté.')
        self.assertContains(response, 'Aquamaria')


class MessageListTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alice', password=PASSWORD)
        self.client.force_login(self.user)
        ContactMessage.objects.create(name="Alice", email="alice@example.com", message="Bonjour")
        ContactMessage.objects.create(name="Bob", email="bob@example.com",
                                      message="Déjà traité", is_treated=True)

    def test_seuls_les_messages_non_traites_sont_affiches(self):
        response = self.client.get(reverse('message_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'message_list.html')
        self.assertContains(response, 'Alice')
        self.assertNotContains(response, 'Bob')

    def test_liste_vide(self):
        ContactMessage.objects.all().delete()
        response = self.client.get('/messages/')
        self.assertContains(response, 'Aucun nouveau message de contact.')

    def test_str(self):
        msg = ContactMessage.objects.get(name="Alice")
        self.assertEqual(str(msg), "Message de Alice")


class StaticFilesTests(TestCase):
    def test_base_lie_la_feuille_de_style(self):
        response = self.client.get('/')
        self.assertContains(response, '/static/css/style.css')
        self.assertContains(response, 'Tous droits réservés')


class AdminTests(TestCase):
    def test_contact_message_est_enregistre_dans_admin(self):
        from django.contrib import admin
        self.assertTrue(admin.site.is_registered(ContactMessage))

    def test_page_admin_accessible(self):
        response = self.client.get('/admin/login/')
        self.assertEqual(response.status_code, 200)


class ContactFormTests(TestCase):
    def test_get_affiche_le_formulaire(self):
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')
        self.assertContains(response, 'csrfmiddlewaretoken')
        self.assertContains(response, 'name="email"')

    def test_post_valide_enregistre_et_redirige(self):
        data = {'name': 'Charlie', 'email': 'charlie@email.com', 'message': 'Bonjour'}
        response = self.client.post(reverse('contact'), data, follow=True)
        self.assertRedirects(response, reverse('home'))
        self.assertContains(response, 'Message envoyé avec succès')
        self.assertTrue(ContactMessage.objects.filter(name='Charlie').exists())

    def test_post_invalide_reste_sur_la_page(self):
        data = {'name': 'X', 'email': 'pas-un-email', 'message': ''}
        response = self.client.post(reverse('contact'), data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('email', response.context['form'].errors)
        self.assertIn('message', response.context['form'].errors)
        self.assertEqual(ContactMessage.objects.count(), 0)


class ClassBasedViewTests(TestCase):
    def test_home_est_une_templateview(self):
        self.assertTrue(issubclass(HomePageView, TemplateView))
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_liste_est_une_listview(self):
        self.assertTrue(issubclass(MessageListView, ListView))
        user = User.objects.create_user(username='alice', password=PASSWORD)
        self.client.force_login(user)
        ContactMessage.objects.create(name="Alice", email="alice@example.com", message="Test")
        response = self.client.get('/messages/')
        self.assertIn('message_list', response.context)


class AuthTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alice', password=PASSWORD)

    def test_page_de_connexion(self):
        response = self.client.get('/comptes/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_connexion_redirige_vers_next(self):
        data = {'username': 'alice', 'password': PASSWORD, 'next': '/messages/'}
        response = self.client.post('/comptes/login/', data)
        self.assertRedirects(response, '/messages/')

    def test_deconnexion_en_post(self):
        self.client.force_login(self.user)
        response = self.client.post('/comptes/logout/')
        self.assertRedirects(response, '/')

    def test_deconnexion_refusee_en_get(self):
        self.client.force_login(self.user)
        response = self.client.get('/comptes/logout/')
        self.assertEqual(response.status_code, 405)

    def test_inscription_cree_un_utilisateur(self):
        data = {'username': 'bob', 'password1': PASSWORD, 'password2': PASSWORD}
        response = self.client.post('/inscription/', data)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='bob').exists())

    def test_messages_protegees_pour_les_anonymes(self):
        response = self.client.get('/messages/')
        self.assertRedirects(response, '/comptes/login/?next=/messages/',
                             fetch_redirect_response=False)

    def test_base_affiche_l_utilisateur_connecte(self):
        self.client.force_login(self.user)
        response = self.client.get('/')
        self.assertContains(response, '<strong>alice</strong>')
        self.assertContains(response, 'Déconnexion')

    def test_base_affiche_connexion_pour_les_anonymes(self):
        response = self.client.get('/')
        self.assertContains(response, 'Connexion')
        self.assertContains(response, 'Inscription')


class ContactTests(TestCase):
    """Alias de sécurité : le formulaire de contact reste public."""
    def test_contact_accessible_sans_connexion(self):
        self.assertEqual(self.client.get('/contact/').status_code, 200)


class SignupFrenchTests(TestCase):
    def test_formulaire_inscription_en_francais(self):
        response = self.client.get('/inscription/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nom d\u2019utilisateur")
        self.assertContains(response, "Confirmation du mot de passe")
        self.assertNotContains(response, "Password confirmation")
        self.assertNotContains(response, "Username")
