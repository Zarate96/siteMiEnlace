import mysql.connector
from django.shortcuts import render, redirect
from mysql.connector import Error
from django.contrib import messages
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .db import *

db = DatabaseConnection(
    settings.DB_CRM_HOST, 
    settings.DB_CRM_NAME,
    settings.DB_CRM_USER, 
    settings.DB_CRM_PASSWORD
)

class Crm(UserPassesTestMixin, TemplateView):
    template_name = 'crm/home.html'

    def test_func(self):
        return self.request.user.is_superuser
        
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['title'] = 'Home'
        return context

class Usuarios(UserPassesTestMixin, TemplateView):
    template_name = 'crm/usuarios.html'

    def test_func(self):
        return self.request.user.is_superuser
        
    def get_context_data(self, *args, **kwargs):
        query = db.excute_query("select id, userName, activo, nombre, apellidopaterno, apellidomaterno, email,isPersonaFisica, idEstado, ciudad, lada, celular from enlace.usuarios")
        db.disconnect()
        context = super().get_context_data(*args,**kwargs)
        context['title'] = 'Usuarios'
        context['usuarios'] = query
        return context

class Test(UserPassesTestMixin, TemplateView):
    template_name = 'crm/templateTest.html'

    def test_func(self):
        return self.request.user.is_superuser
        
    def get_context_data(self, *args, **kwargs):
        query = db.excute_query("""select  CONCAT( 'OCC',SOL.FOLIO) OCC_FOLIO, USR.username Proveedor,
                                    SOD.partida,
                                    COD.descripcion, COD.marca, COD.empaque, COD.cantidad, COD.precioUnitario, COD.precioExtendido, COD.iva
                                    from enlace.solicitudes SOL 
                                    inner join enlace.solicituddetalle SOD on SOL.id = SOD.idSolicitud
                                    inner join enlace.cotizaciondetalle COD on COD.ID = SOD.idCotizacionDetalle
                                    left JOIN enlace.USUARIOS USR ON USR.ID = COD.IDUSUARIO
                                    WHERE  SOL.status = 'confirmada'
                                    and CONCAT('OCC' , SOL.folio) = 'OCCSANATORIO0034';""")
        query2 = db.excute_query("""select id, userName, nombre, apellidopaterno, apellidomaterno, email,isPersonaFisica, 
                                    idEstado, ciudad, lada, celular from enlace.usuarios 
                                    WHERE userName='Sanatorio';""")
        query3 = db.excute_query("""select * from enlace.datosfiscales
                                    WHERE idUsuario='189';""")
        db.disconnect()
        context = super().get_context_data(*args,**kwargs)
        context['title'] = 'Test'
        context['result'] = query
        context['result2'] = query2
        context['result3'] = query3
        return context

class Solicitudes(UserPassesTestMixin, TemplateView):
    template_name = 'crm/solicitudes.html'

    def test_func(self):
        return self.request.user.is_superuser
        
    def get_context_data(self, *args, **kwargs):
        query = db.excute_query("""select  * from enlace_test.solicitudes""")
        db.disconnect()
        context = super().get_context_data(*args,**kwargs)
        context['title'] = 'Solicitudes'
        context['myresult'] = query
        return context

def occ_cliente(request):
    query = ""
    if request.method == 'POST':
        username = request.POST['username']
        try:
            query = db.excute_query(f"""select distinct CONCAT( 'OCC',SOL.FOLIO) OCC_FOLIO,  SOL.FECALTA, SOL.status, SOL.ISPAGADA PAGO
                                FROM enlace_test.solicitudes SOL
                                inner join enlace_test.cotizacion CO on SOL.ID = CO.IdSolicitud
                                inner join enlace_test.cotizaciondetalle COD on SOL.ID = COD.idsolicitud
                                inner join enlace_test.solicituddetalle SOD on SOL.ID = SOD.IdSolicitud
                                INNER JOIN enlace_test.USUARIOS USR ON USR.ID = COD.IDUSUARIO
                                where SOL.FOLIO LIKE '%{username}%'""")
            db.disconnect()
            if not query:
                messages.success(request, f"Usuario '{username}' no encontrado.")
        except:
            messages.error(request, 'Ha occurrido un error')

    context = {
        "title":"OCC por Cliente",
        "result":query,
    }
    return render(request, 'crm/occ_cliente.html', context)

def costo_envio_occ(request):
    query = ""
    if request.method == 'POST':
        occ = request.POST['occ']
        try:
            query = db.excute_query(f"""select CONCAT( 'OCC',SOL.FOLIO) OCC_FOLIO, FL.alto, FL.ancho, FL.largo, FL.peso, FL.costo, FL.combustible, FL.IVA from enlace_test.fletesolicitud FL
                                inner join enlace_test.solicitudes SOL on SOL.id = FL.idSolicitud
                                where CONCAT('OCC' , SOL.folio) = '{occ}';'""")
            db.disconnect()
            if not query:
                messages.success(request, f"OCC '{occ}' no encontrada.")
        except:
            messages.error(request, 'Ha occurrido un error')

    context = {
        "title":"Costo Envío OCC",
        "result":query,
    }
    return render(request, 'crm/costo_envio_occ.html', context)

def facturacion_cliente(request):
    query = ""
    if request.method == 'POST':
        occ = request.POST['occ']
        solicitud = request.POST['solicitud']
        try:
            query = db.excute_query(f"""select  CONCAT( 'OCC',SOL.FOLIO) OCC_FOLIO, USR.username Proveedor,
                                SOD.partida,
                                COD.descripcion, COD.marca, COD.empaque, COD.cantidad, COD.precioUnitario, COD.precioExtendido, COD.iva
                                from enlace.solicitudes SOL 
                                inner join enlace.solicituddetalle SOD on SOL.id = SOD.idSolicitud
                                inner join enlace.cotizaciondetalle COD on COD.ID = SOD.idCotizacionDetalle
                                left JOIN ENLACE.USUARIOS USR ON USR.ID = COD.IDUSUARIO
                                WHERE  SOL.status = 'confirmada'
                                and CONCAT('OCC' , SOL.folio) = 'OCCDRA MAGALLON002';'""")
            db.disconnect()
            if not query:
                messages.success(request, f"OCC '{occ}' no encontrada.")
        except:
            messages.error(request, 'Ha occurrido un error')

    context = {
        "title":"Facturación",
        "result":query,
    }
    return render(request, 'crm/facturacion_cliente.html', context)