
from django.apps import apps

from rest_framework import viewsets, permissions
from rest_framework.decorators import permission_classes, api_view, action
from rest_framework.response import Response

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
        count = self.queryset.model.objects.all().count()

        return Response({'count': count})

# P e r s o n a L e g a l V i e w S e t

@permission_classes((permissions.DjangoModelPermissions,))
class PersonaLegalViewSet(PCRModelViewSet):
    queryset = models.PersonaLegal.objects.all()
    serializer_class = serializers.PersonaLegalSerializer