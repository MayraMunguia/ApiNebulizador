from ..models.lectura import Lectura
from rest_framework import serializers

from src.models import lectura


class LecturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lectura
        fields = '__all__'
