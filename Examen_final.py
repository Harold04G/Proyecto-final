

import pandas as pd
import plotly.express as px
import scipy.stats as stats
import numpy as np
import streamlit as st
from scipy.stats import f_oneway

# Configuración de la página y estilos
st.set_page_config(page_title="Análisis de Cáncer Ocular", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #f5f9ff; }
    h1, h2, h3 { color: #003366; }
    .stPlotlyChart { padding: 10px; background: #ffffff; border-radius: 10px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); }
    .stDataFrame { background: #ffffff; border-radius: 10px; padding: 10px; }
    </style>
""", unsafe_allow_html=True)

# Carga de datos
st.title("🔬 Análisis del Cáncer Ocular")
df = pd.read_csv("eye_cancer_filtrado.csv")
df.columns = df.columns.str.strip()
df['Fecha de diagnóstico'] = pd.to_datetime(df['Fecha de diagnóstico'])
df['Año de diagnóstico'] = df['Fecha de diagnóstico'].dt.year
df['Edad'] = pd.to_numeric(df['Edad'], errors='coerce')
df = df.dropna(subset=['Edad'])

# Información general
st.header("📌 Información sobre el cáncer ocular")
st.image("https://eyecareguam.com/wp-content/uploads/2023/10/AdobeStock_515867330_ocular_tumors-1024x630.jpg")
with st.expander("Ver descripción completa"):
    st.write("""
    El cáncer ocular es una enfermedad poco común pero grave que afecta los tejidos del ojo...
    """)

# Vista previa del dataset
st.header("📁 Vista previa del dataset")
st.dataframe(df.head())
st.markdown(f"**Total de registros:** {df.shape[0]} | **Columnas:** {df.shape[1]}")

# Selector de análisis
analisis = st.selectbox("Selecciona el análisis que deseas realizar:", [
    "Estado por tratamiento",
    "Marcadores genéticos por tipo de cáncer",
    "Diagnósticos por año",
    "Distribución de edad",
    "Edad por tipo de cáncer",
    "Edad por tratamiento",
    "Edad por estado del resultado",
    "Edad por género",
    "Efectividad del tratamiento por tipo de cáncer"
])

# Estado por tratamiento
if analisis == "Estado por tratamiento":
    st.subheader("📊 Estado del paciente por tratamiento")
    resultado_tratamiento = df.groupby(['Tipo de Tratamiento', 'Estado del Resultado']).size().reset_index(name='Cantidad')
    estados = resultado_tratamiento['Estado del Resultado'].unique()
    estado_seleccionado = st.selectbox("Selecciona el estado del resultado:", estados)
    df_estado = resultado_tratamiento[resultado_tratamiento['Estado del Resultado'] == estado_seleccionado]
    fig = px.bar(df_estado, x='Tipo de Tratamiento', y='Cantidad', title=f'Número de Pacientes - Estado: {estado_seleccionado}', labels={'Cantidad': 'Número de Pacientes'}, color='Tipo de Tratamiento')
    st.plotly_chart(fig, use_container_width=True)

# Marcadores genéticos
elif analisis == "Marcadores genéticos por tipo de cáncer":
    st.subheader("🧬 Proporción de marcadores genéticos por tipo de cáncer")
    df_counts = df.groupby(["Tipo de Cáncer", "Marcadores genéticos"]).size().reset_index(name="count")
    total_por_cancer = df_counts.groupby("Tipo de Cáncer")["count"].transform("sum")
    df_counts["Proporción"] = df_counts["count"] / total_por_cancer
    fig_prop = px.bar(df_counts, x="Tipo de Cáncer", y="Proporción", color="Marcadores genéticos", barmode="stack", text_auto=True)
    st.plotly_chart(fig_prop, use_container_width=True)
    fig_gen = px.bar(df_counts, x="Tipo de Cáncer", y="count", color="Marcadores genéticos", barmode="group", text_auto=True)
    st.plotly_chart(fig_gen, use_container_width=True)
    tabla = pd.crosstab(df["Tipo de Cáncer"], df["Marcadores genéticos"])
    chi2, p, dof, _ = stats.chi2_contingency(tabla)
    st.write(f"Chi² = {chi2:.4f}, p-valor = {p:.4f}")
    st.info("Asociación significativa" if p < 0.05 else "No significativa")

# Diagnósticos por año
elif analisis == "Diagnósticos por año":
    st.subheader("📆 Diagnósticos por año")
    diagnosticos = df['Año de diagnóstico'].value_counts().sort_index().reset_index()
    diagnosticos.columns = ['Año', 'Cantidad']
    fig = px.bar(diagnosticos, x='Año', y='Cantidad', text_auto=True)
    st.plotly_chart(fig, use_container_width=True)
    observed = diagnosticos['Cantidad'].values
    expected = [observed.sum() / len(observed)] * len(observed)
    chi2, p = stats.chisquare(f_obs=observed, f_exp=expected)
    st.write(f"Chi² = {chi2:.4f}, p-valor = {p:.4f}")
    st.info("Diferencias significativas" if p < 0.05 else "Sin diferencias")

# Distribución de edad
elif analisis == "Distribución de edad":
    st.subheader("📊 Distribución de edad")
    fig = px.histogram(df, x='Edad', nbins=20, title='Distribución de edad', text_auto=True)
    st.plotly_chart(fig, use_container_width=True)
    st.write(f"Media: {df['Edad'].mean():.2f} | Mediana: {df['Edad'].median():.2f} | Desviación estándar: {df['Edad'].std():.2f}")

# Comparaciones por categorías
elif analisis.startswith("Edad por"):
    categoria = analisis.replace("Edad por ", "")
    st.subheader(f"📈 Edad por {categoria}")
    fig = px.box(df, x=categoria, y='Edad', points='all', title=f'Distribución de Edad por {categoria}')
    st.plotly_chart(fig, use_container_width=True)
    grupos = [group['Edad'].values for _, group in df.groupby(categoria)]
    resultado = f_oneway(*grupos)
    st.write(f"ANOVA F = {resultado.statistic:.4f}, p-valor = {resultado.pvalue:.4f}")
    st.info("Diferencias significativas" if resultado.pvalue < 0.05 else "Sin diferencias significativas")

# Efectividad del tratamiento
elif analisis == "Efectividad del tratamiento por tipo de cáncer":
    st.subheader("💊 Efectividad del tratamiento")
    tipo = st.selectbox("Selecciona el tipo de cáncer:", df['Tipo de Cáncer'].unique())
    df_filtrado = df[df['Tipo de Cáncer'] == tipo]
    resumen = df_filtrado.groupby(['Tipo de Tratamiento', 'Estado del Resultado']).size().reset_index(name='Cantidad')
    resumen['Porcentaje'] = resumen.groupby('Tipo de Tratamiento')['Cantidad'].transform(lambda x: x / x.sum() * 100)
    fig = px.bar(resumen, x='Tipo de Tratamiento', y='Porcentaje', color='Estado del Resultado', barmode='group', text_auto=True)
    st.plotly_chart(fig, use_container_width=True)
    if resumen.shape[0] >= 2:
        tabla = pd.crosstab(df_filtrado['Tipo de Tratamiento'], df_filtrado['Estado del Resultado'])
        chi2, p, dof, _ = stats.chi2_contingency(tabla)
        st.write(f"Chi² = {chi2:.4f}, p-valor = {p:.4f}")
        st.info("Asociación significativa" if p < 0.05 else "No significativa")
    else:
        st.warning("Datos insuficientes para prueba estadística")
