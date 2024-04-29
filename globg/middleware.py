from datetime import timedelta

from django.contrib import messages
from django.utils import timezone
from django.utils.safestring import mark_safe

from globg.models import Documentacio


class AdvertenciaCaducitatMiddleware:
    """
    Quan caduquen els documents a globg Documentacio, mostra un missatge d'advertència a l'usuari.
    Al settings.py a MIDDLEWARE ho posem l'últim, ja que si ho posem abans no funciona però si
    ho posem després hem de fer el truc de tornar a recuperar la resposta després d'enviar el missatge.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # response = self.get_response(request) NOOO, O ES DUPLIQUEM LES DADES AL INSERTAR

        # Només ho mostrem per usuaris autenticats del staff a l'índex de l'admin
        if request.user.is_authenticated and request.user.is_staff and request.path_info.endswith('admin/'):
            data_limit = timezone.now().date() + timedelta(days=30)
            document = Documentacio.objects.filter(caduca_el_dia__lte=data_limit).first()
            # print(data_limit, document)
            if document:
                msg = f"El document <a href='/admin/globg/documentacio/{document.id}/change/'>{document.nom}</a> caduca el dia {document.caduca_el_dia}. "
                messages.warning(request, mark_safe(msg))

        # Si no ho fem així el missatge és veu una url més tard.
        response = self.get_response(request)

        return response