"""
URL configuration for granja project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.conf import settings

urlpatterns = [
    path('api/', include('api.api_urls')),
    path('clients/', include('clients.urls')),
    path('explotacio/', include('explotacio.urls')),
    path('', RedirectView.as_view(url='admin')),
    path('admin/', admin.site.urls),
]

# Imatges en mode debug
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Personalització de l'administració
admin.site.site_title = u'VILARDELL'
admin.site.site_header = u'VILARDELL'
admin.site.index_title = u'Panell administratiu'