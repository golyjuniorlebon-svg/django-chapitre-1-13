from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ArticleForm, CommentaireForm
from .models import Article


def accueil_view(request):
    """Liste paginée des articles, du plus récent au plus ancien (5 par page)."""
    tous_les_articles = Article.objects.all().order_by('-date_creation')
    paginator = Paginator(tous_les_articles, 5)
    page_numero = request.GET.get('page')
    try:
        articles_pages = paginator.page(page_numero)
    except PageNotAnInteger:
        articles_pages = paginator.page(1)
    except EmptyPage:
        articles_pages = paginator.page(paginator.num_pages)
    return render(request, 'blogapp/accueil.html', {'articles_a_afficher': articles_pages})


@login_required
def creer_article_view(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            nouvel_article = form.save(commit=False)
            nouvel_article.auteur = request.user
            nouvel_article.save()
            return redirect('blogapp:detail_article', pk=nouvel_article.pk)
    else:
        form = ArticleForm()
    return render(request, 'blogapp/creer_modifier_article.html', {'form': form, 'action': 'Créer'})


def detail_article_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    context = {
        'article': article,
        'commentaire_form': CommentaireForm(),
    }
    return render(request, 'blogapp/detail_article.html', context)


@login_required
def modifier_article_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if article.auteur != request.user:
        return redirect('blogapp:detail_article', pk=article.pk)

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('blogapp:detail_article', pk=article.pk)
    else:
        form = ArticleForm(instance=article)

    context = {'form': form, 'action': 'Modifier', 'article': article}
    return render(request, 'blogapp/creer_modifier_article.html', context)


@login_required
def supprimer_article_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if article.auteur != request.user:
        return redirect('blogapp:detail_article', pk=article.pk)

    if request.method == 'POST':
        article.delete()
        return redirect('blogapp:accueil')
    return render(request, 'blogapp/confirmer_suppression_article.html', {'article': article})


@login_required
def ajouter_commentaire_view(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    # Règle du cours : l'auteur de l'article ne peut pas le commenter
    if article.auteur == request.user:
        return redirect('blogapp:detail_article', pk=article.pk)

    if request.method == 'POST':
        form = CommentaireForm(request.POST)
        if form.is_valid():
            commentaire = form.save(commit=False)
            commentaire.article = article
            commentaire.auteur = request.user
            commentaire.save()
    return redirect('blogapp:detail_article', pk=article.pk)


def profil_utilisateur_view(request, username):
    utilisateur_profil = get_object_or_404(User, username=username)
    articles_utilisateur = Article.objects.filter(auteur=utilisateur_profil).order_by('-date_creation')
    context = {
        'utilisateur_profil': utilisateur_profil,
        'articles_utilisateur': articles_utilisateur,
    }
    return render(request, 'blogapp/profil_utilisateur.html', context)
