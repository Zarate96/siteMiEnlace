from django.urls import include, path
from .views import *

app_name = 'crm'

urlpatterns = [
    path('', Crm.as_view(), name='crm'),
    path('facturacion/cliente', facturacion_cliente, name='facturacion-cliente'),
    path('facturacion/cliente/exportar/<str:occ>/<int:idUsuario>/', exportFacturacionCliente, name='facturacion-cliente-exportar'),
    path('facturacion/proveedor', facturacion_proveedor, name='facturacion-proveedor'),
    path('facturacion/proveedor/exportar/<str:occ>/<str:oce>/<int:idUsuario>/<int:comision>/<int:envio>', exportFacturacionProveedor, name='facturacion-proveedor-exportar'),
    path('usuarios/', Usuarios.as_view(), name='usuarios'),
    path('solicitudes/', Solicitudes.as_view(), name='solicitudes'),
    path('oce-detalle/', oce_detalle, name='oce-detalle'),
    path('oce-detalle/exportar/<str:occ>/<str:oce>/<int:idProveedor>', export_pdf_oce_detalle, name="oce-exportar-pdf" ),
    path('occ-costo-envio/', costo_envio_occ, name='costo-envio-occ'),
    path('test/', Test.as_view(), name='test'),
]