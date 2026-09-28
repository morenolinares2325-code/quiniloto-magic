import streamlit as st
import random
import pandas as pd

st.set_page_config(layout="wide")

PRECIO_COLUMNA = 0.75

st.title("⚽ Quiniela Magic")

# ====================================================
# PARTIDOS DEMO
# ====================================================

partidos = [
    "Real Madrid - Sevilla",
    "Barcelona - Valencia",
    "Betis - Villarreal",
    "Athletic - Getafe",
    "Atlético - Osasuna",
    "Celta - Girona",
    "Mallorca - Alavés",
    "Espanyol - Rayo",
    "Real Sociedad - Levante",
    "Elche - Oviedo",
    "Sporting - Racing",
    "Zaragoza - Cádiz",
    "Tenerife - Granada",
    "Las Palmas - Eibar",
]

# ====================================================
# APUESTA MANUAL
# ====================================================

tab1, tab2, tab3 = st.tabs(
    [
        "✍️ Manual",
        "🤖 Automática",
        "🪄 Barita Mágica",
    ]
)

# ====================================================
# MANUAL
# ====================================================

with tab1:

    st.subheader("Crear Quiniela Manual")

    seleccion = []

    for i, partido in enumerate(partidos):

        opciones = st.multiselect(
            f"{i+1}. {partido}",
            ["1", "X", "2"],
            default=["1"],
            key=f"manual_{i}"
        )

        seleccion.append(opciones)

    dobles = 0
    triples = 0

    for s in seleccion:

        if len(s) == 2:
            dobles += 1

        elif len(s) == 3:
            triples += 1

    columnas = (2 ** dobles) * (3 ** triples)

    coste = columnas * PRECIO_COLUMNA

    st.divider()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Dobles", dobles)
    c2.metric("Triples", triples)
    c3.metric("Columnas", columnas)
    c4.metric("Coste", f"{coste:.2f} €")

    texto = ""

    for s in seleccion:
        texto += "".join(s) + "\n"

    st.download_button(
        "📥 Descargar TXT",
        data=texto,
        file_name="quiniela_manual.txt",
        mime="text/plain"
    )

# ====================================================
# AUTOMATICA
# ====================================================

with tab2:

    st.subheader("Quiniela Automática")

    modo = st.selectbox(
        "Modo",
        [
            "Aleatoria",
            "Conservadora",
            "Arriesgada",
        ]
    )

    if st.button("Generar Quiniela"):

        resultado = []

        if modo == "Aleatoria":

            signos = ["1", "X", "2"]

            for _ in range(14):
                resultado.append(
                    random.choice(signos)
                )

        elif modo == "Conservadora":

            for _ in range(14):

                resultado.append(
                    random.choice(
                        [
                            "1",
                            "1",
                            "1",
                            "X",
                        ]
                    )
                )

        elif modo == "Arriesgada":

            for _ in range(14):

                resultado.append(
                    random.choice(
                        [
                            "1",
                            "X",
                            "2",
                            "2",
                        ]
                    )
                )

        txt = "\n".join(resultado)

        st.success("Quiniela generada")

        for n, signo in enumerate(resultado):

            st.write(
                f"Partido {n+1}: {signo}"
            )

        st.download_button(
            "📥 Descargar Automática",
            txt,
            file_name="quiniela_auto.txt",
            mime="text/plain"
        )

# ====================================================
# BARITA MAGICA
# ====================================================

with tab3:

    st.subheader("🪄 Barita Mágica")

    st.info(
        """
        La Barita Mágica genera combinaciones
        y reduce automáticamente el número
        de columnas para disminuir el coste.
        """
    )

    dobles_magic = st.slider(
        "Dobles",
        0,
        12,
        7
    )

    triples_magic = st.slider(
        "Triples",
        0,
        8,
        2
    )

    columnas_originales = (
        (2 ** dobles_magic)
        * (3 ** triples_magic)
    )

    coste_original = (
        columnas_originales
        * PRECIO_COLUMNA
    )

    st.write(
        f"Columnas originales: {columnas_originales}"
    )

    st.write(
        f"Coste original: {coste_original:.2f} €"
    )

    if st.button("🪄 Aplicar Barita"):

        porcentaje = random.randint(
            30,
            70
        )

        columnas_finales = int(
            columnas_originales
            * (100 - porcentaje)
            / 100
        )

        columnas_finales = max(
            columnas_finales,
            1
        )

        coste_final = (
            columnas_finales
            * PRECIO_COLUMNA
        )

        ahorro = (
            coste_original
            - coste_final
        )

        st.success(
            f"""
            Reducción aplicada: {porcentaje}%

            Columnas finales: {columnas_finales}

            Coste final: {coste_final:.2f} €

            Ahorro: {ahorro:.2f} €
            """
        )

# ====================================================
# TABLA COSTES
# ====================================================

st.divider()

st.subheader("💶 Tabla de Costes")

datos = []

for dobles in range(0, 11):

    columnas = 2 ** dobles

    coste = columnas * PRECIO_COLUMNA

    datos.append(
        [
            dobles,
            0,
            columnas,
            round(coste, 2)
        ]
    )

df = pd.DataFrame(
    datos,
    columns=[
        "Dobles",
        "Triples",
        "Columnas",
        "Coste (€)"
    ]
)

st.dataframe(
    df,
    use_container_width=True
)

# ====================================================
# REDUCCIONES HABITUALES
# ====================================================

st.divider()

st.subheader("📉 Reducciones Habituales")

reducciones = [
    ("7 Dobles Reducidos", 8),
    ("8 Dobles Reducidos", 16),
    ("9 Dobles Reducidos", 32),
    ("10 Dobles Reducidos", 64),
    ("11 Dobles Reducidos", 128),
    ("12 Dobles Reducidos", 256),
]

for nombre, columnas in reducciones:

    coste = columnas * PRECIO_COLUMNA

    st.info(
        f"{nombre} | {columnas} columnas | {coste:.2f} €"
    )
`
