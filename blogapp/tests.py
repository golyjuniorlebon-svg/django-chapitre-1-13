import io
from contextlib import redirect_stdout

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Article, Commentaire

PASSWORD = 'MotDePasse-Solide-2026'


class BlogBaseTests(TestCase):
    def setUp(self):
        self.auteur = User.objects.create_user(username='auteur', password=PASSWORD)
        self.autre = User.objects.create_user(username='autre', password=PASSWORD)
        self.article = Article.objects.create(titre='Mon article', contenu='Contenu du test', auteur=self.auteur)


class AccueilBlogTests(BlogBaseTests):
    def test_accueil_affiche_les_articles(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mon article')

    def test_pagination_cinq_articles_par_page(self):
        with redirect_stdout(io.StringIO()):
            for i in range(6):
                Article.objects.create(titre=f'Article {i}', contenu='x', auteur=self.auteur)
        response = self.client.get('/blog/')
        self.assertEqual(len(response.context['articles_a_afficher']), 5)
        self.assertEqual(response.context['articles_a_afficher'].paginator.num_pages, 2)

    def test_page_invalide_ne_plante_pas(self):
        self.assertEqual(self.client.get('/blog/?page=toto').status_code, 200)
        self.assertEqual(self.client.get('/blog/?page=999').status_code, 200)


class CrudArticleTests(BlogBaseTests):
    def test_creer_article_redirige_les_anonymes(self):
        response = self.client.get('/blog/article/creer/')
        self.assertRedirects(response, '/comptes/login/?next=/blog/article/creer/',
                             fetch_redirect_response=False)

    def test_utilisateur_connecte_cree_un_article(self):
        self.client.force_login(self.autre)
        with redirect_stdout(io.StringIO()):
            response = self.client.post('/blog/article/creer/', {'titre': 'Nouveau', 'contenu': 'Texte'})
        nouvel_article = Article.objects.get(titre='Nouveau')
        self.assertRedirects(response, reverse('blogapp:detail_article', args=[nouvel_article.pk]))
        self.assertEqual(nouvel_article.auteur, self.autre)

    def test_seul_l_auteur_peut_modifier(self):
        self.client.force_login(self.autre)
        with redirect_stdout(io.StringIO()):
            self.client.post(reverse('blogapp:modifier_article', args=[self.article.pk]),
                             {'titre': 'Piraté', 'contenu': 'x'})
        self.article.refresh_from_db()
        self.assertEqual(self.article.titre, 'Mon article')

    def test_auteur_modifie_son_article(self):
        self.client.force_login(self.auteur)
        with redirect_stdout(io.StringIO()):
            self.client.post(reverse('blogapp:modifier_article', args=[self.article.pk]),
                             {'titre': 'Modifié', 'contenu': 'Nouveau texte'})
        self.article.refresh_from_db()
        self.assertEqual(self.article.titre, 'Modifié')

    def test_seul_l_auteur_peut_supprimer(self):
        self.client.force_login(self.autre)
        with redirect_stdout(io.StringIO()):
            self.client.post(reverse('blogapp:supprimer_article', args=[self.article.pk]))
        self.assertTrue(Article.objects.filter(pk=self.article.pk).exists())

    def test_auteur_supprime_son_article(self):
        self.client.force_login(self.auteur)
        with redirect_stdout(io.StringIO()):
            response = self.client.post(reverse('blogapp:supprimer_article', args=[self.article.pk]))
        self.assertRedirects(response, reverse('blogapp:accueil'))
        self.assertFalse(Article.objects.filter(pk=self.article.pk).exists())

    def test_confirmation_suppression_affichee_en_get(self):
        self.client.force_login(self.auteur)
        response = self.client.get(reverse('blogapp:supprimer_article', args=[self.article.pk]))
        self.assertContains(response, 'Oui, supprimer')
        self.assertTrue(Article.objects.filter(pk=self.article.pk).exists())


class CommentaireTests(BlogBaseTests):
    def test_auteur_ne_peut_pas_commenter_son_article(self):
        self.client.force_login(self.auteur)
        self.client.post(reverse('blogapp:ajouter_commentaire', args=[self.article.pk]),
                         {'contenu': 'Mon propre avis'})
        self.assertEqual(Commentaire.objects.count(), 0)

    def test_autre_utilisateur_peut_commenter(self):
        self.client.force_login(self.autre)
        self.client.post(reverse('blogapp:ajouter_commentaire', args=[self.article.pk]),
                         {'contenu': 'Bel article'})
        commentaire = Commentaire.objects.get()
        self.assertEqual(commentaire.auteur, self.autre)
        self.assertEqual(commentaire.article, self.article)

    def test_anonyme_ne_peut_pas_commenter(self):
        response = self.client.post(reverse('blogapp:ajouter_commentaire', args=[self.article.pk]),
                                    {'contenu': 'x'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Commentaire.objects.count(), 0)

    def test_detail_affiche_commentaires_et_formulaire(self):
        Commentaire.objects.create(article=self.article, auteur=self.autre, contenu='Super')
        self.client.force_login(self.autre)
        response = self.client.get(reverse('blogapp:detail_article', args=[self.article.pk]))
        self.assertContains(response, 'Super')
        self.assertContains(response, 'Laissez un commentaire')


class ProfilEtSignauxTests(BlogBaseTests):
    def test_profil_liste_les_articles_de_l_auteur(self):
        response = self.client.get('/blog/profil/auteur/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mon article')

    def test_profil_inconnu_renvoie_404(self):
        self.assertEqual(self.client.get('/blog/profil/inconnu/').status_code, 404)

    def test_signal_a_la_creation(self):
        sortie = io.StringIO()
        with redirect_stdout(sortie):
            Article.objects.create(titre='Signal', contenu='x', auteur=self.auteur)
        self.assertIn("ARTICLE CRÉÉ : 'Signal' par auteur", sortie.getvalue())

    def test_signal_a_la_mise_a_jour(self):
        sortie = io.StringIO()
        with redirect_stdout(sortie):
            self.article.titre = 'Changé'
            self.article.save()
        self.assertIn("ARTICLE MIS À JOUR : 'Changé'", sortie.getvalue())

    def test_signal_avant_suppression(self):
        sortie = io.StringIO()
        with redirect_stdout(sortie):
            self.article.delete()
        self.assertIn('ATTENTION SUPPRESSION', sortie.getvalue())
