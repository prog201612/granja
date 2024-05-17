from django.urls import path
from rest_framework import routers

from api.globg import views

router = routers.SimpleRouter()
router.register(r'v1/globg-personaLegal', views.PersonaLegalViewSet)
router.register(r'v1/globg-emails', views.EmailViewSet)
router.register(r'v1/globg-telefons', views.TelefonViewSet)
router.register(r'v1/globg-tipusProducte', views.TipusProducteViewSet)
router.register(r'v1/globg-documentacio', views.DocumentacioViewSet)

urlpatterns =[
    path('v1/get_queryset_count/', views.get_queryset_count, name='get_queryset_count'),
    path('v1/upload-file/<str:filename>', views.FileUploadView.as_view(), name='v1_upload_file'),
] + router.urls
