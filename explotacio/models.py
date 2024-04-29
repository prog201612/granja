from django.db import models
from django.utils import timezone

from globg.models import PCRBaseModel
from globg.models import CAPACITAT_TIPUS

MESURES = (
    ('u', 'Unitats'),
    ('kg', 'Quilograms'),
    ('T', 'Tonelades')
)


class Proveidors(PCRBaseModel):
    persona_legal = models.ForeignKey('globg.PersonaLegal', on_delete=models.CASCADE)
    descripcio = models.TextField("Descripció", blank=True, null=True)

    def __str__(self):        
        return self.persona_legal.nom
    
    class Meta:
        verbose_name = "Proveïdor"
        verbose_name_plural = "01 - Proveïdors"
        ordering = ['persona_legal__nom']


class ArticlesProveidor(PCRBaseModel):
    proveidor = models.ForeignKey(Proveidors, on_delete=models.CASCADE)
    nom = models.CharField("Nom de l'article", max_length=100)
    descripcio = models.TextField("Descripció", blank=True, null=True)
    unitat_de_mesura = models.CharField(max_length=2, choices=MESURES, default='u')
    #categoria_corral = models.ForeignKey('globg.CategoriaCorral', on_delete=models.SET_NULL, blank=True, null=True)
    tipus = models.ForeignKey('globg.TipusProducte', on_delete=models.CASCADE)
    preu = models.DecimalField(max_digits=8, decimal_places=2)
    preu_venda = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):        
        return self.nom
    
    class Meta:
        verbose_name = "Article del proveïdor"
        verbose_name_plural = "02 - Articles del proveïdor"
        ordering = ['nom']


class ComandesProveidor(PCRBaseModel):
    proveidor = models.ForeignKey(Proveidors, on_delete=models.CASCADE)
    data_comanda = models.DateField(default=timezone.now)
    data_entrega = models.DateField(default=timezone.now)
    observacions = models.TextField("Observacions", blank=True, null=True)

    def __str__(self):        
        return f"{self.id} - {self.proveidor.persona_legal.nom}"
    
    class Meta:
        verbose_name = "Comanda del proveïdor"
        verbose_name_plural = "03 - Comandes del proveïdor"
        ordering = ['-data_comanda']


class DetallComandaProveidor(PCRBaseModel):
    comanda = models.ForeignKey(ComandesProveidor, on_delete=models.CASCADE)
    article = models.ForeignKey(ArticlesProveidor, on_delete=models.CASCADE)
    quantitat = models.DecimalField(max_digits=8, decimal_places=2)
    processada = models.BooleanField(default=False)

    def __str__(self):        
        return f"{self.comanda.id} - {self.article.nom} - {self.quantitat}"
    
    class Meta:
        verbose_name = "Detall de la comanda del proveïdor"
        verbose_name_plural = "04 - Detalls de la comanda (PROV.)"
        ordering = ['comanda']


class EntradesDeMaterial(PCRBaseModel):
    detall_comanda_proveidor = models.ForeignKey(DetallComandaProveidor, on_delete=models.CASCADE)
    quantitat = models.DecimalField(max_digits=8, decimal_places=2)
    assignats_a_corral = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    article = models.ForeignKey(ArticlesProveidor, on_delete=models.CASCADE)
    # quan quantitat = assignats_a_corral (Capacitat de tipus corral), posarem actiu = False

    class Meta:
        verbose_name = "Entrada de material"
        verbose_name_plural = "05 - Entrades de material"
        ordering = ['detall_comanda_proveidor']


class Capacitat(PCRBaseModel):
    nom = models.CharField(max_length=100)
    # Tipus de capacitat: 'co' - Corral, 'al' - Aliment, 're' - Rebuig
    tipus = models.CharField(max_length=2, choices=CAPACITAT_TIPUS)
    capacitat = models.DecimalField(max_digits=8, decimal_places=2)
    descripcio = models.TextField("Descripció", blank=True, null=True)

    def __str__(self):        
        return f"{self.nom} - {self.get_tipus_display()}"
    
    class Meta:
        verbose_name = "Capacitat"
        verbose_name_plural = "06 - Capacitats"
        ordering = ['tipus', 'capacitat']


class CapacitatEstoc(PCRBaseModel):
    """
    Quan agafem el producte de la EntradesDeMaterial, i l'assignem a un CapacitatEstoc, cal
    validar si ja existeix una entrada d'estoc pel mateix tipus de producte (i capacitat en
    conseqüència). Si existeix l'afegim a la mateixa entrada i si no, en creem una de nova.
    """
    capacitat = models.ForeignKey(Capacitat, on_delete=models.CASCADE)
    quantitat = models.DecimalField(max_digits=8, decimal_places=2)
    # El tipus_producte té el camp tipus_capacitat, i ha de coincidir amb el tipus de la capacitat
    tipus_producte = models.ForeignKey('globg.TipusProducte', on_delete=models.CASCADE, blank=True, null=True)
    article = models.ForeignKey(ArticlesProveidor, on_delete=models.CASCADE)

    def article_nom(self):
        return "" if not self.article else self.article.nom

    def __str__(self):        
        return f"{self.capacitat.nom} - {self.article.nom} - {self.tipus_producte.nom}"
    
    class Meta:
        verbose_name = "Capacitat estoc"
        verbose_name_plural = "07 - Capacitats estoc"
        ordering = ['capacitat__tipus', 'capacitat__capacitat']

    