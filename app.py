# ══════════════════════════════════════════════════════════════
# QUINILOTO MAGIC - v12
# API LoteriaAPI + Reduccion libre 13/12/11/10 + Barita Magica
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

PLENO_OPCIONES = ["0", "1", "2", "M"]

BARITA_DEFAULT = [
    {"id": 1, "nombre": "Poda basica",      "factor": 0.75},
    {"id": 2, "nombre": "Filtro historico", "factor": 0.70},
    {"id": 3, "nombre": "Equilibrio",       "factor": 0.60},
    {"id": 4, "nombre": "Seleccion elite",  "factor": 0.55},
]

EQUIPOS_DEFAULT = {
    "Real Madrid":    {"ataque": 2.10, "defensa": 0.80},
    "Barcelona":      {"ataque": 1.95, "defensa": 0.90},
    "Atletico":       {"ataque": 1.50, "defensa": 0.70},
    "Sevilla":        {"ataque": 1.40, "defensa": 1.00},
    "Valencia":       {"ataque": 1.30, "defensa": 1.10},
    "Betis":          {"ataque": 1.40, "defensa": 1.00},
    "Villarreal":     {"ataque": 1.50, "defensa": 0.90},
    "Athletic":       {"ataque": 1.20, "defensa": 0.90},
    "Real Sociedad":  {"ataque": 1.30, "defensa": 0.90},
    "Girona":         {"ataque": 1.60, "defensa": 1.00},
    "Osasuna":        {"ataque": 1.10, "defensa": 1.00},
    "Celta":          {"ataque": 1.20, "defensa": 1.10},
    "Rayo":           {"ataque": 1.10, "defensa": 1.00},
    "Mallorca":       {"ataque": 1.00, "defensa": 0.95},
    "Getafe":         {"ataque": 0.95, "defensa": 0.90},
    "Alaves":         {"ataque": 1.05, "defensa": 1.00},
    "Las Palmas":     {"ataque": 1.10, "defensa": 1.15},
    "Espanyol":       {"ataque": 1.00, "defensa": 1.05},
    "Leganes":        {"ataque": 0.90, "defensa": 1.00},
    "Valladolid":     {"ataque": 0.85, "defensa": 1.20},
}

