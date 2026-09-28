import streamlit as st
import pandas as pd
import plotly.express as px
import random

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Quiniloto Magic",
    page_icon="🎯",
    layout="wide"
)

PRECIO_APUESTA = 0.75

# --------------------------------------------------
# FUNCIONES
# --------------------------------------------------

def calcular_coste(dobles, triples):
    apuestas = (2 ** dobles) * (3 ** triples)
    coste = apuestas * PRECIO_APUESTA
    return apuestas, coste


def generar_quiniela():
    signos = ["1", "X", "2"]
    return [random.choice(signos) for _ in range(14)]


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("🎯 Quiniloto Magic")

menu = st.sidebar.radio(
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

# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

if menu == "🏠 Dashboard":

    st.title("🎯 Quiniloto Magic")

    c1, c2, c3 = st.columns(3)

    c1.metric("Bonoloto", "1.200.000 €")
    c2.metric("Primitiva", "12.500.000 €")
    c3.metric("Euromillones", "75.000.000 €")

    st.markdown("---")

    st.subheader("Plataforma")

    st.success("""
    ✅ Quiniela

    ✅ Bonoloto

    ✅ Primitiva

    ✅ Euromillones

    ✅ Estadísticas

    ✅ Exportación TXT
    """)

# --------------------------------------------------
# QUINIELA
# --------------------------------------------------

elif menu == "⚽ Quiniela":

    st.title("⚽ Quiniela")

    partidos = pd.DataFrame({
        "Partido": [
            "Real Madrid - Sevilla",
            "Barcelona - Valencia",
            "Betis - Villarreal",
            "Athletic - Getafe",
            "Atlético - Osasuna"
        ],
        "1": [65, 72, 44, 58, 67],
        "X": [20, 15, 31, 24, 17],
        "2": [15, 13, 25, 18, 16]
    })

    st.dataframe(partidos, use_container_width=True)

    st.subheader("Probabilidades")

    partido = st.selectbox(
        "Seleccione un partido",
        partidos["Partido"]
    )

    fila = partidos[
        partidos["Partido"] == partido
    ].iloc[0]

    fig = px.bar(
        x=["1", "X", "2"],
        y=[
            fila["1"],
            fila["X"],
            fila["2"]
        ],
        labels={"x": "Signo", "y": "Probabilidad %"},
        title=partido
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    valor = max(
        fila["1"],
        fila["X"],
        fila["2"]
    )

    if valor == fila["1"\]:
        recomendacion = "1"
    elif valor == fila["X"\]:
        recomendacion = "X"
    else:
        recomendacion = "2"

    st.success(
        f"Recomendación: {recomendacion}"
    )

    st.markdown("---")

    st.subheader("Calculadora de Coste")

    dobles = st.number_input(
        "Dobles",
        0,
        14,
        0
    )

    triples = st.number_input(
        "Triples",
        0,
        14,
        0
    )

    apuestas, coste = calcular_coste(
        dobles,
        triples
    )

    c1, c2 = st.columns(2)

    c1.metric(
        "Nº Apuestas",
        apuestas
    )

    c2.metric(
        "Coste",
        f"{coste:.2f} €"
    )

    st.markdown("---")

    st.subheader("Sistemas Reducidos")

    reducciones = [
        ("7 Dobles Reducidos", 8),
        ("8 Dobles Reducidos", 16),
        ("9 Dobles Reducidos", 32),
        ("10 Dobles Reducidos", 64),
        ("11 Dobles Reducidos", 128)
    ]

    for nombre, columnas in reducciones:

        coste_red = columnas * PRECIO_APUESTA

        st.info(
            f"{nombre} | "
            f"{columnas} columnas | "
            f"{coste_red:.2f} €"
        )

# --------------------------------------------------
# BONOLOTO
# --------------------------------------------------

elif menu == "🎲 Bonoloto":

    st.title("🎲 Bonoloto")

    st.subheader("Último Sorteo")

    st.success(
        "15 - 23 - 25 - 33 - 34 - 43"
    )

    datos = pd.DataFrame({
        "Número": [34, 23, 15, 42, 18],
        "Frecuencia": [420, 412, 408, 405, 401]
    })

    st.dataframe(
        datos,
        use_container_width=True
    )

# --------------------------------------------------
# PRIMITIVA
# --------------------------------------------------

elif menu == "🍀 Primitiva":

    st.title("🍀 Primitiva")

    st.success(
        "03 - 09 - 10 - 30 - 36 - 45"
    )

    st.write(
        "Complementario: 26"
    )

    st.write(
        "Reintegro: 4"
    )

# --------------------------------------------------
# EUROMILLONES
# --------------------------------------------------

elif menu == "🌍 Euromillones":

    st.title("🌍 Euromillones")

    st.success(
        "11 - 12 - 15 - 38 - 49"
    )

    st.write(
        "Estrellas: 10 y 12"
    )

# --------------------------------------------------
# ESTADISTICAS
# --------------------------------------------------

elif menu == "📈 Estadísticas":

    st.title("📈 Estadísticas")

    df = pd.DataFrame({
        "Número": list(range(1, 11)),
        "Frecuencia": [
            44,
            52,
            60,
            48,
            72,
            39,
            55,
            46,
            35,
            67
        ]
    })

    fig = px.bar(
        df,
        x="Número",
        y="Frecuencia",
        title="Frecuencia números"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------------------------
# BARITA MAGICA
# --------------------------------------------------

elif menu == "🤖 Barita Mágica":

    st.title("🤖 Barita Mágica")

    if st.button(
        "🪄 Generar Quiniela"
    ):

        resultado = generar_quiniela()

        st.subheader("Resultado")

        texto = "\n".join(resultado)

        for n, signo in enumerate(resultado, start=1):
            st.write(
                f"Partido {n}: {signo}"
            )

        st.download_button(
            label="📥 Descargar TXT",
            data=texto,
            file_name="quiniela.txt",
            mime="text/plain"
        )

    if st.button(
        "🎲 Generar Bonoloto"
    ):

        numeros = random.sample(
            range(1, 50),
            6
        )

        numeros.sort()

        st.success(
            " - ".join(
                map(str, numeros)
            )
        )
