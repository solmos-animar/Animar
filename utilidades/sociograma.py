# utilidades/sociograma.py
"""
Algoritmo de cálculo del sociograma.
Se ejecuta automáticamente cuando la encuesta alcanza el umbral de participación.
"""
import json
from sqlalchemy import text


def calcular_sociograma(conn, encuesta_id: int) -> dict:
    """
    Calcula todos los índices sociométricos para una encuesta.
    Retorna un dict con los datos por alumno y los índices del grupo.
    """
    with conn.session as s:

        # 1. Alumnos que participaron
        res = s.execute(text("""
            SELECT DISTINCT alumno_id FROM encuesta_respuestas
            WHERE encuesta_id = :eid
        """), {"eid": encuesta_id})
        participantes = [r[0] for r in res.fetchall()]
        n = len(participantes)

        if n == 0:
            return {}

        # 2. Nombres de los alumnos
        res = s.execute(text("""
            SELECT id, nombre, apellido FROM alumnos
            WHERE id = ANY(:ids)
        """), {"ids": participantes})
        alumnos = {r[0]: {"nombre": r[1], "apellido": r[2]} for r in res.fetchall()}

        # 3. Elecciones positivas y negativas
        res = s.execute(text("""
            SELECT ep.tipo, er.alumno_id, er.elegido_id
            FROM encuesta_respuestas er
            INNER JOIN encuesta_preguntas ep ON ep.id = er.pregunta_id
            WHERE er.encuesta_id = :eid
              AND er.elegido_id IS NOT NULL
              AND ep.tipo IN ('eleccion_positiva', 'eleccion_negativa')
        """), {"eid": encuesta_id})
        elecciones = res.fetchall()

        # 4. Respuestas Likert (clima)
        res = s.execute(text("""
            SELECT er.alumno_id, ep.texto, er.valor_likert
            FROM encuesta_respuestas er
            INNER JOIN encuesta_preguntas ep ON ep.id = er.pregunta_id
            WHERE er.encuesta_id = :eid
              AND er.valor_likert IS NOT NULL
        """), {"eid": encuesta_id})
        likerts = res.fetchall()

        # 5. Mensajes confidenciales
        res = s.execute(text("""
            SELECT er.alumno_id, er.texto_libre
            FROM encuesta_respuestas er
            INNER JOIN encuesta_preguntas ep ON ep.id = er.pregunta_id
            WHERE er.encuesta_id = :eid
              AND er.texto_libre IS NOT NULL
              AND ep.tipo = 'texto_libre'
              AND er.texto_libre != ''
        """), {"eid": encuesta_id})
        mensajes = {r[0]: r[1] for r in res.fetchall()}

    # ============================================================
    # CALCULAR ÍNDICES POR ALUMNO
    # ============================================================
    pos_recibidas  = {aid: 0 for aid in participantes}
    neg_recibidas  = {aid: 0 for aid in participantes}
    pos_emitidas   = {aid: 0 for aid in participantes}
    neg_emitidas   = {aid: 0 for aid in participantes}
    mutual_pos     = {aid: 0 for aid in participantes}

    # Registrar elecciones positivas para calcular reciprocidad
    pos_dict = {}  # {emisor: set(elegidos positivos)}
    for tipo, emisor, elegido in elecciones:
        if elegido not in participantes:
            continue
        if tipo == "eleccion_positiva":
            pos_recibidas[elegido] = pos_recibidas.get(elegido, 0) + 1
            pos_emitidas[emisor]   = pos_emitidas.get(emisor, 0) + 1
            if emisor not in pos_dict:
                pos_dict[emisor] = set()
            pos_dict[emisor].add(elegido)
        elif tipo == "eleccion_negativa":
            neg_recibidas[elegido] = neg_recibidas.get(elegido, 0) + 1
            neg_emitidas[emisor]   = neg_emitidas.get(emisor, 0) + 1

    # Calcular elecciones mutuas
    for emisor, elegidos in pos_dict.items():
        for elegido in elegidos:
            if elegido in pos_dict and emisor in pos_dict[elegido]:
                mutual_pos[emisor] = mutual_pos.get(emisor, 0) + 1

    # Máximos posibles (n-1 porque no puede elegirse a sí mismo)
    max_posible = max(n - 1, 1)

    resultados = {}
    for aid in participantes:
        pr = pos_recibidas.get(aid, 0)
        nr = neg_recibidas.get(aid, 0)
        pe = pos_emitidas.get(aid, 0)
        mu = mutual_pos.get(aid, 0)

        idx_popularidad  = round(pr / max_posible, 3)
        idx_rechazo      = round(nr / max_posible, 3)
        idx_integracion  = round((idx_popularidad - idx_rechazo + 1) / 2, 3)
        idx_reciprocidad = round(mu / max(pe, 1), 3)

        # Clasificación de rol
        rol = _clasificar_rol(idx_popularidad, idx_rechazo)

        # Likert promedio de este alumno
        likert_vals = [r[2] for r in likerts if r[0] == aid and r[2] is not None]
        likert_prom = round(sum(likert_vals) / len(likert_vals), 2) if likert_vals else None

        # Alertas
        alertas = []
        if rol in ("rechazado", "ignorado"):
            alertas.append(f"Alumno clasificado como '{rol}' — requiere atención")
        if idx_rechazo > 0.4:
            alertas.append("Alto índice de rechazo")
        if aid in mensajes:
            alertas.append("⚠️ Dejó un mensaje confidencial al docente")

        resultados[aid] = {
            "nombre":          alumnos[aid]["nombre"],
            "apellido":        alumnos[aid]["apellido"],
            "pos_recibidas":   pr,
            "neg_recibidas":   nr,
            "pos_emitidas":    pe,
            "mutuas":          mu,
            "idx_popularidad": idx_popularidad,
            "idx_rechazo":     idx_rechazo,
            "idx_integracion": idx_integracion,
            "idx_reciprocidad":idx_reciprocidad,
            "rol":             rol,
            "likert_prom":     likert_prom,
            "mensaje_conf":    mensajes.get(aid),
            "alertas":         alertas,
        }

    # ============================================================
    # ÍNDICES GRUPALES
    # ============================================================
    todos_integracion = [r["idx_integracion"] for r in resultados.values()]
    todos_rechazo     = [r["idx_rechazo"]     for r in resultados.values()]
    todos_reciprocidad= [r["idx_reciprocidad"] for r in resultados.values()]

    grupo = {
        "cohesion":          round(sum(todos_integracion) / len(todos_integracion), 3),
        "exclusion":         round(sum(todos_rechazo)     / len(todos_rechazo),     3),
        "reciprocidad_media":round(sum(todos_reciprocidad)/ len(todos_reciprocidad),3),
        "n_participantes":   n,
        "n_alertas":         sum(1 for r in resultados.values() if r["alertas"]),
        "roles_resumen": {
            "estrella":       sum(1 for r in resultados.values() if r["rol"] == "estrella"),
            "bien_integrado": sum(1 for r in resultados.values() if r["rol"] == "bien_integrado"),
            "controvertido":  sum(1 for r in resultados.values() if r["rol"] == "controvertido"),
            "ignorado":       sum(1 for r in resultados.values() if r["rol"] == "ignorado"),
            "rechazado":      sum(1 for r in resultados.values() if r["rol"] == "rechazado"),
        }
    }

    # ============================================================
    # ARISTAS PARA EL GRAFO
    # ============================================================
    aristas = []
    for tipo, emisor, elegido in elecciones:
        if elegido in participantes:
            aristas.append({
                "desde": emisor,
                "hacia": elegido,
                "tipo":  tipo,
            })

    return {
        "alumnos":  resultados,
        "grupo":    grupo,
        "aristas":  aristas,
    }


