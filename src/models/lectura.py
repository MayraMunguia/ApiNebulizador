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
    fecha = DateTimeField(auto_now_add=True, editable=False)
    lectura = DecimalField(max_digits = 7,decimal_places=3)
    # sensores = IntegerField(default=1)


    # def __str__(self):
    #     return self.usuario
