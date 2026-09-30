# ══════════════════════════════════════════════════════════════
# QUINILOTO MAGIC - v8
# Botones iluminados + Sidebar bonito
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

# PRECIOS OFICIALES
PASSWORD = "2325"
PRECIO_QUINIELA     = 0.75
PRECIO_BONOLOTO     = 0.50
PRECIO_PRIMITIVA    = 1.00
PRECIO_EUROMILLONES = 2.50
MIN_QUINIELA        = 2
MIN_BONOLOTO        = 2
MIN_PRIMITIVA       = 1
MIN_EUROMILLONES    = 1
API_KEY_DEFAULT     = ""

REDUCCIONES_QUINIELA = {
    "directo":    {"nombre": "Directo (sin reducir)"},
    "reducida_1": {"nombre": "Reduccion 1a (4 triples -> 9 ap.)", "apuestas": 9},
    "reducida_2": {"nombre": "Reduccion 2a (7 dobles -> 16 ap.)", "apuestas": 16},
    "reducida_3": {"nombre": "Reduccion 3a (3 dobles+3 triples -> 24 ap.)", "apuestas": 24},
    "reducida_4": {"nombre": "Reduccion 4a (2 triples+6 dobles -> 64 ap.)", "apuestas": 64},
    "reducida_5": {"nombre": "Reduccion 5a (8 triples -> 81 ap.)", "apuestas": 81},
    "reducida_6": {"nombre": "Reduccion 6a (11 dobles -> 132 ap.)", "apuestas": 132},
}

BARITA_DEFAULT = [
    {"id": 1, "nombre": "Poda basica",      "factor": 0.75},
    {"id": 2, "nombre": "Filtro historico", "factor": 0.70},
    {"id": 3, "nombre": "Equilibrio",       "factor": 0.60},
    {"id": 4, "nombre": "Seleccion elite",  "factor": 0.55},
]

PLENO_OPCIONES = ["0", "1", "2", "M"]

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

# CSS
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
.stButton > button {
    border-radius: 12px;
    font-weight: 600;
}

/* Ocultar el header superior y el nombre "app" del sidebar */
header[data-testid="stHeader"] { display: none; }
[data-testid="stSidebarNav"] { display: none; }
[data-testid="stSidebarHeader"] { display: none; }

/* Botones iluminados (type=primary) */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%) !important;
    color: #0a0b15 !important;
    border: none !important;
    box-shadow: 0 4px 14px rgba(255, 215, 0, 0.5) !important;
}
.stButton > button[kind="secondary"] {
    background: transparent !important;
    color: #e0e0e0 !important;
    border: 1px solid #333 !important;
}
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# API SELAE
# ═══════════════════════════════════════════════
def _get_api_key():
    try:
        return st.secrets.get("API_KEY_LOTERIAS", API_KEY_DEFAULT)
    except Exception:
        return API_KEY_DEFAULT

@st.cache_data(ttl=3600)
def obtener_ultima_jornada():
    key = _get_api_key()
    if not key:
        return {"error": "API_KEY_LOTERIAS no configurada en Secrets."}
    try:
        r = requests.get(
            "https://api.loteriasapi.com/api/v1/results/quiniela/latest",
            headers={"X-API-Key": key}, timeout=15
        )
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}


# ═══════════════════════════════════════════════
# LOGICA QUINIELA
# ═══════════════════════════════════════════════
def generar_combinaciones(signos):
    return list(itertools.product(*[list(s) for s in signos]))

def contar_dobles_triples(signos):
    dobles = sum(1 for s in signos if len(s) == 2)
    triples = sum(1 for s in signos if len(s) == 3)
    return dobles, triples

def aplicar_reduccion_oficial(combinaciones, tipo, signos):
    if tipo == "directo":
        return combinaciones
    dobles, triples = contar_dobles_triples(signos)
    tabla = {
        "reducida_1": (0, 4), "reducida_2": (7, 0),
        "reducida_3": (3, 3), "reducida_4": (6, 2),
        "reducida_5": (0, 8), "reducida_6": (11, 0),
    }
    if tipo in tabla:
        d_esp, t_esp = tabla[tipo]
        if dobles == d_esp and triples == t_esp:
            objetivo = REDUCCIONES_QUINIELA[tipo]["apuestas"]
            return combinaciones[:objetivo]
    objetivo = REDUCCIONES_QUINIELA[tipo].get("apuestas")
    if objetivo and objetivo < len(combinaciones):
        return combinaciones[:objetivo]
    return combinaciones

