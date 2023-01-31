import mysql.connector
from django.shortcuts import render, redirect
from mysql.connector import Error
from django.contrib import messages
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

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
        mydb = mysql.connector.connect(
            host='mienlace.com.mx',
            database='test',
            user='omnipet',
            password='omnipet1524'
        )
        mycursor = mydb.cursor()
        mycursor.execute("select id, userName, activo, nombre, apellidopaterno, apellidomaterno, email,isPersonaFisica, idEstado, ciudad, lada, celular from enlace_test.usuarios")
        myresult = mycursor.fetchall()
        context = super().get_context_data(*args,**kwargs)
        context['title'] = 'Usuarios'
        context['usuarios'] = myresult
        return context

class Test(UserPassesTestMixin, TemplateView):
    template_name = 'crm/templateTest.html'

    def test_func(self):
        return self.request.user.is_superuser
        
    def get_context_data(self, *args, **kwargs):
        mydb = mysql.connector.connect(
            host='mienlace.com.mx',
            database='test',
            user='omnipet',
            password='omnipet1524'
        )
        mycursor = mydb.cursor()
        mycursor.execute("""select  CONCAT( 'OCC',SOL.FOLIO) OCC_FOLIO, USR.username Proveedor,
                            SOD.partida,
                            COD.descripcion, COD.marca, COD.empaque, COD.cantidad, COD.precioUnitario, COD.precioExtendido, COD.iva
                            from enlace.solicitudes SOL 
                            inner join enlace.solicituddetalle SOD on SOL.id = SOD.idSolicitud
                            inner join enlace.cotizaciondetalle COD on COD.ID = SOD.idCotizacionDetalle
                            left JOIN ENLACE.USUARIOS USR ON USR.ID = COD.IDUSUARIO
                            WHERE  SOL.status = 'confirmada'
                            and CONCAT('OCC' , SOL.folio) = 'OCCDRA MAGALLON002';""")
        # mycursor.execute("""select  CONCAT( 'OCC',SOL.FOLIO) OCC_FOLIO, USR.username Proveedor,
        #                     SOD.partida,
        #                     COD.descripcion, COD.marca, COD.empaque, COD.cantidad, COD.precioUnitario, COD.precioExtendido, COD.iva
        #                     from enlace.solicitudes SOL 
        #                     inner join enlace.solicituddetalle SOD on SOL.id = SOD.idSolicitud
        #                     inner join enlace.cotizaciondetalle COD on COD.ID = SOD.idCotizacionDetalle
        #                     left JOIN ENLACE.USUARIOS USR ON USR.ID = COD.IDUSUARIO
        #                     WHERE  SOL.status = 'confirmada'
        #                     and CONCAT('OCC' , SOL.folio) = 'OCCDRA MAGALLON002';""")
        # mycursor.execute("""select distinct CONCAT( 'OCC',SOL.FOLIO) OCC_FOLIO,  SOL.FECALTA, SOL.status, SOL.ISPAGADA PAGO
        #             FROM enlace_test.solicitudes SOL
        #             inner join enlace_test.cotizacion CO on SOL.ID = CO.IdSolicitud
        #             inner join enlace_test.cotizaciondetalle COD on SOL.ID = COD.idsolicitud
        #             inner join enlace_test.solicituddetalle SOD on SOL.ID = SOD.IdSolicitud
        #             INNER JOIN enlace_test.USUARIOS USR ON USR.ID = COD.IDUSUARIO
        #             where SOL.FOLIO LIKE '%TAPERULE%'
        #             order by fecalta desc;""") 
        myresult = mycursor.fetchall()
        mycursor.execute("""select CONCAT( 'OCC',SOL.FOLIO) OCC_FOLIO, FL.alto, FL.ancho, FL.largo, FL.peso, FL.costo, FL.combustible, FL.IVA from enlace_test.fletesolicitud FL
                            inner join enlace_test.solicitudes SOL on SOL.id = FL.idSolicitud
                            where CONCAT('OCC' , SOL.folio) = 'OCCDRA';""")
        myresult2 = mycursor.fetchall()
        context = super().get_context_data(*args,**kwargs)
        context['title'] = 'Inicio'
        context['result'] = myresult
        context['costoEnvio'] = myresult2
        return context

