from django.db.models import (
    Model,
    CharField,
    ForeignKey,
    DateTimeField,
    CASCADE
)

class Configuracion(Model):
    """
    Modelo para la configuración del servidor
    """
    nombre_config = CharField(max_length=200)
    valor_config =  CharField(max_length=200)

    def __str__(self):
        return self.Configuracion