def _clasificar_rol(idx_popularidad: float, idx_rechazo: float) -> str:
    if idx_popularidad > 0.5 and idx_rechazo < 0.2:
        return "estrella"
    elif idx_rechazo > 0.4:
        return "rechazado"
    elif idx_popularidad > 0.3 and idx_rechazo > 0.3:
        return "controvertido"
    elif idx_popularidad < 0.15 and idx_rechazo < 0.15:
        return "ignorado"
    else:
        return "bien_integrado"


def guardar_sociograma(conn, encuesta_id: int, datos: dict):
    """Guarda o actualiza el sociograma calculado en la base de datos."""
    with conn.session as s:
        s.execute(text("""
            INSERT INTO sociogramas (encuesta_id, datos_json)
            VALUES (:eid, :datos)
            ON CONFLICT (encuesta_id) DO UPDATE
                SET datos_json = EXCLUDED.datos_json,
                    generado_en = NOW()
        """), {
            "eid":   encuesta_id,
            "datos": json.dumps(datos),
        })
        # Marcar encuesta como sociograma listo
        s.execute(text("""
            UPDATE encuestas SET estado = 'sociograma_listo'
            WHERE id = :eid
        """), {"eid": encuesta_id})
        s.commit()


def verificar_y_generar(conn, encuesta_id: int) -> bool:
    """
    Verifica si la encuesta alcanzó el umbral de participación.
    Si sí, genera y guarda el sociograma automáticamente.
    Retorna True si se generó el sociograma.
    """
    with conn.session as s:
        # Datos de la encuesta
        res = s.execute(text("""
            SELECT e.umbral_pct, e.grado, e.colegio_id, e.estado
            FROM encuestas e WHERE e.id = :eid
        """), {"eid": encuesta_id})
        enc = res.fetchone()

        if not enc or enc[3] != "activa":
            return False

        umbral_pct, grado, colegio_id, _ = enc

        # Total de alumnos en el grado
        res = s.execute(text("""
            SELECT COUNT(*) FROM alumnos
            WHERE colegio_id = :cid AND grado = :grado AND activo = TRUE
        """), {"cid": colegio_id, "grado": grado})
        total_alumnos = res.fetchone()[0]

        # Alumnos que respondieron (al menos una respuesta)
        res = s.execute(text("""
            SELECT COUNT(DISTINCT alumno_id) FROM encuesta_respuestas
            WHERE encuesta_id = :eid
        """), {"eid": encuesta_id})
        respondieron = res.fetchone()[0]

    if total_alumnos == 0:
        return False

    pct_actual = (respondieron / total_alumnos) * 100

    if pct_actual >= umbral_pct:
        datos = calcular_sociograma(conn, encuesta_id)
        guardar_sociograma(conn, encuesta_id, datos)
        return True

    return False


