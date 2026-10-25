from django.contrib.auth import views as v
from django.urls import path
from . import views as w
urlpatterns = [
    path("login/", v.LoginView.as_view(), name="login"),
    path("logout/", v.LogoutView.as_view(), name="logout"),
    path("registro/", w.registro, name="registro"),
    path("", w.buscar, name="buscar"),
    path("agendar/<int:medico_id>/", w.agendar, name="agendar"),
    path("reprogramar/<int:cita_id>/", w.reprogramar, name="reprogramar"),
    path("cancelar/<int:cita_id>/", w.cancelar, name="cancelar"),
    path("mis-citas/", w.mis_citas, name="mis_citas"),
    path("demografia/", w.demografia, name="demografia"),
    path("chatbot/", w.chatbot, name="chatbot"),
]
