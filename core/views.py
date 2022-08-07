from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .decorators import check_recaptcha
from .models import Mensajes

# Create your views here.

class Inicio(UserPassesTestMixin, TemplateView):
    template_name = 'core/home.html'

    def test_func(self):
        return True
        
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['title'] = 'Inicio'
        context['google_site_key'] = settings.GOOGLE_RECAPTCHA_SITE_KEY
        return context
    
@check_recaptcha
def mensaje(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        telefono = request.POST['telefono']

    if request.recaptcha_is_valid:    
        mensaje = Mensajes(nombre=name, email=email, asunto=subject, mensaje=message, telefono=telefono)
        mensaje.save()
        messages.success(request, 'Tu mensaje ha sido enviado, nos pondremos en contacto contigo en breve.')

    else:
        messages.error(request, 'Porfavor verifique la información')

    return redirect(request.META['HTTP_REFERER'])
    #return render(request, 'pages/home.html', {})