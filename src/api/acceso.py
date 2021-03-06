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
from decimal import *
from django.db import transaction
import json
import logging
import paho.mqtt.client as mqtt
from numpy import random
logger = logging.getLogger(__name__)


MQTT_ADDRESS = '192.168.100.24'
MQTT_USER = 'kael1'
MQTT_PASSWORD = 'lonchis123'
MQTT_TOPIC = 'bomba'

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
                hum_air = Lectura.objects.filter(sensores = "1").values_list('lectura', flat=True)
                hum_so = Lectura.objects.filter(sensores = "2").values_list('lectura', flat=True)
                temp = Lectura.objects.filter(sensores = "3").values_list('lectura', flat=True)
                agua = Lectura.objects.filter(sensores = "4").values_list('lectura', flat=True).order_by('-id')[0]

                # #publish
                mqtt_client = mqtt.Client()
                mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
                mqtt_client.connect(MQTT_ADDRESS, 1883)
                print('new query')

                hum_tierra= Lectura.objects.filter(sensores = "2").values_list('lectura', flat=True).order_by('-id')[0]
                hum_aire = Lectura.objects.filter(sensores = "1").values_list('lectura', flat=True).order_by('-id')[0]
                
                if(float(hum_aire) >= 60 and  float(hum_aire) <= 100):
                    hola = "jala 1"
                    if(float(hum_tierra) <= 20):
                        hola = "jala 1.1"
                        mqtt_client.publish(MQTT_TOPIC,"ON")
                elif(float(hum_aire) >= 30 and float(hum_aire) < 60 ):
                    hola = "jala 2"
                    if(float(hum_tierra) <= 40):
                        hola = "jala 2.2"
                        mqtt_client.publish(MQTT_TOPIC,"ON")
                elif(float(hum_tierra) < 60):
                    hola = "jala 3"
                    mqtt_client.publish(MQTT_TOPIC,"ON")
                else:
                    hola = "jala 4"
                    mqtt_client.publish(MQTT_TOPIC,"OFF")


                return_value={
                    "message" : "Se obtuvo la información correctamente.",
                    "humedad_tierra" : hum_tierra,
                    "humedad_aire" : hum_aire,
                    "jala":hola,
                    "aire" : list(hum_air),
                    "soil" : list(hum_so),
                    "temp" : list(temp),
                    "agua" : list(agua)
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