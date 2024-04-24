from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from clients import models
from explotacio.models import CapacitatEstoc
from globg.models import CAPACITAT_TIPUS_CORRAL

# C l i e n t s
 
@admin.register(models.Clients) 
class ClientsAdmin(admin.ModelAdmin):
    list_display = ('persona_legal', 'descripcio')
    search_fields = ['persona_legal__nom', 'descripcio']

# V e n d e s

class DetallVendaInline(admin.TabularInline):
    model = models.DetallVenda
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(models.Vendes)
class VendesAdmin(admin.ModelAdmin):
    list_display = ('client', 'data_venta', 'quantitat_venda', 'total_venda', 'observacions')
    readonly_fields = ('quantitat_venda', 'total_venda', )
    search_fields = ['client__persona_legal__nom', 'observacions']
    inlines = [DetallVendaInline,]
    actions = ['afegir_articles_estoc_a_venda', 'defuncio',]

    # A c t i o n s

    # Acció per poder seleccionar quantitats de CapacitatEstoc i crear els DetallVenda
    def afegir_articles_estoc_a_venda(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(request, "Selecciona només una línia", level='WARNING')
            return
        capacitat_estoc = CapacitatEstoc.objects.filter(tipus_producte__tipus_capacitat=CAPACITAT_TIPUS_CORRAL)
        context = { "venda": queryset.first(), "capacitat_estoc": capacitat_estoc }
        return render(request, 'clients/afegir-articles-estoc-a-venda.html', context)
    afegir_articles_estoc_a_venda.short_description = "Afegir articles de l'estoc a la venda"

    # Acció per generar defuncions partint de les línies de DetallVenda
    def defuncio(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(request, "Selecciona només una línia", level='WARNING')
            return
        return render(request, 'clients/article-defuncio.html', { "venda": queryset.first() })
    defuncio.short_description = "Defuncions..."

"""
# D e t a l l s   d e   l a   v e n d a

class DefuncionsInline(admin.TabularInline):
    model = models.Defuncions
    extra = 0

@admin.register(models.DetallVenda)
class DetallVendaAdmin(admin.ModelAdmin):
    list_display = ('venda', 'article', 'quantitat')
    search_fields = ['venda__client__persona_legal__nom', 'article__nom']
    inlines = [DefuncionsInline,]
"""

# D e f u n c i o n s

# crearem un filtre per les defuncions no documentades
class DefuncioNoDocumentada(admin.SimpleListFilter):
    title = 'Documentada'
    parameter_name = 'documentada'

    def lookups(self, request, model_admin):
        return (
            ('0', 'No'),
            ('1', 'Sí'),
        )

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(justificant__exact="")
        if self.value() == '1':
            return queryset.exclude(justificant__exact="")
        

@admin.register(models.Defuncions)
class DefuncionsAdmin(admin.ModelAdmin):
    list_display = ('detall_venda', 'tipus', 'data_defuncio', 'documentada')
    readonly_fields = ('documentada', )
    search_fields = ['detall_venda__venda__client__persona_legal__nom', 'observacions']
    date_hierarchy = 'data_defuncio'
    list_filter = [DefuncioNoDocumentada, 'tipus',]

    # No es pot afegir una nova defunció, es creen desde l'acció Defunció de la venda
    def has_add_permission(self, request):
        return False

    # D e f a u l t   F i l t e r

    def changelist_view(self, request, *args, **kwargs):
        if "documentada" not in request.build_absolute_uri():
            url = reverse('admin:%s_%s_changelist' % (self.model._meta.app_label, self.model._meta.model_name))
            return HttpResponseRedirect("%s?%s" % (url, "documentada=0")) #
        return super().changelist_view(request, *args, **kwargs)


