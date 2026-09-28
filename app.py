# ══════════════════════════════════════════════════════════════
# 🎯 QUINILOTO MAGIC — Todo en uno
# Precio oficial apuesta: 0,75 € | Mínimo boleto: 2 apuestas (1,50 €)
# Modelo probabilidades: Poisson (sin API externa)
# ══════════════════════════════════════════════════════════════

import itertools
import math
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
# CONSTANTES
# ─────────────────────────────────────────────────
PASSWORD = "2325"
PRECIO_APUESTA = 0.75
MIN_APUESTAS = 2
COSTE_MINIMO = MIN_APUESTAS * PRECIO_APUESTA

CAPAS_BARITA = [
    {"id": 1, "nombre": "🪄 Poda básica",      "factor": 0.75},
    {"id": 2, "nombre": "🪄 Filtro histórico", "factor": 0.70},
    {"id": 3, "nombre": "🪄 Equilibrio",       "factor": 0.60},
    {"id": 4, "nombre": "🪄 Selección élite",  "factor": 0.55},
]

# Equipos por defecto con fuerzas (editables desde la interfaz)
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
.login-title {
    font-size: 42px;
    font-weight: 800;
    color: #FFD700;
    margin-bottom: 8px;
}
.login-sub { color: #a0a0b8; font-size: 14px; margin-bottom: 32px; }

.prob-1 { color: #4ade80; font-weight: 700; }
.prob-X { color: #facc15; font-weight: 700; }
.prob-2 { color: #f87171; font-weight: 700; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────
# LÓGICA QUINIELA
# ─────────────────────────────────────────────────
def generar_combinaciones(signos):
    opciones = [list(s) for s in signos]
    return list(itertools.product(*opciones))


def coste(combinaciones, precio=PRECIO_APUESTA):
    return round(len(combinaciones) * precio, 2)


def aplicar_barita(combinaciones, nivel):
    if nivel < 1 or nivel > len(CAPAS_BARITA):
        return combinaciones
    capa = CAPAS_BARITA[nivel - 1]
    n = max(MIN_APUESTAS, int(len(combinaciones) * capa["factor"]))

    def score(c):
        unos = c.count("1")
        doses = c.count("2")
        return abs(unos - doses)

    return sorted(combinaciones, key=score)[:n]


def aplicar_baritas(combinaciones, niveles):
    res = list(combinaciones)
    for n in niveles:
        res = aplicar_barita(res, n)
    return res


def a_txt(combinaciones):
    return "\n".join("".join(c) for c in combinaciones)


# ─────────────────────────────────────────────────
# LÓGICA POISSON — Probabilidades 1X2
# ─────────────────────────────────────────────────
def poisson_probability(k, lam):
    return (lam ** k) * math.exp(-lam) / math.factorial(k)


def predecir_partido(lambda_local, lambda_visitante, max_goles=10):
    prob_1 = prob_X = prob_2 = 0.0
    for gl in range(max_goles + 1):
        for gv in range(max_goles + 1):
            p = poisson_probability(gl, lambda_local) * poisson_probability(gv, lambda_visitante)
            if gl > gv:
                prob_1 += p
            elif gl == gv:
                prob_X += p
            else:
                prob_2 += p
    return {
        "1": round(prob_1 * 100, 1),
        "X": round(prob_X * 100, 1),
        "2": round(prob_2 * 100, 1),
    }


def estimar_lambdas(equipo_local, equipo_visitante, equipos):
    local = equipos.get(equipo_local, {"ataque": 1.3, "defensa": 1.0})
    visit = equipos.get(equipo_visitante, {"ataque": 1.3, "defensa": 1.0})

    # Local juega en casa (factor 1.15), visitante fuera (factor 0.85)
    lam_local = local["ataque"] * visit["defensa"] * 1.15
    lam_visit = visit["ataque"] * local["defensa"] * 0.85
    return round(lam_local, 2), round(lam_visit, 2)


def signo_mas_probable(probs):
    return max(probs, key=probs.get)


# ─────────────────────────────────────────────────
# LOGIN
# ─────────────────────────────────────────────────
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown(
        """
        <div class="login-box">
            <div class="login-title">🎯 Quiniloto Magic</div>
            <div class="login-sub">Acceso privado</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
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


# ─────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────
if "signos" not in st.session_state:
    st.session_state.signos = ["1"] * 14
if "combinaciones" not in st.session_state:
    st.session_state.combinaciones = None
if "baritas" not in st.session_state:
    st.session_state.baritas = []
if "equipos" not in st.session_state:
    st.session_state.equipos = dict(EQUIPOS_DEFAULT)
if "partidos_equipos" not in st.session_state:
    # 14 partidos por defecto (local, visitante)
    st.session_state.partidos_equipos = [
        ("Real Madrid", "Barcelona"),
        ("Atlético", "Sevilla"),
        ("Valencia", "Betis"),
        ("Villarreal", "Athletic"),
        ("Real Sociedad", "Girona"),
        ("Osasuna", "Celta"),
        ("Rayo", "Mallorca"),
        ("Getafe", "Alavés"),
        ("Las Palmas", "Espanyol"),
        ("Leganés", "Valladolid"),
        ("Real Madrid", "Atlético"),
        ("Barcelona", "Sevilla"),
        ("Betis", "Villarreal"),
        ("Athletic", "Valencia"),
    ]


# ─────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🎯 Quiniloto Magic")
    st.markdown("---")
    seccion = st.radio(
        "Sección",
        [
            "🏠 Inicio",
            "⚽ Quiniela",
            "🧠 Probabilidades 1X2",
            "🎲 Bonoloto",
            "🍀 Primitiva",
            "🌍 Euromillones",
            "🤖 IA Magic",
            "⚙️ Cuenta",
        ],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.caption(f"Precio apuesta: {PRECIO_APUESTA} €")
    st.caption(f"Mínimo boleto: {COSTE_MINIMO:.2f} €")
    if st.button("🚪 Cerrar sesión", use_container_width=True):
        st.session_state.autenticado = False
        st.rerun()


# ═════════════════════════════════════════════════
# 🏠 INICIO
# ═════════════════════════════════════════════════
if seccion == "🏠 Inicio":
    st.markdown('<p class="main-header">🎯 Quiniloto Magic</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Plataforma Inteligente para Quinielas y Loterías</p>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("⚽ Quiniela",     "14 partidos")
    c2.metric("🧠 Poisson",      "1X2 en vivo")
    c3.metric("🎲 Loterías",     "3 módulos")
    c4.metric("🪄 Barita",       "4 capas")

    st.divider()

    info1, info2, info3 = st.columns(3)
    info1.metric("Precio por apuesta", f"{PRECIO_APUESTA:.2f} €")
    info2.metric("Mínimo por boleto",  f"{COSTE_MINIMO:.2f} €")
    info3.metric("Apuestas mínimas",   f"{MIN_APUESTAS}")

    st.divider()

    izq, der = st.columns([2, 1])
    with izq:
        st.subheader("🚀 ¿Qué puedes hacer aquí?")
        st.success("""
✅ Configurar tu quiniela partido a partido

✅ Calcular las **probabilidades 1X2** con modelo Poisson

✅ Aplicar dobles, triples y reducciones

✅ Usar la **Barita Mágica** para bajar el coste

✅ Descargar tu `.txt` listo para EduardoLosilla
""")
    with der:
        st.info("""
📁 Secciones

🏠 Inicio

⚽ Quiniela

🧠 Probabilidades 1X2

🎲 Bonoloto

🍀 Primitiva

🌍 Euromillones

🤖 IA Magic
""")

    st.divider()
    st.subheader("💶 Costes rápidos (precio oficial 0,75 €)")
    tabla = [
        ("1 doble", 2, 1.50), ("2 dobles", 4, 3.00),
        ("3 dobles", 8, 6.00), ("4 dobles", 16, 12.00),
        ("5 dobles", 32, 24.00), ("6 dobles", 64, 48.00),
        ("7 dobles", 128, 96.00), ("8 dobles", 256, 192.00),
    ]
    cols = st.columns(4)
    for i, (n, c, cost) in enumerate(tabla):
        with cols[i % 4]:
            st.metric(n, f"{c} apuestas", f"{cost:.2f} €")


# ═════════════════════════════════════════════════
# ⚽ QUINIELA
# ═════════════════════════════════════════════════
elif seccion == "⚽ Quiniela":
    st.title("⚽ Quiniela")
    st.caption(f"Precio oficial {PRECIO_APUESTA} €/apuesta · Mínimo {COSTE_MINIMO:.2f} €")

    st.subheader("1️⃣ Configura los partidos")
    opciones = ["1", "X", "2", "1X", "X2", "12", "1X2"]
    cols = st.columns(2)
    for i in range(14):
        with cols[i % 2]:
            st.session_state.signos[i] = st.selectbox(
                f"Partido {i+1}",
                opciones,
                index=opciones.index(st.session_state.signos[i]),
                key=f"p{i}",
            )

    st.divider()

    st.subheader("2️⃣ Coste directo")
    directas = generar_combinaciones(st.session_state.signos)
    c1, c2 = st.columns(2)
    c1.metric("Apuestas directas", f"{len(directas):,}")
    c2.metric("Coste directo", f"{coste(directas):,.2f} €")

    if st.button("🎯 Generar combinaciones", type="primary", use_container_width=True):
        st.session_state.combinaciones = directas
        st.session_state.baritas = []
        st.rerun()

    st.divider()

    if st.session_state.combinaciones:
        st.subheader("3️⃣ Barita Mágica 🪄")

        actuales = aplicar_baritas(
            st.session_state.combinaciones,
            st.session_state.baritas,
        )

        apuestas_actuales = len(actuales)
        coste_actual = coste(actuales)

        st.markdown(
            f"""
            <div class="card" style="text-align:center;">
                <div style="color:#a0a0b8;font-size:14px;">APUESTAS ACTUALES</div>
                <div class="precio-grande">{apuestas_actuales:,}</div>
                <div style="color:#a0a0b8;font-size:14px;margin-top:8px;">COSTE FINAL</div>
                <div style="color:#FFD700;font-size:32px;font-weight:800;">{coste_actual:,.2f} €</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if coste_actual < COSTE_MINIMO:
            st.warning(
                f"⚠️ Coste final ({coste_actual:.2f} €) por debajo del mínimo oficial "
                f"({COSTE_MINIMO:.2f} €). Añade más apuestas."
            )

        st.caption("Pulsa las baritas para bajar el coste. Cada una aplica un filtro distinto.")

        cols_b = st.columns(4)
        for idx, capa in enumerate(CAPAS_BARITA):
            with cols_b[idx]:
                usada = capa["id"] in st.session_state.baritas
                label = f"{'✅ ' if usada else ''}{capa['nombre']}"
                if st.button(
                    label,
                    key=f"b{capa['id']}",
                    use_container_width=True,
                    disabled=usada,
                ):
                    st.session_state.baritas.append(capa["id"])
                    st.rerun()

        if st.session_state.baritas:
            if st.button("↩️ Deshacer última barita", use_container_width=True):
                st.session_state.baritas.pop()
                st.rerun()

        st.divider()

        st.subheader("4️⃣ Descargar .txt")
        st.caption("Formato listo para pegar en EduardoLosilla.")
        st.download_button(
            "📥 Descargar .txt",
            data=a_txt(actuales).encode("utf-8"),
            file_name="quiniela_reducida.txt",
            mime="text/plain",
            use_container_width=True,
            type="primary",
        )

        with st.expander("👀 Ver primeras 20 apuestas"):
            preview = "\n".join("".join(c) for c in actuales[:20])
            st.code(preview, language=None)


# ═════════════════════════════════════════════════
# 🧠 PROBABILIDADES 1X2
# ═════════════════════════════════════════════════
elif seccion == "🧠 Probabilidades 1X2":
    st.title("🧠 Probabilidades 1X2")
    st.caption("Modelo Poisson — sin API externa, sin LLM, todo en local.")

    st.markdown("### 1️⃣ Configura los emparejamientos")
    st.caption("Elige local y visitante para cada uno de los 14 partidos.")

    equipos_disponibles = sorted(st.session_state.equipos.keys())

    for i in range(14):
        local_actual, visit_actual = st.session_state.partidos_equipos[i]
        cols = st.columns([1, 3, 3])

        cols[0].markdown(f"**#{i+1}**")
        local = cols[1].selectbox(
            "Local", equipos_disponibles,
            index=equipos_disponibles.index(local_actual) if local_actual in equipos_disponibles else 0,
            key=f"loc{i}",
        )
        visit = cols[2].selectbox(
            "Visitante", equipos_disponibles,
            index=equipos_disponibles.index(visit_actual) if visit_actual in equipos_disponibles else 1,
            key=f"vis{i}",
        )

        st.session_state.partidos_equipos[i] = (local, visit)

    st.divider()

    if st.button("📊 Calcular probabilidades", type="primary", use_container_width=True):
        st.subheader("📈 Resultados")
        for i, (local, visit) in enumerate(st.session_state.partidos_equipos):
            lam_l, lam_v = estimar_lambdas(local, visit, st.session_state.equipos)
            probs = predecir_partido(lam_l, lam_v)
            favorito = signo_mas_probable(probs)

            st.markdown(f"**Partido {i+1}: {local} vs {visit}**")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("1 (Local)",     f"{probs['1']}%")
            c2.metric("X (Empate)",    f"{probs['X']}%")
            c3.metric("2 (Visitante)", f"{probs['2']}%")
            c4.metric("Favorito",      favorito)

            st.caption(f"λ local = {lam_l} · λ visitante = {lam_v}")
            st.divider()

    st.divider()

    st.subheader("🔧 Editar fuerzas de equipos")
    st.caption("Modifica los valores de ataque y defensa para afinar el modelo.")
    with st.expander("Editar equipos"):
        for nombre in sorted(st.session_state.equipos.keys()):
            eq = st.session_state.equipos[nombre]
            cols = st.columns([3, 2, 2])
            cols[0].markdown(f"**{nombre}**")
            eq["ataque"] = cols[1].number_input(
                f"Ataque ({nombre})", 0.0, 5.0, eq["ataque"], 0.05,
                key=f"at_{nombre}", label_visibility="collapsed",
            )
            eq["defensa"] = cols[2].number_input(
                f"Defensa ({nombre})", 0.0, 5.0, eq["defensa"], 0.05,
                key=f"df_{nombre}", label_visibility="collapsed",
            )


# ═════════════════════════════════════════════════
# 🎲 BONOLOTO
# ═════════════════════════════════════════════════
elif seccion == "🎲 Bonoloto":
    st.title("🎲 Bonoloto")
    st.info("🚧 Módulo en construcción. Próximamente: generador de combinaciones y filtros.")


# ═════════════════════════════════════════════════
# 🍀 PRIMITIVA
# ═════════════════════════════════════════════════
elif seccion == "🍀 Primitiva":
    st.title("🍀 Primitiva")
    st.info("🚧 Módulo en construcción. Próximamente: generador de combinaciones y filtros.")


# ═════════════════════════════════════════════════
# 🌍 EUROMILLONES
# ═════════════════════════════════════════════════
elif seccion == "🌍 Euromillones":
    st.title("🌍 Euromillones")
    st.info("🚧 Módulo en construcción. Próximamente: generador de combinaciones y filtros.")


# ═════════════════════════════════════════════════
# 🤖 IA MAGIC
# ═════════════════════════════════════════════════
elif seccion == "🤖 IA Magic":
    st.title("🤖 IA Magic — La Barita Mágica")
    st.caption("Cómo funciona el sistema de reducción y probabilidades.")

    st.markdown("### 🧠 Modelo de probabilidades (Poisson)")
    st.write("""
Tu web calcula las probabilidades 1X2 con un modelo estadístico de **distribución de Poisson**:

1. Cada equipo tiene un **poder de ataque** y una **fuerza defensiva**.
2. Se calculan los **goles esperados (λ)** de cada equipo según sus fuerzas y el factor de campo.
3. Con Poisson se calcula la probabilidad de cada marcador posible (0-0, 1-0, 2-1…).
4. Se agrupan los marcadores en **victoria local (1)**, **empate (X)** y **victoria visitante (2)**.
""")

    st.markdown("### 🪄 Barita Mágica (reducción de coste)")
    for capa in CAPAS_BARITA:
        st.markdown(
            f"""
            <div class="card">
                <b>{capa['nombre']}</b><br>
                <span style="color:#a0a0b8;">
                Reduce aproximadamente al {int(capa['factor']*100)}% de las combinaciones.
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.success("👉 Ve a **⚽ Quiniela** o **🧠 Probabilidades 1X2** para probarlo.")


# ═════════════════════════════════════════════════
# ⚙️ CUENTA
# ═════════════════════════════════════════════════
elif seccion == "⚙️ Cuenta":
    st.title("⚙️ Cuenta")
    st.markdown(f"""
    - **Plan:** Free (demo)
    - **Usuario:** privado
    - **Baritas disponibles:** 4
    - **Precio apuesta:** {PRECIO_APUESTA} € (oficial SELAE)
    - **Mínimo boleto:** {COSTE_MINIMO:.2f} €
    - **Modelo de probabilidades:** Poisson (local)
    """)
    if st.button("🚪 Cerrar sesión", use_container_width=True):
        st.session_state.autenticado = False
        st.rerun()
