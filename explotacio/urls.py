from django.urls import path

from . import views

urlpatterns = [
    path('nova-entrada-de-material/', views.nova_entrada_de_material, name='explotacio_nova-entrada-de-material'),
    path('enviar-material-al-estoc/', views.enviar_material_al_estoc, name='explotacio_enviar-material-al-estoc'),
    path('moure-estoc-entre-capacitats-del-mateix-tipus/', views.moure_estoc_entre_capacitats_del_mateix_tipus, name='explotacio_moure-estoc-entre-capacitats-del-mateix-tipus'),
]