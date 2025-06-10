import pandas as pd
import plotly.express as px
import scipy.stats as stats
import numpy as np
import streamlit as st
from scipy.stats import f_oneway

# Carga de datos
st.title("🔬 Análisis del Cáncer Ocular")
st.write("En este proyecto analizaremos el dataset de cancer ocular, " \
        "el cual contiene datos sobre pacientes con esta enfermedad." \
        " El objetivo es realizar un análisis exploratorio y visualización de los datos.")
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
        El cáncer ocular es una enfermedad poco común pero grave que afecta los tejidos del ojo y sus estructuras
        circundantes. Aunque su incidencia es menor en comparación con otros tipos de cáncer, puede comprometer 
        seriamente la visión e incluso la vida del paciente si no se detecta y trata a tiempo.

        Existen varios tipos de cáncer ocular, entre los que destacan el melanoma ocular, el retinoblastoma,el 
        carcinoma de células escamosas y el linfoma ocular. Cada uno de ellos afecta diferentes partes del ojo 
        y tiene características particulares. Por ejemplo, el melanoma ocular es el más frecuente en adultos y 
        se origina en las células productoras de pigmento, mientras que el retinoblastoma es un cáncer pediátrico 
        que afecta la retina.

        Los síntomas del cáncer ocular pueden variar dependiendo del tipo y la ubicación del tumor, pero algunos de
        los más comunes incluyen visión borrosa, pérdida de visión parcial, la presencia de manchas oscuras en el 
        campo visual, dolor ocular persistente, cambios en la forma o tamaño de la pupila y protuberancias visibles
        en el ojo o el párpado. Ante la aparición de cualquiera de estos signos, es fundamental acudir a un especialista 
        para una evaluación detallada.

        El diagnóstico temprano es clave para mejorar el pronóstico del paciente. Los médicos utilizan diversas pruebas,
         como la ecografía ocular, la resonancia magnética y la biopsia, para identificar la presencia de un tumor y determinar 
        su naturaleza. Una vez confirmado el diagnóstico, el tratamiento puede incluir cirugía, radioterapia, quimioterapia y 
        terapias dirigidas, dependiendo del tipo y la etapa de la enfermedad.

        Si bien no existen medidas específicas para prevenir el cáncer ocular, proteger los ojos de la exposición excesiva a la 
        radiación ultravioleta y realizar chequeos oftalmológicos periódicos pueden ser estrategias efectivas para detectar 
        anomalías a tiempo. Además, mantener un estilo de vida saludable ayuda a fortalecer el sistema inmunológico y reducir el 
        riesgo de desarrollar enfermedades oncológicas.

        El cáncer ocular es una condición seria, pero con un diagnóstico temprano y un tratamiento adecuado, las posibilidades 
        de recuperación pueden mejorar significativamente. La conciencia y la prevención juegan un papel fundamental en la protección
         de la salud visual. Mantenerse informado y consultar regularmente con un especialista es el mejor camino para cuidar nuestros
         ojos.
        """)

# Vista previa del dataset
st.header("📁 Vista previa del dataset")
st.dataframe(df.head())
st.markdown(f"**Total de registros:** {df.shape[0]} | **Columnas:** {df.shape[1]}")

# Selector de análisis
st.header("🔍 Selecciona el análisis que deseas realizar")
analisis = st.selectbox("Selecciona el análisis que deseas realizar:", [
    "Estado del paciente por tratamiento",
    "Influencia de los marcadores genéticos por tipo de cáncer",
    "Número de diagnósticos por año",
    "Número de pacientes por edad",
    "Efectividad del tratamiento segun el tipo de cáncer"
])

# Estado por tratamiento
if analisis == "Estado del paciente por tratamiento":
    st.subheader("📊 Estado del paciente por tratamiento")
    resultado_tratamiento = df.groupby(['Tipo de Tratamiento', 'Estado del Resultado']).size().reset_index(name='Cantidad')
    estados = resultado_tratamiento['Estado del Resultado'].unique()
    estado_seleccionado = st.selectbox("Selecciona el estado del resultado:", estados)
    df_estado = resultado_tratamiento[resultado_tratamiento['Estado del Resultado'] == estado_seleccionado]
    fig = px.pie(df_estado, names='Tipo de Tratamiento', values='Cantidad', title=f'Distribución de Pacientes - Estado: {estado_seleccionado}')
    st.plotly_chart(fig, use_container_width=True)

    tabla = pd.crosstab(df['Tipo de Tratamiento'], df['Estado del Resultado'])
    chi2, p, dof, _ = stats.chi2_contingency(tabla)
    st.write(f"Chi² = {chi2:.4f}, p-valor = {p:.4f}")
    conclusion = "Existe una asociación significativa entre tipo de tratamiento y el estado del paciente." if p < 0.05 else "No se encontró asociación significativa entre tratamiento y estado."
    st.info(conclusion)

# Marcadores genéticos
elif analisis == "Influencia de los marcadores genéticos por tipo de cáncer":
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
    conclusion = "Existe una relación significativa entre tipo de cáncer y marcador genético." if p < 0.05 else "No se encontró relación significativa entre los marcadores y tipos de cáncer."
    st.info(conclusion)

# Diagnósticos por año
elif analisis == "Número de diagnósticos por año":
    st.subheader("📆 Diagnósticos por año")
    diagnosticos = df['Año de diagnóstico'].value_counts().sort_index().reset_index()
    diagnosticos.columns = ['Año', 'Cantidad']
    fig = px.bar(diagnosticos, x='Año', y='Cantidad', text_auto=True)
    st.plotly_chart(fig, use_container_width=True)
    observed = diagnosticos['Cantidad'].values
    expected = [observed.sum() / len(observed)] * len(observed)
    chi2, p = stats.chisquare(f_obs=observed, f_exp=expected)
    st.write(f"Chi² = {chi2:.4f}, p-valor = {p:.4f}")
    conclusion = "La cantidad de diagnósticos varía significativamente entre los años." if p < 0.05 else "No hay diferencia significativa entre los años analizados."
    st.info(conclusion)

# Distribución de edad
elif analisis == "Número de pacientes por edad":
    st.subheader("📊 Distribución de edad")
    fig = px.histogram(df, x='Edad', nbins=20, title='Distribución de edad', text_auto=True)
    st.plotly_chart(fig, use_container_width=True)
    st.write(f"Media: {df['Edad'].mean():.2f} | Mediana: {df['Edad'].median():.2f} | Desviación estándar: {df['Edad'].std():.2f}")
    st.info("La distribución muestra un rango amplio de edades con una tendencia central clara, útil para evaluar riesgos por grupo etario.")

# Efectividad del tratamiento
elif analisis == "Efectividad del tratamiento segun el tipo de cáncer":
    st.subheader("💊 Efectividad del tratamiento")
    tipo = st.selectbox("Selecciona el tipo de cáncer:", df['Tipo de Cáncer'].unique())
    df_filtrado = df[df['Tipo de Cáncer'] == tipo]
    resumen = df_filtrado.groupby(['Tipo de Tratamiento', 'Estado del Resultado']).size().reset_index(name='Cantidad')
    resumen['Porcentaje'] = resumen.groupby('Tipo de Tratamiento')['Cantidad'].transform(lambda x: x / x.sum() * 100)
    fig = px.sunburst(resumen, path=['Tipo de Tratamiento', 'Estado del Resultado'], values='Porcentaje', title=f'Efectividad del tratamiento - {tipo}')
    st.plotly_chart(fig, use_container_width=True)
    if resumen.shape[0] >= 2:
        tabla = pd.crosstab(df_filtrado['Tipo de Tratamiento'], df_filtrado['Estado del Resultado'])
        chi2, p, dof, _ = stats.chi2_contingency(tabla)
        st.write(f"Chi² = {chi2:.4f}, p-valor = {p:.4f}")
        conclusion = "El tipo de tratamiento influye significativamente en los resultados del paciente." if p < 0.05 else "No se encontró relación significativa entre tratamiento y resultado en este tipo de cáncer."
        st.info(conclusion)
    else:
        st.warning("Datos insuficientes para prueba estadística")

# Conclusión general
st.header("📌 Conclusión General")
st.write("""
    Este análisis exploratorio del dataset de cáncer ocular ha permitido identificar patrones y relaciones significativas 
    entre las variables. Los resultados sugieren que el tipo de tratamiento y los marcadores genéticos tienen un impacto 
    considerable en el estado del paciente y la efectividad del tratamiento. Además, la distribución de diagnósticos por año 
    y la edad de los pacientes ofrecen una visión clara de la demografía afectada por esta enfermedad.

    La información obtenida es valiosa para mejorar la comprensión del cáncer ocular y puede servir como base para futuras 
    investigaciones y estrategias de tratamiento.
""")
#Sugerecnios y recomendaciones de diagnóstico tempreno
st.header("💡 Sugerencias y Recomendaciones")
st.write("""
    - **Chequeos regulares:** Realizar exámenes oftalmológicos periódicos para detectar cualquier anomalía a tiempo.
    - **Protección UV:** Usar gafas de sol con protección UV para reducir el riesgo de daño ocular.
    - **Educación:** Informar a los pacientes sobre los síntomas del cáncer ocular para que busquen atención médica temprana.
    - **Investigación continua:** Fomentar la investigación en tratamientos y diagnósticos para mejorar las tasas de supervivencia.
""")
