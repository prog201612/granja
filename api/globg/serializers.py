
from rest_framework import serializers

from globg import models

class PersonaLegalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PersonaLegal
        fields = '__all__'


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Email
        fields = '__all__'


class TelefonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Telefon
        fields = '__all__'


class TipusProducteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TipusProducte
        fields = '__all__'


class DocumentacioSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Documentacio
        fields = '__all__'
    document_url = serializers.ReadOnlyField()