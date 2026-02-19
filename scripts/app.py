# ============================================
# Dashboard ENIGH - Consumo Energético
# Servicio Social IER - UNAM
# ============================================

import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --------------------------------------------
# Configuración general
# --------------------------------------------

st.set_page_config(
    page_title="Dashboard ENIGH",
    layout="wide"
)

st.title("📊 Análisis Multivariado del Consumo Energético")
st.markdown("Servicio Social - IER UNAM")

# --------------------------------------------
# Rutas dinámicas
# --------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RUTA_OUTPUTS = os.path.abspath(os.path.join(BASE_DIR, "..", "outputs"))
RUTA_ENIGH = os.path.abspath(os.path.join(BASE_DIR, "..", "ENIGH"))

# --------------------------------------------
# Función para cargar datos procesados
# --------------------------------------------

@st.cache_data
def cargar_datos_outputs():

    prep = pd.read_csv(os.path.join(RUTA_OUTPUTS, "01_preparacion_pca.csv"))
    componentes = pd.read_csv(os.path.join(RUTA_OUTPUTS, "02_componentes_pca.csv"))
    varianza = pd.read_csv(os.path.join(RUTA_OUTPUTS, "02_varianza_explicada_pca.csv"))
    nodos = pd.read_csv(os.path.join(RUTA_OUTPUTS, "03_red_nodos.csv"))
    aristas = pd.read_csv(os.path.join(RUTA_OUTPUTS, "03_red_aristas.csv"))
    centralidad = pd.read_csv(os.path.join(RUTA_OUTPUTS, "04_centralidad.csv"))

    return prep, componentes, varianza, nodos, aristas, centralidad


if os.path.exists(RUTA_OUTPUTS):
    try:
        prep, componentes, varianza, nodos, aristas, centralidad = cargar_datos_outputs()
    except:
        prep = componentes = varianza = nodos = aristas = centralidad = None
else:
    prep = componentes = varianza = nodos = aristas = centralidad = None


# --------------------------------------------
# Función para cargar cualquier CSV
# --------------------------------------------

@st.cache_data
def cargar_base(ruta):
    return pd.read_csv(ruta, low_memory=False)


# --------------------------------------------
# Navegación por pestañas
# --------------------------------------------

tab0, tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Exploración ENIGH",
    "📂 Datos Preparados",
    "📈 PCA",
    "🕸 Redes",
    "⭐ Centralidad",
    "📁 3.1 Dataset Maestro 2024"
])

# ============================================
# TAB 0 - Exploración dinámica ENIGH
# ============================================

with tab0:

    st.subheader("Exploración de Bases ENIGH")

    if os.path.exists(RUTA_ENIGH):

        anios_disponibles = sorted([
            carpeta for carpeta in os.listdir(RUTA_ENIGH)
            if os.path.isdir(os.path.join(RUTA_ENIGH, carpeta))
        ])

        if anios_disponibles:

            anio_seleccionado = st.selectbox("Selecciona año", anios_disponibles)

            ruta_anio = os.path.join(RUTA_ENIGH, anio_seleccionado)

            bases_disponibles = [
                archivo for archivo in os.listdir(ruta_anio)
                if archivo.endswith(".csv")
            ]

            if bases_disponibles:

                base_seleccionada = st.selectbox("Selecciona base", bases_disponibles)

                ruta_base = os.path.join(ruta_anio, base_seleccionada)

                df = cargar_base(ruta_base)

                st.write("Dimensiones del dataset:", df.shape)

                columnas_seleccionadas = st.multiselect(
                    "Selecciona columnas",
                    df.columns.tolist(),
                    default=df.columns[:5]
                )

                if columnas_seleccionadas:
                    df_filtrado = df[columnas_seleccionadas]
                    st.dataframe(df_filtrado.head())

                    st.download_button(
                        label="⬇️ Descargar base filtrada completa",
                        data=df_filtrado.to_csv(index=False).encode("utf-8"),
                        file_name=f"{base_seleccionada.replace('.csv','')}_{anio_seleccionado}_filtrado.csv",
                        mime="text/csv"
                    )

            else:
                st.warning("No se encontraron archivos CSV en este año.")
        else:
            st.warning("No se encontraron años dentro de ENIGH.")
    else:
        st.error("La carpeta ENIGH no existe en el proyecto.")


