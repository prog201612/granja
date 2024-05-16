from django.urls import path

from api.api_views import CustomAuthToken

from api.globg import urls as globg_urls

urlpatterns = [
    path('v1/api-token-auth/', CustomAuthToken.as_view())
]

urlpatterns += globg_urls.urlpatterns
