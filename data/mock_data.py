# data/mock_data.py — Datos de prueba para ConVivir

COLEGIOS = [
    {"id": 1, "nombre": "Instituto San Martín",      "ciudad": "Buenos Aires", "docentes": 4, "aulas": 6,  "estado": "Activo"},
    {"id": 2, "nombre": "Colegio del Valle",          "ciudad": "Córdoba",      "docentes": 2, "aulas": 3,  "estado": "Activo"},
    {"id": 3, "nombre": "Escuela Belgrano",            "ciudad": "Rosario",      "docentes": 1, "aulas": 2,  "estado": "Pendiente KYC"},
    {"id": 4, "nombre": "Colegio Las Flores",          "ciudad": "Mendoza",      "docentes": 3, "aulas": 4,  "estado": "Activo"},
    {"id": 5, "nombre": "Instituto Rivadavia",         "ciudad": "Tucumán",      "docentes": 0, "aulas": 0,  "estado": "Suspendido"},
]

DOCENTES = [
    {"id": 1, "nombre": "María García",    "email": "docente@colegio.ar",   "colegio": "Instituto San Martín", "aulas": 2, "estado": "Validado",  "kyc": "Aprobado"},
    {"id": 2, "nombre": "Carlos López",    "email": "clopez@colegio.ar",    "colegio": "Instituto San Martín", "aulas": 1, "estado": "Validado",  "kyc": "Aprobado"},
    {"id": 3, "nombre": "Ana Fernández",   "email": "afernandez@valle.ar",  "colegio": "Colegio del Valle",    "aulas": 2, "estado": "Pendiente", "kyc": "Pendiente"},
    {"id": 4, "nombre": "Roberto Soria",   "email": "rsoria@belgrano.ar",   "colegio": "Escuela Belgrano",     "aulas": 0, "estado": "Pendiente", "kyc": "En revisión"},
    {"id": 5, "nombre": "Laura Vega",      "email": "lvega@flores.ar",      "colegio": "Colegio Las Flores",   "aulas": 3, "estado": "Validado",  "kyc": "Aprobado"},
]

AULAS = [
    {"id": 1, "nombre": "3° A Primaria",  "colegio": "Instituto San Martín", "docente": "María García",  "alumnos": 24, "estado": "Habilitada",    "sociograma": "Completado"},
    {"id": 2, "nombre": "4° B Primaria",  "colegio": "Instituto San Martín", "docente": "María García",  "alumnos": 22, "estado": "Habilitada",    "sociograma": "En progreso"},
    {"id": 3, "nombre": "5° A Secundaria","colegio": "Instituto San Martín", "docente": "Carlos López",  "alumnos": 28, "estado": "Deshabilitada", "sociograma": "Sin iniciar"},
    {"id": 4, "nombre": "2° B Secundaria","colegio": "Colegio del Valle",    "docente": "Ana Fernández", "alumnos": 19, "estado": "Habilitada",    "sociograma": "Sin iniciar"},
]

ALUMNOS = [
    {"id":  1, "nombre": "Lucas Martínez",    "aula": "3° A Primaria", "genero": "M", "encuesta": True,  "perfil": "Popular",    "indice_aceptacion": 0.82, "indice_rechazo": 0.05, "alerta": None},
    {"id":  2, "nombre": "Sofía Rodríguez",   "aula": "3° A Primaria", "genero": "F", "encuesta": True,  "perfil": "Integrado",  "indice_aceptacion": 0.60, "indice_rechazo": 0.10, "alerta": None},
    {"id":  3, "nombre": "Mateo González",     "aula": "3° A Primaria", "genero": "M", "encuesta": True,  "perfil": "Aislado",    "indice_aceptacion": 0.08, "indice_rechazo": 0.12, "alerta": "Alta"},
    {"id":  4, "nombre": "Valentina Torres",   "aula": "3° A Primaria", "genero": "F", "encuesta": True,  "perfil": "Rechazado",  "indice_aceptacion": 0.05, "indice_rechazo": 0.78, "alerta": "Alta"},
    {"id":  5, "nombre": "Benjamín López",     "aula": "3° A Primaria", "genero": "M", "encuesta": True,  "perfil": "Integrado",  "indice_aceptacion": 0.55, "indice_rechazo": 0.08, "alerta": None},
    {"id":  6, "nombre": "Camila Díaz",        "aula": "3° A Primaria", "genero": "F", "encuesta": True,  "perfil": "Popular",    "indice_aceptacion": 0.75, "indice_rechazo": 0.06, "alerta": None},
    {"id":  7, "nombre": "Nicolás Pérez",      "aula": "3° A Primaria", "genero": "M", "encuesta": True,  "perfil": "Controvertido","indice_aceptacion":0.48, "indice_rechazo": 0.42, "alerta": "Media"},
    {"id":  8, "nombre": "Isabella Moreno",    "aula": "3° A Primaria", "genero": "F", "encuesta": True,  "perfil": "Integrado",  "indice_aceptacion": 0.50, "indice_rechazo": 0.15, "alerta": None},
    {"id":  9, "nombre": "Santiago Romero",    "aula": "3° A Primaria", "genero": "M", "encuesta": False, "perfil": "—",          "indice_aceptacion": None, "indice_rechazo": None, "alerta": None},
    {"id": 10, "nombre": "Emma Álvarez",       "aula": "3° A Primaria", "genero": "F", "encuesta": True,  "perfil": "Integrado",  "indice_aceptacion": 0.45, "indice_rechazo": 0.20, "alerta": None},
    {"id": 11, "nombre": "Joaquín Ramírez",    "aula": "3° A Primaria", "genero": "M", "encuesta": True,  "perfil": "Integrado",  "indice_aceptacion": 0.40, "indice_rechazo": 0.18, "alerta": None},
    {"id": 12, "nombre": "Martina Castro",     "aula": "3° A Primaria", "genero": "F", "encuesta": False, "perfil": "—",          "indice_aceptacion": None, "indice_rechazo": None, "alerta": None},
]