# ============================================
# TAB 1 - Datos preparados
# ============================================

with tab1:

    if prep is not None:
        st.subheader("Vista general de datos preparados")
        st.write("Dimensiones del dataset:", prep.shape)
        st.dataframe(prep.head())
    else:
        st.warning("No se encontraron archivos en outputs.")


# ============================================
# TAB 2 - PCA
# ============================================

with tab2:

    if varianza is not None:

        st.subheader("Varianza explicada por componente")

        fig_var = px.bar(
            varianza,
            x="Componente",
            y="Varianza_explicada",
            title="Varianza explicada por componente"
        )

        st.plotly_chart(fig_var, use_container_width=True)

        st.subheader("Varianza acumulada")

        fig_acum = px.line(
            varianza,
            x="Componente",
            y="Varianza_acumulada",
            markers=True,
            title="Varianza acumulada"
        )

        st.plotly_chart(fig_acum, use_container_width=True)

    else:
        st.warning("No se encontraron resultados de PCA.")


# ============================================
# TAB 3 - Redes
# ============================================

with tab3:

    if nodos is not None and aristas is not None:

        st.subheader("Información general de la red")

        col1, col2 = st.columns(2)
        col1.metric("Número de nodos", nodos.shape[0])
        col2.metric("Número de aristas", aristas.shape[0])

        st.dataframe(aristas.head())

    else:
        st.warning("No se encontraron resultados de red.")


# ============================================
# TAB 4 - Centralidad
# ============================================

with tab4:

    if centralidad is not None:

        st.subheader("Ranking de centralidad")

        tipo_centralidad = st.selectbox(
            "Selecciona tipo de centralidad",
            ["grado", "betweenness", "closeness"]
        )

        df_top = centralidad.sort_values(by=tipo_centralidad, ascending=False).head(10)

        fig_centralidad = px.bar(
            df_top,
            x="variable",
            y=tipo_centralidad,
            title=f"Top 10 Variables por {tipo_centralidad}"
        )

        st.plotly_chart(fig_centralidad, use_container_width=True)

    else:
        st.warning("No se encontraron resultados de centralidad.")


# ============================================
# TAB 5 - 3.1 Dashboard Dinámico Dataset Maestro
# ============================================

with tab5:

    st.subheader("3.1 - Dashboard Dinámico Dataset Maestro ENIGH 2024")

    archivos_disponibles = {
        "Estructura Familiar 2024": "estructura_familiar_2024.csv",
        "Dataset Maestro ENIGH 2024": "dataset_maestro_enigh_2024.csv"
    }

    seleccion = st.selectbox("Selecciona dataset", list(archivos_disponibles.keys()))

    ruta_archivo = os.path.join(RUTA_OUTPUTS, archivos_disponibles[seleccion])

    if os.path.exists(ruta_archivo):

        df = cargar_base(ruta_archivo)

        col1, col2 = st.columns(2)
        col1.metric("Filas", df.shape[0])
        col2.metric("Columnas", df.shape[1])

        st.dataframe(df.head())

        columnas_numericas = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

        if len(columnas_numericas) > 1:

            st.markdown("### 📊 Generador Automático de Gráficas")

            tipo_grafica = st.selectbox(
                "Selecciona tipo de gráfica",
                ["Dispersión", "Barras", "Boxplot", "Histograma"]
            )

            col_x = st.selectbox("Variable X", columnas_numericas)

            if tipo_grafica != "Histograma":
                col_y = st.selectbox("Variable Y", columnas_numericas)

            if tipo_grafica == "Dispersión":
                fig = px.scatter(df, x=col_x, y=col_y)

            elif tipo_grafica == "Barras":
                df_group = df.groupby(col_x)[col_y].mean().reset_index()
                fig = px.bar(df_group, x=col_x, y=col_y)

            elif tipo_grafica == "Boxplot":
                fig = px.box(df, x=col_x, y=col_y)

            elif tipo_grafica == "Histograma":
                fig = px.histogram(df, x=col_x, nbins=30)

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("No se detectaron suficientes variables numéricas para graficar.")

        st.download_button(
            label="⬇️ Descargar dataset completo",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name=archivos_disponibles[seleccion],
            mime="text/csv"
        )

    else:
        st.error("No se encontró el archivo en la carpeta outputs.")
