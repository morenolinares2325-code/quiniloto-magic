# ══════════════════════════════════════════════════════════════
# QUINILOTO MAGIC - v16
# Calculo solo al pulsar Generar | Barita unica | 4 secciones
# ══════════════════════════════════════════════════════════════

import itertools
import math
import random
import requests
import streamlit as st

st.set_page_config(
    page_title="Quiniloto Magic",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────
# CONFIGURACION
# ─────────────────────────────────────────────────
PASSWORD = "2325"
PRECIO_QUINIELA     = 0.75
PRECIO_BONOLOTO     = 0.50
PRECIO_PRIMITIVA    = 1.00
PRECIO_EUROMILLONES = 2.50
MIN_QUINIELA        = 2
MIN_BONOLOTO        = 2
MIN_PRIMITIVA       = 1
MIN_EUROMILLONES    = 1

MAX_COMBINACIONES_DIRECTAS = 100000
MAX_APUESTAS_FINALES = 5000
MAX_BOLETOS_VISUALES = 200

PLENO_OPCIONES = ["0", "1", "2", "M"]

# ─────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: radial-gradient(circle at 20% 0%, #14152a 0%, #0a0b15 60%); }
h1, h2, h3 { color: #ffffff; letter-spacing: -0.5px; }
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d0e1c 0%, #14152a 100%);
    border-right: 1px solid rgba(255, 215, 0, 0.15);
}
header[data-testid="stHeader"] { display: none; }
[data-testid="stSidebarNav"] { display: none; }
[data-testid="stSidebarHeader"] { display: none; }
.stButton > button { border-radius: 8px; font-weight: 600; padding: 4px 8px; min-height: 32px; }
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%) !important;
    color: #0a0b15 !important;
    border: none !important;
    box-shadow: 0 2px 10px rgba(255, 215, 0, 0.5) !important;
}
.stButton > button[kind="secondary"] {
    background: transparent !important;
    color: #e0e0e0 !important;
    border: 1px solid #333 !important;
}
.num-partido { color: #FFD700; font-weight: 700; font-size: 14px; text-align: center; padding-top: 6px; }
.nombre-partido { color: #ffffff; font-weight: 500; font-size: 13px; padding-top: 6px; }
.resultado-oficial { color: #a0a0b8; font-size: 12px; text-align: center; padding-top: 8px; }
.boletin-cab {
    background: linear-gradient(180deg, rgba(255, 215, 0, 0.3) 0%, rgba(255, 165, 0, 0.15) 100%);
    color: #FFD700; text-align: center; font-weight: 700; font-size: 11px;
    padding: 6px 2px; border-radius: 4px;
}
.signo-celda {
    display: inline-block; padding: 4px 8px; border-radius: 4px;
    font-weight: 800; font-size: 12px; min-width: 22px; text-align: center;
}
.signo-1 { background: #22c55e; color: white; }
.signo-X { background: #eab308; color: white; }
.signo-2 { background: #ef4444; color: white; }
.titulo-seccion-dorado { color: #FFD700; font-weight: 800; letter-spacing: 1px; }
.titulo-columnas {
    text-align: center; color: #FFD700; font-weight: 800; font-size: 22px;
    padding: 16px 0; letter-spacing: 1px;
}
.barita-magica-container {
    text-align: center; margin: 30px 0 20px 0; padding: 24px;
    background: radial-gradient(circle, rgba(255,215,0,0.08) 0%, transparent 70%);
    border-radius: 20px;
}
.barita-magica-titulo {
    color: #FFD700; font-size: 32px; font-weight: 900; letter-spacing: 6px;
    text-shadow: 0 0 20px rgba(255,215,0,0.9), 0 0 40px rgba(255,215,0,0.5);
    margin-bottom: 6px;
}
.barita-magica-sub { color: #a0a0b8; font-size: 13px; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# API
# ═══════════════════════════════════════════════
def _get_api_key():
    try:
        return st.secrets.get("API_KEY_LOTERIAS", "")
    except Exception:
        return ""


@st.cache_data(ttl=1800, show_spinner=False)
def obtener_jornada(endpoint):
    key = _get_api_key()
    if not key:
        return {"error": "API_KEY_LOTERIAS no configurada."}
    try:
        url = "https://api.loteriasapi.com/api/v1/results/quiniela/" + endpoint
        r = requests.get(url, headers={"X-API-Key": key}, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}


def extraer_partidos(datos):
    partidos = []
    jornada_num = None
    fecha = None
    if not isinstance(datos, dict):
        return partidos, jornada_num, fecha
    jornada_num = datos.get("jornada") or datos.get("matchday") or datos.get("numero")
    fecha = datos.get("fecha") or datos.get("draw_date") or datos.get("fecha_sorteo")
    for k in ["resultados", "matches", "partidos", "games", "fixtures", "data"]:
        if k in datos and isinstance(datos[k], list):
            for r in datos[k]:
                if not isinstance(r, dict):
                    continue
                local = r.get("local") or r.get("home") or r.get("equipo_local") or "-"
                visit = r.get("visitante") or r.get("away") or r.get("equipo_visitante") or "-"
                signo = r.get("signo") or r.get("result") or r.get("sign") or ""
                partidos.append((local, visit, signo))
            return partidos, jornada_num, fecha
    for v in datos.values():
        if isinstance(v, dict):
            sp, sj, sf = extraer_partidos(v)
            if sp:
                return sp, sj, sf
    return partidos, jornada_num, fecha


# ═══════════════════════════════════════════════
# LOGICA
# ═══════════════════════════════════════════════
def generar_combinaciones(signos):
    return list(itertools.product(*[list(s) for s in signos]))


def contar_dobles_triples(signos):
    return (sum(1 for s in signos if len(s) == 2),
            sum(1 for s in signos if len(s) == 3))


def ordenar_signos(s):
    return "".join(sorted(set(s), key=lambda x: ["1", "X", "2"].index(x)))


def reducir_por_cobertura(combinaciones, garantia, objetivo=None):
    n_total = len(combinaciones)
    if n_total == 0:
        return []
    if objetivo is None:
        ratios = {13: 0.0625, 12: 0.0150, 11: 0.0030, 10: 0.0008}
        objetivo = max(MIN_QUINIELA, int(n_total * ratios.get(garantia, 0.01)))
    if objetivo >= n_total:
        return ["".join(c) for c in combinaciones]
    random.seed(42)
    combos_lista = [tuple(c) for c in combinaciones]
    indices = list(range(n_total))
    random.shuffle(indices)
    seleccionadas = []
    vistos = [set() for _ in range(14)]
    for idx in indices:
        if len(seleccionadas) >= objetivo:
            break
        c = combos_lista[idx]
        aporta = any(c[p] not in vistos[p] for p in range(14))
        if aporta or len(seleccionadas) > objetivo * 0.7:
            seleccionadas.append(c)
            for p in range(14):
                vistos[p].add(c[p])
    if len(seleccionadas) < objetivo:
        for idx in indices:
            if len(seleccionadas) >= objetivo:
                break
            if combos_lista[idx] not in seleccionadas:
                seleccionadas.append(combos_lista[idx])
    return ["".join(c) for c in seleccionadas]


def a_txt_quiniela(apuestas, pleno_local, pleno_visit):
    lineas = list(apuestas)
    if pleno_local and pleno_visit:
        lineas.append(str(pleno_local) + str(pleno_visit))
    return "\n".join(lineas)


def aplicar_barita_quiniela(apuestas, contador):
    if contador <= 0 or not apuestas:
        return list(apuestas)
    factores = [0.65, 0.45, 0.30, 0.20, 0.12, 0.07, 0.04, 0.02, 0.01, 0.005, 0.002]
    idx = min(contador - 1, len(factores) - 1)
    n_nuevo = max(1, int(len(apuestas) * factores[idx]))
    def score(c):
        s = "".join(c) if not isinstance(c, str) else c
        return abs(s.count("1") - s.count("2"))
    return sorted(apuestas, key=score)[:n_nuevo]


def aplicar_barita_numeros(combinaciones, contador):
    if contador <= 0 or not combinaciones:
        return list(combinaciones)
    factores = [0.65, 0.45, 0.30, 0.20, 0.12, 0.07, 0.04, 0.02, 0.01, 0.005, 0.002]
    idx = min(contador - 1, len(factores) - 1)
    n_nuevo = max(1, int(len(combinaciones) * factores[idx]))
    def score(c):
        nums = c[0] if (isinstance(c, tuple) and len(c) == 2 and isinstance(c[0], tuple)) else c
        suma = sum(nums)
        pares = sum(1 for x in nums if x % 2 == 0)
        return abs(suma - 125) + abs(pares - len(nums)//2) * 5
    return sorted(combinaciones, key=score)[:n_nuevo]


def generar_bonoloto(numeros):
    return list(itertools.combinations(sorted(numeros), 6)) if len(numeros) >= 6 else []


def generar_primitiva(numeros):
    return list(itertools.combinations(sorted(numeros), 6)) if len(numeros) >= 6 else []


def generar_euromillones(numeros, estrellas):
    if len(numeros) < 5 or len(estrellas) < 2: return []
    cn = list(itertools.combinations(sorted(numeros), 5))
    ce = list(itertools.combinations(sorted(estrellas), 2))
    return [(n, e) for n in cn for e in ce]


def txt_loteria(combinaciones):
    lineas = []
    for c in combinaciones:
        if isinstance(c, tuple) and len(c) == 2 and isinstance(c[0], tuple):
            nums, est = c
            lineas.append(" ".join(str(n).zfill(2) for n in nums) + " | " + " ".join(str(e).zfill(2) for e in est))
        else:
            lineas.append(" ".join(str(n).zfill(2) for n in c))
    return "\n".join(lineas)


def coste_real(n_ap, precio, min_ap):
    if n_ap < min_ap:
        return round(min_ap * precio, 2), True
    return round(n_ap * precio, 2), False


# ═══════════════════════════════════════════════
# LOGIN
# ═══════════════════════════════════════════════
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown(
        "<h1 style='text-align:center;font-family:Inter,sans-serif;"
        "font-size:52px;font-weight:900;letter-spacing:-2px;"
        "color:#FFD700;margin-top:15vh;margin-bottom:0;'>QUINILOTO</h1>"
        "<h2 style='text-align:center;font-family:Inter,sans-serif;"
        "font-size:32px;font-weight:700;letter-spacing:14px;"
        "color:#FFD700;margin-top:0;'>MAGIC</h2>",
        unsafe_allow_html=True,
    )
    st.markdown("<p style='text-align:center;color:#a0a0b8;font-size:14px;'>Acceso privado</p>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        pwd = st.text_input("Contrasena", type="password", label_visibility="collapsed")
        if st.button("Entrar", use_container_width=True, type="primary"):
            if pwd == PASSWORD:
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.error("Contrasena incorrecta")
    st.stop()


# ═══════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════
defaults = {
    "signos": ["1"] * 14,
    "pleno_local": "1",
    "pleno_visit": "0",
    "apuestas_reducidas": None,
    "red_sel": "13",
    "partidos_cargados": False,
    "auto_load_intentado": False,
    "bono_nums": [], "bono_combs": None, "bono_barita": 0,
    "pri_nums": [], "pri_combs": None, "pri_barita": 0,
    "eu_nums": [], "eu_est": [], "eu_combs": None, "eu_barita": 0,
    "barita_quiniela": 0,
    "partidos_jornada": [
        ("Equipo 1 L", "Equipo 1 V", ""), ("Equipo 2 L", "Equipo 2 V", ""),
        ("Equipo 3 L", "Equipo 3 V", ""), ("Equipo 4 L", "Equipo 4 V", ""),
        ("Equipo 5 L", "Equipo 5 V", ""), ("Equipo 6 L", "Equipo 6 V", ""),
        ("Equipo 7 L", "Equipo 7 V", ""), ("Equipo 8 L", "Equipo 8 V", ""),
        ("Equipo 9 L", "Equipo 9 V", ""), ("Equipo 10 L", "Equipo 10 V", ""),
        ("Equipo 11 L", "Equipo 11 V", ""), ("Equipo 12 L", "Equipo 12 V", ""),
        ("Equipo 13 L", "Equipo 13 V", ""), ("Equipo 14 L", "Equipo 14 V", ""),
    ],
    "pleno_partido": ("Local 15", "Visitante 15", ""),
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# AUTO-CARGA
if not st.session_state.partidos_cargados and not st.session_state.auto_load_intentado:
    st.session_state.auto_load_intentado = True
    try:
        datos = obtener_jornada("next")
        partidos = []
        if datos and "error" not in datos:
            partidos, _, _ = extraer_partidos(datos)
        if not partidos or len(partidos) < 14:
            datos = obtener_jornada("latest")
            if datos and "error" not in datos:
                partidos, _, _ = extraer_partidos(datos)
        if partidos and len(partidos) >= 14:
            st.session_state.partidos_jornada = partidos[:14]
            st.session_state.partidos_cargados = True
    except Exception:
        pass


# ═══════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════
with st.sidebar:
    st.markdown(
        "<h1 style='text-align:center;font-family:Inter,sans-serif;"
        "font-size:30px;font-weight:900;letter-spacing:-1px;"
        "color:#FFD700;margin-bottom:0;'>QUINILOTO</h1>"
        "<h2 style='text-align:center;font-family:Inter,sans-serif;"
        "font-size:22px;font-weight:700;letter-spacing:10px;"
        "color:#FFD700;margin-top:0;margin-bottom:25px;'>MAGIC</h2>",
        unsafe_allow_html=True,
    )
    st.markdown("---")
    seccion = st.radio(
        "Seccion",
        ["Inicio", "Quiniela", "Jornada actual", "Jornada siguiente",
         "Bonoloto", "Primitiva", "Euromillones", "Cuenta"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    if st.button("Recargar partidos", use_container_width=True):
        st.session_state.auto_load_intentado = False
        st.session_state.partidos_cargados = False
        st.cache_data.clear()
        st.rerun()
    if st.button("Cerrar sesion", use_container_width=True):
        st.session_state.autenticado = False
        st.rerun()


# ═══════════════════════════════════════════════
# INICIO
# ═══════════════════════════════════════════════
if seccion == "Inicio":
    st.markdown(
        "<h1 style='text-align:center;font-family:Inter,sans-serif;"
        "font-size:48px;font-weight:900;letter-spacing:-2px;"
        "color:#FFD700;margin-bottom:0;'>QUINILOTO MAGIC</h1>"
        "<p style='text-align:center;color:#a0a0b8;font-size:15px;"
        "margin-top:4px;'>Plataforma inteligente para quinielas y loterias</p>",
        unsafe_allow_html=True,
    )
    st.divider()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Quiniela", "14+1")
    c2.metric("Bonoloto", "6/49")
    c3.metric("Primitiva", "6/49")
    c4.metric("Euromillones", "5/50+2/12")


# ═══════════════════════════════════════════════
# QUINIELA (sin calculos hasta Generar)
# ═══════════════════════════════════════════════
elif seccion == "Quiniela":
    st.title("Quiniela")
    st.caption("Marca dobles/triples, elige reduccion y pulsa Generar.")

    if st.session_state.partidos_cargados:
        st.success("Partidos cargados desde la API.")

    # ── PARTIDOS ──
    st.subheader("1. Configura los partidos")
    for i in range(14):
        local_actual, visit_actual, resultado = st.session_state.partidos_jornada[i]
        cols = st.columns([0.5, 2.5, 2.5, 1, 1, 1])
        cols[0].markdown("<div class='num-partido'>" + str(i+1) + "</div>", unsafe_allow_html=True)
        with cols[1]:
            local = st.text_input("L" + str(i), value=local_actual, key="q_loc_" + str(i), label_visibility="collapsed")
        with cols[2]:
            visit = st.text_input("V" + str(i), value=visit_actual, key="q_vis_" + str(i), label_visibility="collapsed")
        st.session_state.partidos_jornada[i] = (local, visit, resultado)
        for j, signo in enumerate(["1", "X", "2"]):
            with cols[3 + j]:
                activo = signo in st.session_state.signos[i]
                if st.button(signo, key="q_" + str(i) + "_" + signo, use_container_width=True,
                             type="primary" if activo else "secondary"):
                    actual = st.session_state.signos[i]
                    if signo in actual:
                        nuevo = actual.replace(signo, "")
                        if nuevo == "": nuevo = "1"
                        st.session_state.signos[i] = nuevo
                    else:
                        st.session_state.signos[i] = ordenar_signos(actual + signo)
                    # Reset apuestas y barita al cambiar signos
                    st.session_state.apuestas_reducidas = None
                    st.session_state.barita_quiniela = 0
                    st.rerun()

    # ── PLENO ──
    st.markdown("---")
    st.markdown("<div class='titulo-seccion-dorado'>PLENO AL 15</div>", unsafe_allow_html=True)
    eq_local, eq_visit, _ = st.session_state.pleno_partido
    pl_cols = st.columns([0.5, 2.5, 2.5])
    pl_cols[0].markdown("<div class='num-partido'>15</div>", unsafe_allow_html=True)
    with pl_cols[1]:
        eq_local = st.text_input("PL", value=eq_local, key="q_pl_loc", label_visibility="collapsed")
    with pl_cols[2]:
        eq_visit = st.text_input("PV", value=eq_visit, key="q_pl_vis", label_visibility="collapsed")
    st.session_state.pleno_partido = (eq_local, eq_visit, "")

    st.caption("Goles LOCAL:")
    p_loc_cols = st.columns(4)
    for j, signo in enumerate(PLENO_OPCIONES):
        with p_loc_cols[j]:
            activo = signo == st.session_state.pleno_local
            if st.button("L:" + signo, key="pl_loc_" + signo, use_container_width=True,
                         type="primary" if activo else "secondary"):
                st.session_state.pleno_local = signo
                st.rerun()

    st.caption("Goles VISITANTE:")
    p_vis_cols = st.columns(4)
    for j, signo in enumerate(PLENO_OPCIONES):
        with p_vis_cols[j]:
            activo = signo == st.session_state.pleno_visit
            if st.button("V:" + signo, key="pl_vis_" + signo, use_container_width=True,
                         type="primary" if activo else "secondary"):
                st.session_state.pleno_visit = signo
                st.rerun()

    # ── RESUMEN SIN CALCULAR ──
    st.markdown("---")
    dobles, triples = contar_dobles_triples(st.session_state.signos)
    st.caption("Triples marcados: **" + str(triples) + "** · Dobles marcados: **" + str(dobles) + "**")

    # ── REDUCCION ──
    st.markdown("---")
    st.markdown("<div class='titulo-seccion-dorado'>SELECCIONAR REDUCCION</div>", unsafe_allow_html=True)
    c_red = st.columns(4)
    for i, (valor, label) in enumerate([
        ("13", "Reduccion al 13"), ("12", "Reduccion al 12"),
        ("11", "Reduccion al 11"), ("10", "Reduccion al 10"),
    ]):
        with c_red[i]:
            activo = st.session_state.red_sel == valor
            if st.button(label, key="red_" + valor, use_container_width=True,
                         type="primary" if activo else "secondary"):
                st.session_state.red_sel = valor
                st.rerun()

    # ── BOTONES ──
    st.markdown("---")
    b1, b2 = st.columns(2)
    with b1:
        if st.button("Borrar seleccion", use_container_width=True):
            st.session_state.signos = ["1"] * 14
            st.session_state.pleno_local = "1"
            st.session_state.pleno_visit = "0"
            st.session_state.apuestas_reducidas = None
            st.session_state.barita_quiniela = 0
            st.rerun()
    with b2:
        if st.button("Generar reduccion", type="primary", use_container_width=True):
            # SOLO AHORA calculamos todo
            dobles, triples = contar_dobles_triples(st.session_state.signos)
            apuestas_directas = (2 ** dobles) * (3 ** triples)
            
            if apuestas_directas == 1:
                st.warning("Marca al menos un doble o triple para que la reduccion tenga sentido.")
            elif apuestas_directas > MAX_COMBINACIONES_DIRECTAS:
                st.error("Demasiadas combinaciones (" + f"{apuestas_directas:,}" + "). Max " + f"{MAX_COMBINACIONES_DIRECTAS:,}" + ". Quita algun triple.")
            else:
                with st.spinner("Calculando reduccion al " + st.session_state.red_sel + "..."):
                    combinaciones = generar_combinaciones(st.session_state.signos)
                    apuestas = reducir_por_cobertura(combinaciones, int(st.session_state.red_sel))
                    if len(apuestas) > MAX_APUESTAS_FINALES:
                        apuestas = apuestas[:MAX_APUESTAS_FINALES]
                    st.session_state.apuestas_reducidas = apuestas
                    st.session_state.barita_quiniela = 0
                st.rerun()

    # ── RESULTADOS ──
    if st.session_state.apuestas_reducidas:
        st.markdown("---")

        # BARITA MAGICA
        st.markdown(
            "<div class='barita-magica-container'>"
            "<div class='barita-magica-titulo'>BARITA MAGICA</div>"
            "<div class='barita-magica-sub'>Pulsa para reducir el coste</div>"
            "</div>",
            unsafe_allow_html=True,
        )
        _, col_b, _ = st.columns([1, 2, 1])
        with col_b:
            if st.button("🪄 MAGIA 🪄", use_container_width=True, key="magia_q"):
                if len(st.session_state.apuestas_reducidas) > 1:
                    st.session_state.barita_quiniela += 1
                    st.rerun()

        apuestas_actuales = aplicar_barita_quiniela(
            st.session_state.apuestas_reducidas,
            st.session_state.barita_quiniela,
        )

        if st.session_state.barita_quiniela > 0:
            _, col_undo, _ = st.columns([1, 1, 1])
            with col_undo:
                if st.button("↩️ Deshacer magia", use_container_width=True, key="undo_q"):
                    st.session_state.barita_quiniela = max(0, st.session_state.barita_quiniela - 1)
                    st.rerun()

        n_ap = len(apuestas_actuales)
        coste = round(n_ap * PRECIO_QUINIELA, 2)

        st.markdown(
            "<div class='titulo-columnas'>" + f"{n_ap:,}" + " COLUMNAS · " + f"{coste:,.2f}" + " EUR</div>",
            unsafe_allow_html=True,
        )
        c1, c2 = st.columns(2)
        c1.metric("Apuestas", f"{n_ap:,}")
        c2.metric("Coste final", f"{coste:,.2f} EUR")

        # BOLETOS
        st.markdown("---")
        if n_ap > MAX_BOLETOS_VISUALES:
            st.info("Vista previa de las primeras " + str(MAX_BOLETOS_VISUALES) + " de " + f"{n_ap:,}")
            apuestas_mostrar = apuestas_actuales[:MAX_BOLETOS_VISUALES]
            n_mostrar = MAX_BOLETOS_VISUALES
        else:
            apuestas_mostrar = apuestas_actuales
            n_mostrar = n_ap

        BOLETOS_POR_PESTANA = 8
        numero_pestanas = (n_mostrar + BOLETOS_POR_PESTANA - 1) // BOLETOS_POR_PESTANA
        nombres = []
        for i in range(numero_pestanas):
            inicio = i * BOLETOS_POR_PESTANA + 1
            fin = min((i + 1) * BOLETOS_POR_PESTANA, n_mostrar)
            nombres.append("Boleto " + str(inicio) + "-" + str(fin))

        pestanas = st.tabs(nombres)
        for i, pestana in enumerate(pestanas):
            with pestana:
                inicio = i * BOLETOS_POR_PESTANA
                fin = min(inicio + BOLETOS_POR_PESTANA, n_mostrar)
                num_bol = fin - inicio
                cab = st.columns([0.5, 3, 1] + [0.6] * num_bol)
                cab[0].markdown("<div class='boletin-cab'>#</div>", unsafe_allow_html=True)
                cab[1].markdown("<div class='boletin-cab'>Partido</div>", unsafe_allow_html=True)
                cab[2].markdown("<div class='boletin-cab'>R.</div>", unsafe_allow_html=True)
                for j in range(num_bol):
                    cab[3 + j].markdown("<div class='boletin-cab'>B" + str(inicio + j + 1) + "</div>", unsafe_allow_html=True)
                for p in range(14):
                    local, visit, resultado = st.session_state.partidos_jornada[p]
                    fila = st.columns([0.5, 3, 1] + [0.6] * num_bol)
                    fila[0].markdown("<div class='num-partido'>" + str(p+1) + "</div>", unsafe_allow_html=True)
                    fila[1].markdown("<div class='nombre-partido'>" + str(local) + " - " + str(visit) + "</div>", unsafe_allow_html=True)
                    fila[2].markdown("<div class='resultado-oficial'>" + (resultado if resultado else "-") + "</div>", unsafe_allow_html=True)
                    for j in range(num_bol):
                        idx = inicio + j
                        if idx < fin:
                            signo = apuestas_mostrar[idx][p]
                            clase = "signo-1" if signo == "1" else ("signo-X" if signo == "X" else "signo-2")
                            fila[3 + j].markdown(
                                "<div style='text-align:center;padding-top:4px;'>"
                                "<span class='" + clase + " signo-celda'>" + signo + "</span>"
                                "</div>",
                                unsafe_allow_html=True,
                            )

        st.markdown("---")
        contenido = a_txt_quiniela(apuestas_actuales, st.session_state.pleno_local, st.session_state.pleno_visit)
        st.download_button(
            "Descargar txt (" + f"{n_ap:,}" + " apuestas)",
            data=contenido.encode("utf-8"),
            file_name="quiniela_reducida.txt",
            mime="text/plain",
            use_container_width=True,
            type="primary",
        )


# ═══════════════════════════════════════════════
# JORNADA ACTUAL / SIGUIENTE (igual que antes)
# ═══════════════════════════════════════════════
elif seccion == "Jornada actual":
    st.title("Jornada actual")
    if st.button("Refrescar", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    datos = obtener_jornada("latest")
    if datos and "error" not in datos:
        partidos, j, f = extraer_partidos(datos)
        c1, c2 = st.columns(2)
        c1.metric("Jornada", str(j) if j else "-")
        c2.metric("Fecha", str(f) if f else "-")
        if partidos:
            st.divider()
            for i, (loc, vis, sig) in enumerate(partidos[:14]):
                st.write("#" + str(i+1) + " - " + str(loc) + " vs " + str(vis) + " -> " + str(sig))
            if st.button("Cargar en Quiniela", use_container_width=True, type="primary"):
                st.session_state.partidos_jornada = partidos[:14]
                st.session_state.signos = ["1"] * 14
                st.session_state.apuestas_reducidas = None
                st.session_state.barita_quiniela = 0
                st.session_state.partidos_cargados = True
                st.success("Cargados.")
        else:
            with st.expander("Ver crudo"):
                st.json(datos)
    else:
        st.error("Error: " + str(datos.get("error", "desconocido")))


elif seccion == "Jornada siguiente":
    st.title("Jornada siguiente")
    if st.button("Refrescar", use_container_width=True, key="ref_next"):
        st.cache_data.clear()
        st.rerun()
    datos = obtener_jornada("next")
    if datos and "error" not in datos:
        partidos, j, f = extraer_partidos(datos)
        c1, c2 = st.columns(2)
        c1.metric("Jornada", str(j) if j else "-")
        c2.metric("Fecha", str(f) if f else "-")
        if partidos:
            st.divider()
            for i, (loc, vis, _) in enumerate(partidos[:14]):
                st.write("#" + str(i+1) + " - " + str(loc) + " vs " + str(vis))
            if st.button("Cargar en Quiniela", use_container_width=True, type="primary", key="load_next"):
                st.session_state.partidos_jornada = partidos[:14]
                st.session_state.signos = ["1"] * 14
                st.session_state.apuestas_reducidas = None
                st.session_state.barita_quiniela = 0
                st.session_state.partidos_cargados = True
                st.success("Cargados.")
        else:
            with st.expander("Ver crudo"):
                st.json(datos)
    else:
        st.error("Error: " + str(datos.get("error", "desconocido")))


# ═══════════════════════════════════════════════
# BONOLOTO (sin calculos hasta Generar)
# ═══════════════════════════════════════════════
elif seccion == "Bonoloto":
    st.title("Bonoloto")
    st.caption("Precio: " + str(PRECIO_BONOLOTO) + " EUR/apuesta")

    st.subheader("1. Numeros (1-49)")
    cols = st.columns(10)
    for n in range(1, 50):
        with cols[(n-1) % 10]:
            activo = n in st.session_state.bono_nums
            if st.button(str(n), key="bn" + str(n), use_container_width=True,
                         type="primary" if activo else "secondary"):
                if activo: st.session_state.bono_nums.remove(n)
                else: st.session_state.bono_nums.append(n)
                st.session_state.bono_combs = None
                st.session_state.bono_barita = 0
                st.rerun()

    st.caption("Seleccionados: **" + str(len(st.session_state.bono_nums)) + "**")
    c1, c2 = st.columns(2)
    if c1.button("Aleatorio", use_container_width=True):
        st.session_state.bono_nums = random.sample(range(1, 50), 6)
        st.session_state.bono_combs = None
        st.session_state.bono_barita = 0
        st.rerun()
    if c2.button("Limpiar", use_container_width=True):
        st.session_state.bono_nums = []
        st.session_state.bono_combs = None
        st.session_state.bono_barita = 0
        st.rerun()

    st.divider()

    if len(st.session_state.bono_nums) >= 6:
        if st.button("Generar combinaciones", type="primary", use_container_width=True, key="gen_bono"):
            combs = generar_bonoloto(st.session_state.bono_nums)
            st.session_state.bono_combs = combs
            st.session_state.bono_barita = 0
            st.rerun()

        if st.session_state.bono_combs:
            n_dir = len(st.session_state.bono_combs)
            st.caption("Combinaciones directas: **" + f"{n_dir:,}" + "**")

            st.markdown("---")
            st.markdown(
                "<div class='barita-magica-container'>"
                "<div class='barita-magica-titulo'>BARITA MAGICA</div>"
                "<div class='barita-magica-sub'>Pulsa para reducir el coste</div>"
                "</div>",
                unsafe_allow_html=True,
            )
            _, col_b, _ = st.columns([1, 2, 1])
            with col_b:
                if st.button("🪄 MAGIA 🪄", use_container_width=True, key="magia_b"):
                    if len(st.session_state.bono_combs) > 1:
                        st.session_state.bono_barita += 1
                        st.rerun()

            actuales = aplicar_barita_numeros(st.session_state.bono_combs, st.session_state.bono_barita)

            if st.session_state.bono_barita > 0:
                _, col_undo, _ = st.columns([1, 1, 1])
                with col_undo:
                    if st.button("↩️ Deshacer magia", use_container_width=True, key="undo_b"):
                        st.session_state.bono_barita = max(0, st.session_state.bono_barita - 1)
                        st.rerun()

            n_act = len(actuales)
            coste_act, aviso = coste_real(n_act, PRECIO_BONOLOTO, MIN_BONOLOTO)

            st.markdown(
                "<div class='titulo-columnas'>" + f"{n_act:,}" + " APUESTAS · " + f"{coste_act:,.2f}" + " EUR</div>",
                unsafe_allow_html=True,
            )
            c1, c2 = st.columns(2)
            c1.metric("Apuestas", f"{n_act:,}")
            c2.metric("Coste final", f"{coste_act:,.2f} EUR")
            if aviso:
                st.warning("Minimo oficial: " + str(MIN_BONOLOTO) + " apuestas")

            st.markdown("---")
            st.download_button("Descargar txt (" + f"{n_act:,}" + " apuestas)",
                               data=txt_loteria(actuales).encode("utf-8"),
                               file_name="bonoloto_reducida.txt", mime="text/plain",
                               use_container_width=True, type="primary")


# ═══════════════════════════════════════════════
# PRIMITIVA
# ═══════════════════════════════════════════════
elif seccion == "Primitiva":
    st.title("Primitiva")
    st.caption("Precio: " + str(PRECIO_PRIMITIVA) + " EUR/apuesta")

    st.subheader("1. Numeros (1-49)")
    cols = st.columns(10)
    for n in range(1, 50):
        with cols[(n-1) % 10]:
            activo = n in st.session_state.pri_nums
            if st.button(str(n), key="pn" + str(n), use_container_width=True,
                         type="primary" if activo else "secondary"):
                if activo: st.session_state.pri_nums.remove(n)
                else: st.session_state.pri_nums.append(n)
                st.session_state.pri_combs = None
                st.session_state.pri_barita = 0
                st.rerun()

    st.caption("Seleccionados: **" + str(len(st.session_state.pri_nums)) + "**")
    c1, c2 = st.columns(2)
    if c1.button("Aleatorio", use_container_width=True):
        st.session_state.pri_nums = random.sample(range(1, 50), 6)
        st.session_state.pri_combs = None
        st.session_state.pri_barita = 0
        st.rerun()
    if c2.button("Limpiar", use_container_width=True):
        st.session_state.pri_nums = []
        st.session_state.pri_combs = None
        st.session_state.pri_barita = 0
        st.rerun()

    st.divider()

    if len(st.session_state.pri_nums) >= 6:
        if st.button("Generar combinaciones", type="primary", use_container_width=True, key="gen_pri"):
            combs = generar_primitiva(st.session_state.pri_nums)
            st.session_state.pri_combs = combs
            st.session_state.pri_barita = 0
            st.rerun()

        if st.session_state.pri_combs:
            n_dir = len(st.session_state.pri_combs)
            st.caption("Combinaciones directas: **" + f"{n_dir:,}" + "**")

            st.markdown("---")
            st.markdown(
                "<div class='barita-magica-container'>"
                "<div class='barita-magica-titulo'>BARITA MAGICA</div>"
                "<div class='barita-magica-sub'>Pulsa para reducir el coste</div>"
                "</div>",
                unsafe_allow_html=True,
            )
            _, col_b, _ = st.columns([1, 2, 1])
            with col_b:
                if st.button("🪄 MAGIA 🪄", use_container_width=True, key="magia_p"):
                    if len(st.session_state.pri_combs) > 1:
                        st.session_state.pri_barita += 1
                        st.rerun()

            actuales = aplicar_barita_numeros(st.session_state.pri_combs, st.session_state.pri_barita)

            if st.session_state.pri_barita > 0:
                _, col_undo, _ = st.columns([1, 1, 1])
                with col_undo:
                    if st.button("↩️ Deshacer magia", use_container_width=True, key="undo_p"):
                        st.session_state.pri_barita = max(0, st.session_state.pri_barita - 1)
                        st.rerun()

            n_act = len(actuales)
            coste_act = round(n_act * PRECIO_PRIMITIVA, 2)

            st.markdown(
                "<div class='titulo-columnas'>" + f"{n_act:,}" + " APUESTAS · " + f"{coste_act:,.2f}" + " EUR</div>",
                unsafe_allow_html=True,
            )
            c1, c2 = st.columns(2)
            c1.metric("Apuestas", f"{n_act:,}")
            c2.metric("Coste final", f"{coste_act:,.2f} EUR")

            st.markdown("---")
            st.download_button("Descargar txt (" + f"{n_act:,}" + " apuestas)",
                               data=txt_loteria(actuales).encode("utf-8"),
                               file_name="primitiva_reducida.txt", mime="text/plain",
                               use_container_width=True, type="primary")


# ═══════════════════════════════════════════════
# EUROMILLONES
# ═══════════════════════════════════════════════
elif seccion == "Euromillones":
    st.title("Euromillones")
    st.caption("5 numeros (1-50) + 2 estrellas (1-12) - " + str(PRECIO_EUROMILLONES) + " EUR/apuesta")

    st.subheader("1. Numeros (1-50)")
    cols = st.columns(10)
    for n in range(1, 51):
        with cols[(n-1) % 10]:
            activo = n in st.session_state.eu_nums
            if st.button(str(n), key="en" + str(n), use_container_width=True,
                         type="primary" if activo else "secondary"):
                if activo: st.session_state.eu_nums.remove(n)
                else: st.session_state.eu_nums.append(n)
                st.session_state.eu_combs = None
                st.session_state.eu_barita = 0
                st.rerun()

    st.subheader("2. Estrellas (1-12)")
    cols_e = st.columns(12)
    for n in range(1, 13):
        with cols_e[n-1]:
            activo = n in st.session_state.eu_est
            if st.button("E" + str(n), key="ee" + str(n), use_container_width=True,
                         type="primary" if activo else "secondary"):
                if activo: st.session_state.eu_est.remove(n)
                else: st.session_state.eu_est.append(n)
                st.session_state.eu_combs = None
                st.session_state.eu_barita = 0
                st.rerun()

    st.caption("Numeros: **" + str(len(st.session_state.eu_nums)) + "** · Estrellas: **" + str(len(st.session_state.eu_est)) + "**")
    c1, c2 = st.columns(2)
    if c1.button("Aleatorio", use_container_width=True, key="rand_eu"):
        st.session_state.eu_nums = random.sample(range(1, 51), 5)
        st.session_state.eu_est = random.sample(range(1, 13), 2)
        st.session_state.eu_combs = None
        st.session_state.eu_barita = 0
        st.rerun()
    if c2.button("Limpiar", use_container_width=True, key="clear_eu"):
        st.session_state.eu_nums = []
        st.session_state.eu_est = []
        st.session_state.eu_combs = None
        st.session_state.eu_barita = 0
        st.rerun()

    st.divider()

    if len(st.session_state.eu_nums) >= 5 and len(st.session_state.eu_est) >= 2:
        if st.button("Generar combinaciones", type="primary", use_container_width=True, key="gen_eu"):
            combs = generar_euromillones(st.session_state.eu_nums, st.session_state.eu_est)
            st.session_state.eu_combs = combs
            st.session_state.eu_barita = 0
            st.rerun()

        if st.session_state.eu_combs:
            n_dir = len(st.session_state.eu_combs)
            st.caption("Combinaciones directas: **" + f"{n_dir:,}" + "**")

            st.markdown("---")
            st.markdown(
                "<div class='barita-magica-container'>"
                "<div class='barita-magica-titulo'>BARITA MAGICA</div>"
                "<div class='barita-magica-sub'>Pulsa para reducir el coste</div>"
                "</div>",
                unsafe_allow_html=True,
            )
            _, col_b, _ = st.columns([1, 2, 1])
            with col_b:
                if st.button("🪄 MAGIA 🪄", use_container_width=True, key="magia_e"):
                    if len(st.session_state.eu_combs) > 1:
                        st.session_state.eu_barita += 1
                        st.rerun()

            actuales = aplicar_barita_numeros(st.session_state.eu_combs, st.session_state.eu_barita)

            if st.session_state.eu_barita > 0:
                _, col_undo, _ = st.columns([1, 1, 1])
                with col_undo:
                    if st.button("↩️ Deshacer magia", use_container_width=True, key="undo_e"):
                        st.session_state.eu_barita = max(0, st.session_state.eu_barita - 1)
                        st.rerun()

            n_act = len(actuales)
            coste_act = round(n_act * PRECIO_EUROMILLONES, 2)

            st.markdown(
                "<div class='titulo-columnas'>" + f"{n_act:,}" + " APUESTAS · " + f"{coste_act:,.2f}" + " EUR</div>",
                unsafe_allow_html=True,
            )
            c1, c2 = st.columns(2)
            c1.metric("Apuestas", f"{n_act:,}")
            c2.metric("Coste final", f"{coste_act:,.2f} EUR")

            st.markdown("---")
            st.download_button("Descargar txt (" + f"{n_act:,}" + " apuestas)",
                               data=txt_loteria(actuales).encode("utf-8"),
                               file_name="euromillones_reducida.txt", mime="text/plain",
                               use_container_width=True, type="primary")


# ═══════════════════════════════════════════════
# CUENTA
# ═══════════════════════════════════════════════
elif seccion == "Cuenta":
    st.title("Cuenta")
    st.write("**Plan:** Free (demo)")
    if st.button("Cerrar sesion", use_container_width=True):
        st.session_state.autenticado = False
        st.rerun()
