import json
from datetime import date, datetime, timedelta
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Cita, Centro, Especialidad, Medico, Perfil
from .triage import clasificar

def registro(request):
    f = UserCreationForm(request.POST or None)
    if request.method == "POST" and f.is_valid():
        u = f.save()
        Perfil.objects.create(user=u, telefono=request.POST.get("telefono", ""),
            ciudad=request.POST.get("ciudad", "").strip().title(), barrio=request.POST.get("barrio", "").strip().title(),
            expediente=request.POST.get("expediente", ""))
        login(request, u)
        return redirect("buscar")
    return render(request, "registro.html", {"f": f})

@login_required
def buscar(request):
    g = request.GET
    q = Medico.objects.select_related("especialidad", "centro")
    if g.get("esp"): q = q.filter(especialidad_id=g["esp"])
    if g.get("centro"): q = q.filter(centro_id=g["centro"])
    if g.get("especialidad"): q = q.filter(especialidad__nombre=g["especialidad"])
    if g.get("ciudad"): q = q.filter(centro__ciudad=g["ciudad"])
    return render(request, "buscar.html", {"medicos": q, "esps": Especialidad.objects.all(),
        "centros": Centro.objects.all(), "ciudades": Centro.objects.values_list("ciudad", flat=True).distinct()})

def horarios(medico, dia):
    ocupadas = set(Cita.objects.filter(medico=medico, estado="programada").values_list("fecha_hora", flat=True))
    t = timezone.make_aware(datetime.combine(dia, medico.hora_inicio))
    fin = timezone.make_aware(datetime.combine(dia, medico.hora_fin))
    out = []
    while t < fin:
        if t > timezone.now() and t not in ocupadas: out.append(t)
        t += timedelta(minutes=medico.duracion)
    return out

@login_required
def agendar(request, medico_id, cita_id=None):
    medico = get_object_or_404(Medico, pk=medico_id)
    cita = get_object_or_404(Cita, pk=cita_id) if cita_id else None
    if cita and not (request.user.is_staff or cita.paciente == request.user):
        return redirect("mis_citas")
    try: dia = date.fromisoformat(request.POST.get("dia") or request.GET.get("dia"))
    except (TypeError, ValueError): dia = date.today() + timedelta(days=1)
    if request.method == "POST":
        hora = datetime.fromisoformat(request.POST["hora"])
        paciente = cita.paciente if cita else request.user
        if request.user.is_staff and not cita and request.POST.get("paciente"):
            paciente = User.objects.filter(username=request.POST["paciente"]).first()
        if not paciente:
            messages.error(request, "Ese paciente no existe.")
        elif Cita.objects.filter(paciente=paciente, fecha_hora=hora, estado="programada").exclude(pk=cita_id).exists():
            messages.error(request, "El paciente ya tiene otra cita a esa hora.")
        else:
            try:
                with transaction.atomic():
                    if cita:
                        cita.fecha_hora = hora; cita.save()
                    else:
                        Cita.objects.create(paciente=paciente, medico=medico, fecha_hora=hora,
                            motivo=request.POST.get("motivo", ""), creada_por=request.user)
                messages.success(request, "Cita guardada correctamente.")
                return redirect("mis_citas")
            except IntegrityError:
                messages.error(request, "Ese horario ya fue tomado. Elige otro.")
    return render(request, "agendar.html", {"medico": medico, "cita": cita, "dia": dia,
        "hoy": date.today(), "horas": horarios(medico, dia)})

@login_required
def reprogramar(request, cita_id):
    cita = get_object_or_404(Cita, pk=cita_id, estado="programada")
    return agendar(request, cita.medico_id, cita.id)

@login_required
@require_POST
def cancelar(request, cita_id):
    cita = get_object_or_404(Cita, pk=cita_id)
    if request.user.is_staff or cita.paciente == request.user:
        cita.estado = "cancelada"; cita.save()
        messages.success(request, "Cita cancelada.")
    return redirect("mis_citas")

@login_required
def mis_citas(request):
    qs = Cita.objects.select_related("medico__especialidad", "medico__centro", "paciente").order_by("fecha_hora")
    if not request.user.is_staff: qs = qs.filter(paciente=request.user)
    return render(request, "mis_citas.html", {"citas": qs})

@user_passes_test(lambda u: u.is_staff)
def demografia(request):
    def agrupar(campo):
        d = list(Perfil.objects.exclude(**{campo: ""}).values(campo).annotate(n=Count("id")).order_by("-n")[:10])
        m = d[0]["n"] if d else 1
        return [{"nombre": x[campo], "n": x["n"], "pct": round(x["n"] * 100 / m)} for x in d]
    return render(request, "demografia.html", {"ciudades": agrupar("ciudad"), "barrios": agrupar("barrio"),
        "total": Perfil.objects.count()})

@login_required
def chatbot(request):
    if request.method == "POST":
        texto = json.loads(request.body).get("texto", "")
        perfil = Perfil.objects.filter(user=request.user).first()
        return JsonResponse(clasificar(texto, perfil.expediente if perfil else ""))
    return redirect("buscar")
