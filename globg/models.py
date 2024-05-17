from django.db import models
from django.utils import timezone

# B a s e   M o d e l   U F K   (UserForeignKey)

class PCRBaseModel(models.Model):
    """
     Classe base per a tots els models de l'aplicació
    """
    actiu = models.BooleanField(default=True)
    creat_el_dia = models.DateTimeField(auto_now_add=True)
    modificat_el_dia =models.DateTimeField(auto_now=True) 

    class Meta:
        # Django no utilitza les classes Abstractes a les migracions
        abstract = True

# ----------------------------------------------

CAPACITAT_TIPUS_CORRAL = 'co'
CAPACITAT_TIPUS_ALIMENT = 'al'
CAPACITAT_TIPUS_REBUIG = 're'
CAPACITAT_TIPUS = (
    (CAPACITAT_TIPUS_CORRAL, 'Corral'),
    (CAPACITAT_TIPUS_ALIMENT, 'Aliment'),
    (CAPACITAT_TIPUS_REBUIG, 'Rebuig'),
)

class Explotacio(PCRBaseModel):
    nom = models.CharField(max_length=100)
    descripcio = models.TextField()


class PersonaLegal(PCRBaseModel):
    nom = models.CharField(max_length=100)
    dni_nif = models.CharField(max_length=20)

    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name = "Persona Legal"
        verbose_name_plural = "Persones Legals"
        ordering = ['nom']


class Email(PCRBaseModel):
    persona_legal = models.ForeignKey(PersonaLegal, on_delete=models.CASCADE)
    email = models.EmailField()
    descripcio = models.CharField("Descripció", max_length=100)


class Telefon(PCRBaseModel):
    persona_legal = models.ForeignKey(PersonaLegal, on_delete=models.CASCADE)
    telefon = models.CharField("Telèfon", max_length=20)
    descripcio = models.CharField("Descripció", max_length=100)


class TipusProducte(PCRBaseModel):
    nom = models.CharField(max_length=100)
    # Tipus de capacitat: 'co' - Corral, 'al' - Aliment, 're' - Rebuig
    tipus_capacitat = models.CharField(max_length=2, choices=CAPACITAT_TIPUS)

    def __str__(self):
        return self.nom + ' - ' + self.get_tipus_capacitat_display()


class Documentacio(PCRBaseModel):
    nom = models.CharField(max_length=100)
    descripcio = models.TextField(blank=True, null=True)
    caduca_el_dia = models.DateField(default=timezone.now)
    document = models.FileField(upload_to='documents/', blank=True, null=True)

    def document_url(self):
        return self.document.url if self.document else None

    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name = "Documentació"
        verbose_name_plural = "Documentacions"
        ordering = ['nom']