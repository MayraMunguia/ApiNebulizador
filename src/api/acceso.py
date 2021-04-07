from rest_framework.generics import RetrieveAPIView, UpdateAPIView, CreateAPIView,ListCreateAPIView,ListAPIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers.lectura import LecturaSerializer, lectura
from ..serializers.usuario import UsuariosSerializer
from ..models.lectura import Lectura
from rest_framework.status import ( 
    HTTP_200_OK, 
    HTTP_400_BAD_REQUEST,
    HTTP_405_METHOD_NOT_ALLOWED,
    HTTP_500_INTERNAL_SERVER_ERROR
    )
from datetime import datetime, date
from django.db import transaction
import json
import logging
from numpy import random
logger = logging.getLogger(__name__)


# MQTT_ADDRESS = '192.168.100.43'
# MQTT_USER = 'kael1'
# MQTT_PASSWORD = 'lonchis123'
# MQTT_TOPIC = 'cabin/enable'

# class AccesoUsuariosCreateView(ListCreateAPIView):
#     """
#     Vista usada para crear nuevos registros de entrada e inicializar proceso de cabina
#     """
#     serializer_class = UsuariosSerializer

#     def post(self, request, *args, **kwargs):

#         data = request.data
#         serializer = UsuariosSerializer
#         serialized_data = serializer(data=data)
#         data_is_valid = serialized_data.is_valid(raise_exception=True)

#         try:
#             with transaction.atomic():
#                 # validamos activo, accion a realizar y usuarioS
#                 usuario = Usuarios.objects.get(id_usuario = data['id_usuario'])


#                 print(usuario)

#                 nuevo_ingreso =  Acceso(
#                     usuario = usuario,
#                     fecha = datetime.now()
#                 )

#                 nuevo_ingreso.save()

#                 # #publish
#                 # mqtt_client = mqtt.Client()
#                 # mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
#                 # mqtt_client.connect(MQTT_ADDRESS, 1883)
#                 # mqtt_client.publish(MQTT_TOPIC,"ON")
#                 # print('hi from the mqtt side')


#                 return_value={
#                     "message" : "Se realizó el check-In y sanitización con éxito.",
#                     "nombre" : usuario.nombre,
#                     "Apellido_Paterno" : usuario.a_paterno,
#                     "Apellido_Materno" :  usuario.a_materno
#                 }

#                 return Response(return_value, status=HTTP_200_OK)
#         except Exception as ex:
#             logger.error(ex)
#             return_value={"message" : "Ocurrió un error inesperado..", "exception": str(ex) }
#             return Response(return_value, status=HTTP_400_BAD_REQUEST)




class InitiateCabinCreateView(ListCreateAPIView):
    """
    Vista usada para solo inicializar proceso de cabina
    """
    queryset =  Lectura.objects.all()
    serializer_class = LecturaSerializer

    def post(self, request, *args, **kwargs):

        try:
            with transaction.atomic():
                # validamos activo, accion a realizar y usuarioS
                queryset = Lectura.objects.values_list('lectura', flat=True)

                mean = sum(queryset)/len(queryset) 
                print(mean)
                flomean = float(mean)
                var = 0
                for i in queryset:
                    var = var + (float(i)- flomean)**2

                var = var/len(queryset)
                std= var ** .5 #calculates standard deviation


                ul = round(flomean + 2*std, 3)
                il = round(flomean - 2*std,3)


                return_value={
                    "message" : "Se obtuvo la información correctamente.",
                    "limInfer" : il,
                    "limSuper": ul,
                    "res" : list(queryset)
                }

                return Response(return_value,status=HTTP_200_OK)
        except Exception as ex:
            logger.error(ex)
            return_value={"message" : "Ocurrió un error inesperado..", "exception": str(ex) }
            return Response(return_value, status=HTTP_400_BAD_REQUEST)


# class StatsListView(ListAPIView):
#     """
#     Vista usada para obtener todos los registros
#     """
#     queryset = Acceso.objects.all()
#     serializer_class = AccesoSerializer