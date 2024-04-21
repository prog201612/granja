from django.contrib import admin

from globg import models

# admin.site.register(models.Explotacio)

# T i p u s  P r o d u c t e

@admin.register(models.TipusProducte)
class TipusProducteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'tipus_capacitat')
    ordering = ['nom']
    list_filter = ('tipus_capacitat',)
    search_fields = ['nom']

# P e r s o n a   L e g a l

class EmailInline(admin.TabularInline):
    model = models.Email
    extra = 1


class TelefonInline(admin.TabularInline):
    model = models.Telefon
    extra = 1


@admin.register(models.PersonaLegal)
class PersonaLegalAdmin(admin.ModelAdmin):
    list_display = ('nom', 'dni_nif',)
    inlines = [EmailInline, TelefonInline]
    search_fields = ['nom', 'dni_nif']

