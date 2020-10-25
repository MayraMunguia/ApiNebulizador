from ..models.usuario import Usuarios
from rest_framework import serializers


class UsuariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuarios
        fields = '__all__'
