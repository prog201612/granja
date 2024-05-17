
from django.apps import apps
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from rest_framework import viewsets, permissions
from rest_framework.decorators import permission_classes, api_view, action
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.views import APIView

from api.globg import serializers
from globg import models

# G e t   Q u e r y   S e t   C o u n t

@api_view()
def get_queryset_count(request):
    # ?app=appName&model=modelName&filters=name__exact=El pitxa,active=True
    if request.method != 'GET':
        return Response({'error': 'GET request required'}, status=400)
    
    app = request.query_params.get('app', None)
    model = request.query_params.get('model', None)
    filters = request.query_params.get('filters', None)

    if not app or not model:
        return Response({'error': 'app and model query parameters required'}, status=400)

    # F i l t r e s
    filter_dict = {}
    if filters:
        filter_pairs = filters.split(',')
        for pair in filter_pairs:
            key, value = pair.split('=')
            filter_dict[key] = value

    # Recuperem el model partint del nom de l'aplicació i el nom del model
    model = apps.get_model(app, model)

    count = 0
    if filter:
        count = model.objects.filter(**filter_dict).count()
    count = model.objects.all().count()

    return Response({'count': count})
    


# P C R M o d e l V i e w S e t

class PCRModelViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        return self.queryset_by_url_params(self.request, self.queryset.model)

    def queryset_by_url_params(self, request, model):
        # ?page=1&offset=3&filters=name__exact=El pitxa,active=True&orderby=name,-active
        page = request.query_params.get('page', None)
        offset = request.query_params.get('offset', None)
        filters = request.query_params.get('filters', None)
        orders = request.query_params.get('orderby', None)

        # F i l t r e s
        filter_dict = {}
        if filters:
            filter_pairs = filters.split(',')
            for pair in filter_pairs:
                key, value = pair.split('=')
                filter_dict[key] = value

        # O r d e n a c i ó
        order_list = []
        if orders:
            order_list = orders.split(',')

        # P a g i n a c i ó   f i l t r a d a
        if page and offset:
            try:
                page =int(page) - 1
                offset = int(offset)
                # Ens interessa només la pàgina actual que està sol·licitant el client
                if filter:
                    return model.objects.filter(**filter_dict).order_by(*order_list)[page*offset:page*offset+offset]
                return model.objects.all().order_by(*order_list)[page*offset:page*offset+offset]
            except Exception as e:
                print("ERROR: ", e)
        return self.queryset # model.objects.all()  
    
    @action(detail=False, methods=['get'])
    def count(self, request, *args, **kwargs):
        # /count/?filters=name__exact=El pitxa,active=True
        filters = request.query_params.get('filters', None)

        # F i l t r e s
        filter_dict = {}
        if filters:
            filter_pairs = filters.split(',')
            for pair in filter_pairs:
                key, value = pair.split('=')
                filter_dict[key] = value

        count = 0
        if filter:
            count = self.queryset.model.objects.filter(**filter_dict).count()
        else:
            count = self.queryset.model.objects.all().count()

        return Response({'count': count})

# P e r s o n a L e g a l V i e w S e t

@permission_classes((permissions.DjangoModelPermissions,))
class PersonaLegalViewSet(PCRModelViewSet):
    queryset = models.PersonaLegal.objects.all()
    serializer_class = serializers.PersonaLegalSerializer


@permission_classes((permissions.DjangoModelPermissions,))
class TelefonViewSet(PCRModelViewSet):
    queryset = models.Telefon.objects.all()
    serializer_class = serializers.TelefonSerializer


@permission_classes((permissions.DjangoModelPermissions,))
class EmailViewSet(PCRModelViewSet):
    queryset = models.Email.objects.all()
    serializer_class = serializers.EmailSerializer

    """ DE MOMENT NO HO UTILITZEM
    @action(detail=False, methods=['get'])
    def x_persona_legal(self, request, *args, **kwargs):
        # /x_persona_legal/?persona_legal_id=1
        persona_legal_id = request.query_params.get('persona_legal_id', None)
        persona_legal = get_object_or_404(models.PersonaLegal, pk=persona_legal_id)
        if persona_legal:
            return Response(models.Email.objects.filter(persona_legal=persona_legal))
        return Response({'error': 'no hi ha dades de la persona_legal'}, status=400)
    """

# T i p u s   P r o d u c t e

@permission_classes((permissions.DjangoModelPermissions,))
class TipusProducteViewSet(PCRModelViewSet):
    queryset = models.TipusProducte.objects.all()
    serializer_class = serializers.TipusProducteSerializer

# D o c u m e n t a c i ó

@permission_classes((permissions.DjangoModelPermissions,))
class DocumentacioViewSet(PCRModelViewSet):
    queryset = models.Documentacio.objects.all()
    serializer_class = serializers.DocumentacioSerializer


# U p l o a d   I m a g e

@permission_classes((permissions.IsAuthenticated,))
class FileUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request, filename, format=None):
        # filename = "app_model-id-field"
        print("FileUploadView", filename, request.data)

        filename_array = filename.split('-')
        field = filename_array[-1:][0]
        id = filename_array[-2:-1][0]
        app_model = filename_array[-3:-2][0]

        print(field, id, app_model, format)
        returned_filename = ""

        if app_model == "globgdocumentacio":
            from globg.models import Documentacio
            documentacio = get_object_or_404(Documentacio, pk=id)
            #material_reference.image.delete(save=True) # Al copiar un item s'eliminaria el  del original
            #material_reference.save()
            documentacio.document = request.data['file'] # request.FILES['file']
            documentacio.save()
            returned_filename = documentacio.document.url

        return JsonResponse({'filename': returned_filename})