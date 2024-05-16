from django.contrib import admin
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from explotacio import models

# P r o v e ï d o r

class ArticlesProveidorInline(admin.TabularInline):
    model = models.ArticlesProveidor
    extra = 1

@admin.register(models.Proveidors)
class ProveidorAdmin(admin.ModelAdmin):
    list_display = ('persona_legal', 'descripcio',) #  'actiu', 'creat_el_dia', 'modificat_el_dia'
    list_filter = ('actiu',)
    search_fields = ('persona_legal__nom', 'descripcio')
    # date_hierarchy = 'creat_el_dia'
    inlines = [ArticlesProveidorInline,]


# A r t i c l e   d e l   p r o v e ï d o r

@admin.register(models.ArticlesProveidor)
class ArticlesProveidorAdmin(admin.ModelAdmin):
    list_display = ('proveidor', 'nom', 'unitat_de_mesura', 'tipus', 'preu', 'actiu') # , 'creat_el_dia', 'modificat_el_dia'
    list_filter = ('actiu','tipus') # 'creat_el_dia', 'modificat_el_dia'
    search_fields = ('proveidor__persona_legal__nom', 'nom', 'categoria_corral__nom')
    # date_hierarchy = 'creat_el_dia'


# C o m a n d a   d e l   p r o v e ï d o r

class DetallComandaProveidorInline(admin.TabularInline):
    model = models.DetallComandaProveidor
    extra = 1
    fields = ['article', 'quantitat']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(processada=False)  # només mostrar les línies no processades

    # Les línies han de ser readonly si s'està afegint la comanda
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return []
        return ['actiu', 'article', 'quantitat']
    
    # només es pot afegir línies si la comanda ja està creada
    def has_add_permission(self, request, obj=None):
        if obj:
            return True
        return False

    # Ens cal filtrar que els articles siguin del proveïdor de la comanda
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # si el path acaba amb '/add/' és que estem afegint una nova comanda
        if request.META['PATH_INFO'].endswith('/add/'):
            return super().formfield_for_foreignkey(db_field, request, **kwargs)

        # Si s'està editant filtrem els articles que siguin del proveïdor de la comanda
        comanda_id = int(request.META['PATH_INFO'].rstrip('/').split('/')[-2])
        comanda = models.ComandesProveidor.objects.get(pk=comanda_id)
        proveidor_id = comanda.proveidor.id
        if db_field.name == 'article':
            kwargs['queryset'] = models.ArticlesProveidor.objects.filter(proveidor=proveidor_id)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class DetallComandaProveidorProcessadaInline(admin.TabularInline):
    model = models.DetallComandaProveidor
    extra = 0

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.title = 'Línies processades'
        return formset

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(processada=True)  # només mostrar les línies processades

    # només es pot afegir línies si la comanda ja està creada
    def has_add_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    

@admin.register(models.ComandesProveidor)
class ComandesProveidorAdmin(admin.ModelAdmin):
    list_display = ('proveidor', 'data_comanda', 'data_entrega', 'observacions', 'actiu', 'creat_el_dia', 'modificat_el_dia')
    list_filter = ('actiu', 'creat_el_dia', 'modificat_el_dia')
    search_fields = ('proveidor__persona_legal__nom', 'observacions')
    date_hierarchy = 'creat_el_dia'
    inlines = [DetallComandaProveidorInline, DetallComandaProveidorProcessadaInline,]

    # D e f a u l t   F i l t e r

    def changelist_view(self, request, *args, **kwargs):
        if "actiu__exact" not in request.build_absolute_uri():
            url = reverse('admin:%s_%s_changelist' % (self.model._meta.app_label, self.model._meta.model_name))
            return HttpResponseRedirect("%s?%s" % (url, "actiu__exact=1")) #
        return super().changelist_view(request, *args, **kwargs)


# D e t a l l   d e   l a   c o m a n d a   d e l   p r o v e ï d o r

