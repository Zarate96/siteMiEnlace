from django.urls import include, path
from .views import *

app_name = 'core'

urlpatterns = [
    path('', Inicio.as_view(), name='inicio'),
    path('mensaje/', mensaje, name='mensaje'),
]