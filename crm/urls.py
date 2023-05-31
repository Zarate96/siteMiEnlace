from django.urls import include, path
from .views import *

app_name = 'crm'

urlpatterns = [
    path('', Crm.as_view(), name='crm'),
    path('facturacion/cliente', facturacion_cliente, name='facturacion-cliente'),
    path('usuarios/', Usuarios.as_view(), name='usuarios'),
    path('solicitudes/', Solicitudes.as_view(), name='solicitudes'),
    path('occ-cliente/', occ_cliente, name='occ-cliente'),
    path('occ-costo-envio/', costo_envio_occ, name='costo-envio-occ'),
    path('test/', Test.as_view(), name='test'),
]