@admin.register(models.DetallComandaProveidor)
class DetallComandaProveidorAdmin(admin.ModelAdmin):
    list_display = ('comanda', 'article', 'quantitat', 'actiu', 'creat_el_dia', 'modificat_el_dia')
    list_filter = ('processada', 'creat_el_dia', 'modificat_el_dia') # 'actiu', 
    search_fields = ('comanda__proveidor__persona_legal__nom', 'article__nom')
    date_hierarchy = 'creat_el_dia'
    actions = ['crear_entrades_de_material', 'enviar_material_al_estoc',]
    #readonly_fields = ['comanda', 'article', 'processada']

    # R e a d o n l y

    def get_readonly_fields(self, request, obj=None):    
        if obj and obj.processada:
            return ['comanda', 'article', 'quantitat', 'processada', 'actiu']
        return ['comanda', 'article', 'processada', 'actiu']

    # P e r m i s s i o n s

    def has_add_permission(self, request):
        return False
    
    # A c t i o n s

    def crear_entrades_de_material(modeladmin, request, queryset):
        # Ens cal una acció per crear EntradesDeMaterial a partir dels DetallComandaProveidor seleccionats
        # Si es selecciona més d'una fila mostrem un error
        if len(queryset) != 1:
            modeladmin.message_user(request, "Selecciona només una línia", level='WARNING')
            return
        elif queryset[0].processada == True:
            modeladmin.message_user(request, "La línia ja ha estat processada", level='ERROR')
            return
        return render(request, 'explotacio/crear-entrades-de-material.html', {'linia': queryset[0]})
    crear_entrades_de_material.short_description = "Crear Entrades de Material"

    def enviar_material_al_estoc(modeladmin, request, queryset):
        """
        Aquesta acció fa 2 feines a l'hora:
        - crear_entrades_de_material
        - enviar_material_al_estoc (de EntradesDeMaterialAdmin)
        """
        if len(queryset) != 1:
            modeladmin.message_user(request, "Selecciona només una línia", level='WARNING')
            return
        elif queryset[0].processada == True:
            modeladmin.message_user(request, "La línia ja ha estat processada", level='ERROR')
            return
        
        # Creem una entrada de material
        capacitats = models.Capacitat.objects.filter(tipus=queryset[0].article.tipus.tipus_capacitat)
        quantitat = queryset[0].quantitat
        entrada = models.EntradesDeMaterial.objects.create(
            detall_comanda_proveidor = queryset[0],
            article = queryset[0].article,
            quantitat = quantitat
        )

        # Actualitzem el DetallComandaProveidor per marcar-lo com a processat
        queryset[0].processada = True
        queryset[0].save()

        context = {'linia': entrada, 'capacitats': capacitats, 'quantitat': quantitat}
        return render(request, 'explotacio/enviar-material-al-estoc.html', context)
    enviar_material_al_estoc.short_description = "Enviar material al estoc"

    # D e f a u l t   F i l t e r

    def changelist_view(self, request, *args, **kwargs):
        if "processada__exact" not in request.build_absolute_uri():
            url = reverse('admin:%s_%s_changelist' % (self.model._meta.app_label, self.model._meta.model_name))
            return HttpResponseRedirect("%s?%s" % (url, "processada__exact=0")) #
        return super().changelist_view(request, *args, **kwargs)
        

# E n t r a d e s   D e   M a t e r i a l