def cargar_sociograma(conn, encuesta_id: int) -> dict | None:
    """Carga el sociograma guardado de la base de datos."""
    with conn.session as s:
        res = s.execute(text("""
            SELECT datos_json FROM sociogramas WHERE encuesta_id = :eid
        """), {"eid": encuesta_id})
        row = res.fetchone()
    if row:
        return json.loads(row[0]) if isinstance(row[0], str) else row[0]
    return None


def get_participacion(conn, encuesta_id: int) -> tuple[int, int, float]:
    """Retorna (respondieron, total, porcentaje)."""
    with conn.session as s:
        res = s.execute(text("""
            SELECT e.grado, e.colegio_id FROM encuestas e WHERE e.id = :eid
        """), {"eid": encuesta_id})
        enc = res.fetchone()
        if not enc:
            return 0, 0, 0.0

        res = s.execute(text("""
            SELECT COUNT(*) FROM alumnos
            WHERE colegio_id = :cid AND grado = :grado AND activo = TRUE
        """), {"cid": enc[1], "grado": enc[0]})
        total = res.fetchone()[0]

        res = s.execute(text("""
            SELECT COUNT(DISTINCT alumno_id) FROM encuesta_respuestas
            WHERE encuesta_id = :eid
        """), {"eid": encuesta_id})
        respondieron = res.fetchone()[0]

    pct = round((respondieron / total * 100), 1) if total > 0 else 0.0
    return respondieron, total, pct