def aplicar_barita(combinaciones, nivel, factores, min_ap):
    if nivel < 1 or nivel > len(factores):
        return combinaciones
    factor = factores[nivel - 1]
    n = max(min_ap, int(len(combinaciones) * factor))
    def score(c):
        s = "".join(c)
        return abs(s.count("1") - s.count("2"))
    return sorted(combinaciones, key=score)[:n]

def aplicar_baritas(combinaciones, niveles, factores, min_ap):
    res = list(combinaciones)
    for n in niveles:
        res = aplicar_barita(res, n, factores, min_ap)
    return res

def a_txt_quiniela(combinaciones, pleno_local, pleno_visit):
    lineas = ["".join(c) for c in combinaciones]
    if pleno_local and pleno_visit:
        lineas.append(str(pleno_local) + str(pleno_visit))
    return "\n".join(lineas)

def ordenar_signos(s):
    return "".join(sorted(set(s), key=lambda x: ["1", "X", "2"].index(x)))


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
        if g >= 3:
            p_local["M"] += p
        else:
            p_local[str(g)] += p
        p = poisson(g, lam_v)
        if g >= 3:
            p_visit["M"] += p
        else:
            p_visit[str(g)] += p
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
        "color:#FFD700;margin-top:15vh;margin-bottom:0;'>QUINILOTO</h1>"
        "<h2 style='text-align:center;font-family:Inter,sans-serif;"
        "font-size:32px;font-weight:700;letter-spacing:14px;"
        "color:#FFD700;margin-top:0;'>MAGIC</h2>",
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
if "combinaciones" not in st.session_state:
    st.session_state.combinaciones = None
if "baritas" not in st.session_state:
    st.session_state.baritas = []
if "equipos" not in st.session_state:
    st.session_state.equipos = dict(EQUIPOS_DEFAULT)
if "partidos_equipos" not in st.session_state:
    st.session_state.partidos_equipos = [
        ("Real Madrid", "Barcelona"), ("Atletico", "Sevilla"),
        ("Valencia", "Betis"),        ("Villarreal", "Athletic"),
        ("Real Sociedad", "Girona"),  ("Osasuna", "Celta"),
        ("Rayo", "Mallorca"),         ("Getafe", "Alaves"),
        ("Las Palmas", "Espanyol"),   ("Leganes", "Valladolid"),
        ("Real Madrid", "Atletico"),  ("Barcelona", "Sevilla"),
        ("Betis", "Villarreal"),      ("Athletic", "Valencia"),
    ]
if "pleno_equipos" not in st.session_state:
    st.session_state.pleno_equipos = ("Real Madrid", "Barcelona")
if "barita_factores" not in st.session_state:
    st.session_state.barita_factores = {
        "quiniela":    [0.75, 0.70, 0.60, 0.55],
        "bonoloto":    [0.75, 0.70, 0.60, 0.55],
        "primitiva":   [0.75, 0.70, 0.60, 0.55],
        "euromillones":[0.75, 0.70, 0.60, 0.55],
    }