ALERTAS = [
    {"id": 1, "alumno": "Valentina Torres", "aula": "3° A Primaria", "tipo": "Rechazo elevado",  "prioridad": "Alta",  "fecha": "2025-05-10", "estado": "Pendiente",  "nota": ""},
    {"id": 2, "alumno": "Mateo González",   "aula": "3° A Primaria", "tipo": "Aislamiento",      "prioridad": "Alta",  "fecha": "2025-05-10", "estado": "En gestión", "nota": "Se habló con la familia."},
    {"id": 3, "alumno": "Nicolás Pérez",    "aula": "3° A Primaria", "tipo": "Perfil controvertido","prioridad":"Media","fecha": "2025-05-10", "estado": "Pendiente",  "nota": ""},
]

CONTENIDO_EDUCATIVO = {
    "docente": [
        {"titulo": "Cómo identificar el bullying en el aula",        "tipo": "Guía",      "tiempo": "8 min"},
        {"titulo": "Intervención temprana: primeros pasos",           "tipo": "Artículo",  "tiempo": "5 min"},
        {"titulo": "Cómo leer e interpretar un sociograma",           "tipo": "Tutorial",  "tiempo": "12 min"},
        {"titulo": "Comunicación con familias en situaciones difíciles","tipo":"Guía",     "tiempo": "6 min"},
        {"titulo": "Dinámica de cohesión grupal: actividades prácticas","tipo":"Actividad","tiempo": "15 min"},
    ],
    "student": [
        {"titulo": "¿Qué es el bullying y cómo reconocerlo?",         "tipo": "Artículo",  "tiempo": "4 min"},
        {"titulo": "Cómo pedir ayuda si estás pasando mal",           "tipo": "Guía",      "tiempo": "3 min"},
        {"titulo": "Ser buen compañero/a: pequeñas acciones grandes cambios","tipo":"Video","tiempo": "5 min"},
        {"titulo": "Emociones difíciles: está bien sentirse así",     "tipo": "Artículo",  "tiempo": "4 min"},
    ],
}

SOCIOGRAMA_EDGES = [
    # (origen_id, destino_id, tipo)  tipo: "positivo" | "negativo"
    (1, 2, "positivo"), (1, 6, "positivo"), (1, 5, "positivo"),
    (2, 1, "positivo"), (2, 6, "positivo"),
    (3, 5, "positivo"), (3, 2, "positivo"),
    (4, 3, "positivo"),
    (5, 1, "positivo"), (5, 6, "positivo"),
    (6, 1, "positivo"), (6, 2, "positivo"), (6, 8, "positivo"),
    (7, 1, "positivo"), (7, 4, "negativo"),
    (8, 6, "positivo"), (8, 10, "positivo"),
    (9, 5, "positivo"),
    (10, 8, "positivo"), (10, 11, "positivo"),
    (11, 10, "positivo"), (11, 2, "positivo"),
    (12, 6, "positivo"),
    # Rechazos hacia Valentina (id=4)
    (1, 4, "negativo"), (5, 4, "negativo"), (6, 4, "negativo"),
    (2, 4, "negativo"), (8, 4, "negativo"),
]
