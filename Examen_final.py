import pandas as pd
import plotly.express as px
import scipy.stats as stats
import numpy as np
import streamlit as st

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

import pandas as pd
import plotly.express as px
import scipy.stats as stats
import numpy as np
import streamlit as st
from scipy.stats import f_oneway

# Cargar dataset
df = pd.read_csv("eye_cancer_filtrado.csv")
df.columns = df.columns.str.strip()
df['Fecha de diagnóstico'] = pd.to_datetime(df['Fecha de diagnóstico'])
df['Año de diagnóstico'] = df['Fecha de diagnóstico'].dt.year
df['Edad'] = pd.to_numeric(df['Edad'], errors='coerce')
df = df.dropna(subset=['Edad'])

# Título principal
st.title("Análisis del Cáncer Ocular")
st.write("Exploración del dataset médico de pacientes con distintos tipos de cáncer ocular.")

# --- Selector en la barra lateral ---
opcion = st.sidebar.selectbox(
    "Selecciona el análisis que deseas visualizar:",
    [
        "Información sobre el cáncer ocular",
        "Vista previa del dataset",
        "Tratamiento vs Estado del Paciente",
        "Marcadores Genéticos por Tipo de Cáncer",
        "Diagnósticos por Año",
        "Distribución de Edad",
        "Edad por Tipo de Cáncer"
    ]
)

# --- 1. Información sobre el cáncer ocular ---
if opcion == "Información sobre el cáncer ocular":
    st.subheader("¿Qué es el cáncer ocular?")
    st.write("""
    El cáncer ocular es una enfermedad poco común pero grave que afecta los tejidos del ojo...
    """)  # Puedes usar tu contenido completo aquí.
    st.image("https://eyecareguam.com/wp-content/uploads/2023/10/AdobeStock_515867330_ocular_tumors-1024x630.jpg")

# --- 2. Vista previa del dataset ---
elif opcion == "Vista previa del dataset":
    st.subheader("Vista previa del dataset")
    st.dataframe(df.head())

# --- 3. Tratamiento vs Estado del Paciente ---
elif opcion == "Tratamiento vs Estado del Paciente":
    st.subheader("Análisis del estado del paciente por tipo de tratamiento")
    resultado_tratamiento = df.groupby(['Tipo de Tratamiento', 'Estado del Resultado']).size().reset_index(name='Cantidad')
    estados = resultado_tratamiento['Estado del Resultado'].unique()
    figs = {}
    for estado in estados:
        df_estado = resultado_tratamiento[resultado_tratamiento['Estado del Resultado'] == estado]
        fig = px.bar(df_estado, x='Tipo de Tratamiento', y='Cantidad', title=f'Estado: {estado}')
        figs[estado] = fig
    estado_seleccionado = st.selectbox("Selecciona el estado del resultado:", estados)
    st.plotly_chart(figs[estado_seleccionado], use_container_width=True)

# --- 4. Marcadores Genéticos por Tipo de Cáncer ---
elif opcion == "Marcadores Genéticos por Tipo de Cáncer":
    st.subheader("Proporción de marcadores genéticos por tipo de cáncer")
    df_counts = df.groupby(["Tipo de Cáncer", "Marcadores genéticos"]).size().reset_index(name="count")
    total_por_cancer = df_counts.groupby("Tipo de Cáncer")["count"].transform("sum")
    df_counts["Proporción"] = df_counts["count"] / total_por_cancer

    fig_prop = px.bar(df_counts, x="Tipo de Cáncer", y="Proporción", color="Marcadores genéticos",
                      barmode="stack", text_auto=True)

    st.plotly_chart(fig_prop, use_container_width=True)

    fig_geneticos = px.bar(df_counts, x="Tipo de Cáncer", y="count", color="Marcadores genéticos",
                           barmode="group", text_auto=True)
    st.subheader("Distribución de tipos de cáncer según marcadores genéticos")
    st.plotly_chart(fig_geneticos, use_container_width=True)

    tabla = pd.crosstab(df["Tipo de Cáncer"], df["Marcadores genéticos"])
    chi2, p, dof, _ = stats.chi2_contingency(tabla)
    st.subheader("Prueba Chi-cuadrado de independencia")
    st.write(f"Chi2: {chi2:.4f}, p-valor: {p:.4f}")
    st.info("Se encontró una asociación significativa." if p < 0.05 else "No se encontró una asociación significativa.")

# --- 5. Diagnósticos por Año ---
elif opcion == "Diagnósticos por Año":
    st.subheader("Cantidad de pacientes diagnosticados por año")
    df_diagnosticos = df['Año de diagnóstico'].value_counts().sort_index().reset_index()
    df_diagnosticos.columns = ['Año de diagnóstico', 'Cantidad']
    fig_diag = px.bar(df_diagnosticos, x='Año de diagnóstico', y='Cantidad', text_auto=True)
    st.plotly_chart(fig_diag, use_container_width=True)

    observed = df_diagnosticos['Cantidad'].values
    expected = [observed.sum() / len(observed)] * len(observed)
    chi2_diag, p_diag = stats.chisquare(f_obs=observed, f_exp=expected)
    st.write(f"Chi2: {chi2_diag:.4f}, p-valor: {p_diag:.4f}")
    st.info("Diferencias significativas entre años." if p_diag < 0.05 else "No hay diferencias significativas.")

# --- 6. Distribución de Edad ---
elif opcion == "Distribución de Edad":
    st.subheader("Distribución de la Edad de los Pacientes Diagnosticados")
    fig_edad = px.histogram(df, x='Edad', nbins=20, title='Distribución de Edad', text_auto=True)
    st.plotly_chart(fig_edad, use_container_width=True)

    st.subheader("Estadísticas Descriptivas")
    st.write(f"Media: {df['Edad'].mean():.2f}")
    st.write(f"Mediana: {df['Edad'].median():.2f}")
    st.write(f"Desviación Estándar: {df['Edad'].std():.2f}")

# --- 7. Edad por Tipo de Cáncer ---
elif opcion == "Edad por Tipo de Cáncer":
    st.subheader("Edad de los Pacientes por Tipo de Cáncer")
    fig_edad_cancer = px.box(df, x='Tipo de Cáncer', y='Edad',
                             title='Distribución de Edad por Tipo de Cáncer',
                             points='all')
    st.plotly_chart(fig_edad_cancer, use_container_width=True)

    grupos_edad = [grupo['Edad'].values for _, grupo in df.groupby('Tipo de Cáncer')]
    anova_result = f_oneway(*grupos_edad)
    st.write(f"ANOVA F: {anova_result.statistic:.4f}, p-valor: {anova_result.pvalue:.4f}")
    st.info("Diferencias significativas entre grupos." if anova_result.pvalue < 0.05 else "No hay diferencias significativas.")
