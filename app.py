import streamlit as st

st.set_page_config(
    page_title="Quiniloto Magic",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# CSS
# ==================================================

st.markdown("""
<style>

.main-header{
    text-align:center;
    font-size:42px;
    font-weight:bold;
    color:#FFD700;
}

.card{
    padding:20px;
    border-radius:15px;
    background:#1f2937;
    color:white;
    text-align:center;
}

.small{
    font-size:14px;
    color:#d1d5db;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# CABECERA
# ==================================================

st.markdown(
    '<p class="main-header">🎯 Quiniloto Magic</p>',
    unsafe_allow_html=True
)

st.markdown(
    "### Plataforma Inteligente para Quinielas y Loterías"
)

# ==================================================
# DASHBOARD
# ==================================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "⚽ Quiniela",
        "14 partidos"
    )

with c2:
    st.metric(
        "🎲 Bonoloto",
        "Disponible"
    )

with c3:
    st.metric(
        "🍀 Primitiva",
        "Disponible"
    )

with c4:
    st.metric(
        "🌍 Euromillones",
        "Disponible"
    )

st.divider()

# ==================================================
# INFORMACION
# ==================================================

izq, der = st.columns([2, 1])

with izq:

    st.subheader("🚀 Funcionalidades")

    st.success("""
✅ Quiniela manual

✅ Quiniela automática

✅ Dobles y triples

✅ Cálculo de costes

✅ Barita Mágica

✅ Exportación TXT

✅ Bonoloto

✅ Primitiva

✅ Euromillones

✅ Estadísticas
""")

with der:

    st.info("""
📁 Páginas disponibles

⚽ Quiniela

🎲 Bonoloto

🍀 Primitiva

🌍 Euromillones

📈 Estadísticas

🤖 IA Magic
""")

st.divider()

# ==================================================
# COSTES RAPIDOS
# ==================================================

st.subheader("💶 Costes rápidos")

tabla = [
    ("1 Doble", 2, 1.50),
    ("2 Dobles", 4, 3.00),
    ("3 Dobles", 8, 6.00),
    ("4 Dobles", 16, 12.00),
    ("5 Dobles", 32, 24.00),
    ("6 Dobles", 64, 48.00),
    ("7 Dobles", 128, 96.00),
    ("8 Dobles", 256, 192.00)
]

for nombre, columnas, coste in tabla:

    st.write(
        f"• {nombre} → {columnas} columnas → {coste:.2f} €"
    )

st.divider()

# ==================================================
# REDUCCIONES
# ==================================================

st.subheader("📉 Sistemas Reducidos")

st.info("""
7 Dobles Reducidos

8 columnas

Coste aproximado: 6 €

--------------------------------

8 Dobles Reducidos

16 columnas

Coste aproximado: 12 €

--------------------------------

9 Dobles Reducidos

32 columnas

Coste aproximado: 24 €

--------------------------------

10 Dobles Reducidos

64 columnas

Coste aproximado: 48 €
""")

st.divider()

st.subheader("🪄 Barita Mágica")

st.write("""
La Barita Mágica genera reducciones automáticas para disminuir el número
de columnas y reducir el coste final de la apuesta.

Cada ejecución aplica un filtro distinto para proponer una combinación
más económica.
""")

st.success(
    "Selecciona una página en el menú lateral para comenzar."
)
