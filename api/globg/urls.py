from django.urls import path
from rest_framework import routers

from api.globg import views

router = routers.SimpleRouter()
router.register(r'v1/globg-personaLegal', views.PersonaLegalViewSet)

urlpatterns =[
    path('v1/get_queryset_count/', views.get_queryset_count, name='get_queryset_count'),
] + router.urls