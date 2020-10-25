from django.db.models import (
    Model,
    CharField,
    ForeignKey,
    DateTimeField,
    CASCADE
)
from .usuario import Usuarios

class Acceso(Model):
    ''' 
        Modelo para el acceso de usuarios al recinto.
    '''
    Fecha = DateTimeField(auto_now_add=True, editable=False)
    usuario = ForeignKey(Usuarios, on_delete = CASCADE)


    def __str__(self):
        return self.campaign