import mysql.connector
from django.shortcuts import render
from mysql.connector import Error
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# try:
#     connection = mysql.connector.connect(host='https://mienlace.com.mx/',
#                                          database='test',
#                                          user='omnipet',
#                                          password='omnipet1524')
#     if connection.is_connected():
#         db_Info = connection.get_server_info()
#         print("Connected to MySQL Server version ", db_Info)
#         cursor = connection.cursor()
#         cursor.execute("select database();")
#         record = cursor.fetchone()
#         print("You're connected to database: ", record)

# except Error as e:
#     print("Error while connecting to MySQL", e)
# finally:
#     if connection.is_connected():
#         cursor.close()
#         connection.close()
#         print("MySQL connection is closed")

# Create your views here.

class Crm(TemplateView):
    template_name = 'crm/baseCrm.html'

    def test_func(self):
        return True
        
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
        print(type(myresult))
        for x in myresult:
            print(type(x))
        context = super().get_context_data(*args,**kwargs)
        context['title'] = 'Inicio'
        context['usuarios'] = myresult
        return context