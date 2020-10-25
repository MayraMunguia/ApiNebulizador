from ..models.dispositivos import Configuracion
from rest_framework import serializers


class ConfiguracionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuracion
        fields = '__all__'
