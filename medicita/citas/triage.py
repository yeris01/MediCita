import unicodedata

def norm(t):
    return "".join(c for c in unicodedata.normalize("NFD", t.lower()) if unicodedata.category(c) != "Mn")

CRITICOS = ["dolor de pecho", "no puedo respirar", "falta de aire", "desmayo", "convulsion", "sangrado abundante",
            "paralisis", "perdida de conciencia", "no respira", "ahogo"]
ALTOS = ["fiebre alta", "vomito con sangre", "dolor abdominal fuerte", "fractura", "dificultad para respirar",
         "mareo intenso", "confusion"]
MEDIOS = ["fiebre", "vomito", "diarrea", "dolor", "tos", "mareo", "infeccion", "erupcion"]
RIESGO = ["diabetes", "hipertension", "asma", "cardiac", "embarazo", "cancer"]
ESPECIALIDAD = {"pecho": "Cardiología", "corazon": "Cardiología", "piel": "Dermatología", "erupcion": "Dermatología",
                "hueso": "Ortopedia", "fractura": "Ortopedia", "rodilla": "Ortopedia", "espalda": "Ortopedia",
                "nino": "Pediatría", "bebe": "Pediatría", "embarazo": "Ginecología"}

def clasificar(texto, expediente=""):
    t, e = norm(texto), norm(expediente)
    if any(k in t for k in CRITICOS): puntos = 100
    elif any(k in t for k in ALTOS): puntos = 60
    elif any(k in t for k in MEDIOS): puntos = 30
    else: puntos = 10
    riesgo = any(k in e for k in RIESGO)
    if riesgo and puntos >= 30: puntos += 15
    esp = next((v for k, v in ESPECIALIDAD.items() if k in t), "Medicina General")
    if puntos >= 100:
        return {"nivel": "Crítico", "lv": 1, "especialidad": esp,
                "mensaje": "Posible emergencia. Llama al 123 o acude YA a urgencias; no esperes una cita."}
    if puntos >= 60:
        return {"nivel": "Alto", "lv": 2, "especialidad": esp,
                "mensaje": "Requiere atención el mismo día. Agenda la cita más próxima o acude a urgencias." +
                           (" Tu expediente indica un factor de riesgo." if riesgo else "")}
    if puntos >= 30:
        return {"nivel": "Medio", "lv": 3, "especialidad": esp,
                "mensaje": "Agenda una cita en los próximos 2-3 días." +
                           (" Tu expediente indica un factor de riesgo." if riesgo else "")}
    return {"nivel": "Bajo", "lv": 4, "especialidad": esp,
            "mensaje": "Cita de control o consulta general; sin señales de urgencia."}
