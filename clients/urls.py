from django.urls import path

from . import views

urlpatterns = [
    path('afegir-articles-estoc-a-venda/', views.afegir_articles_estoc_a_venda, name='clients_afegir-articles-estoc-a-venda'),
    path('article-defuncio/', views.article_defuncio, name='clients_article-defuncio'),
    
]