import random
from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction
from django.utils import timezone
from citas.models import *

class Command(BaseCommand):
    help = "Simulación de datos: especialidades, centros, médicos, pacientes y citas"
    def handle(self, *a, **k):
        esps = [Especialidad.objects.get_or_create(nombre=n)[0] for n in
                ["Medicina General", "Cardiología", "Dermatología", "Pediatría", "Ginecología", "Ortopedia"]]
        centros = [Centro.objects.get_or_create(nombre=n, ciudad=c, direccion=d)[0] for n, c, d in
                   [("Clínica Norte", "Barranquilla", "Cra 51 #80-10"), ("Centro Médico Caribe", "Barranquilla", "Cl 72 #45-20"),
                    ("Clínica Andina", "Bogotá", "Av 19 #104-30"), ("Salud Paisa", "Medellín", "Cl 10 #43-15")]]
        if not Medico.objects.exists():
            for i, n in enumerate(["Dra. Ana Torres", "Dr. Luis Pérez", "Dra. Marta Ruiz", "Dr. Carlos Gómez",
                                   "Dra. Sofía Vega", "Dr. Andrés Mora", "Dra. Laura Díaz", "Dr. Jorge Silva"]):
                Medico.objects.create(nombre=n, especialidad=esps[i % 6], centro=centros[i % 4])
        a, _ = User.objects.get_or_create(username="admin", defaults={"is_staff": True, "is_superuser": True})
        a.set_password("admin123"); a.save()
        h = make_password("demo1234")
        for i in range(1, 31):
            u, nuevo = User.objects.get_or_create(username=f"paciente{i}", defaults={"password": h})
            if nuevo:
                Perfil.objects.create(user=u, telefono=f"300{random.randint(1000000, 9999999)}",
                    ciudad=random.choice(["Barranquilla"] * 3 + ["Bogotá", "Medellín", "Soledad"]),
                    barrio=random.choice(["El Prado", "Alto Prado", "Riomar", "Chapinero", "Laureles", "Centro"]),
                    expediente=random.choice(["", "", "Hipertensión", "Asma", "Diabetes tipo 2"]))
        pacientes, medicos = list(User.objects.filter(username__startswith="paciente")), list(Medico.objects.all())
        for _ in range(40):
            m = random.choice(medicos)
            t = timezone.make_aware(datetime.combine((timezone.now() + timedelta(days=random.randint(1, 10))).date(), m.hora_inicio)) \
                + timedelta(minutes=m.duracion * random.randint(0, 15))
            try:
                with transaction.atomic():
                    Cita.objects.create(paciente=random.choice(pacientes), medico=m, fecha_hora=t, motivo="Consulta simulada", creada_por=a)
            except IntegrityError: pass
        self.stdout.write("Datos simulados listos. Admin: admin / admin123 · Pacientes: paciente1..30 / demo1234")
