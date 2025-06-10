import pandas as pd
import plotly.express as px
import scipy.stats as stats
import numpy as np
import streamlit as st
from scipy.stats import f_oneway

st.title("Analisis del cancer ocular")
st.write("En este proyecto analizaremos el dataset de cancer ocular, " \
        "el cual contiene datos sobre pacientes con esta enfermedad." \
        " El objetivo es realizar un análisis exploratorio y visualización de los datos.")

#Infromacions sobre el cancer ocular
st.subheader("Informacion sobre el cancer ocular")
st.write("El cáncer ocular es una enfermedad poco común pero grave que afecta los tejidos del ojo" \
        " y sus estructuras circundantes. Aunque su incidencia es menor en comparación con otros tipos de " \
        "cáncer, puede comprometer seriamente la visión e incluso la vida del paciente si no se detecta y trata a tiempo.")
st.write("Existen varios tipos de cáncer ocular, entre los que destacan el melanoma ocular, el retinoblastoma," \
        "el carcinoma de células escamosas y el linfoma ocular. Cada uno de ellos afecta diferentes partes del ojo y" \
        " tiene características particulares. Por ejemplo, el melanoma ocular es el más frecuente en adultos y" \
        " se origina en las células productoras de pigmento, mientras que el retinoblastoma es un cáncer pediátrico" \
        " que afecta la retina.")
st.write("Los síntomas del cáncer ocular pueden variar dependiendo del tipo y la ubicación del tumor, pero algunos " \
        "de los más comunes incluyen visión borrosa, pérdida de visión parcial, la presencia de manchas oscuras en el" \
        " campo visual, dolor ocular persistente, cambios en la forma o tamaño de la pupila y protuberancias visibles" \
        " en el ojo o el párpado. Ante la aparición de cualquiera de estos signos, es fundamental acudir a un especialista" \
        " para una evaluación detallada.")
st.write("El diagnóstico temprano es clave para mejorar el pronóstico del paciente. Los médicos utilizan diversas pruebas," \
        " como la ecografía ocular, la resonancia magnética y la biopsia, para identificar la presencia de un tumor y determinar" \
        " su naturaleza. Una vez confirmado el diagnóstico, el tratamiento puede incluir cirugía, radioterapia, quimioterapia y" \
        " terapias dirigidas, dependiendo del tipo y la etapa de la enfermedad.")
st.write("Si bien no existen medidas específicas para prevenir el cáncer ocular, proteger los ojos de la exposición excesiva" \
        " a la radiación ultravioleta y realizar chequeos oftalmológicos periódicos pueden ser estrategias efectivas para " \
        "detectar anomalías a tiempo. Además, mantener un estilo de vida saludable ayuda a fortalecer el sistema inmunológico" \
        " y reducir el riesgo de desarrollar enfermedades oncológicas.")
st.write("El cáncer ocular es una condición seria, pero con un diagnóstico temprano y un tratamiento adecuado, las posibilidades" \
        " de recuperación pueden mejorar significativamente. La conciencia y la prevención juegan un papel fundamental en la " \
        "protección de la salud visual. Mantenerse informado y consultar regularmente con un especialista es el mejor camino " \
        "para cuidar nuestros ojos.")
st.image("https://eyecareguam.com/wp-content/uploads/2023/10/AdobeStock_515867330_ocular_tumors-1024x630.jpg")


# Título de la página
st.title("Análisis de Datos de Cáncer Ocular")
st.write("El análisis de un dataset sobre cáncer ocular es esencial para comprender mejor esta enfermedad poco común pero grave." \
        " Mediante el estudio de datos de pacientes, síntomas, factores de riesgo y tratamientos, se pueden identificar patrones " \
        "que ayuden a mejorar el diagnóstico temprano y la eficacia de los tratamientos disponibles. Además, el análisis epidemiológico" \
        " contribuye a determinar la prevalencia de la enfermedad en distintas poblaciones, lo que permite desarrollar estrategias de" \
        " prevención y concienciación. El uso de herramientas avanzadas de inteligencia artificial y estadística en el estudio de estos" \
        " datos también abre nuevas posibilidades para una medicina personalizada, ofreciendo soluciones adaptadas a cada paciente." \
        " La exploración de estos datos no solo optimiza la atención médica, sino que también impulsa el desarrollo de nuevas terapias" \
        " y enfoques para mejorar la calidad de vida de quienes padecen esta enfermedad.")

