from django.contrib import admin
from .models import Mensajes, Newsletter

class MensajestAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'email', 'asunto', 'is_answered')
    search_fields = ('nombre', 'email')
    list_per_page = 10

admin.site.register(Mensajes, MensajestAdmin)
admin.site.register(Newsletter)