class Solicitudes(UserPassesTestMixin, TemplateView):
    template_name = 'crm/solicitudes.html'

    def test_func(self):
        return self.request.user.is_superuser
        
    def get_context_data(self, *args, **kwargs):
        mydb = mysql.connector.connect(
            host='mienlace.com.mx',
            database='test',
            user='omnipet',
            password='omnipet1524'
        )
        mycursor = mydb.cursor()
        mycursor.execute("""select  * from enlace_test.solicitudes""")
        myresult = mycursor.fetchall()
        print("***data****")
        print(myresult)
        context = super().get_context_data(*args,**kwargs)
        context['title'] = 'Solicitudes'
        context['myresult'] = myresult
        return context

def occ_cliente(request):
    myresult = ""
    if request.method == 'POST':
        username = request.POST['username']
        try:
            mydb = mysql.connector.connect(
            host='mienlace.com.mx',
            database='test',
            user='omnipet',
            password='omnipet1524'
            )
            mycursor = mydb.cursor()
            mycursor.execute(f"""select distinct CONCAT( 'OCC',SOL.FOLIO) OCC_FOLIO,  SOL.FECALTA, SOL.status, SOL.ISPAGADA PAGO
                                FROM enlace_test.solicitudes SOL
                                inner join enlace_test.cotizacion CO on SOL.ID = CO.IdSolicitud
                                inner join enlace_test.cotizaciondetalle COD on SOL.ID = COD.idsolicitud
                                inner join enlace_test.solicituddetalle SOD on SOL.ID = SOD.IdSolicitud
                                INNER JOIN enlace_test.USUARIOS USR ON USR.ID = COD.IDUSUARIO
                                where SOL.FOLIO LIKE '%{username}%'""")
            myresult = mycursor.fetchall()
            print("***data****")
            print(myresult)
            if not myresult:
                messages.success(request, f"Usuario '{username}' no encontrado.")
        except:
            messages.error(request, 'Ha occurrido un error')

    context = {
        "title":"OCC por Cliente",
        "result":myresult,
    }
    return render(request, 'crm/occ_cliente.html', context)

def costo_envio_occ(request):
    myresult = ""
    if request.method == 'POST':
        occ = request.POST['occ']
        try:
            mydb = mysql.connector.connect(
            host='mienlace.com.mx',
            database='test',
            user='omnipet',
            password='omnipet1524'
            )
            mycursor = mydb.cursor()
            mycursor.execute(f"""select CONCAT( 'OCC',SOL.FOLIO) OCC_FOLIO, FL.alto, FL.ancho, FL.largo, FL.peso, FL.costo, FL.combustible, FL.IVA from enlace_test.fletesolicitud FL
                                inner join enlace_test.solicitudes SOL on SOL.id = FL.idSolicitud
                                where CONCAT('OCC' , SOL.folio) = '{occ}';'""")
            myresult = mycursor.fetchall()
            print("***data****")
            print(myresult)
            if not myresult:
                messages.success(request, f"OCC '{occ}' no encontrada.")
        except:
            messages.error(request, 'Ha occurrido un error')

    context = {
        "title":"Costo Envío OCC",
        "result":myresult,
    }
    return render(request, 'crm/costo_envio_occ.html', context)

def facturacion_cliente(request):
    myresult = ""
    if request.method == 'POST':
        occ = request.POST['occ']
        solicitud = request.POST['solicitud']
        try:
            mydb = mysql.connector.connect(
            host='mienlace.com.mx',
            database='test',
            user='omnipet',
            password='omnipet1524'
            )
            mycursor = mydb.cursor()
            mycursor.execute(f"""select  CONCAT( 'OCC',SOL.FOLIO) OCC_FOLIO, USR.username Proveedor,
                                SOD.partida,
                                COD.descripcion, COD.marca, COD.empaque, COD.cantidad, COD.precioUnitario, COD.precioExtendido, COD.iva
                                from enlace.solicitudes SOL 
                                inner join enlace.solicituddetalle SOD on SOL.id = SOD.idSolicitud
                                inner join enlace.cotizaciondetalle COD on COD.ID = SOD.idCotizacionDetalle
                                left JOIN ENLACE.USUARIOS USR ON USR.ID = COD.IDUSUARIO
                                WHERE  SOL.status = 'confirmada'
                                and CONCAT('OCC' , SOL.folio) = 'OCCDRA MAGALLON002';'""")
            myresult = mycursor.fetchall()
            print("***data****")
            print(myresult)
            if not myresult:
                messages.success(request, f"OCC '{occ}' no encontrada.")
        except:
            messages.error(request, 'Ha occurrido un error')

    context = {
        "title":"Facturación",
        "result":myresult,
    }
    return render(request, 'crm/facturacion_cliente.html', context)