st.markdown("Exploración de un dataset médico de pacientes con distintos tipos de cáncer ocular.")


# -------------------------
# CONFIGURACIÓN VISUAL
# -------------------------
st.set_page_config(
    page_title="Análisis de Cáncer Ocular",
    page_icon="🧿",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        .main {
            background-color: #f7f9fc;
            color: #1f1f1f;
            font-family: 'Segoe UI', sans-serif;
        }
        h1, h2, h3, h4 {
            color: #00264d;
        }
        .stAlert, .stMarkdown, .stDataFrame, .stPlotlyChart {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 1em;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

# -------------------------
# CARGA Y PREPROCESAMIENTO
# -------------------------
st.sidebar.header("Configuración de análisis")
df = pd.read_csv("eye_cancer_filtrado.csv")
df.columns = df.columns.str.strip()
df['Fecha de diagnóstico'] = pd.to_datetime(df['Fecha de diagnóstico'])
df['Año de diagnóstico'] = df['Fecha de diagnóstico'].dt.year
df['Edad'] = pd.to_numeric(df['Edad'], errors='coerce')
df = df.dropna(subset=['Edad'])

# -------------------------
# MENÚ LATERAL DE NAVEGACIÓN
# -------------------------
opciones = [
    "Información general sobre el cáncer ocular",
    "Vista previa del dataset",
    "Análisis por tratamiento y estado",
    "Análisis de marcadores genéticos",
    "Diagnósticos por año",
    "Distribución de edad de pacientes",
    "Edad según atributos clínicos",
    "Efectividad del tratamiento por tipo de cáncer"
]

seleccion = st.sidebar.radio("Selecciona un análisis:", opciones)

# -------------------------
# INFORMACIÓN GENERAL
# -------------------------
if seleccion == opciones[0]:
    st.title("🧿 Información sobre el cáncer ocular")
    st.image("https://eyecareguam.com/wp-content/uploads/2023/10/AdobeStock_515867330_ocular_tumors-1024x630.jpg")
    with st.expander("Leer más sobre la enfermedad"):
        st.write("""
        El cáncer ocular es una enfermedad poco común pero grave que afecta los tejidos del ojo y sus estructuras circundantes...
        """)

# -------------------------
# PREVISUALIZACIÓN DEL DATASET
# -------------------------
elif seleccion == opciones[1]:
    st.title("📋 Vista previa del dataset")
    st.dataframe(df.head())
    st.success("Dimensiones del dataset: {} filas y {} columnas".format(df.shape[0], df.shape[1]))

# -------------------------
# ANÁLISIS POR TRATAMIENTO Y ESTADO
# -------------------------
elif seleccion == opciones[2]:
    st.title("📊 Análisis del estado del paciente por tratamiento")
    resultado_tratamiento = df.groupby(['Tipo de Tratamiento', 'Estado del Resultado']).size().reset_index(name='Cantidad')
    estados = resultado_tratamiento['Estado del Resultado'].unique()
    estado_seleccionado = st.selectbox("Selecciona el estado del resultado:", estados)
    df_estado = resultado_tratamiento[resultado_tratamiento['Estado del Resultado'] == estado_seleccionado]
    fig = px.bar(df_estado, x='Tipo de Tratamiento', y='Cantidad',
                 title=f'Número de Pacientes - Estado: {estado_seleccionado}',
                 labels={'Cantidad': 'Número de Pacientes'}, color='Tipo de Tratamiento')
    st.plotly_chart(fig, use_container_width=True)

# -------------------------
# ANÁLISIS DE MARCADORES GENÉTICOS
# -------------------------
elif seleccion == opciones[3]:
    st.title("🧬 Marcadores genéticos y tipos de cáncer")
    df_counts = df.groupby(["Tipo de Cáncer", "Marcadores genéticos"]).size().reset_index(name="count")
    total_por_cancer = df_counts.groupby("Tipo de Cáncer")["count"].transform("sum")
    df_counts["Proporción"] = df_counts["count"] / total_por_cancer

    fig_prop = px.bar(df_counts, x="Tipo de Cáncer", y="Proporción", color="Marcadores genéticos",
                      barmode="stack", text_auto=True, title="Proporción de marcadores genéticos")
    st.plotly_chart(fig_prop, use_container_width=True)

    fig_gen = px.bar(df_counts, x="Tipo de Cáncer", y="count", color="Marcadores genéticos",
                     barmode="group", text_auto=True, title="Distribución absoluta de marcadores")
    st.plotly_chart(fig_gen, use_container_width=True)

    tabla = pd.crosstab(df["Tipo de Cáncer"], df["Marcadores genéticos"])
    chi2, p, dof, _ = stats.chi2_contingency(tabla)
    st.info(f"Chi² = {chi2:.4f}, p-valor = {p:.4f}, df = {dof}")
    st.success("Hay asociación significativa." if p < 0.05 else "No hay asociación significativa.")

# -------------------------
# DIAGNÓSTICOS POR AÑO
# -------------------------
elif seleccion == opciones[4]:
    st.title("📅 Diagnósticos por año")
    diagnosticos_por_año = df['Año de diagnóstico'].value_counts().sort_index().reset_index()
    diagnosticos_por_año.columns = ['Año', 'Cantidad']
    fig = px.bar(diagnosticos_por_año, x='Año', y='Cantidad', text_auto=True,
                 title="Cantidad de diagnósticos por año")
    st.plotly_chart(fig, use_container_width=True)
    obs = diagnosticos_por_año['Cantidad'].values
    exp = [obs.sum() / len(obs)] * len(obs)
    chi2, p = stats.chisquare(f_obs=obs, f_exp=exp)
    st.info(f"Chi² = {chi2:.4f}, p-valor = {p:.4f}")
    st.success("Diferencias significativas" if p < 0.05 else "Sin diferencias significativas")

# -------------------------
# DISTRIBUCIÓN DE EDAD
# -------------------------
elif seleccion == opciones[5]:
    st.title("🎂 Distribución de edad")
    fig = px.histogram(df, x='Edad', nbins=20, title='Distribución de la edad')
    st.plotly_chart(fig, use_container_width=True)
    st.metric("Media", f"{df['Edad'].mean():.1f} años")
    st.metric("Mediana", f"{df['Edad'].median():.1f} años")
    st.metric("Desviación estándar", f"{df['Edad'].std():.1f} años")

# -------------------------
# EDAD SEGÚN ATRIBUTOS CLÍNICOS
# -------------------------
elif seleccion == opciones[6]:
    st.title("📈 Comparación de edad por atributos")
    opciones_atributos = ['Tipo de Cáncer', 'Tipo de Tratamiento', 'Estado del Resultado', 'Género']
    atributo = st.selectbox("Selecciona un atributo para comparar edades:", opciones_atributos)
    fig = px.box(df, x=atributo, y='Edad', points='all', title=f"Edad por {atributo}")
    st.plotly_chart(fig, use_container_width=True)
    grupos = [g['Edad'].values for _, g in df.groupby(atributo)]
    resultado = f_oneway(*grupos)
    st.info(f"ANOVA F = {resultado.statistic:.4f}, p-valor = {resultado.pvalue:.4f}")
    st.success("Diferencias significativas" if resultado.pvalue < 0.05 else "Sin diferencias significativas")

# -------------------------
# EFECTIVIDAD POR TIPO DE CÁNCER
# -------------------------
elif seleccion == opciones[7]:
    st.title("💊 Efectividad del tratamiento por tipo de cáncer")
    tipo = st.selectbox("Selecciona un tipo de cáncer:", df['Tipo de Cáncer'].unique())
    df_filtrado = df[df['Tipo de Cáncer'] == tipo]
    resumen = df_filtrado.groupby(['Tipo de Tratamiento', 'Estado del Resultado']).size().reset_index(name='Cantidad')
    resumen['Porcentaje'] = resumen.groupby('Tipo de Tratamiento')['Cantidad'].transform(lambda x: x / x.sum() * 100)

    fig = px.bar(resumen, x='Tipo de Tratamiento', y='Porcentaje', color='Estado del Resultado',
                 barmode='group', title=f'Efectividad del tratamiento para {tipo}', text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

    if resumen.shape[0] >= 2:
        tabla = pd.crosstab(df_filtrado['Tipo de Tratamiento'], df_filtrado['Estado del Resultado'])
        chi2, p, dof, _ = stats.chi2_contingency(tabla)
        st.info(f"Chi² = {chi2:.4f}, p-valor = {p:.4f}, df = {dof}")
        st.success("Asociación significativa" if p < 0.05 else "No hay asociación significativa")
    else:
        st.warning("No hay suficientes datos para realizar prueba estadística")

