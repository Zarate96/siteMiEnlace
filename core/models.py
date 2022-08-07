from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.utils.text import slugify

class Newsletter(models.Model):
    email = models.CharField(max_length=100)
    fecha = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Newsletter"

    def __str__(self):
        return f"{self.email} se suscribio el día {self.fecha}"

class Mensajes(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100)
    fecha = models.DateTimeField(default=timezone.now)
    asunto = models.CharField(max_length=100)
    mensaje = models.TextField(blank=True)
    is_answered = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Mensajes"

    def __str__(self):
        return f"Mensaje enviado por {self.email} el día {self.fecha}, respondido: {self.is_answered} "

