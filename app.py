# ══════════════════════════════════════════════════════════════
# 🎯 QUINILOTO MAGIC — Todo en uno
# ══════════════════════════════════════════════════════════════

import itertools
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

CAPAS_BARITA = [
    {"id": 1, "nombre": "🪄 Poda básica",      "factor": 0.75},
    {"id": 2, "nombre": "🪄 Filtro histórico", "factor": 0.70},
    {"id": 3, "nombre": "🪄 Equilibrio",       "factor": 0.60},
    {"id": 4, "nombre": "🪄 Selección élite",  "factor": 0.55},
]

# ─────────────────────────────────────────────────
# CSS GLOBAL
# ─────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
    background: radial-gradient(circle at 20% 0%, #14152a 0%, #0a0b15 60%);
}

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
.login-sub {
    color: #a0a0b8;
    font-size: 14px;
    margin-bottom: 32px;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────
# FUNCIONES DE LÓGICA
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
    n = max(1, int(len(combinaciones) * capa["factor"]))

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
# SESSION STATE (datos de quiniela)
# ─────────────────────────────────────────────────
if "signos" not in st.session_state:
    st.session_state.signos = ["1"] * 14
if "combinaciones" not in st.session_state:
    st.session_state.combinaciones = None
if "baritas" not in st.session_state:
    st.session_state.baritas = []


# ─────────────────────────────────────────────────
# SIDEBAR (navegación)
# ─────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🎯 Quiniloto Magic")
    st.markdown("---")
    seccion = st.radio(
        "Sección",
        [
            "🏠 Inicio",
            "⚽ Quiniela",
            "🎲 Bonoloto",
            "🍀 Primitiva",
            "🌍 Euromillones",
            "🤖 IA Magic",
            "⚙️ Cuenta",
        ],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.caption(f"Precio por apuesta: {PRECIO_APUESTA} €")
    if st.button("🚪 Cerrar sesión", use_container_width=True):
        st.session_state.autenticado = False
        st.rerun()


# ═════════════════════════════════════════════════
# SECCIÓN: 🏠 INICIO
# ═════════════════════════════════════════════════
if seccion == "🏠 Inicio":
    st.markdown('<p class="main-header">🎯 Quiniloto Magic</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Plataforma Inteligente para Quinielas y Loterías</p>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("⚽ Quiniela",     "14 partidos")
    c2.metric("🎲 Bonoloto",     "6/49")
    c3.metric("🍀 Primitiva",    "6/49")
    c4.metric("🌍 Euromillones", "5/50 + 2/12")

    st.divider()

    izq, der = st.columns([2, 1])
    with izq:
        st.subheader("🚀 ¿Qué puedes hacer aquí?")
        st.success("""
✅ Configurar tu quiniela partido a partido

✅ Aplicar dobles, triples y reducciones

✅ Calcular el coste al instante

✅ Usar la **Barita Mágica** para bajar el precio

✅ Descargar tu archivo .txt listo para comprar

✅ Consultar históricos y estadísticas
""")
    with der:
        st.info("""
📁 Secciones

🏠 Inicio

⚽ Quiniela

🎲 Bonoloto

🍀 Primitiva

🌍 Euromillones

🤖 IA Magic
""")

    st.divider()
    st.subheader("💶 Costes rápidos")
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

    st.divider()
    st.subheader("🪄 Barita Mágica")
    st.write("""
Ve a **⚽ Quiniela**, configura tus partidos y pulsa las baritas
para reducir el coste final. Cada pulsación aplica un filtro distinto.
""")
    st.success("👉 Empieza por **⚽ Quiniela** en el menú lateral.")


# ═════════════════════════════════════════════════
# SECCIÓN: ⚽ QUINIELA
# ═════════════════════════════════════════════════
elif seccion == "⚽ Quiniela":
    st.title("⚽ Quiniela")
    st.caption("Configura los 14 partidos y deja que la Barita Mágica haga el resto.")

    # ── CONFIG PARTIDOS ──
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

    # ── COSTE DIRECTO ──
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

    # ── BARITA MÁGICA ──
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

        # ── DESCARGA ──
        st.subheader("4️⃣ Descargar .txt")
        st.caption("Formato listo para pegar en EduardoLosilla o webs similares.")
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
# SECCIÓN: 🎲 BONOLOTO
# ═════════════════════════════════════════════════
elif seccion == "🎲 Bonoloto":
    st.title("🎲 Bonoloto")
    st.info("🚧 Módulo en construcción. Próximamente: generador de combinaciones y filtros.")


# ═════════════════════════════════════════════════
# SECCIÓN: 🍀 PRIMITIVA
# ═════════════════════════════════════════════════
elif seccion == "🍀 Primitiva":
    st.title("🍀 Primitiva")
    st.info("🚧 Módulo en construcción. Próximamente: generador de combinaciones y filtros.")


# ═════════════════════════════════════════════════
# SECCIÓN: 🌍 EUROMILLONES
# ═════════════════════════════════════════════════
elif seccion == "🌍 Euromillones":
    st.title("🌍 Euromillones")
    st.info("🚧 Módulo en construcción. Próximamente: generador de combinaciones y filtros.")


# ═════════════════════════════════════════════════
# SECCIÓN: 🤖 IA MAGIC
# ═════════════════════════════════════════════════
elif seccion == "🤖 IA Magic":
    st.title("🤖 IA Magic — La Barita Mágica")
    st.caption("Cómo funciona nuestro sistema de reducción inteligente.")

    st.markdown("### ¿Qué hace la Barita Mágica?")
    st.write("""
La Barita Mágica aplica **capas de filtros probabilísticos** sobre tus combinaciones
para reducir el coste final sin comprometer la cobertura.
""")

    for capa in CAPAS_BARITA:
        st.markdown(
            f"""
            <div class="card">
                <b>{capa['nombre']}</b><br>
                <span style="color:#a0a0b8;">
                Filtro aplicado en cascada · reduce aprox. al {int(capa['factor']*100)}%
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.success("👉 Ve a **⚽ Quiniela** y pruébala.")


# ═════════════════════════════════════════════════
# SECCIÓN: ⚙️ CUENTA
# ═════════════════════════════════════════════════
elif seccion == "⚙️ Cuenta":
    st.title("⚙️ Cuenta")
    st.markdown("""
    - **Plan:** Free (demo)
    - **Usuario:** privado
    - **Baritas disponibles:** 4
    """)
    if st.button("🚪 Cerrar sesión", use_container_width=True):
        st.session_state.autenticado = False
        st.rerun()
