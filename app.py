import streamlit as st

st.set_page_config(
    page_title="Quiniloto Magic",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Quiniloto Magic")
st.subheader("Generador de reducciones para quinielas y loterías")

st.write("""
Bienvenido a Quiniloto Magic.
Aquí podrás generar combinaciones optimizadas
para quinielas y loterías.
""")

tipo = st.selectbox(
    "Seleccione juego",
    ["Quiniela", "Primitiva", "Bonoloto", "Euromillones"]
)

st.success(f"Juego seleccionado: {tipo}")
