from ..models.acceso import Acceso
from rest_framework import serializers


class AccesoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acceso
        fields = '__all__'