# ═══════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════
with st.sidebar:
    st.markdown(
        "<h1 style='text-align:center;font-family:Inter,sans-serif;"
        "font-size:30px;font-weight:800;letter-spacing:-1px;"
        "color:#FFD700;margin-bottom:0;'>QUINILOTO</h1>"
        "<h2 style='text-align:center;font-family:Inter,sans-serif;"
        "font-size:22px;font-weight:700;letter-spacing:10px;"
        "color:#FFD700;margin-top:0;margin-bottom:25px;'>MAGIC</h2>",
        unsafe_allow_html=True,
    )
    st.markdown("---")
    seccion = st.radio(
        "Seccion",
        [
            "Inicio",
            "Jornada actual",
            "Quiniela",
            "Probabilidades 1X2 + Pleno",
            "Bonoloto",
            "Primitiva",
            "Euromillones",
            "Configurar Barita",
            "IA Magic",
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

    st.divider()
    st.subheader("Precios oficiales (por apuesta)")
    t1, t2, t3, t4 = st.columns(4)
    t1.metric("Quiniela", str(PRECIO_QUINIELA) + " EUR", "min " + str(MIN_QUINIELA) + " ap.")
    t2.metric("Bonoloto", str(PRECIO_BONOLOTO) + " EUR", "min " + str(MIN_BONOLOTO) + " ap.")
    t3.metric("Primitiva", str(PRECIO_PRIMITIVA) + " EUR", "min " + str(MIN_PRIMITIVA) + " ap.")
    t4.metric("Euromillones", str(PRECIO_EUROMILLONES) + " EUR", "min " + str(MIN_EUROMILLONES) + " ap.")


# ═══════════════════════════════════════════════
# JORNADA ACTUAL
# ═══════════════════════════════════════════════
elif seccion == "Jornada actual":
    st.title("Jornada actual")
    st.write("Datos oficiales de SELAE.")

    with st.spinner("Consultando la ultima jornada..."):
        datos = obtener_ultima_jornada()

    if datos and "error" not in datos:
        matchday = datos.get("matchday", "-")
        draw_date = datos.get("draw_date", "-")
        matches = datos.get("matches", [])
        pleno = datos.get("pleno_15", {})

        c1, c2 = st.columns(2)
        c1.metric("Jornada num.", str(matchday))
        c2.metric("Fecha sorteo", str(draw_date))

        st.divider()
        st.subheader("Partidos y resultados")
        for m in matches:
            pos = m.get("position", "?")
            home = m.get("home", "-")
            away = m.get("away", "-")
            sign = m.get("sign", "-")
            st.write("#" + str(pos) + " - " + str(home) + " vs " + str(away) + " -> " + str(sign))

        st.divider()
        st.subheader("Pleno al 15")
        if pleno:
            ph = pleno.get("home_goals", "-")
            pa = pleno.get("away_goals", "-")
            st.write("Resultado: " + str(ph) + " - " + str(pa))

        st.divider()
        if st.button("Refrescar datos", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

    elif datos and "error" in datos:
        st.error("No se han podido obtener datos oficiales: " + str(datos["error"]))
        st.info("Registrate gratis en loteriasapi.com y anade API_KEY_LOTERIAS en Secrets.")
    else:
        st.warning("No hay datos disponibles.")


# ═══════════════════════════════════════════════
# QUINIELA (botones que se iluminan)
# ═══════════════════════════════════════════════
elif seccion == "Quiniela":
    st.title("Quiniela + Pleno al 15")
    st.caption("Precio: " + str(PRECIO_QUINIELA) + " EUR/apuesta - Minimo " + str(MIN_QUINIELA) + " apuestas")

    st.subheader("1. Configura los 14 partidos")
    st.caption("Pulsa 1, X o 2 para marcar. Varios por partido = doble o triple.")

    for i in range(14):
        cols = st.columns([1, 1, 1, 1])
        cols[0].markdown(
            "<div style='padding-top:8px;font-weight:600;color:#a0a0b8;'>P" + str(i+1) + "</div>",
            unsafe_allow_html=True,
        )
        for j, signo in enumerate(["1", "X", "2"]):
            with cols[j+1]:
                activo = signo in st.session_state.signos[i]
                if st.button(
                    signo,
                    key="sig_" + str(i) + "_" + signo,
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

    dobles, triples = contar_dobles_triples(st.session_state.signos)
    st.caption("Dobles: " + str(dobles) + " - Triples: " + str(triples))

    if st.button("Resetear todos a 1", use_container_width=True):
        st.session_state.signos = ["1"] * 14
        st.rerun()

    st.divider()
    st.subheader("2. Reduccion oficial")
    tipo_red = st.selectbox(
        "Sistema",
        list(REDUCCIONES_QUINIELA.keys()),
        format_func=lambda x: REDUCCIONES_QUINIELA[x]["nombre"],
    )

    st.divider()
    st.subheader("Pleno al 15")
    col_pl1, col_pl2 = st.columns(2)
    with col_pl1:
        pleno_loc = st.multiselect("Goles local", PLENO_OPCIONES, default=[st.session_state.pleno_local], key="pleno_loc_ms")
    with col_pl2:
        pleno_vis = st.multiselect("Goles visitante", PLENO_OPCIONES, default=[st.session_state.pleno_visit], key="pleno_vis_ms")

    st.session_state.pleno_local = pleno_loc[0] if pleno_loc else "1"
    st.session_state.pleno_visit = pleno_vis[0] if pleno_vis else "0"
    pleno_mult = max(1, len(pleno_loc)) * max(1, len(pleno_vis))
    st.caption("Multiplicador del Pleno: x" + str(pleno_mult))

    st.divider()
    st.subheader("3. Coste")
    directas = generar_combinaciones(st.session_state.signos)
    total_directas = len(directas) * pleno_mult

    c1, c2 = st.columns(2)
    c1.metric("Apuestas directas", str(total_directas))
    c2.metric("Coste directo", str(round(total_directas * PRECIO_QUINIELA, 2)) + " EUR")

    if st.button("Generar combinaciones", type="primary", use_container_width=True):
        st.session_state.combinaciones = directas
        st.session_state.baritas = []
        st.rerun()

    st.divider()

    if st.session_state.combinaciones:
        st.subheader("4. Barita Magica")
        reducidas = aplicar_reduccion_oficial(st.session_state.combinaciones, tipo_red, st.session_state.signos)
        factores = st.session_state.barita_factores["quiniela"]
        actuales = aplicar_baritas(reducidas, st.session_state.baritas, factores, min_ap=MIN_QUINIELA)

        n_sin_pleno = len(actuales)
        n_total = n_sin_pleno * pleno_mult
        coste_act, aviso = coste_real(n_total, PRECIO_QUINIELA, MIN_QUINIELA)

        c1, c2 = st.columns(2)
        c1.metric("Apuestas totales", str(n_total))
        c2.metric("Coste final", str(coste_act) + " EUR")

        if aviso:
            st.warning("Minimo oficial: " + str(MIN_QUINIELA) + " apuestas")

        cols_b = st.columns(4)
        for idx, capa in enumerate(BARITA_DEFAULT):
            with cols_b[idx]:
                usada = capa["id"] in st.session_state.baritas
                pct = int(factores[idx] * 100)
                label = capa["nombre"] + " (" + str(pct) + "%)"
                if st.button(label, key="b" + str(capa["id"]), use_container_width=True, disabled=usada,
                             type="primary" if usada else "secondary"):
                    st.session_state.baritas.append(capa["id"])
                    st.rerun()

        if st.session_state.baritas:
            if st.button("Deshacer ultima barita", use_container_width=True):
                st.session_state.baritas.pop()
                st.rerun()

        st.divider()
        st.subheader("5. Descargar txt")
        contenido = a_txt_quiniela(actuales, st.session_state.pleno_local, st.session_state.pleno_visit)
        st.download_button(
            "Descargar txt",
            data=contenido.encode("utf-8"),
            file_name="quiniela_reducida.txt",
            mime="text/plain",
            use_container_width=True,
            type="primary",
        )


# ═══════════════════════════════════════════════
# PROBABILIDADES
# ═══════════════════════════════════════════════
elif seccion == "Probabilidades 1X2 + Pleno":
    st.title("Probabilidades 1X2 + Pleno al 15")

    equipos_disponibles = sorted(st.session_state.equipos.keys())

    st.markdown("### Emparejamientos (14 partidos)")
    for i in range(14):
        local_actual, visit_actual = st.session_state.partidos_equipos[i]
        cols = st.columns([1, 3, 3])
        cols[0].markdown("**#" + str(i+1) + "**")
        local = cols[1].selectbox("Local", equipos_disponibles,
            index=equipos_disponibles.index(local_actual) if local_actual in equipos_disponibles else 0,
            key="loc" + str(i))
        visit = cols[2].selectbox("Visitante", equipos_disponibles,
            index=equipos_disponibles.index(visit_actual) if visit_actual in equipos_disponibles else 1,
            key="vis" + str(i))
        st.session_state.partidos_equipos[i] = (local, visit)

    st.divider()
    st.markdown("### Pleno al 15")
    p_loc, p_vis = st.columns(2)
    pl_local = p_loc.selectbox("Local", equipos_disponibles,
        index=equipos_disponibles.index(st.session_state.pleno_equipos[0]) if st.session_state.pleno_equipos[0] in equipos_disponibles else 0,
        key="pleno_loc_eq")
    pl_visit = p_vis.selectbox("Visitante", equipos_disponibles,
        index=equipos_disponibles.index(st.session_state.pleno_equipos[1]) if st.session_state.pleno_equipos[1] in equipos_disponibles else 1,
        key="pleno_vis_eq")
    st.session_state.pleno_equipos = (pl_local, pl_visit)

    st.divider()

    if st.button("Calcular", type="primary", use_container_width=True):
        st.subheader("14 partidos")
        for i, (local, visit) in enumerate(st.session_state.partidos_equipos):
            lam_l, lam_v = estimar_lambdas(local, visit, st.session_state.equipos)
            probs = predecir_1x2(lam_l, lam_v)
            favorito = max(probs, key=probs.get)
            st.markdown("**P" + str(i+1) + ": " + local + " vs " + visit + "**")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("1", str(probs["1"]) + "%")
            c2.metric("X", str(probs["X"]) + "%")
            c3.metric("2", str(probs["2"]) + "%")
            c4.metric("Fav.", favorito)
            st.divider()

        st.subheader("Pleno al 15")
        lam_l, lam_v = estimar_lambdas(pl_local, pl_visit, st.session_state.equipos)
        pl = predecir_pleno(lam_l, lam_v)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**" + pl_local + "**")
            for k in ["0", "1", "2", "M"]:
                st.metric(k + " goles", str(pl["local"][k]) + "%")
        with c2:
            st.markdown("**" + pl_visit + "**")
            for k in ["0", "1", "2", "M"]:
                st.metric(k + " goles", str(pl["visitante"][k]) + "%")

    st.divider()
    st.subheader("Editar fuerzas")
    with st.expander("Editar equipos"):
        for nombre in sorted(st.session_state.equipos.keys()):
            eq = st.session_state.equipos[nombre]
            cols = st.columns([3, 2, 2])
            cols[0].markdown("**" + nombre + "**")
            eq["ataque"] = cols[1].number_input("Ataque", 0.0, 5.0, eq["ataque"], 0.05, key="at_" + nombre, label_visibility="collapsed")
            eq["defensa"] = cols[2].number_input("Defensa", 0.0, 5.0, eq["defensa"], 0.05, key="df_" + nombre, label_visibility="collapsed")


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
            if st.button(
                str(n),
                key="bn" + str(n),
                use_container_width=True,
                type="primary" if activo else "secondary",
            ):
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

            st.download_button(
                "Descargar txt",
                data=txt_loteria(actuales).encode("utf-8"),
                file_name="bonoloto_reducida.txt",
                mime="text/plain",
                use_container_width=True,
                type="primary",
            )


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
            if st.button(
                str(n),
                key="pn" + str(n),
                use_container_width=True,
                type="primary" if activo else "secondary",
            ):
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

            st.download_button(
                "Descargar txt",
                data=txt_loteria(actuales).encode("utf-8"),
                file_name="primitiva_reducida.txt",
                mime="text/plain",
                use_container_width=True,
                type="primary",
            )


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
            if st.button(
                str(n),
                key="en" + str(n),
                use_container_width=True,
                type="primary" if activo else "secondary",
            ):
                if activo: st.session_state.eu_nums.remove(n)
                else: st.session_state.eu_nums.append(n)
                st.rerun()

    st.subheader("2. Estrellas (1-12)")
    cols_e = st.columns(12)
    for n in range(1, 13):
        with cols_e[n-1]:
            activo = n in st.session_state.eu_est
            if st.button(
                "E" + str(n),
                key="ee" + str(n),
                use_container_width=True,
                type="primary" if activo else "secondary",
            ):
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

            st.download_button(
                "Descargar txt",
                data=txt_loteria(actuales).encode("utf-8"),
                file_name="euromillones_reducida.txt",
                mime="text/plain",
                use_container_width=True,
                type="primary",
            )


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
# IA MAGIC
# ═══════════════════════════════════════════════
elif seccion == "IA Magic":
    st.title("IA Magic")
    st.write("Como funciona todo.")

    st.subheader("Poisson")
    st.write("1. Cada equipo tiene ataque y defensa.")
    st.write("2. Se calculan goles esperados (lambda) con factor campo 1.15 local / 0.85 visitante.")
    st.write("3. Con Poisson se obtiene la probabilidad de cada marcador.")
    st.write("4. Se agrupan en 1, X, 2 y en el Pleno en 0, 1, 2, M.")

    st.subheader("Barita Magica")
    st.write("Cada pulsacion mantiene un porcentaje de combinaciones. Puedes ajustar esos porcentajes en Configurar Barita.")

    st.subheader("Precios oficiales")
    st.table({
        "Juego": ["Quiniela", "Bonoloto", "Primitiva", "Euromillones"],
        "EUR/apuesta": [PRECIO_QUINIELA, PRECIO_BONOLOTO, PRECIO_PRIMITIVA, PRECIO_EUROMILLONES],
        "Min. apuestas": [MIN_QUINIELA, MIN_BONOLOTO, MIN_PRIMITIVA, MIN_EUROMILLONES],
    })


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
