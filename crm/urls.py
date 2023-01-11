from django.urls import include, path
from .views import *

app_name = 'crm'

urlpatterns = [
    path('', Crm.as_view(), name='crm'),
]