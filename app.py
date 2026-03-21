"""
data/engine.py  —  Motor de datos de ConVivir
Guarda y lee respuestas en JSON local.
Calcula perfiles sociométricos y construye los edges del sociograma.
"""

import json
import os
from pathlib import Path
from datetime import datetime

# ── Ruta del archivo de datos ──────────────────────────────────────────────────
DATA_DIR  = Path(__file__).parent
AULAS_FILE = DATA_DIR / "aulas.json"
RESP_FILE  = DATA_DIR / "respuestas.json"

# ── Helpers de IO ──────────────────────────────────────────────────────────────
def _load(path: Path) -> dict:
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}

def _save(path: Path, data: dict):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

# ══════════════════════════════════════════════════════════════════════════════
# AULAS Y ALUMNOS
# ══════════════════════════════════════════════════════════════════════════════

def get_aulas() -> dict:
    """Devuelve {codigo_aula: {nombre, docente, alumnos: [{id, nombre, genero}]}}"""
    data = _load(AULAS_FILE)
    if not data:
        # Aula de demo precargada
        data = {
            "AULA2025": {
                "nombre": "3° A Primaria",
                "docente": "Prof. María García",
                "creada": "2025-01-01",
                "alumnos": [
                    {"id": 1,  "nombre": "Lucas Martínez",   "genero": "M"},
                    {"id": 2,  "nombre": "Sofía Rodríguez",  "genero": "F"},
                    {"id": 3,  "nombre": "Mateo González",   "genero": "M"},
                    {"id": 4,  "nombre": "Valentina Torres", "genero": "F"},
                    {"id": 5,  "nombre": "Benjamín López",   "genero": "M"},
                    {"id": 6,  "nombre": "Camila Díaz",      "genero": "F"},
                    {"id": 7,  "nombre": "Nicolás Pérez",    "genero": "M"},
                    {"id": 8,  "nombre": "Isabella Moreno",  "genero": "F"},
                    {"id": 9,  "nombre": "Santiago Romero",  "genero": "M"},
                    {"id": 10, "nombre": "Emma Álvarez",     "genero": "F"},
                    {"id": 11, "nombre": "Joaquín Ramírez",  "genero": "M"},
                    {"id": 12, "nombre": "Martina Castro",   "genero": "F"},
                ]
            }
        }
        _save(AULAS_FILE, data)
    return data


def get_aula(codigo: str) -> dict | None:
    return get_aulas().get(codigo.upper())


def crear_aula(codigo: str, nombre: str, docente: str, alumnos: list):
    """alumnos = [{nombre, genero}]"""
    aulas = get_aulas()
    alumnos_con_id = [
        {"id": i + 1, "nombre": a["nombre"], "genero": a.get("genero", "?")}
        for i, a in enumerate(alumnos)
    ]
    aulas[codigo.upper()] = {
        "nombre": nombre,
        "docente": docente,
        "creada": datetime.now().strftime("%Y-%m-%d"),
        "alumnos": alumnos_con_id,
    }
    _save(AULAS_FILE, aulas)


def get_alumno_by_numero(codigo_aula: str, numero: int) -> dict | None:
    aula = get_aula(codigo_aula)
    if not aula:
        return None
    for a in aula["alumnos"]:
        if a["id"] == numero:
            return a
    return None

# ══════════════════════════════════════════════════════════════════════════════
# RESPUESTAS DE ENCUESTA
# ══════════════════════════════════════════════════════════════════════════════

def get_respuestas() -> dict:
    return _load(RESP_FILE)


def ya_respondio(codigo_aula: str, alumno_id: int) -> bool:
    resp = get_respuestas()
    key = f"{codigo_aula.upper()}_{alumno_id}"
    return key in resp


def guardar_respuesta(codigo_aula: str, alumno_id: int, respuesta: dict):
    resp = get_respuestas()
    key = f"{codigo_aula.upper()}_{alumno_id}"
    respuesta["alumno_id"]    = alumno_id
    respuesta["codigo_aula"]  = codigo_aula.upper()
    respuesta["timestamp"]    = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    resp[key] = respuesta
    _save(RESP_FILE, resp)


def get_respuestas_aula(codigo_aula: str) -> list:
    resp = get_respuestas()
    codigo = codigo_aula.upper()
    return [v for k, v in resp.items() if k.startswith(codigo + "_")]

# ══════════════════════════════════════════════════════════════════════════════
# CÁLCULO DEL SOCIOGRAMA
# ══════════════════════════════════════════════════════════════════════════════

