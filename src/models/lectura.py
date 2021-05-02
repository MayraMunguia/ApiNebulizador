from django.db.models import (
    Model,
    CharField,
    ForeignKey,
    DateTimeField,
    DecimalField,
    CASCADE,
    IntegerField
)
from django.db.models.fields import IntegerField
from .usuario import Usuarios

class Lectura(Model):
    ''' 
        Modelo para guardar lecturas de sensores
    '''
    #fecha = DateTimeField(auto_now_add=True, editable=False)
    lectura = CharField(max_length=6)
    sensores = CharField(max_length=6, default= 1)

    # def __str__(self):
    #     return self.usuario