# ─────────────────────────────────────────────────
# CSS NEON
# ─────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
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
.tabla-header {
    background: linear-gradient(180deg, rgba(255, 215, 0, 0.15) 0%, rgba(255, 165, 0, 0.05) 100%);
    border-bottom: 2px solid rgba(255, 215, 0, 0.4);
    padding: 8px 4px;
    color: #FFD700;
    font-weight: 700;
    text-align: center;
    font-size: 12px;
    text-shadow: 0 0 6px rgba(255, 215, 0, 0.5);
}
.num-partido { color: #FFD700; font-weight: 700; font-size: 14px; text-align: center; padding-top: 6px; }
.nombre-partido { color: #ffffff; font-weight: 500; font-size: 13px; padding-top: 6px; }
.resultado-oficial { color: #a0a0b8; font-size: 12px; text-align: center; padding-top: 8px; }
.boletin-cab {
    background: linear-gradient(180deg, rgba(255, 215, 0, 0.3) 0%, rgba(255, 165, 0, 0.15) 100%);
    color: #FFD700; text-align: center; font-weight: 700; font-size: 11px;
    padding: 6px 2px; border-radius: 4px; text-shadow: 0 0 6px rgba(255, 215, 0, 0.6);
}
.signo-celda {
    display: inline-block; padding: 4px 8px; border-radius: 4px;
    font-weight: 800; font-size: 12px; min-width: 22px; text-align: center;
}
.signo-1 { background: #22c55e; color: white; box-shadow: 0 0 8px rgba(34,197,94,0.6); }
.signo-X { background: #eab308; color: white; box-shadow: 0 0 8px rgba(234,179,8,0.6); }
.signo-2 { background: #ef4444; color: white; box-shadow: 0 0 8px rgba(239,68,68,0.6); }
.titulo-seccion-dorado {
    color: #FFD700; font-weight: 800; letter-spacing: 1px;
    text-shadow: 0 0 12px rgba(255, 215, 0, 0.6);
}
.titulo-columnas {
    text-align: center; color: #FFD700; font-weight: 800; font-size: 20px;
    text-shadow: 0 0 20px rgba(255, 215, 0, 0.7); padding: 12px 0;
}
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# API LOTERIAAPI
# ═══════════════════════════════════════════════
def _get_api_key():
    try:
        return st.secrets.get("API_KEY_LOTERIAS", "")
    except Exception:
        return ""


@st.cache_data(ttl=1800)
def obtener_jornada(endpoint):
    """endpoint = 'latest' o 'next'"""
    key = _get_api_key()
    if not key:
        return {"error": "API_KEY_LOTERIAS no configurada en Secrets."}
    try:
        url = "https://api.loteriasapi.com/api/v1/results/quiniela/" + endpoint
        r = requests.get(url, headers={"X-API-Key": key}, timeout=15)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}


def extraer_partidos(datos):
    """Extrae partidos de la respuesta JSON de forma flexible."""
    partidos = []
    jornada_num = None
    fecha = None

    if not isinstance(datos, dict):
        return partidos, jornada_num, fecha

    # Buscar campos de jornada y fecha en cualquier nivel
    jornada_num = (
        datos.get("jornada") or datos.get("matchday") or datos.get("numero")
        or datos.get("num_jornada")
    )
    fecha = (
        datos.get("fecha") or datos.get("draw_date")
        or datos.get("fecha_sorteo") or datos.get("date")
    )

    # Buscar lista de partidos en cualquier clave conocida
    candidatos = ["resultados", "matches", "partidos", "games", "fixtures", "data"]
    lista = None
    for k in candidatos:
        if k in datos and isinstance(datos[k], list):
            lista = datos[k]
            break

    if lista is None:
        # Si el propio dict es la jornada, buscar en sub-claves
        for v in datos.values():
            if isinstance(v, dict):
                sub_partidos, sub_j, sub_f = extraer_partidos(v)
                if sub_partidos:
                    return sub_partidos, sub_j, sub_f

    if lista:
        for r in lista:
            if not isinstance(r, dict):
                continue
            local = (r.get("local") or r.get("home") or r.get("equipo_local")
                     or r.get("team1") or r.get("local_team") or "-")
            visit = (r.get("visitante") or r.get("away") or r.get("equipo_visitante")
                     or r.get("team2") or r.get("visit_team") or "-")
            signo = (r.get("signo") or r.get("result") or r.get("sign")
                     or r.get("resultado") or "")
            partidos.append((local, visit, signo))

    return partidos, jornada_num, fecha


# ═══════════════════════════════════════════════
# LOGICA QUINIELA
# ═══════════════════════════════════════════════
def generar_combinaciones(signos):
    return list(itertools.product(*[list(s) for s in signos]))


def contar_dobles_triples(signos):
    dobles = sum(1 for s in signos if len(s) == 2)
    triples = sum(1 for s in signos if len(s) == 3)
    return dobles, triples


def ordenar_signos(s):
    return "".join(sorted(set(s), key=lambda x: ["1", "X", "2"].index(x)))


def distancia_hamming(a, b):
    return sum(1 for x, y in zip(a, b) if x != y)


def reducir_por_cobertura(combinaciones, garantia, objetivo=None):
    """
    Reduccion aproximada por cobertura de Hamming.
    garantia: 13, 12, 11 o 10.
    objetivo: numero maximo de columnas a devolver.
    """
    n_total = len(combinaciones)
    if n_total == 0:
        return []

    max_dist = 14 - garantia

    # Objetivo de columnas segun garantia (basado en ratios empiricos)
    if objetivo is None:
        ratios = {13: 0.0625, 12: 0.0150, 11: 0.0030, 10: 0.0008}
        objetivo = max(MIN_QUINIELA, int(n_total * ratios.get(garantia, 0.01)))

    # Si el objetivo cubre todo, devolvemos todo
    if objetivo >= n_total:
        return ["".join(c) for c in combinaciones]

    combos = [tuple(c) for c in combinaciones]

    # Greedy: seleccionar combinaciones que cubran mas no-cubiertas
    random.seed(42)
    cubiertas = set()
    seleccionadas = []
    indices_disponibles = list(range(n_total))
    random.shuffle(indices_disponibles)

    for _ in range(objetivo):
        mejor_idx = None
        mejor_cobertura = -1

        for idx in indices_disponibles:
            if idx in cubiertas:
                continue
            c = combos[idx]
            cubre = 0
            for j, otra in enumerate(combos):
                if j in cubiertas:
                    continue
                if distancia_hamming(c, otra) <= max_dist:
                    cubre += 1
            if cubre > mejor_cobertura:
                mejor_cobertura = cubre
                mejor_idx = idx

        if mejor_idx is None:
            break

        seleccionadas.append(combos[mejor_idx])
        c = combos[mejor_idx]
        for j, otra in enumerate(combos):
            if j not in cubiertas and distancia_hamming(c, otra) <= max_dist:
                cubiertas.add(j)

        if len(cubiertas) >= n_total:
            break

    return ["".join(c) for c in seleccionadas]


def a_txt_quiniela(apuestas, pleno_local, pleno_visit):
    lineas = list(apuestas)
    if pleno_local and pleno_visit:
        lineas.append(str(pleno_local) + str(pleno_visit))
    return "\n".join(lineas)


# ═══════════════════════════════════════════════
# LOGICA POISSON
# ═══════════════════════════════════════════════
def poisson(k, lam):
    return (lam ** k) * math.exp(-lam) / math.factorial(k)


def predecir_1x2(lam_l, lam_v, max_g=10):
    p1 = pX = p2 = 0.0
    for gl in range(max_g + 1):
        for gv in range(max_g + 1):
            p = poisson(gl, lam_l) * poisson(gv, lam_v)
            if gl > gv: p1 += p
            elif gl == gv: pX += p
            else: p2 += p
    return {"1": round(p1*100, 1), "X": round(pX*100, 1), "2": round(p2*100, 1)}


def predecir_pleno(lam_l, lam_v, max_g=10):
    p_local = {"0": 0.0, "1": 0.0, "2": 0.0, "M": 0.0}
    p_visit = {"0": 0.0, "1": 0.0, "2": 0.0, "M": 0.0}
    for g in range(max_g + 1):
        p = poisson(g, lam_l)
        if g >= 3: p_local["M"] += p
        else: p_local[str(g)] += p
        p = poisson(g, lam_v)
        if g >= 3: p_visit["M"] += p
        else: p_visit[str(g)] += p
    return {
        "local": {k: round(v * 100, 1) for k, v in p_local.items()},
        "visitante": {k: round(v * 100, 1) for k, v in p_visit.items()},
    }


def estimar_lambdas(local, visitante, equipos):
    L = equipos.get(local, {"ataque": 1.3, "defensa": 1.0})
    V = equipos.get(visitante, {"ataque": 1.3, "defensa": 1.0})
    return round(L["ataque"] * V["defensa"] * 1.15, 2), round(V["ataque"] * L["defensa"] * 0.85, 2)


# ═══════════════════════════════════════════════
# LOGICA LOTERIAS
# ═══════════════════════════════════════════════
def generar_bonoloto(numeros):
    return list(itertools.combinations(sorted(numeros), 6)) if len(numeros) >= 6 else []


def generar_primitiva(numeros):
    return list(itertools.combinations(sorted(numeros), 6)) if len(numeros) >= 6 else []


def generar_euromillones(numeros, estrellas):
    if len(numeros) < 5 or len(estrellas) < 2: return []
    cn = list(itertools.combinations(sorted(numeros), 5))
    ce = list(itertools.combinations(sorted(estrellas), 2))
    return [(n, e) for n in cn for e in ce]


def barita_loteria(combinaciones, nivel, factores, min_ap):
    if nivel < 1 or nivel > len(factores):
        return combinaciones
    factor = factores[nivel - 1]
    n = max(min_ap, int(len(combinaciones) * factor))
    def score(c):
        nums = c[0] if (isinstance(c, tuple) and len(c) == 2 and isinstance(c[0], tuple)) else c
        suma = sum(nums)
        pares = sum(1 for x in nums if x % 2 == 0)
        return abs(suma - 125) + abs(pares - len(nums)//2) * 5
    return sorted(combinaciones, key=score)[:n]


def baritas_loteria(combinaciones, niveles, factores, min_ap):
    res = list(combinaciones)
    for n in niveles:
        res = barita_loteria(res, n, factores, min_ap)
    return res


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
        "font-size:52px;font-weight:800;letter-spacing:-2px;"
        "color:#FFD700;text-shadow:0 0 30px rgba(255,215,0,0.6);"
        "margin-top:15vh;margin-bottom:0;'>QUINILOTO</h1>"
        "<h2 style='text-align:center;font-family:Inter,sans-serif;"
        "font-size:32px;font-weight:700;letter-spacing:14px;"
        "color:#FFD700;text-shadow:0 0 20px rgba(255,215,0,0.5);"
        "margin-top:0;'>MAGIC</h2>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:center;color:#a0a0b8;font-size:14px;'>Acceso privado</p>",
        unsafe_allow_html=True,
    )
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
if "signos" not in st.session_state:
    st.session_state.signos = ["1"] * 14
if "pleno_local" not in st.session_state:
    st.session_state.pleno_local = "1"
if "pleno_visit" not in st.session_state:
    st.session_state.pleno_visit = "0"
if "apuestas_reducidas" not in st.session_state:
    st.session_state.apuestas_reducidas = None
if "baritas" not in st.session_state:
    st.session_state.baritas = []
if "equipos" not in st.session_state:
    st.session_state.equipos = dict(EQUIPOS_DEFAULT)
if "partidos_jornada" not in st.session_state:
    st.session_state.partidos_jornada = [
        ("Equipo 1 L", "Equipo 1 V", ""),
        ("Equipo 2 L", "Equipo 2 V", ""),
        ("Equipo 3 L", "Equipo 3 V", ""),
        ("Equipo 4 L", "Equipo 4 V", ""),
        ("Equipo 5 L", "Equipo 5 V", ""),
        ("Equipo 6 L", "Equipo 6 V", ""),
        ("Equipo 7 L", "Equipo 7 V", ""),
        ("Equipo 8 L", "Equipo 8 V", ""),
        ("Equipo 9 L", "Equipo 9 V", ""),
        ("Equipo 10 L", "Equipo 10 V", ""),
        ("Equipo 11 L", "Equipo 11 V", ""),
        ("Equipo 12 L", "Equipo 12 V", ""),
        ("Equipo 13 L", "Equipo 13 V", ""),
        ("Equipo 14 L", "Equipo 14 V", ""),
    ]
if "pleno_partido" not in st.session_state:
    st.session_state.pleno_partido = ("Local 15", "Visitante 15", "")
if "red_sel" not in st.session_state:
    st.session_state.red_sel = "13"
if "barita_factores" not in st.session_state:
    st.session_state.barita_factores = {
        "quiniela":    [0.75, 0.70, 0.60, 0.55],
        "bonoloto":    [0.75, 0.70, 0.60, 0.55],
        "primitiva":   [0.75, 0.70, 0.60, 0.55],
        "euromillones":[0.75, 0.70, 0.60, 0.55],
    }
# Auto-cargar jornada actual si no hay partidos reales
if "partidos_cargados" not in st.session_state:
    st.session_state.partidos_cargados = False

if not st.session_state.partidos_cargados:
    try:
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
        "font-size:30px;font-weight:800;letter-spacing:-1px;"
        "color:#FFD700;text-shadow:0 0 20px rgba(255,215,0,0.6);"
        "margin-bottom:0;'>QUINILOTO</h1>"
        "<h2 style='text-align:center;font-family:Inter,sans-serif;"
        "font-size:22px;font-weight:700;letter-spacing:10px;"
        "color:#FFD700;text-shadow:0 0 15px rgba(255,215,0,0.5);"
        "margin-top:0;margin-bottom:25px;'>MAGIC</h2>",
        unsafe_allow_html=True,
    )
    st.markdown("---")
    seccion = st.radio(
        "Seccion",
        [
            "Inicio",
            "Jornada actual",
            "Jornada siguiente",
            "Quiniela",
            "Bonoloto",
            "Primitiva",
            "Euromillones",
            "Configurar Barita",
            "Cuenta",
        ],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.caption("Precios oficiales:")
    st.caption("Quiniela: " + str(PRECIO_QUINIELA) + " EUR")
    st.caption("Bonoloto: " + str(PRECIO_BONOLOTO) + " EUR")
    st.caption("Primitiva: " + str(PRECIO_PRIMITIVA) + " EUR")
    st.caption("Euromillones: " + str(PRECIO_EUROMILLONES) + " EUR")
    if st.button("Cerrar sesion", use_container_width=True):
        st.session_state.autenticado = False
        st.rerun()


# ═══════════════════════════════════════════════
# INICIO
# ═══════════════════════════════════════════════
if seccion == "Inicio":
    st.markdown(
        "<h1 style='text-align:center;font-family:Inter,sans-serif;"
        "font-size:48px;font-weight:800;letter-spacing:-2px;"
        "color:#FFD700;text-shadow:0 0 40px rgba(255,215,0,0.6);"
        "margin-bottom:0;'>QUINILOTO MAGIC</h1>"
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
# JORNADA ACTUAL
# ═══════════════════════════════════════════════
elif seccion == "Jornada actual":
    st.title("Jornada actual")
    st.caption("Partidos con resultados oficiales desde LoteriaAPI.")

    if st.button("Refrescar datos", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    with st.spinner("Consultando jornada actual..."):
        datos = obtener_jornada("latest")

    if datos and "error" not in datos:
        partidos, jornada_num, fecha = extraer_partidos(datos)

        c1, c2 = st.columns(2)
        c1.metric("Jornada", str(jornada_num) if jornada_num else "-")
        c2.metric("Fecha", str(fecha) if fecha else "-")

        if partidos:
            st.divider()
            st.subheader("Partidos")

            for i, (loc, vis, sig) in enumerate(partidos[:14]):
                cols = st.columns([0.5, 3, 1, 3])
                cols[0].markdown("**" + str(i+1) + "**")
                cols[1].markdown(str(loc))
                cols[2].markdown("**" + str(sig) + "**" if sig else "-")
                cols[3].markdown(str(vis))

            st.divider()
            if st.button("Cargar en Quiniela", use_container_width=True, type="primary"):
                st.session_state.partidos_jornada = partidos[:14]
                st.session_state.signos = ["1"] * 14
                st.session_state.apuestas_reducidas = None
                st.session_state.baritas = []
                st.success("Cargados " + str(len(partidos)) + " partidos. Ve a Quiniela.")
        else:
            st.warning("No se han podido extraer partidos de la respuesta.")
            with st.expander("Ver respuesta cruda de la API"):
                st.json(datos)
    else:
        st.error("Error de API: " + str(datos.get("error", "desconocido")))
        st.info("Verifica que API_KEY_LOTERIAS esta bien configurada en Secrets.")


# ═══════════════════════════════════════════════
# JORNADA SIGUIENTE
# ═══════════════════════════════════════════════
elif seccion == "Jornada siguiente":
    st.title("Jornada siguiente")
    st.caption("Partidos programados para la proxima jornada.")

    if st.button("Refrescar datos", use_container_width=True, key="ref_next"):
        st.cache_data.clear()
        st.rerun()

    with st.spinner("Consultando proxima jornada..."):
        datos = obtener_jornada("next")

    if datos and "error" not in datos:
        partidos, jornada_num, fecha = extraer_partidos(datos)

        c1, c2 = st.columns(2)
        c1.metric("Jornada", str(jornada_num) if jornada_num else "-")
        c2.metric("Fecha", str(fecha) if fecha else "-")

        if partidos:
            st.divider()
            st.subheader("Partidos")

            for i, (loc, vis, _) in enumerate(partidos[:14]):
                cols = st.columns([0.5, 5, 5])
                cols[0].markdown("**" + str(i+1) + "**")
                cols[1].markdown(str(loc))
                cols[2].markdown(str(vis))

            st.divider()
            if st.button("Cargar en Quiniela", use_container_width=True, type="primary", key="load_next"):
                st.session_state.partidos_jornada = partidos[:14]
                st.session_state.signos = ["1"] * 14
                st.session_state.apuestas_reducidas = None
                st.session_state.baritas = []
                st.success("Cargados " + str(len(partidos)) + " partidos. Ve a Quiniela.")
        else:
            st.warning("No se han podido extraer partidos de la respuesta.")
            with st.expander("Ver respuesta cruda de la API"):
                st.json(datos)
    else:
        st.error("Error de API: " + str(datos.get("error", "desconocido")))
        st.info("Es posible que la proxima jornada aun no este disponible.")


# ═══════════════════════════════════════════════
# QUINIELA
# ═══════════════════════════════════════════════
elif seccion == "Quiniela":
    st.title("Calculo de reducciones para la Quiniela")
    st.caption("Introduce los partidos, marca dobles/triples, elige reduccion y genera las apuestas.")

    # ── 1. CONFIGURAR PARTIDOS (editables) ──
    st.subheader("1. Configura los partidos")
    st.caption("Edita los equipos y marca 1-X-2. Varios por partido = doble o triple.")

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
                if st.button(
                    signo,
                    key="q_" + str(i) + "_" + signo,
                    use_container_width=True,
                    type="primary" if activo else "secondary",
                ):
                    actual = st.session_state.signos[i]
                    if signo in actual:
                        nuevo = actual.replace(signo, "")
                        if nuevo == "":
                            nuevo = "1"
                        st.session_state.signos[i] = nuevo
                    else:
                        st.session_state.signos[i] = ordenar_signos(actual + signo)
                    st.rerun()

    # ── 2. PLENO AL 15 ──
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
            if st.button(
                "L:" + signo,
                key="pl_loc_" + signo,
                use_container_width=True,
                type="primary" if activo else "secondary",
            ):
                st.session_state.pleno_local = signo
                st.rerun()

    st.caption("Goles VISITANTE:")
    p_vis_cols = st.columns(4)
    for j, signo in enumerate(PLENO_OPCIONES):
        with p_vis_cols[j]:
            activo = signo == st.session_state.pleno_visit
            if st.button(
                "V:" + signo,
                key="pl_vis_" + signo,
                use_container_width=True,
                type="primary" if activo else "secondary",
            ):
                st.session_state.pleno_visit = signo
                st.rerun()

    # ── 3. RESUMEN ──
    st.markdown("---")
    dobles, triples = contar_dobles_triples(st.session_state.signos)
    apuestas_directas = 2 ** dobles * 3 ** triples

    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Triples", str(triples))
    r2.metric("Dobles", str(dobles))
    r3.metric("Apuestas directas", str(apuestas_directas))
    r4.metric("Coste directo", str(round(apuestas_directas * PRECIO_QUINIELA, 2)) + " EUR")

    # ── 4. REDUCCION ──
    st.markdown("---")
    st.markdown("<div class='titulo-seccion-dorado'>SELECCIONAR REDUCCION</div>", unsafe_allow_html=True)

    c_red = st.columns(4)
    for i, (valor, label) in enumerate([
        ("13", "Reduccion al 13"),
        ("12", "Reduccion al 12"),
        ("11", "Reduccion al 11"),
        ("10", "Reduccion al 10"),
    ]):
        with c_red[i]:
            activo = st.session_state.red_sel == valor
            if st.button(
                label,
                key="red_" + valor,
                use_container_width=True,
                type="primary" if activo else "secondary",
            ):
                st.session_state.red_sel = valor
                st.rerun()

    # ── 5. BOTONES ACCION ──
    st.markdown("---")
    b1, b2 = st.columns(2)
    with b1:
        if st.button("Borrar seleccion", use_container_width=True):
            st.session_state.signos = ["1"] * 14
            st.session_state.pleno_local = "1"
            st.session_state.pleno_visit = "0"
            st.session_state.apuestas_reducidas = None
            st.session_state.baritas = []
            st.rerun()
    with b2:
        if st.button("Generar reduccion", type="primary", use_container_width=True):
            if apuestas_directas == 1:
                st.warning("Marca al menos un doble o un triple para que la reduccion tenga sentido.")
            else:
                with st.spinner("Calculando reduccion al " + st.session_state.red_sel + "..."):
                    combinaciones = generar_combinaciones(st.session_state.signos)
                    apuestas = reducir_por_cobertura(
                        combinaciones,
                        int(st.session_state.red_sel),
                    )
                    st.session_state.apuestas_reducidas = apuestas
                    st.session_state.baritas = []
                st.rerun()

    # ── 6. RESULTADOS ──
    if st.session_state.apuestas_reducidas:
        st.markdown("---")
        apuestas_actuales = list(st.session_state.apuestas_reducidas)

        # Aplicar baritas
        if st.session_state.baritas:
            factor = 1.0
            for capa_id in st.session_state.baritas:
                factor *= st.session_state.barita_factores["quiniela"][capa_id - 1]
            n_mantener = max(MIN_QUINIELA, int(len(apuestas_actuales) * factor))
            apuestas_actuales = apuestas_actuales[:n_mantener]

        n_ap = len(apuestas_actuales)
        coste = round(n_ap * PRECIO_QUINIELA, 2)

        st.markdown(
            "<div class='titulo-columnas'>" + str(n_ap) + " COLUMNAS QUE FORMAN LA REDUCCION SELECCIONADA</div>",
            unsafe_allow_html=True,
        )

        c1, c2 = st.columns(2)
        c1.metric("Apuestas finales", str(n_ap))
        c2.metric("Coste final", str(coste) + " EUR")

        st.markdown("<div class='titulo-seccion-dorado'>BARITA MAGICA</div>", unsafe_allow_html=True)
        cols_b = st.columns(4)
        for idx, capa in enumerate(BARITA_DEFAULT):
            with cols_b[idx]:
                usada = capa["id"] in st.session_state.baritas
                pct = int(st.session_state.barita_factores["quiniela"][idx] * 100)
                label = capa["nombre"] + " (" + str(pct) + "%)"
                if st.button(label, key="b" + str(capa["id"]), use_container_width=True, disabled=usada,
                             type="primary" if usada else "secondary"):
                    st.session_state.baritas.append(capa["id"])
                    st.rerun()

        if st.session_state.baritas:
            if st.button("Deshacer ultima barita", use_container_width=True):
                st.session_state.baritas.pop()
                st.rerun()

        # ── BOLETOS VISUALES ──
        st.markdown("---")
        BOLETOS_POR_PESTANA = 8
        numero_pestanas = (n_ap + BOLETOS_POR_PESTANA - 1) // BOLETOS_POR_PESTANA

        nombres = []
        for i in range(numero_pestanas):
            inicio = i * BOLETOS_POR_PESTANA + 1
            fin = min((i + 1) * BOLETOS_POR_PESTANA, n_ap)
            nombres.append("Boleto " + str(inicio) + "-" + str(fin))

        pestanas = st.tabs(nombres)

        for i, pestana in enumerate(pestanas):
            with pestana:
                inicio = i * BOLETOS_POR_PESTANA
                fin = min(inicio + BOLETOS_POR_PESTANA, n_ap)
                num_bol = fin - inicio

                cab = st.columns([0.5, 3, 1] + [0.6] * num_bol)
                cab[0].markdown("<div class='boletin-cab'>#</div>", unsafe_allow_html=True)
                cab[1].markdown("<div class='boletin-cab' style='text-align:left;padding-left:8px;'>Partido</div>", unsafe_allow_html=True)
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
                            signo = apuestas_actuales[idx][p]
                            clase = "signo-1" if signo == "1" else ("signo-X" if signo == "X" else "signo-2")
                            fila[3 + j].markdown(
                                "<div style='text-align:center;padding-top:4px;'>"
                                "<span class='" + clase + " signo-celda'>" + signo + "</span>"
                                "</div>",
                                unsafe_allow_html=True,
                            )

        # ── DESCARGAR ──
        st.markdown("---")
        st.markdown("<div class='titulo-seccion-dorado'>DESCARGAR</div>", unsafe_allow_html=True)
        contenido = a_txt_quiniela(apuestas_actuales, st.session_state.pleno_local, st.session_state.pleno_visit)
        st.download_button(
            "Descargar txt",
            data=contenido.encode("utf-8"),
            file_name="quiniela_reducida.txt",
            mime="text/plain",
            use_container_width=True,
            type="primary",
        )


# ═══════════════════════════════════════════════
# BONOLOTO
# ═══════════════════════════════════════════════
elif seccion == "Bonoloto":
    st.title("Bonoloto")
    st.caption("Precio: " + str(PRECIO_BONOLOTO) + " EUR/apuesta - Minimo " + str(MIN_BONOLOTO) + " apuestas")

    if "bono_nums" not in st.session_state: st.session_state.bono_nums = []
    if "bono_combs" not in st.session_state: st.session_state.bono_combs = None
    if "bono_baritas" not in st.session_state: st.session_state.bono_baritas = []

    st.subheader("1. Selecciona numeros (1-49)")
    cols = st.columns(10)
    for n in range(1, 50):
        with cols[(n-1) % 10]:
            activo = n in st.session_state.bono_nums
            if st.button(str(n), key="bn" + str(n), use_container_width=True,
                         type="primary" if activo else "secondary"):
                if activo: st.session_state.bono_nums.remove(n)
                else: st.session_state.bono_nums.append(n)
                st.rerun()

    st.caption("Seleccionados: " + str(len(st.session_state.bono_nums)) + " -> " + str(sorted(st.session_state.bono_nums)))

    c1, c2 = st.columns(2)
    if c1.button("Aleatorio", use_container_width=True):
        st.session_state.bono_nums = random.sample(range(1, 50), 6)
        st.rerun()
    if c2.button("Limpiar", use_container_width=True):
        st.session_state.bono_nums = []
        st.session_state.bono_combs = None
        st.session_state.bono_baritas = []
        st.rerun()

    st.divider()

    if len(st.session_state.bono_nums) >= 6:
        combs = generar_bonoloto(st.session_state.bono_nums)
        n_ap = len(combs)
        coste_dir, aviso_dir = coste_real(n_ap, PRECIO_BONOLOTO, MIN_BONOLOTO)

        st.subheader("2. Coste directo")
        c1, c2 = st.columns(2)
        c1.metric("Apuestas", str(n_ap))
        c2.metric("Coste", str(coste_dir) + " EUR")
        if aviso_dir:
            st.warning("Minimo: " + str(MIN_BONOLOTO) + " apuestas")

        if st.button("Generar", type="primary", use_container_width=True):
            st.session_state.bono_combs = combs
            st.session_state.bono_baritas = []
            st.rerun()

        if st.session_state.bono_combs:
            st.divider()
            st.subheader("3. Barita Magica")
            factores = st.session_state.barita_factores["bonoloto"]
            actuales = baritas_loteria(st.session_state.bono_combs, st.session_state.bono_baritas, factores, MIN_BONOLOTO)
            n_act = len(actuales)
            coste_act, aviso = coste_real(n_act, PRECIO_BONOLOTO, MIN_BONOLOTO)

            c1, c2 = st.columns(2)
            c1.metric("Apuestas", str(n_act))
            c2.metric("Coste", str(coste_act) + " EUR")
            if aviso:
                st.warning("Minimo: " + str(MIN_BONOLOTO) + " apuestas")

            cols_b = st.columns(4)
            for idx, capa in enumerate(BARITA_DEFAULT):
                with cols_b[idx]:
                    usada = capa["id"] in st.session_state.bono_baritas
                    pct = int(factores[idx] * 100)
                    label = capa["nombre"] + " (" + str(pct) + "%)"
                    if st.button(label, key="bb" + str(capa["id"]), use_container_width=True, disabled=usada,
                                 type="primary" if usada else "secondary"):
                        st.session_state.bono_baritas.append(capa["id"])
                        st.rerun()

            if st.session_state.bono_baritas:
                if st.button("Deshacer", use_container_width=True, key="undo_bono"):
                    st.session_state.bono_baritas.pop()
                    st.rerun()

            st.download_button("Descargar txt", data=txt_loteria(actuales).encode("utf-8"),
                               file_name="bonoloto_reducida.txt", mime="text/plain",
                               use_container_width=True, type="primary")


# ═══════════════════════════════════════════════
# PRIMITIVA
# ═══════════════════════════════════════════════
elif seccion == "Primitiva":
    st.title("Primitiva")
    st.caption("Precio: " + str(PRECIO_PRIMITIVA) + " EUR/apuesta - Minimo " + str(MIN_PRIMITIVA) + " apuesta")

    if "pri_nums" not in st.session_state: st.session_state.pri_nums = []
    if "pri_combs" not in st.session_state: st.session_state.pri_combs = None
    if "pri_baritas" not in st.session_state: st.session_state.pri_baritas = []

    st.subheader("1. Selecciona numeros (1-49)")
    cols = st.columns(10)
    for n in range(1, 50):
        with cols[(n-1) % 10]:
            activo = n in st.session_state.pri_nums
            if st.button(str(n), key="pn" + str(n), use_container_width=True,
                         type="primary" if activo else "secondary"):
                if activo: st.session_state.pri_nums.remove(n)
                else: st.session_state.pri_nums.append(n)
                st.rerun()

    st.caption("Seleccionados: " + str(len(st.session_state.pri_nums)) + " -> " + str(sorted(st.session_state.pri_nums)))

    c1, c2 = st.columns(2)
    if c1.button("Aleatorio", use_container_width=True):
        st.session_state.pri_nums = random.sample(range(1, 50), 6)
        st.rerun()
    if c2.button("Limpiar", use_container_width=True):
        st.session_state.pri_nums = []
        st.session_state.pri_combs = None
        st.session_state.pri_baritas = []
        st.rerun()

    st.divider()

    if len(st.session_state.pri_nums) >= 6:
        combs = generar_primitiva(st.session_state.pri_nums)
        n_ap = len(combs)
        coste_dir = round(n_ap * PRECIO_PRIMITIVA, 2)

        st.subheader("2. Coste directo")
        c1, c2 = st.columns(2)
        c1.metric("Apuestas", str(n_ap))
        c2.metric("Coste", str(coste_dir) + " EUR")

        if st.button("Generar", type="primary", use_container_width=True, key="gen_pri"):
            st.session_state.pri_combs = combs
            st.session_state.pri_baritas = []
            st.rerun()

        if st.session_state.pri_combs:
            st.divider()
            st.subheader("3. Barita Magica")
            factores = st.session_state.barita_factores["primitiva"]
            actuales = baritas_loteria(st.session_state.pri_combs, st.session_state.pri_baritas, factores, MIN_PRIMITIVA)
            n_act = len(actuales)
            coste_act = round(n_act * PRECIO_PRIMITIVA, 2)

            c1, c2 = st.columns(2)
            c1.metric("Apuestas", str(n_act))
            c2.metric("Coste", str(coste_act) + " EUR")

            cols_b = st.columns(4)
            for idx, capa in enumerate(BARITA_DEFAULT):
                with cols_b[idx]:
                    usada = capa["id"] in st.session_state.pri_baritas
                    pct = int(factores[idx] * 100)
                    label = capa["nombre"] + " (" + str(pct) + "%)"
                    if st.button(label, key="pb" + str(capa["id"]), use_container_width=True, disabled=usada,
                                 type="primary" if usada else "secondary"):
                        st.session_state.pri_baritas.append(capa["id"])
                        st.rerun()

            if st.session_state.pri_baritas:
                if st.button("Deshacer", use_container_width=True, key="undo_pri"):
                    st.session_state.pri_baritas.pop()
                    st.rerun()

            st.download_button("Descargar txt", data=txt_loteria(actuales).encode("utf-8"),
                               file_name="primitiva_reducida.txt", mime="text/plain",
                               use_container_width=True, type="primary")


# ═══════════════════════════════════════════════
# EUROMILLONES
# ═══════════════════════════════════════════════
elif seccion == "Euromillones":
    st.title("Euromillones")
    st.caption("5 numeros (1-50) + 2 estrellas (1-12) - " + str(PRECIO_EUROMILLONES) + " EUR/apuesta")

    if "eu_nums" not in st.session_state: st.session_state.eu_nums = []
    if "eu_est" not in st.session_state: st.session_state.eu_est = []
    if "eu_combs" not in st.session_state: st.session_state.eu_combs = None
    if "eu_baritas" not in st.session_state: st.session_state.eu_baritas = []

    st.subheader("1. Numeros (1-50)")
    cols = st.columns(10)
    for n in range(1, 51):
        with cols[(n-1) % 10]:
            activo = n in st.session_state.eu_nums
            if st.button(str(n), key="en" + str(n), use_container_width=True,
                         type="primary" if activo else "secondary"):
                if activo: st.session_state.eu_nums.remove(n)
                else: st.session_state.eu_nums.append(n)
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
                st.rerun()

    st.caption("Numeros: " + str(len(st.session_state.eu_nums)) + " -> " + str(sorted(st.session_state.eu_nums)))
    st.caption("Estrellas: " + str(len(st.session_state.eu_est)) + " -> " + str(sorted(st.session_state.eu_est)))

    c1, c2 = st.columns(2)
    if c1.button("Aleatorio", use_container_width=True, key="rand_eu"):
        st.session_state.eu_nums = random.sample(range(1, 51), 5)
        st.session_state.eu_est = random.sample(range(1, 13), 2)
        st.rerun()
    if c2.button("Limpiar", use_container_width=True, key="clear_eu"):
        st.session_state.eu_nums = []
        st.session_state.eu_est = []
        st.session_state.eu_combs = None
        st.session_state.eu_baritas = []
        st.rerun()

    st.divider()

    if len(st.session_state.eu_nums) >= 5 and len(st.session_state.eu_est) >= 2:
        combs = generar_euromillones(st.session_state.eu_nums, st.session_state.eu_est)
        n_ap = len(combs)
        coste_dir = round(n_ap * PRECIO_EUROMILLONES, 2)

        st.subheader("3. Coste directo")
        c1, c2 = st.columns(2)
        c1.metric("Apuestas", str(n_ap))
        c2.metric("Coste", str(coste_dir) + " EUR")

        if st.button("Generar", type="primary", use_container_width=True, key="gen_eu"):
            st.session_state.eu_combs = combs
            st.session_state.eu_baritas = []
            st.rerun()

        if st.session_state.eu_combs:
            st.divider()
            st.subheader("4. Barita Magica")
            factores = st.session_state.barita_factores["euromillones"]
            actuales = baritas_loteria(st.session_state.eu_combs, st.session_state.eu_baritas, factores, MIN_EUROMILLONES)
            n_act = len(actuales)
            coste_act = round(n_act * PRECIO_EUROMILLONES, 2)

            c1, c2 = st.columns(2)
            c1.metric("Apuestas", str(n_act))
            c2.metric("Coste", str(coste_act) + " EUR")

            cols_b = st.columns(4)
            for idx, capa in enumerate(BARITA_DEFAULT):
                with cols_b[idx]:
                    usada = capa["id"] in st.session_state.eu_baritas
                    pct = int(factores[idx] * 100)
                    label = capa["nombre"] + " (" + str(pct) + "%)"
                    if st.button(label, key="eb" + str(capa["id"]), use_container_width=True, disabled=usada,
                                 type="primary" if usada else "secondary"):
                        st.session_state.eu_baritas.append(capa["id"])
                        st.rerun()

            if st.session_state.eu_baritas:
                if st.button("Deshacer", use_container_width=True, key="undo_eu"):
                    st.session_state.eu_baritas.pop()
                    st.rerun()

            st.download_button("Descargar txt", data=txt_loteria(actuales).encode("utf-8"),
                               file_name="euromillones_reducida.txt", mime="text/plain",
                               use_container_width=True, type="primary")


# ═══════════════════════════════════════════════
# CONFIGURAR BARITA
# ═══════════════════════════════════════════════
elif seccion == "Configurar Barita":
    st.title("Configurar Barita Magica")
    st.write("Ajusta el porcentaje de combinaciones que se mantienen al pulsar cada barita.")

    juegos = ["quiniela", "bonoloto", "primitiva", "euromillones"]
    nombres_bonitos = {
        "quiniela": "Quiniela",
        "bonoloto": "Bonoloto",
        "primitiva": "Primitiva",
        "euromillones": "Euromillones",
    }
    nombres_capas = ["Poda basica", "Filtro historico", "Equilibrio", "Seleccion elite"]

    for juego in juegos:
        st.subheader(nombres_bonitos[juego])
        cols = st.columns(4)
        for i, capa_nombre in enumerate(nombres_capas):
            with cols[i]:
                pct = st.slider(
                    capa_nombre,
                    min_value=5, max_value=100,
                    value=int(st.session_state.barita_factores[juego][i] * 100),
                    step=5, key="barita_" + juego + "_" + str(i),
                    format="%d%%",
                )
                st.session_state.barita_factores[juego][i] = pct / 100.0
        st.divider()

    if st.button("Restaurar valores por defecto", use_container_width=True):
        st.session_state.barita_factores = {
            "quiniela":    [0.75, 0.70, 0.60, 0.55],
            "bonoloto":    [0.75, 0.70, 0.60, 0.55],
            "primitiva":   [0.75, 0.70, 0.60, 0.55],
            "euromillones":[0.75, 0.70, 0.60, 0.55],
        }
        st.rerun()


# ═══════════════════════════════════════════════
# CUENTA
# ═══════════════════════════════════════════════
elif seccion == "Cuenta":
    st.title("Cuenta")
    st.write("**Plan:** Free (demo)")
    st.write("Precios oficiales:")
    st.write("Quiniela: " + str(PRECIO_QUINIELA) + " EUR")
    st.write("Bonoloto: " + str(PRECIO_BONOLOTO) + " EUR")
    st.write("Primitiva: " + str(PRECIO_PRIMITIVA) + " EUR")
    st.write("Euromillones: " + str(PRECIO_EUROMILLONES) + " EUR")
    st.write("Minimos (apuestas):")
    st.write("Quiniela: " + str(MIN_QUINIELA))
    st.write("Bonoloto: " + str(MIN_BONOLOTO))
    st.write("Primitiva: " + str(MIN_PRIMITIVA))
    st.write("Euromillones: " + str(MIN_EUROMILLONES))
    if st.button("Cerrar sesion", use_container_width=True):
        st.session_state.autenticado = False
        st.rerun()
