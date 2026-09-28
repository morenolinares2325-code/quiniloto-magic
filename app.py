import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.set_page_config(
    page_title="Quiniloto Magic",
    page_icon="🎯",
    layout="wide"
)

# ==========================
# CONFIG
# ==========================

FOOTBALL_API_KEY = st.secrets.get("FOOTBALL_API_KEY", "")
LOTERIA_API_KEY = st.secrets.get("LOTERIA_API_KEY", "")

# ==========================
# SIDEBAR
# ==========================

st.sidebar.title("🎯 Quiniloto Magic")

opcion = st.sidebar.radio(
    "Menú",
    [
        "🏠 Dashboard",
        "⚽ Quiniela",
        "🎲 Bonoloto",
        "🍀 Primitiva",
        "🌍 Euromillones",
        "📈 Estadísticas",
        "🤖 Barita Mágica"
    ]
)

# ==========================
# DASHBOARD
# ==========================

if opcion == "🏠 Dashboard":

    st.title("🎯 Quiniloto Magic")

    c1, c2, c3 = st.columns(3)

    c1.metric("💰 Euromillones", "Cargando...")
    c2.metric("💰 Primitiva", "Cargando...")
    c3.metric("💰 Bonoloto", "Cargando...")

    st.divider()

    st.subheader("Resumen")

    st.info("""
    Plataforma inteligente para:
    
    ✅ Quiniela
    ✅ Bonoloto
    ✅ Primitiva
    ✅ Euromillones
    ✅ Estadísticas
    ✅ Predicciones IA
    """)

# ==========================
# QUINIELA
# ==========================

elif opcion == "⚽ Quiniela":

    st.title("⚽ Quiniela")

    partidos_demo = pd.DataFrame(
        {
            "Partido":[
                "Real Madrid - Sevilla",
                "Barcelona - Valencia",
                "Betis - Villarreal",
                "Athletic - Getafe"
            ],
            "1":[65,72,45,58],
            "X":[20,15,30,24],
            "2":[15,13,25,18]
        }
    )

    st.dataframe(partidos_demo,use_container_width=True)

    st.subheader("Probabilidades")

    partido = st.selectbox(
        "Seleccione partido",
        partidos_demo["Partido"]
    )

    fila = partidos_demo[
        partidos_demo["Partido"] == partido
    ].iloc[0]

    fig = px.bar(
        x=["1","X","2"],
        y=[fila["1"],fila["X"],fila["2"]],
        title=partido
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    valor = max(fila["1"],fila["X"],fila["2"])

    if valor == fila["1"\]:
        recomendacion = "1"
    elif valor == fila["X"\]:
        recomendacion = "X"
    else:
        recomendacion = "2"

    st.success(
        f"✅ Recomendación: {recomendacion}"
    )

# ==========================
# BONOLOTO
# ==========================

elif opcion == "🎲 Bonoloto":

    st.title("🎲 Bonoloto")

    st.subheader("Último sorteo")

    st.info("15 - 23 - 25 - 33 - 34 - 43")

    calientes = pd.DataFrame(
        {
            "Número":[34,23,15,18,42],
            "Frecuencia":[420,412,408,405,401]
        }
    )

    st.dataframe(
        calientes,
        use_container_width=True
    )

# ==========================
# PRIMITIVA
# ==========================

elif opcion == "🍀 Primitiva":

    st.title("🍀 Primitiva")

    st.info(
        "Último resultado disponible"
    )

    numeros = [3,9,10,30,36,45]

    st.write(numeros)

# ==========================
# EUROMILLONES
# ==========================

elif opcion == "🌍 Euromillones":

    st.title("🌍 Euromillones")

    st.info(
        "11 - 12 - 15 - 38 - 49"
    )

    st.write(
        "⭐ Estrellas: 10 y 12"
    )

# ==========================
# ESTADISTICAS
# ==========================

elif opcion == "📈 Estadísticas":

    st.title("📈 Estadísticas")

    datos = pd.DataFrame(
        {
            "Número":[
                1,2,3,4,5,
                6,7,8,9,10
            ],
            "Frecuencia":[
                45,51,39,62,70,
                40,58,44,37,72
            ]
        }
    )

    fig = px.bar(
        datos,
        x="Número",
        y="Frecuencia",
        title="Frecuencia de aparición"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================
# IA
# ==========================

elif opcion == "🤖 Barita Mágica":

    st.title("🤖 Barita Mágica")

    if st.button(
        "🪄 Generar Quiniela"
    ):

        resultado = [
            "1","1","X","2",
            "1","1","2","X",
            "1","2","1","1",
            "X","2"
        ]

        for i,r in enumerate(
            resultado,
            start=1
        ):
            st.write(
                f"Partido {i}: {r}"
            )

    if st.button(
        "🎲 Generar Bonoloto"
    ):

        st.success(
            "4 - 11 - 18 - 27 - 34 - 46"
        )
