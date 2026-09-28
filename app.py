# ══════════════════════════════════════════════════════════════
# 🎯 QUINILOTO MAGIC — Todo en uno
# Quiniela + Pleno al 15 + Bonoloto + Primitiva + Euromillones
# Precios oficiales SELAE | Reducciones oficiales | Poisson
# ══════════════════════════════════════════════════════════════

import itertools
import math
import random
import streamlit as st

# ─────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────
st.set_page_config(
    page_title="Quiniloto Magic",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────
# PRECIOS OFICIALES
# ─────────────────────────────────────────────────
PASSWORD = "2325"

PRECIO_QUINIELA   = 0.75      # € por apuesta
MIN_QUINIELA      = 2         # mínimo 2 apuestas (1,50 €)

PRECIO_BONOLOTO   = 0.50      # € por apuesta
MIN_BONOLOTO      = 2         # mínimo 2 apuestas (1,00 €)

PRECIO_PRIMITIVA  = 1.00      # € por apuesta
MIN_PRIMITIVA     = 1

PRECIO_EUROMILLONES = 2.50    # € por apuesta
MIN_EUROMILLONES    = 1

# ─────────────────────────────────────────────────
# REDUCCIONES OFICIALES QUINIELA (tablas SELAE)
# ─────────────────────────────────────────────────
REDUCCIONES_QUINIELA = {
    "directo":        {"nombre": "Directo (sin reducir)", "apuestas": None},
    "reducida_1":     {"nombre": "Reducción 1ª (4 triples → 9 ap.)",   "apuestas": 9},
    "reducida_2":     {"nombre": "Reducción 2ª (7 dobles → 16 ap.)",   "apuestas": 16},
    "reducida_3":     {"nombre": "Reducción 3ª (3 dobles+3 triples → 24 ap.)", "apuestas": 24},
    "reducida_4":     {"nombre": "Reducción 4ª (2 triples+6 dobles → 64 ap.)", "apuestas": 64},
    "reducida_5":     {"nombre": "Reducción 5ª (8 triples → 81 ap.)",  "apuestas": 81},
    "reducida_6":     {"nombre": "Reducción 6ª (11 dobles → 132 ap.)", "apuestas": 132},
}

CAPAS_BARITA = [
    {"id": 1, "nombre": "🪄 Poda básica",      "factor": 0.75},
    {"id": 2, "nombre": "🪄 Filtro histórico", "factor": 0.70},
    {"id": 3, "nombre": "🪄 Equilibrio",       "factor": 0.60},
    {"id": 4, "nombre": "🪄 Selección élite",  "factor": 0.55},
]

PLENO_OPCIONES = ["0", "1", "2", "M"]

EQUIPOS_DEFAULT = {
    "Real Madrid":    {"ataque": 2.10, "defensa": 0.80},
    "Barcelona":      {"ataque": 1.95, "defensa": 0.90},
    "Atlético":       {"ataque": 1.50, "defensa": 0.70},
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
    "Alavés":         {"ataque": 1.05, "defensa": 1.00},
    "Las Palmas":     {"ataque": 1.10, "defensa": 1.15},
    "Espanyol":       {"ataque": 1.00, "defensa": 1.05},
    "Leganés":        {"ataque": 0.90, "defensa": 1.00},
    "Valladolid":     {"ataque": 0.85, "defensa": 1.20},
}

# ─────────────────────────────────────────────────
# CSS
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
.stButton > button {
    border-radius: 12px;
    font-weight: 600;
    transition: all 0.2s ease;
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 8px 20px rgba(255, 215, 0, 0.35);
}
.main-header {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    color: #FFD700;
    margin-bottom: 8px;
}
.sub-header {
    text-align: center;
    color: #a0a0b8;
    font-size: 15px;
    margin-bottom: 24px;
}
.card {
    background: linear-gradient(145deg, #16172b 0%, #1e1f36 100%);
    border: 1px solid rgba(255, 215, 0, 0.2);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.3);
}
.precio-grande {
    font-size: 48px;
    font-weight: 800;
    color: #FFD700;
    letter-spacing: -2px;
}
.login-box {
    max-width: 420px;
    margin: 8vh auto;
    padding: 40px;
    border-radius: 20px;
    background: linear-gradient(145deg, #0f1020 0%, #1a1b2e 100%);
    border: 1px solid rgba(255, 215, 0, 0.3);
    box-shadow: 0 20px 60px rgba(0,0,0,0.5);
    text-align: center;
}
.login-title { font-size: 42px; font-weight: 800; color: #FFD700; margin-bottom: 8px; }
.login-sub { color: #a0a0b8; font-size: 14px; margin-bottom: 32px; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# LÓGICA QUINIELA
# ═══════════════════════════════════════════════
def generar_combinaciones(signos):
    opciones = [list(s) for s in signos]
    return list(itertools.product(*opciones))


def coste(combinaciones, precio):
    return round(len(combinaciones) * precio, 2)


def contar_dobles_triples(signos):
    dobles = sum(1 for s in signos if len(s) == 2)
    triples = sum(1 for s in signos if len(s) == 3)
    return dobles, triples


def aplicar_reduccion_oficial(combinaciones, tipo_reduccion, signos):
    """Aplica la reducción oficial SELAE correspondiente."""
    dobles, triples = contar_dobles_triples(signos)

    if tipo_reduccion == "directo":
        return combinaciones

    # Reducción 1ª: 4 triples → 9 apuestas
    if tipo_reduccion == "reducida_1" and triples == 4 and dobles == 0:
        return combinaciones[:9]

    # Reducción 2ª: 7 dobles → 16 apuestas
    if tipo_reduccion == "reducida_2" and dobles == 7 and triples == 0:
        return combinaciones[:16]

    # Reducción 3ª: 3 dobles + 3 triples → 24 apuestas
    if tipo_reduccion == "reducida_3" and dobles == 3 and triples == 3:
        return combinaciones[:24]

    # Reducción 4ª: 2 triples + 6 dobles → 64 apuestas
    if tipo_reduccion == "reducida_4" and dobles == 6 and triples == 2:
        return combinaciones[:64]

    # Reducción 5ª: 8 triples → 81 apuestas
    if tipo_reduccion == "reducida_5" and triples == 8 and dobles == 0:
        return combinaciones[:81]

    # Reducción 6ª: 11 dobles → 132 apuestas
    if tipo_reduccion == "reducida_6" and dobles == 11 and triples == 0:
        return combinaciones[:132]

    # Si no coincide exactamente, aplicar factor proporcional
    objetivo = REDUCCIONES_QUINIELA[tipo_reduccion]["apuestas"]
    if objetivo and objetivo < len(combinaciones):
        return combinaciones[:objetivo]
    return combinaciones


def aplicar_barita(combinaciones, nivel, min_apuestas=1):
    if nivel < 1 or nivel > len(CAPAS_BARITA):
        return combinaciones
    capa = CAPAS_BARITA[nivel - 1]
    n = max(min_apuestas, int(len(combinaciones) * capa["factor"]))

    def score(c):
        s = "".join(c)
        return abs(s.count("1") - s.count("2"))

    return sorted(combinaciones, key=score)[:n]


def aplicar_baritas(combinaciones, niveles, min_apuestas=1):
    res = list(combinaciones)
    for n in niveles:
        res = aplicar_barita(res, n, min_apuestas)
    return res


def a_txt_quiniela(combinaciones, pleno_local, pleno_visit):
    lineas = ["".join(c) for c in combinaciones]
    if pleno_local is not None and pleno_visit is not None:
        lineas.append(f"{pleno_local}{pleno_visit}")
    return "\n".join(lineas)


# ═══════════════════════════════════════════════
# LÓGICA POISSON
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
    p_local = {0: 0, 1: 0, 2: 0, "M": 0}
    p_visit = {0: 0, 1: 0, 2: 0, "M": 0}
    for g in range(max_g + 1):
        p = poisson(g, lam_l)
        if g >= 3: p_local["M"] += p
        else: p_local[g] += p
        p = poisson(g, lam_v)
        if g >= 3: p_visit["M"] += p
        else: p_visit[g] += p
    return {
        "local": {k: round(v*100, 1) for k, v in p_local.items()},
        "visitante": {k: round(v*100, 1) for k, v in p_visit.items()},
    }


def estimar_lambdas(local, visitante, equipos):
    L = equipos.get(local, {"ataque": 1.3, "defensa": 1.0})
    V = equipos.get(visitante, {"ataque": 1.3, "defensa": 1.0})
    return round(L["ataque"] * V["defensa"] * 1.15, 2), round(V["ataque"] * L["defensa"] * 0.85, 2)


# ═══════════════════════════════════════════════
# LÓGICA LOTERÍAS
# ═══════════════════════════════════════════════
def generar_bonoloto(numeros):
    if len(numeros) < 6: return []
    return list(itertools.combinations(sorted(numeros), 6))


def generar_primitiva(numeros):
    if len(numeros) < 6: return []
    return list(itertools.combinations(sorted(numeros), 6))


def generar_euromillones(numeros, estrellas):
    if len(numeros) < 5 or len(estrellas) < 2: return []
    comb_num = list(itertools.combinations(sorted(numeros), 5))
    comb_est = list(itertools.combinations(sorted(estrellas), 2))
    return [(n, e) for n in comb_num for e in comb_est]


def barita_loteria(combinaciones, nivel, min_ap):
    if nivel < 1 or nivel > len(CAPAS_BARITA):
        return combinaciones
    factor = CAPAS_BARITA[nivel - 1]["factor"]
    n = max(min_ap, int(len(combinaciones) * factor))

    def score(c):
        if isinstance(c, tuple) and len(c) == 2 and isinstance(c[0], tuple):
            nums = c[0]
        else:
            nums = c
        suma = sum(nums)
        pares = sum(1 for x in nums if x % 2 == 0)
        return abs(suma - 125) + abs(pares - len(nums)//2) * 5

    return sorted(combinaciones, key=score)[:n]


def baritas_loteria(combinaciones, niveles, min_ap):
    res = list(combinaciones)
    for n in niveles:
        res = barita_loteria(res, n, min_ap)
    return res


def txt_loteria(combinaciones):
    lineas = []
    for c in combinaciones:
        if isinstance(c, tuple) and len(c) == 2 and isinstance(c[0], tuple):
            nums, est = c
            lineas.append(" ".join(f"{n:02d}" for n in nums) + " | " + " ".join(f"{e:02d}" for e in est))
        else:
            lineas.append(" ".join(f"{n:02d}" for n in c))
    return "\n".join(lineas)


# ═══════════════════════════════════════════════
# LOGIN
# ═══════════════════════════════════════════════
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown("""
        <div class="login-box">
            <div class="login-title">🎯 Quiniloto Magic</div>
            <div class="login-sub">Acceso privado</div>
        </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        pwd = st.text_input("Contraseña", type="password", label_visibility="collapsed")
        if st.button("Entrar", use_container_width=True, type="primary"):
            if pwd == PASSWORD:
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.error("❌ Contraseña incorrecta")
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
        ("Real Madrid", "Barcelona"), ("Atlético", "Sevilla"),
        ("Valencia", "Betis"),        ("Villarreal", "Athletic"),
        ("Real Sociedad", "Girona"),  ("Osasuna", "Celta"),
        ("Rayo", "Mallorca"),         ("Getafe", "Alavés"),
        ("Las Palmas", "Espanyol"),   ("Leganés", "Valladolid"),
        ("Real Madrid", "Atlético"),  ("Barcelona", "Sevilla"),
        ("Betis", "Villarreal"),      ("Athletic", "Valencia"),
    ]
if "pleno_equipos" not in st.session_state:
    st.session_state.pleno_equipos = ("Real Madrid", "Barcelona")


# ═══════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════
with st.sidebar:
    st.markdown("### 🎯 Quiniloto Magic")
    st.markdown("---")
    seccion = st.radio(
        "Sección",
        [
            "🏠 Inicio",
            "⚽ Quiniela",
            "🧠 Probabilidades 1X2 + Pleno",
            "🎲 Bonoloto",
            "🍀 Primitiva",
            "🌍 Euromillones",
            "🤖 IA Magic",
            "⚙️ Cuenta",
        ],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.caption("Precios oficiales:")
    st.caption(f"⚽ Quiniela: {PRECIO_QUINIELA} €")
    st.caption(f"🎲 Bonoloto: {PRECIO_BONOLOTO} €")
    st.caption(f"🍀 Primitiva: {PRECIO_PRIMITIVA} €")
    st.caption(f"🌍 Euromillones: {PRECIO_EUROMILLONES} €")
    if st.button("🚪 Cerrar sesión", use_container_width=True):
        st.session_state.autenticado = False
        st.rerun()


# ═══════════════════════════════════════════════
# 🏠 INICIO
# ═══════════════════════════════════════════════
if seccion == "🏠 Inicio":
    st.markdown('<p class="main-header">🎯 Quiniloto Magic</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Quiniela · Pleno al 15 · Bonoloto · Primitiva · Euromillones</p>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("⚽ Quiniela + Pleno", "14+1")
    c2.metric("🎲 Bonoloto", "6/49")
    c3.metric("🍀 Primitiva", "6/49")
    c4.metric("🌍 Euromillones", "5/50+2/12")

    st.divider()

    st.subheader("💶 Precios oficiales")
    t1, t2, t3, t4 = st.columns(4)
    t1.metric("Quiniela",      f"{PRECIO_QUINIELA} €", f"min {MIN_QUINIELA*PRECIO_QUINIELA:.2f} €")
    t2.metric("Bonoloto",      f"{PRECIO_BONOLOTO} €", f"min {MIN_BONOLOTO*PRECIO_BONOLOTO:.2f} €")
    t3.metric("Primitiva",     f"{PRECIO_PRIMITIVA} €")
    t4.metric("Euromillones",  f"{PRECIO_EUROMILLONES} €")

    st.divider()

    st.subheader("🚀 ¿Qué puedes hacer aquí?")
    st.success("""
✅ **Quiniela** con 14 partidos + **Pleno al 15** y **reducciones oficiales SELAE**

✅ **Probabilidades 1X2** y **Pleno** con modelo Poisson

✅ **Bonoloto / Primitiva / Euromillones** con reducciones y Barita Mágica

✅ **Barita Mágica** para bajar el coste en todos los juegos

✅ **Descarga .txt** lista para EduardoLosilla
""")


# ═══════════════════════════════════════════════
# ⚽ QUINIELA (+ PLENO AL 15)
# ═══════════════════════════════════════════════
elif seccion == "⚽ Quiniela":
    st.title("⚽ Quiniela + Pleno al 15")
    st.caption(f"Precio: {PRECIO_QUINIELA} €/apuesta · Mínimo {MIN_QUINIELA*PRECIO_QUINIELA:.2f} €")

    # ── 14 PARTIDOS ──
    st.subheader("1️⃣ Configura los 14 partidos")
    opciones = ["1", "X", "2", "1X", "X2", "12", "1X2"]
    cols = st.columns(2)
    for i in range(14):
        with cols[i % 2]:
            st.session_state.signos[i] = st.selectbox(
                f"Partido {i+1}", opciones,
                index=opciones.index(st.session_state.signos[i]),
                key=f"p{i}",
            )

    dobles, triples = contar_dobles_triples(st.session_state.signos)
    st.info(f"📊 Dobles: {dobles} · Triples: {triples} · Combinaciones directas: {3**triples * 2**dobles:,}")

    st.divider()

    # ── TIPO DE REDUCCIÓN ──
    st.subheader("2️⃣ Tipo de reducción")
    tipo_red = st.selectbox(
        "Selecciona el sistema",
        list(REDUCCIONES_QUINIELA.keys()),
        format_func=lambda x: REDUCCIONES_QUINIELA[x]["nombre"],
    )

    st.divider()

    # ── PLENO AL 15 ──
    st.subheader("1️⃣5️⃣ Pleno al 15")
    col_pl1, col_pl2 = st.columns(2)
    with col_pl1:
        st.markdown("**Local**")
        pleno_loc = st.multiselect("Goles local", PLENO_OPCIONES, default=[st.session_state.pleno_local],
                                    key="pleno_loc_ms", label_visibility="collapsed")
    with col_pl2:
        st.markdown("**Visitante**")
        pleno_vis = st.multiselect("Goles visitante", PLENO_OPCIONES, default=[st.session_state.pleno_visit],
                                    key="pleno_vis_ms", label_visibility="collapsed")

    st.session_state.pleno_local = pleno_loc[0] if pleno_loc else "1"
    st.session_state.pleno_visit = pleno_vis[0] if pleno_vis else "0"
    pleno_mult = max(1, len(pleno_loc)) * max(1, len(pleno_vis))
    st.info(f"Multiplicador del Pleno: ×{pleno_mult}")

    st.divider()

    # ── COSTE DIRECTO ──
    st.subheader("3️⃣ Coste")
    directas = generar_combinaciones(st.session_state.signos)
    total_directas = len(directas) * pleno_mult

    c1, c2 = st.columns(2)
    c1.metric("Apuestas directas", f"{total_directas:,}")
    c2.metric("Coste directo", f"{total_directas * PRECIO_QUINIELA:,.2f} €")

    if st.button("🎯 Generar combinaciones", type="primary", use_container_width=True):
        st.session_state.combinaciones = directas
        st.session_state.baritas = []
        st.rerun()

    st.divider()

    # ── BARITA MÁGICA ──
    if st.session_state.combinaciones:
        st.subheader("4️⃣ Barita Mágica 🪄")

        # Primero aplicar reducción oficial
        reducidas = aplicar_reduccion_oficial(
            st.session_state.combinaciones, tipo_red, st.session_state.signos
        )
        # Luego aplicar baritas
        actuales = aplicar_baritas(reducidas, st.session_state.baritas, min_apuestas=MIN_QUINIELA)

        apuestas_sin_pleno = len(actuales)
        apuestas_totales = apuestas_sin_pleno * pleno_mult
        coste_actual = apuestas_totales * PRECIO_QUINIELA

        st.markdown(f"""
            <div class="card" style="text-align:center;">
                <div style="color:#a0a0b8;font-size:14px;">APUESTAS TOTALES</div>
                <div class="precio-grande">{apuestas_totales:,}</div>
                <div style="color:#a0a0b8;font-size:14px;margin-top:8px;">COSTE FINAL</div>
                <div style="color:#FFD700;font-size:32px;font-weight:800;">{coste_actual:,.2f} €</div>
            </div>
        """, unsafe_allow_html=True)

        if coste_actual < MIN_QUINIELA * PRECIO_QUINIELA:
            st.warning(f"⚠️ Coste por debajo del mínimo ({MIN_QUINIELA*PRECIO_QUINIELA:.2f} €).")

        cols_b = st.columns(4)
        for idx, capa in enumerate(CAPAS_BARITA):
            with cols_b[idx]:
                usada = capa["id"] in st.session_state.baritas
                label = f"{'✅ ' if usada else ''}{capa['nombre']}"
                if st.button(label, key=f"b{capa['id']}", use_container_width=True, disabled=usada):
                    st.session_state.baritas.append(capa["id"])
                    st.rerun()

        if st.session_state.baritas:
            if st.button("↩️ Deshacer última barita", use_container_width=True):
                st.session_state.baritas.pop()
                st.rerun()

        st.divider()

        st.subheader("5️⃣ Descargar .txt")
        contenido = a_txt_quiniela(actuales, st.session_state.pleno_local, st.session_state.pleno_visit)
        st.download_button(
            "📥 Descargar .txt",
            data=contenido.encode("utf-8"),
            file_name="quiniela_reducida.txt",
            mime="text/plain",
            use_container_width=True,
            type="primary",
        )

        with st.expander("👀 Ver primeras 20 apuestas + Pleno"):
            preview = "\n".join("".join(c) for c in actuales[:20])
            preview += f"\n\nPLENO AL 15: {st.session_state.pleno_local}-{st.session_state.pleno_visit}"
            st.code(preview, language=None)


# ═══════════════════════════════════════════════
# 🧠 PROBABILIDADES
# ═══════════════════════════════════════════════
elif seccion == "🧠 Probabilidades 1X2 + Pleno":
    st.title("🧠 Probabilidades 1X2 + Pleno al 15")
    st.caption("Modelo Poisson · 14 partidos + Pleno · Sin API externa.")

    equipos_disponibles = sorted(st.session_state.equipos.keys())

    st.markdown("### 1️⃣ Emparejamientos (14 partidos)")
    for i in range(14):
        local_actual, visit_actual = st.session_state.partidos_equipos[i]
        cols = st.columns([1, 3, 3])
        cols[0].markdown(f"**#{i+1}**")
        local = cols[1].selectbox("Local", equipos_disponibles,
            index=equipos_disponibles.index(local_actual) if local_actual in equipos_disponibles else 0,
            key=f"loc{i}")
        visit = cols[2].selectbox("Visitante", equipos_disponibles,
            index=equipos_disponibles.index(visit_actual) if visit_actual in equipos_disponibles else 1,
            key=f"vis{i}")
        st.session_state.partidos_equipos[i] = (local, visit)

    st.divider()
    st.markdown("### 1️⃣5️⃣ Pleno al 15")
    p_loc, p_vis = st.columns(2)
    pl_local = p_loc.selectbox("Equipo local del Pleno", equipos_disponibles,
        index=equipos_disponibles.index(st.session_state.pleno_equipos[0]) if st.session_state.pleno_equipos[0] in equipos_disponibles else 0,
        key="pleno_loc_eq")
    pl_visit = p_vis.selectbox("Equipo visitante del Pleno", equipos_disponibles,
        index=equipos_disponibles.index(st.session_state.pleno_equipos[1]) if st.session_state.pleno_equipos[1] in equipos_disponibles else 1,
        key="pleno_vis_eq")
    st.session_state.pleno_equipos = (pl_local, pl_visit)

    st.divider()

    if st.button("📊 Calcular probabilidades", type="primary", use_container_width=True):
        st.subheader("📈 Resultados de los 14 partidos")
        for i, (local, visit) in enumerate(st.session_state.partidos_equipos):
            lam_l, lam_v = estimar_lambdas(local, visit, st.session_state.equipos)
            probs = predecir_1x2(lam_l, lam_v)
            favorito = max(probs, key=probs.get)
            st.markdown(f"**Partido {i+1}: {local} vs {visit}**")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("1", f"{probs['1']}%")
            c2.metric("X", f"{probs['X']}%")
            c3.metric("2", f"{probs['2']}%")
            c4.metric("Favorito", favorito)
            st.caption(f"λ local={lam_l} · λ visitante={lam_v}")
            st.divider()

        st.subheader("1️⃣5️⃣ Pleno al 15 — Probabilidades por marcador")
        lam_l, lam_v = estimar_lambdas(pl_local, pl_visit, st.session_state.equipos)
        pl = predecir_pleno(lam_l, lam_v)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**{pl_local} (local)**")
            for k in ["0", "1", "2", "M"]:
                st.metric(f"{k} goles", f"{pl['local'][k]}%")
        with c2:
            st.markdown(f"**{pl_visit} (visitante)**")
            for k in ["0", "1", "2", "M"]:
                st.metric(f"{k} goles", f"{pl['visitante'][k]}%")

    st.divider()
    st.subheader("🔧 Editar fuerzas de equipos")
    with st.expander("Editar"):
        for nombre in sorted(st.session_state.equipos.keys()):
            eq = st.session_state.equipos[nombre]
            cols = st.columns([3, 2, 2])
            cols[0].markdown(f"**{nombre}**")
            eq["ataque"] = cols[1].number_input("Ataque", 0.0, 5.0, eq["ataque"], 0.05, key=f"at_{nombre}", label_visibility="collapsed")
            eq["defensa"] = cols[2].number_input("Defensa", 0.0, 5.0, eq["defensa"], 0.05, key=f"df_{nombre}", label_visibility="collapsed")


# ═══════════════════════════════════════════════
# 🎲 BONOLOTO
# ═══════════════════════════════════════════════
elif seccion == "🎲 Bonoloto":
    st.title("🎲 Bonoloto")
    st.caption(f"6 números del 1 al 49 · {PRECIO_BONOLOTO} €/apuesta · Mínimo {MIN_BONOLOTO*PRECIO_BONOLOTO:.2f} €")

    if "bono_nums" not in st.session_state:
        st.session_state.bono_nums = []
    if "bono_combs" not in st.session_state:
        st.session_state.bono_combs = None
    if "bono_baritas" not in st.session_state:
        st.session_state.bono_baritas = []

    st.subheader("1️⃣ Selecciona tus números")
    cols = st.columns(10)
    for n in range(1, 50):
        with cols[(n-1) % 10]:
            activo = n in st.session_state.bono_nums
            label = f"**{n}**" if activo else str(n)
            if st.button(label, key=f"bn{n}", use_container_width=True):
                if activo: st.session_state.bono_nums.remove(n)
                else: st.session_state.bono_nums.append(n)
                st.rerun()

    st.info(f"Seleccionados: {len(st.session_state.bono_nums)} → {sorted(st.session_state.bono_nums)}")

    if st.button("🎲 Aleatorio", use_container_width=True):
        st.session_state.bono_nums = random.sample(range(1, 50), 6)
        st.rerun()
    if st.button("🗑️ Limpiar", use_container_width=True):
        st.session_state.bono_nums = []
        st.session_state.bono_combs = None
        st.session_state.bono_baritas = []
        st.rerun()

    st.divider()

    if len(st.session_state.bono_nums) >= 6:
        combs = generar_bonoloto(st.session_state.bono_nums)
        n_ap = len(combs)
        coste_dir = max(n_ap * PRECIO_BONOLOTO, MIN_BONOLOTO * PRECIO_BONOLOTO)

        st.subheader("2️⃣ Coste directo")
        c1, c2 = st.columns(2)
        c1.metric("Apuestas", f"{n_ap:,}")
        c2.metric("Coste", f"{coste_dir:,.2f} €")

        if st.button("✅ Generar", type="primary", use_container_width=True):
            st.session_state.bono_combs = combs
            st.session_state.bono_baritas = []
            st.rerun()

        if st.session_state.bono_combs:
            st.divider()
            st.subheader("3️⃣ Barita Mágica 🪄")
            actuales = baritas_loteria(st.session_state.bono_combs, st.session_state.bono_baritas, MIN_BONOLOTO)
            n_act = len(actuales)
            coste_act = max(n_act * PRECIO_BONOLOTO, MIN_BONOLOTO * PRECIO_BONOLOTO)

            st.markdown(f"""
                <div class="card" style="text-align:center;">
                    <div style="color:#a0a0b8;font-size:14px;">APUESTAS</div>
                    <div class="precio-grande">{n_act:,}</div>
                    <div style="color:#FFD700;font-size:32px;font-weight:800;">{coste_act:,.2f} €</div>
                </div>
            """, unsafe_allow_html=True)

            cols_b = st.columns(4)
            for idx, capa in enumerate(CAPAS_BARITA):
                with cols_b[idx]:
                    usada = capa["id"] in st.session_state.bono_baritas
                    label = f"{'✅ ' if usada else ''}{capa['nombre']}"
                    if st.button(label, key=f"bb{capa['id']}", use_container_width=True, disabled=usada):
                        st.session_state.bono_baritas.append(capa["id"])
                        st.rerun()

            if st.session_state.bono_baritas:
                if st.button("↩️ Deshacer barita", use_container_width=True, key="undo_bono"):
                    st.session_state.bono_baritas.pop()
                    st.rerun()

            st.download_button(
                "📥 Descargar .txt",
                data=txt_loteria(actuales).encode("utf-8"),
                file_name="bonoloto_reducida.txt",
                mime="text/plain",
                use_container_width=True,
                type="primary",
            )


# ═══════════════════════════════════════════════
# 🍀 PRIMITIVA
# ═══════════════════════════════════════════════
elif seccion == "🍀 Primitiva":
    st.title("🍀 Primitiva")
    st.caption(f"6 números del 1 al 49 · {PRECIO_PRIMITIVA} €/apuesta · Mínimo {MIN_PRIMITIVA*PRECIO_PRIMITIVA:.2f} €")

    if "pri_nums" not in st.session_state:
        st.session_state.pri_nums = []
    if "pri_combs" not in st.session_state:
        st.session_state.pri_combs = None
    if "pri_baritas" not in st.session_state:
        st.session_state.pri_baritas = []

    st.subheader("1️⃣ Selecciona tus números")
    cols = st.columns(10)
    for n in range(1, 50):
        with cols[(n-1) % 10]:
            activo = n in st.session_state.pri_nums
            label = f"**{n}**" if activo else str(n)
            if st.button(label, key=f"pn{n}", use_container_width=True):
                if activo: st.session_state.pri_nums.remove(n)
                else: st.session_state.pri_nums.append(n)
                st.rerun()

    st.info(f"Seleccionados: {len(st.session_state.pri_nums)} → {sorted(st.session_state.pri_nums)}")

    c1, c2 = st.columns(2)
    if c1.button("🎲 Aleatorio", use_container_width=True):
        st.session_state.pri_nums = random.sample(range(1, 50), 6)
        st.rerun()
    if c2.button("🗑️ Limpiar", use_container_width=True):
        st.session_state.pri_nums = []
        st.session_state.pri_combs = None
        st.session_state.pri_baritas = []
        st.rerun()

    st.divider()

    if len(st.session_state.pri_nums) >= 6:
        combs = generar_primitiva(st.session_state.pri_nums)
        n_ap = len(combs)
        coste_dir = max(n_ap * PRECIO_PRIMITIVA, MIN_PRIMITIVA * PRECIO_PRIMITIVA)

        st.subheader("2️⃣ Coste directo")
        c1, c2 = st.columns(2)
        c1.metric("Apuestas", f"{n_ap:,}")
        c2.metric("Coste", f"{coste_dir:,.2f} €")

        if st.button("✅ Generar", type="primary", use_container_width=True, key="gen_pri"):
            st.session_state.pri_combs = combs
            st.session_state.pri_baritas = []
            st.rerun()

        if st.session_state.pri_combs:
            st.divider()
            st.subheader("3️⃣ Barita Mágica 🪄")
            actuales = baritas_loteria(st.session_state.pri_combs, st.session_state.pri_baritas, MIN_PRIMITIVA)
            n_act = len(actuales)
            coste_act = max(n_act * PRECIO_PRIMITIVA, MIN_PRIMITIVA * PRECIO_PRIMITIVA)

            st.markdown(f"""
                <div class="card" style="text-align:center;">
                    <div style="color:#a0a0b8;font-size:14px;">APUESTAS</div>
                    <div class="precio-grande">{n_act:,}</div>
                    <div style="color:#FFD700;font-size:32px;font-weight:800;">{coste_act:,.2f} €</div>
                </div>
            """, unsafe_allow_html=True)

            cols_b = st.columns(4)
            for idx, capa in enumerate(CAPAS_BARITA):
                with cols_b[idx]:
                    usada = capa["id"] in st.session_state.pri_baritas
                    label = f"{'✅ ' if usada else ''}{capa['nombre']}"
                    if st.button(label, key=f"pb{capa['id']}", use_container_width=True, disabled=usada):
                        st.session_state.pri_baritas.append(capa["id"])
                        st.rerun()

            if st.session_state.pri_baritas:
                if st.button("↩️ Deshacer barita", use_container_width=True, key="undo_pri"):
                    st.session_state.pri_baritas.pop()
                    st.rerun()

            st.download_button(
                "📥 Descargar .txt",
                data=txt_loteria(actuales).encode("utf-8"),
                file_name="primitiva_reducida.txt",
                mime="text/plain",
                use_container_width=True,
                type="primary",
            )


# ═══════════════════════════════════════════════
# 🌍 EUROMILLONES
# ═══════════════════════════════════════════════
elif seccion == "🌍 Euromillones":
    st.title("🌍 Euromillones")
    st.caption(f"5 números (1-50) + 2 estrellas (1-12) · {PRECIO_EUROMILLONES} €/apuesta")

    if "eu_nums" not in st.session_state:
        st.session_state.eu_nums = []
    if "eu_est" not in st.session_state:
        st.session_state.eu_est = []
    if "eu_combs" not in st.session_state:
        st.session_state.eu_combs = None
    if "eu_baritas" not in st.session_state:
        st.session_state.eu_baritas = []

    st.subheader("1️⃣ Números (1-50)")
    cols = st.columns(10)
    for n in range(1, 51):
        with cols[(n-1) % 10]:
            activo = n in st.session_state.eu_nums
            label = f"**{n}**" if activo else str(n)
            if st.button(label, key=f"en{n}", use_container_width=True):
                if activo: st.session_state.eu_nums.remove(n)
                else: st.session_state.eu_nums.append(n)
                st.rerun()

    st.subheader("2️⃣ Estrellas (1-12)")
    cols_e = st.columns(12)
    for n in range(1, 13):
        with cols_e[n-1]:
            activo = n in st.session_state.eu_est
            label = f"**⭐{n}**" if activo else f"⭐{n}"
            if st.button(label, key=f"ee{n}", use_container_width=True):
                if activo: st.session_state.eu_est.remove(n)
                else: st.session_state.eu_est.append(n)
                st.rerun()

    st.info(f"Números: {len(st.session_state.eu_nums)} → {sorted(st.session_state.eu_nums)}")
    st.info(f"Estrellas: {len(st.session_state.eu_est)} → {sorted(st.session_state.eu_est)}")

    c1, c2 = st.columns(2)
    if c1.button("🎲 Aleatorio", use_container_width=True, key="rand_eu"):
        st.session_state.eu_nums = random.sample(range(1, 51), 5)
        st.session_state.eu_est = random.sample(range(1, 13), 2)
        st.rerun()
    if c2.button("🗑️ Limpiar", use_container_width=True, key="clear_eu"):
        st.session_state.eu_nums = []
        st.session_state.eu_est = []
        st.session_state.eu_combs = None
        st.session_state.eu_baritas = []
        st.rerun()

    st.divider()

    if len(st.session_state.eu_nums) >= 5 and len(st.session_state.eu_est) >= 2:
        combs = generar_euromillones(st.session_state.eu_nums, st.session_state.eu_est)
        n_ap = len(combs)
        coste_dir = n_ap * PRECIO_EUROMILLONES

        st.subheader("3️⃣ Coste directo")
        c1, c2 = st.columns(2)
        c1.metric("Apuestas", f"{n_ap:,}")
        c2.metric("Coste", f"{coste_dir:,.2f} €")

        if st.button("✅ Generar", type="primary", use_container_width=True, key="gen_eu"):
            st.session_state.eu_combs = combs
            st.session_state.eu_baritas = []
            st.rerun()

        if st.session_state.eu_combs:
            st.divider()
            st.subheader("4️⃣ Barita Mágica 🪄")
            actuales = baritas_loteria(st.session_state.eu_combs, st.session_state.eu_baritas, MIN_EUROMILLONES)
            n_act = len(actuales)
            coste_act = n_act * PRECIO_EUROMILLONES

            st.markdown(f"""
                <div class="card" style="text-align:center;">
                    <div style="color:#a0a0b8;font-size:14px;">APUESTAS</div>
                    <div class="precio-grande">{n_act:,}</div>
                    <div style="color:#FFD700;font-size:32px;font-weight:800;">{coste_act:,.2f} €</div>
                </div>
            """, unsafe_allow_html=True)

            cols_b = st.columns(4)
            for idx, capa in enumerate(CAPAS_BARITA):
                with cols_b[idx]:
                    usada = capa["id"] in st.session_state.eu_baritas
                    label = f"{'✅ ' if usada else ''}{capa['nombre']}"
                    if st.button(label, key=f"eb{capa['id']}", use_container_width=True, disabled=usada):
                        st.session_state.eu_baritas.append(capa["id"])
                        st.rerun()

            if st.session_state.eu_baritas:
                if st.button("↩️ Deshacer barita", use_container_width=True, key="undo_eu"):
                    st.session_state.eu_baritas.pop()
                    st.rerun()

            st.download_button(
                "📥 Descargar .txt",
                data=txt_loteria(actuales).encode("utf-8"),
                file_name="euromillones_reducida.txt",
                mime="text/plain",
                use_container_width=True,
                type="primary",
            )


# ═══════════════════════════════════════════════
# 🤖 IA MAGIC
# ═══════════════════════════════════════════════
elif seccion == "🤖 IA Magic":
    st.title("🤖 IA Magic — Todo lo que hace la web")
    st.caption("Cómo funciona cada motor por dentro.")

    st.markdown("### 🧠 Probabilidades 1X2 y Pleno (Poisson)")
    st.write("""
1. Cada equipo tiene un **poder de ataque** y una **fuerza defensiva**.
2. Se calculan los **goles esperados (λ)** según las fuerzas y el factor campo (1.15 local / 0.85 visitante).
3. Con la **distribución de Poisson** se calcula la probabilidad de cada marcador (0-0, 1-0, 2-1…).
4. Se agrupan en **victoria local (1)**, **empate (X)**, **victoria visitante (2)**.
5. Para el **Pleno al 15**, se calcula la probabilidad de 0, 1, 2 y **M** (3 o más goles) por equipo.
""")

    st.markdown("### 🪄 Barita Mágica (reducción de coste)")
    for capa in CAPAS_BARITA:
        st.markdown(f"""
            <div class="card">
                <b>{capa['nombre']}</b><br>
                <span style="color:#a0a0b8;">
                Reduce aproximadamente al {int(capa['factor']*100)}% de las combinaciones.
                </span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("### 💶 Precios oficiales aplicados")
    st.table({
        "Juego": ["Quiniela", "Bonoloto", "Primitiva", "Euromillones"],
        "Precio": [f"{PRECIO_QUINIELA} €", f"{PRECIO_BONOLOTO} €", f"{PRECIO_PRIMITIVA} €", f"{PRECIO_EUROMILLONES} €"],
        "Mínimo": [f"{MIN_QUINIELA} apuestas", f"{MIN_BONOLOTO} apuestas", f"{MIN_PRIMITIVA} apuesta", f"{MIN_EUROMILLONES} apuesta"],
    })


# ═══════════════════════════════════════════════
# ⚙️ CUENTA
# ═══════════════════════════════════════════════
elif seccion == "⚙️ Cuenta":
    st.title("⚙️ Cuenta")
    st.markdown(f"""
    - **Plan:** Free (demo)
    - **Usuario:** privado
    - **Baritas disponibles:** 4 por juego
    - **Precios aplicados:** Quiniela {PRECIO_QUINIELA} € · Bonoloto {PRECIO_BONOLOTO} € · Primitiva {PRECIO_PRIMITIVA} € · Euromillones {PRECIO_EUROMILLONES} €
    """)
    if st.button("🚪 Cerrar sesión", use_container_width=True):
        st.session_state.autenticado = False
        st.rerun()