# Dimensiones de la encuesta → categoría sociométrica
# positivo = elección preferida  |  negativo = rechazo  |  neutro = conducta observada
DIM_META = {
    "me_gusta":         ("positivo",  1.0),
    "mis_amigos":       ("positivo",  1.2),   # peso mayor: amistad declarada
    "ayuda":            ("positivo",  0.8),
    "anima":            ("positivo",  0.8),
    "no_me_gusta":      ("negativo", -1.0),
    "no_deja_participar": ("negativo", -0.8),
    "empujones_hace":   ("negativo", -0.7),
    "insulta":          ("negativo", -0.7),
    # víctima (recibe)
    "empujones_recibe": ("victima",  -0.6),
    "insulta_recibe":   ("victima",  -0.6),
    "excluido":         ("victima",  -0.8),
    "rumores":          ("negativo", -0.7),
}

def calcular_sociograma(codigo_aula: str) -> dict:
    """
    Devuelve:
      {
        alumno_id: {
          nombre, genero,
          score_social,      # suma ponderada de votos recibidos
          votos_positivos,   # cuántos lo eligieron positivo
          votos_negativos,   # cuántos lo rechazaron
          es_victima,        # bool
          perfil,            # Popular / Integrado / Controvertido / Aislado / Rechazado / Sin datos
          alerta,            # None / "Media" / "Alta"
          respondio,         # bool
        },
        "_edges": [(origen_id, destino_id, tipo, dimension)]
      }
    """
    aula = get_aula(codigo_aula)
    if not aula:
        return {}

    alumnos = {a["id"]: a for a in aula["alumnos"]}
    respuestas = get_respuestas_aula(codigo_aula)

    # Inicializar contadores
    stats = {
        aid: {
            "nombre": a["nombre"],
            "genero": a["genero"],
            "score_social": 0.0,
            "votos_positivos": 0,
            "votos_negativos": 0,
            "votos_victima": 0,
            "respondio": False,
            "perfil": "Sin datos",
            "alerta": None,
        }
        for aid, a in alumnos.items()
    }

    edges = []

    # Procesar cada respuesta
    for r in respuestas:
        origen_id = r["alumno_id"]
        if origen_id in stats:
            stats[origen_id]["respondio"] = True

        for dim, (tipo, peso) in DIM_META.items():
            elegidos = r.get(dim, [])
            if isinstance(elegidos, int):
                elegidos = [elegidos]
            for dest_id in elegidos:
                if dest_id not in stats or dest_id == origen_id:
                    continue
                stats[dest_id]["score_social"] += peso
                if tipo == "positivo":
                    stats[dest_id]["votos_positivos"] += 1
                    edges.append((origen_id, dest_id, "positivo", dim))
                elif tipo == "negativo":
                    stats[dest_id]["votos_negativos"] += 1
                    edges.append((origen_id, dest_id, "negativo", dim))
                elif tipo == "victima":
                    stats[dest_id]["votos_victima"] += 1
                    stats[dest_id]["votos_negativos"] += 1
                    edges.append((origen_id, dest_id, "victima", dim))

    # Clasificar perfiles
    n_resp = len(respuestas)
    for aid, s in stats.items():
        if not any(r.get("alumno_id") != aid for r in respuestas):
            # Sin respuestas de otros sobre este alumno: usar sus propios votos recibidos
            pass
        vp = s["votos_positivos"]
        vn = s["votos_negativos"]
        vv = s["votos_victima"]
        score = s["score_social"]

        if n_resp == 0:
            perfil = "Sin datos"
            alerta = None
        elif vp == 0 and vn == 0 and vv == 0:
            perfil = "Sin datos"
            alerta = None
        elif vp >= 4 and vn <= 1:
            perfil = "Popular"
            alerta = None
        elif vn >= 4 and vp <= 1:
            perfil = "Rechazado"
            alerta = "Alta"
        elif vp <= 1 and vn <= 1 and vv <= 1:
            perfil = "Aislado"
            alerta = "Alta" if vp == 0 else "Media"
        elif vp >= 2 and vn >= 2:
            perfil = "Controvertido"
            alerta = "Media"
        else:
            perfil = "Integrado"
            alerta = None

        # Víctima adicional
        if vv >= 3:
            alerta = "Alta"

        s["perfil"] = perfil
        s["alerta"] = alerta

    stats["_edges"] = edges
    stats["_n_respuestas"] = n_resp
    stats["_total_alumnos"] = len(alumnos)

    return stats
