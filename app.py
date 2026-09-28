import streamlit as st

st.set_page_config(
    page_title="Quiniloto Magic",
    page_icon="🎯",
    layout="wide"
)

st.sidebar.title("🎯 Quiniloto Magic")

menu = st.sidebar.radio(
    "Menú",
    [
        "🏠 Inicio",
        "⚽ Quiniela",
        "🎲 Bonoloto",
        "🍀 Primitiva",
        "🌍 Euromillones",
        "🤖 Barita Mágica"
    ]
)

# ------------------------------------------------
# INICIO
# ------------------------------------------------

if menu == "🏠 Inicio":

    st.title("🎯 Quiniloto Magic")

    c1, c2, c3 = st.columns(3)

    c1.metric("Bonoloto", "Pendiente API")
    c2.metric("Primitiva", "Pendiente API")
    c3.metric("Euromillones", "Pendiente API")

    st.success("Sistema cargado correctamente")

# ------------------------------------------------
# QUINIELA
# ------------------------------------------------

elif menu == "⚽ Quiniela":

    st.title("⚽ Quiniela")

    st.write("Próximamente jornada automática")

# ------------------------------------------------
# BONOLOTO
# ------------------------------------------------

elif menu == "🎲 Bonoloto":

    st.title("🎲 Bonoloto")

    st.write("Pendiente conexión API")

# ------------------------------------------------
# PRIMITIVA
# ------------------------------------------------

elif menu == "🍀 Primitiva":

    st.title("🍀 Primitiva")

    st.write("Pendiente conexión API")

# ------------------------------------------------
# EUROMILLONES
# ------------------------------------------------

elif menu == "🌍 Euromillones":

    st.title("🌍 Euromillones")

    st.write("Pendiente conexión API")

# ------------------------------------------------
# BARITA MÁGICA
# ------------------------------------------------

elif menu == "🤖 Barita Mágica":

    st.title("🤖 Barita Mágica")

    st.write("Generador pendiente")
