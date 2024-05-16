
from rest_framework import serializers

from globg import models

class PersonaLegalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PersonaLegal
        fields = '__all__'