from django.db.models import (
    Model,
    CharField,
    ForeignKey,
    DateTimeField,
    CASCADE
)

class Usuarios(Model):
    """
    Modelo para los empleados/usuarios
    """
    id_usuario = CharField(max_length=200)
    nombre = CharField(max_length=200)
    a_paterno = CharField(max_length=200)
    a_materno = CharField(max_length=200)

    # def __str__(self):
    #     return self.nombre

