
from django.db import models
from django.utils import timezone
from django.utils.html import format_html

from globg.models import PCRBaseModel
from globg.utils import str_to_float_or_zero


TIPUS_DEFUNCIO_CORRAL = 'co'
TIPUS_DEFUNCIO_ESCORXADOR = 'es'
TIPUS_DEFUNCIO_CORRAL_ESCORXADOR = 'ce'
TIPUS_DEFUNCIO_TRANSPORT = 'tr'
TIPUS_DEFUNCIO_ALTRES = 'al'
TIPUS_DEFUNCIO = (
    (TIPUS_DEFUNCIO_CORRAL, 'Corral'),
    (TIPUS_DEFUNCIO_ESCORXADOR, 'Escorxador'),
    (TIPUS_DEFUNCIO_CORRAL_ESCORXADOR, 'Corral Escorxador'),
    (TIPUS_DEFUNCIO_TRANSPORT, 'Transport'),
    (TIPUS_DEFUNCIO_ALTRES, 'Altres'),
)

class Clients(PCRBaseModel):
    persona_legal = models.ForeignKey('globg.PersonaLegal', on_delete=models.CASCADE)
    descripcio = models.TextField("Descripció", blank=True, null=True)

    def __str__(self):
        return self.persona_legal.nom
    
    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ['persona_legal__nom']


class Vendes(PCRBaseModel):
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    data_venta = models.DateField(default=timezone.now)
    observacions = models.TextField("Observacions", blank=True, null=True)

    def quantitat_venda(self):
        total = self.detallvenda_set.all().aggregate(models.Sum('quantitat'))
        # total és un diccionari amb la clau 'quantitat__sum'
        return total['quantitat__sum']
    
    def total_venda(self):
        total = 0
        for detall in self.detallvenda_set.all():
            total += detall.total()
        return str_to_float_or_zero(total)

    def __str__(self):
        return f"{self.id} - {self.client.persona_legal.nom}"
    
    class Meta:
        verbose_name = "Venda"
        verbose_name_plural = "Ventes"
        ordering = ['-data_venta']


class DetallVenda(PCRBaseModel):
    venda = models.ForeignKey(Vendes, on_delete=models.CASCADE)
    article = models.ForeignKey('explotacio.ArticlesProveidor', on_delete=models.CASCADE)
    quantitat = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    preu_venda = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)

    def total(self):
        return self.quantitat * self.preu_venda

    def __str__(self):
        return f"{self.venda.id} - {self.article.nom} - {self.quantitat}"
    
    class Meta:
        verbose_name = "Detall de la venda"
        verbose_name_plural = "Detalls de la venda"
        ordering = ['venda__data_venta']


class Defuncions(PCRBaseModel):
    detall_venda = models.ForeignKey(DetallVenda, on_delete=models.CASCADE)
    data_defuncio = models.DateField(default=timezone.now)
    tipus = models.CharField(max_length=2, choices=TIPUS_DEFUNCIO, default=TIPUS_DEFUNCIO_ALTRES)
    justificant = models.FileField(upload_to='defuncions/', blank=True, null=True)

    def documentada(self):
        if self.justificant:
            return format_html('<img src="/static/admin/img/icon-yes.svg" alt="True">')
        return format_html('<img src="/static/admin/img/icon-no.svg" alt="False">')