@admin.register(models.EntradesDeMaterial)
class EntradesDeMaterialAdmin(admin.ModelAdmin):
    list_display = ('detall_comanda_proveidor', 'quantitat', 'assignats_a_corral') # , 'actiu', 'creat_el_dia', 'modificat_el_dia'
    list_filter = ('actiu', 'creat_el_dia', 'modificat_el_dia')
    search_fields = ('detall_comanda_proveidor__article__nom', 'detall_comanda_proveidor__comanda__proveidor__persona_legal__nom')
    date_hierarchy = 'creat_el_dia'
    actions = ['enviar_material_al_estoc',]

    # A c t i o n s

    def enviar_material_al_estoc(modeladmin, request, queryset):
        # Ens cal una acció per enviar el material entrat cap a l'estoc d'alguna capacitat
        if len(queryset) != 1:
            modeladmin.message_user(request, "Selecciona només una línia", level='WARNING')
            return
        elif queryset[0].quantitat == queryset[0].assignats_a_corral:
            modeladmin.message_user(request, "La línia ja ha estat processada", level='ERROR')
            return
        elif queryset[0].detall_comanda_proveidor.article.tipus is None:
            modeladmin.message_user(request, "L'article no té un tipus seleccionat, modifica l'article", level='ERROR')
            return
        capacitats = models.Capacitat.objects.filter(tipus=queryset[0].detall_comanda_proveidor.article.tipus.tipus_capacitat)
        quantitat = queryset[0].quantitat - queryset[0].assignats_a_corral
        context = {'linia': queryset[0], 'capacitats': capacitats, 'quantitat': quantitat}
        return render(request, 'explotacio/enviar-material-al-estoc.html', context)
    enviar_material_al_estoc.short_description = "Enviar material al estoc"

    # D e f a u l t   F i l t e r

    def changelist_view(self, request, *args, **kwargs):
        if "actiu__exact" not in request.build_absolute_uri():
            url = reverse('admin:%s_%s_changelist' % (self.model._meta.app_label, self.model._meta.model_name))
            return HttpResponseRedirect("%s?%s" % (url, "actiu__exact=1")) #
        return super().changelist_view(request, *args, **kwargs)


# C a p a c i t a t

class CapacitatEstocInline(admin.TabularInline):
    model = models.CapacitatEstoc
    extra = 1

    # només es pot afegir línies si la comanda ja està creada
    def has_add_permission(self, request, obj=None):
        if obj:
            return True
        return False


@admin.register(models.Capacitat)
class CapacitatAdmin(admin.ModelAdmin):
    list_display = ('nom', 'tipus', 'capacitat') # , 'creat_el_dia', 'modificat_el_dia'
    list_filter = ('tipus', 'actiu') # , 'creat_el_dia', 'modificat_el_dia'
    search_fields = ('corral__nom', 'article__nom')
    date_hierarchy = 'creat_el_dia'
    inlines = [CapacitatEstocInline,]


# C a p a c i t a t   E s t o c

@admin.register(models.CapacitatEstoc)
class CapacitatEstocAdmin(admin.ModelAdmin):
    list_display = ('capacitat', 'article_nom', 'quantitat', )
    list_filter = ('capacitat__tipus', 'actiu', ) # 'creat_el_dia', 'modificat_el_dia'
    search_fields = ('capacitat__nom', 'tipus_producte__nom')
    date_hierarchy = 'creat_el_dia'
    actions = ['moure_estoc_entre_capacitats_del_mateix_tipus',]

    # A c c i o n s

    def moure_estoc_entre_capacitats_del_mateix_tipus(modeladmin, request, queryset):
        # Ens cal una acció per moure material entre capacitats d'estoc del mateix tipus
        if len(queryset) != 1:
            modeladmin.message_user(request, "Selecciona només una línia", level='WARNING')
            return
        # Ens cal recuperar totes les capacitats del mateix tipus que la capacitat de la linia seleccionada
        capacitats = models.Capacitat.objects.filter(tipus=queryset[0].capacitat.tipus).exclude(pk=queryset[0].capacitat.pk)
        context = {'linia': queryset[0], 'capacitats': capacitats}
        return render(request, 'explotacio/moure-estoc-entre-capacitats-del-mateix-tipus.html', context)
    moure_estoc_entre_capacitats_del_mateix_tipus.short_description = "Moure estoc entre capacitats del mateix tipus"