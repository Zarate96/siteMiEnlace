import csv  
import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from openpyxl.worksheet.table import Table, TableStyleInfo

from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.contrib.auth.mixins import UserPassesTestMixin

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
        query2 = db.excute_query("""select * from enlace.usuarios 
                                    WHERE id='189';""")
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
            query = db.excute_query(f"""select CONCAT( 'OCC',SOL.FOLIO) OCC_FOLIO, FL.alto, FL.ancho, FL.largo, FL.peso, FL.costo, FL.combustible, FL.IVA from enlace.fletesolicitud FL
                                inner join enlace.solicitudes SOL on SOL.id = FL.idSolicitud
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
    #OCCSANATORIO0034
    #189
    if request.method == 'POST':
        occ = request.POST['occ']
        idUsuario = request.POST['idUsuario']
        try:
            query = db.excute_query(f"""select  CONCAT( 'OCC',SOL.FOLIO) OCC_FOLIO, USR.username Proveedor,
                                    SOD.partida,
                                    COD.descripcion, COD.marca, COD.empaque, COD.cantidad, COD.precioUnitario, COD.precioExtendido, COD.iva
                                    from enlace.solicitudes SOL 
                                    inner join enlace.solicituddetalle SOD on SOL.id = SOD.idSolicitud
                                    inner join enlace.cotizaciondetalle COD on COD.ID = SOD.idCotizacionDetalle
                                    left JOIN enlace.USUARIOS USR ON USR.ID = COD.IDUSUARIO
                                    WHERE  SOL.status = 'confirmada'
                                    and CONCAT('OCC' , SOL.folio) = '{occ}';""")
            query2 = db.excute_query(f"""select * from enlace.usuarios 
                                        WHERE id='{idUsuario}';""")
            query3 = db.excute_query(f"""select * from enlace.datosfiscales
                                        WHERE idUsuario='{idUsuario}';""")
           
            # PERSONA FISICA  isPersonaFisica 1=Si, 0=No
            query4 = db.excute_query(f"""select isPersonaFisica from enlace.usuarios WHERE id='{idUsuario}';;""")

            query5 = db.excute_query(f"""select CONCAT( 'OCC',SOL.FOLIO) OCC_FOLIO, FL.alto, FL.ancho, FL.largo, FL.peso, FL.costo, FL.combustible, FL.IVA from enlace.fletesolicitud FL
                                inner join enlace.solicitudes SOL on SOL.id = FL.idSolicitud
                                where CONCAT('OCC' , SOL.folio) = '{occ}';'""")
            idEsatdo = query3[0][11]
            estado = db.excute_query(f"""select estado from enlace.estados WHERE id='{idEsatdo}';""")
            db.disconnect()
            
            if query and query2 and query3:
                subtotal = 0
                isFisica = query4[0][0]
                name = f'{query3[0][3]} {query3[0][4]} {query3[0][5]}' if isFisica else f'{query3[0][2]}'
                address = f'Calle {query3[0][6]} #{query3[0][7]} {query3[0][8]},  Colonia {query3[0][9]} <br> {query3[0][10]}, {estado[0][0]} {query3[0][12]} <br> RFC: <b>{query3[0][13]}</b>'
                costo_envio = query5[0][6]
                iva_envio = query5[0][7]
                for row in query:
                    subtotal = row[8] + subtotal
                subtotal = float(subtotal) + float(costo_envio)
                iva = float(subtotal) * 0.16 + float(iva_envio)
                total = float(subtotal) + iva
                now = datetime.datetime.now()
                date = now.strftime('%d-%m-%Y')
                context = {
                    "title":"Facturación",
                    "result":query,
                    "name":name,
                    "address":address,
                    "subtotal":subtotal,
                    "iva":round(iva, 2),
                    "total":round(total, 2),
                    "costo_envio":costo_envio,
                    "occ":occ,
                    "idUsuario":idUsuario,
                    "query5":query5,
                    "date":date,
                }

            if not query:
                messages.success(request, f"OCC '{occ}' no encontrada.")
            if not query2:
                messages.success(request, f"Usuario '{idUsuario}' no encontrado.")

            return render(request, 'crm/facturacion_cliente.html', context)
        
        except Exception as e:
            messages.error(request, f'Ha occurrido un error: {e}')
            
    context = {"title":"Facturación"}
    return render(request, 'crm/facturacion_cliente.html', context)

def exportFacturacionCliente(request,occ,idUsuario):
    try:
        query = db.excute_query(f"""select  CONCAT( 'OCC',SOL.FOLIO) OCC_FOLIO, USR.username Proveedor,
                                SOD.partida,
                                COD.descripcion, COD.marca, COD.empaque, COD.cantidad, COD.precioUnitario, COD.precioExtendido, COD.iva
                                from enlace.solicitudes SOL 
                                inner join enlace.solicituddetalle SOD on SOL.id = SOD.idSolicitud
                                inner join enlace.cotizaciondetalle COD on COD.ID = SOD.idCotizacionDetalle
                                left JOIN enlace.USUARIOS USR ON USR.ID = COD.IDUSUARIO
                                WHERE  SOL.status = 'confirmada'
                                and CONCAT('OCC' , SOL.folio) = '{occ}';""")
        query2 = db.excute_query(f"""select * from enlace.usuarios 
                                    WHERE id='{idUsuario}';""")
        query3 = db.excute_query(f"""select * from enlace.datosfiscales
                                    WHERE idUsuario='{idUsuario}';""")
        
        # PERSONA FISICA  isPersonaFisica 1=Si, 0=No
        query4 = db.excute_query(f"""select isPersonaFisica from enlace.usuarios WHERE id='{idUsuario}';;""")

        query5 = db.excute_query(f"""select CONCAT( 'OCC',SOL.FOLIO) OCC_FOLIO, FL.alto, FL.ancho, FL.largo, FL.peso, FL.costo, FL.combustible, FL.IVA from enlace.fletesolicitud FL
                            inner join enlace.solicitudes SOL on SOL.id = FL.idSolicitud
                            where CONCAT('OCC' , SOL.folio) = '{occ}';'""")
        idEsatdo = query3[0][11]
        estado = db.excute_query(f"""select estado from enlace.estados WHERE id='{idEsatdo}';""")
        db.disconnect()
        
        if query and query2 and query3:
            subtotal = 0
            isFisica = query4[0][0]
            name = f'{query3[0][3]} {query3[0][4]} {query3[0][5]}' if isFisica else f'{query3[0][2]}'
            address = f'Calle {query3[0][6]} #{query3[0][7]} {query3[0][8]},  Colonia {query3[0][9]} <br> {query3[0][10]}, {estado[0][0]} {query3[0][12]} <br> RFC: <b>{query3[0][13]}</b>'
            costo_envio = query5[0][6]
            iva_envio = query5[0][7]
            for row in query:
                subtotal = row[8] + subtotal
            subtotal = float(subtotal) + float(costo_envio)
            iva = float(subtotal) * 0.16 + float(iva_envio)
            total = float(subtotal) + iva
            
            #Creamos el libro de trabajo
            wb = Workbook()
            #Definimos como nuestra hoja de trabajo, la hoja activa, por defecto la primera del libro
            ws = wb.active
            #Titulo
            ws['F3'] = 'PROVEEDORA OMNIPET S. DE R.L DE C.V'
            ws['F3'].font = Font(bold=True)
            ws.merge_cells('F3:J3')
            ws['F4'] = 'Av. Cuauhtemoc 451-209, Col. Narvarte,'
            ws.merge_cells('F4:J4')
            ws['F5'] = 'México, D.F. 03020'
            ws.merge_cells('F5:G5')
            ws['F6'] = 'POM 020313 MS0'
            ws.merge_cells('F6:G6')

            #datos fiscales del cliente
            ws['B8'] = f'{name}'
            ws['B8'].font = Font(bold=True)
            ws.merge_cells('B8:G8')
            ws['L8'] = 'México D.F'
            ws.merge_cells('L8:M8')
            now = datetime.datetime.now()
            date = now.strftime('%d-%m-%Y')
            ws['L9'] = f'{date}'
            ws.merge_cells('L9:N9')
            ws['B9'] = f'Calle {query3[0][6]} #{query3[0][7]} {query3[0][8]},  Colonia {query3[0][9]}'
            ws.merge_cells('B9:G9')
            ws['B10'] = f'{query3[0][10]}, {estado[0][0]} {query3[0][12]}'
            ws.merge_cells('B10:F10')
            ws['B12'] = 'CLIENTE'
            ws['B12'].font = Font(bold=True)
            ws['B13'] = f'RFC: {query3[0][13]}'
            ws['B13'].font = Font(bold=True)
            ws.merge_cells('B13:D13')

            #datos de la factura
            ws['B17'] = 'Partida'
            ws['C17'] = 'Descripción'
            ws.merge_cells('C17:H17')
            ws['L17'] = 'Cantidad'
            ws['M17'] = 'P.Unitario'
            ws['N17'] = 'Total'
            row = 19

            for partida in query:
                ws[f'B{row}'] = f'{partida[2]}'
                ws[f'C{row}'] = f'{partida[3]} {partida[4]} {partida[5]}'
                ws.merge_cells(f'C{row}:K{row}')
                ws[f'L{row}'] = f'{partida[6]}'
                ws[f'M{row}'] = f'{partida[7]}'
                ws[f'N{row}'] = f'{partida[8]}'
                row = row + 1
            
            ws[f'C{row + 1}'] = f'COSTO DE ENVÍO'
            ws.merge_cells(f'C{row + 1}:K{row + 1}')
            ws[f'L{row + 1}'] = f'1'
            ws[f'M{row + 1}'] = f'{costo_envio}'
            ws[f'N{row + 1}'] = f'{iva_envio}'

            #Totales
            subtotal = round(subtotal, 2)
            iva = round(iva, 2)
            total = round(total, 2)
            ws[f'L{row + 4}'] = 'Subtotal'
            ws[f'N{row + 4}'] = f'${subtotal}'
            ws[f'L{row + 5}'] = 'IVA'
            ws[f'N{row + 5}'] = f'${iva}'
            ws[f'L{row + 6}'] = 'Total'
            ws[f'N{row + 6}'] = f'${total}'
    
            #Guardamos el archivo
            nombre_archivo =f"{occ}.xlsx"
            response = HttpResponse(content_type="application/ms-excel") 
            contenido = "attachment; filename={0}".format(nombre_archivo)
            response["Content-Disposition"] = contenido
            wb.save(response)
            return response

        if not query:
            messages.success(request, f"OCC '{occ}' no encontrada.")
        if not query2:
            messages.success(request, f"Usuario '{idUsuario}' no encontrado.")
    
    except Exception as e:
        messages.error(request, f'Ha occurrido un error: {e}')
            
    