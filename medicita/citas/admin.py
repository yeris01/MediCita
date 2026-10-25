from django.contrib import admin
from .models import *
for m in (Especialidad, Centro, Perfil, Medico, Cita): admin.site.register(m)
