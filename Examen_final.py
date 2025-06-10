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

# Cargar dataset
df = pd.read_csv("eye_cancer_filtrado.csv")
df.columns = df.columns.str.strip()  # Elimina espacios extra en los nombres de columnas
#st.write("Columnas del DataFrame:", df.columns.tolist())  # Muestra los nombres para depuración

# Mostrar tabla de datos
st.subheader("Vista previa del dataset")
st.dataframe(df.head())

st.title("Analisis del estado del paciente por tipo de tratamiento.")
# Gráfico: Estado del resultado por tipo de tratamiento, uno para cada estado
resultado_tratamiento = df.groupby(['Tipo de Tratamiento', 'Estado del Resultado']).size().reset_index(name='Cantidad')
estados = resultado_tratamiento['Estado del Resultado'].unique()
figs = {}
# Crear los gráficos para cada estado
for estado in estados:
    df_estado = resultado_tratamiento[resultado_tratamiento['Estado del Resultado'] == estado]
    fig = px.bar(df_estado, x='Tipo de Tratamiento', y='Cantidad',
                 title=f'Número de Pacientes - Estado: {estado}',
                 labels={'Cantidad': 'Número de Pacientes'})
    figs[estado] = fig

# Selección del estado del resultado
estado_seleccionado = st.selectbox("Selecciona el estado del resultado:", estados)
# Mostrar el gráfico correspondiente
st.plotly_chart(figs[estado_seleccionado], use_container_width=True)

# Verifica si existe la columna 'Proporción', si no, la calcula como ejemplo
if "Proporción" not in df.columns:
    # Calcula la proporción de cada marcador genético por tipo de cáncer
    df_counts = df.groupby(["Tipo de Cáncer", "Marcadores genéticos"]).size().reset_index(name="count")
    total_por_cancer = df_counts.groupby("Tipo de Cáncer")["count"].transform("sum")
    df_counts["Proporción"] = df_counts["count"] / total_por_cancer
else:
    df_counts = df

# Gráfica de barras apiladas: proporción de marcadores genéticos por tipo de cáncer
fig_prop = px.bar(
    df_counts,
    x="Tipo de Cáncer",
    y="Proporción",
    color="Marcadores genéticos",
    barmode="stack",
    text_auto=True,
    title="Proporción de marcadores genéticos por tipo de cáncer"
)

# Gráfica de barras agrupadas: conteo de marcadores genéticos por tipo de cáncer
df_genetico_counts = df.groupby(["Tipo de Cáncer", "Marcadores genéticos"]).size().reset_index(name="count")
fig_geneticos = px.bar(
    df_genetico_counts,
    x="Tipo de Cáncer",
    y="count",
    color="Marcadores genéticos",
    barmode="group",
    text_auto=True,
    title="Distribución de tipos de cáncer según marcadores genéticos"
)

# Análisis estadístico: prueba de chi-cuadrado de independencia
tabla_cancer_genetico = pd.crosstab(df["Tipo de Cáncer"], df["Marcadores genéticos"])
chi2_gen, p_gen, dof_gen, expected_gen = stats.chi2_contingency(tabla_cancer_genetico)

# Conclusión
if p_gen < 0.05:
    conclusion_gen = "Se encontró una asociación estadísticamente significativa entre los marcadores genéticos y el tipo de cáncer diagnosticado (p < 0.05)."
else:
    conclusion_gen = "No se encontró una asociación estadísticamente significativa entre los marcadores genéticos y el tipo de cáncer diagnosticado (p ≥ 0.05)."

# Mostrar los resultados del análisis estadístico y gráficos en Streamlit
st.title("Análisis de Marcadores Genéticos y Tipos de Cáncer")

st.subheader("Proporción de marcadores genéticos por tipo de cáncer")
st.plotly_chart(fig_prop, use_container_width=True)

st.subheader("Distribución de tipos de cáncer según marcadores genéticos")
st.plotly_chart(fig_geneticos, use_container_width=True)

st.subheader("Prueba de Chi-cuadrado de independencia")
st.write(f"Chi2: {chi2_gen:.4f}, p-valor: {p_gen:.4f}, grados de libertad: {dof_gen}")
st.info(conclusion_gen)


import plotly.express as px
import scipy.stats as stats

# Asegurarse de que la columna de fecha es datetime
df['Fecha de diagnóstico'] = pd.to_datetime(df['Fecha de diagnóstico'])

# Cantidad de pacientes diagnosticados por año
df['Año de diagnóstico'] = df['Fecha de diagnóstico'].dt.year
diagnosticos_por_año = df['Año de diagnóstico'].value_counts().sort_index()
df_diagnosticos = diagnosticos_por_año.reset_index()
df_diagnosticos.columns = ['Año de diagnóstico', 'Cantidad']

# Gráfica de barras con plotly
fig_diag = px.bar(
    df_diagnosticos,
    x='Año de diagnóstico',
    y='Cantidad',
    text_auto=True,
    title='Cantidad de pacientes diagnosticados por año'
)
fig_diag.show()

# Análisis estadístico: ¿la cantidad de diagnósticos varía significativamente entre años?
# Prueba de chi-cuadrado sobre la frecuencia observada vs. uniforme
observed = df_diagnosticos['Cantidad'].values
expected = [observed.sum() / len(observed)] * len(observed)
chi2_diag, p_diag = stats.chisquare(f_obs=observed, f_exp=expected)

# Conclusión
if p_diag < 0.05:
    conclusion_diag = "Existe una diferencia estadísticamente significativa en la cantidad de pacientes diagnosticados entre los años (p < 0.05)."
else:
    conclusion_diag = "No se observa una diferencia estadísticamente significativa en la cantidad de pacientes diagnosticados entre los años (p ≥ 0.05)."

print(f"Chi2: {chi2_diag:.4f}, p-valor: {p_diag:.4f}")
print("Conclusión:", conclusion_diag)
# Mostrar el gráfico en Streamlit
st.title("Cantidad de Pacientes Diagnosticados por Año")
st.plotly_chart(fig_diag, use_container_width=True)
st.subheader("Análisis de la cantidad de pacientes diagnosticados por año")
st.write(f"Chi2: {chi2_diag:.4f}, p-valor: {p_diag:.4f}")
st.info(conclusion_diag)
# Análisis de la edad de los pacientes diagnosticados
st.title("Análisis de la Edad de los Pacientes Diagnosticados")
# Asegurarse de que la columna de edad es numérica
df['Edad'] = pd.to_numeric(df['Edad'], errors='coerce')
# Eliminar filas con edad NaN
df = df.dropna(subset=['Edad'])
# Histograma de la edad de los pacientes diagnosticados
fig_edad = px.histogram(
    df,
    x='Edad',
    nbins=20,
    title='Distribución de la Edad de los Pacientes Diagnosticados',
    labels={'Edad': 'Edad del Paciente'},
    text_auto=True
)
# Mostrar el gráfico en Streamlit
st.plotly_chart(fig_edad, use_container_width=True)
# Análisis estadístico: media, mediana y desviación estándar de la edad
media_edad = df['Edad'].mean()
mediana_edad = df['Edad'].median()
desviacion_edad = df['Edad'].std()
st.subheader("Estadísticas de la Edad de los Pacientes")
st.write(f"Media de Edad: {media_edad:.2f} años")
st.write(f"Mediana de Edad: {mediana_edad:.2f} años")
st.write(f"Desviación Estándar de Edad: {desviacion_edad:.2f} años")

# Análisis de la edad de los pacientes diagnosticados por tipo de cáncer
st.title("Análisis de la Edad de los Pacientes Diagnosticados por Tipo de Cáncer")
# Gráfico de caja de la edad por tipo de cáncer
fig_edad_cancer = px.box(
    df,
    x='Tipo de Cáncer',
    y='Edad',
    title='Distribución de la Edad de los Pacientes por Tipo de Cáncer',
    labels={'Edad': 'Edad del Paciente', 'Tipo de Cáncer': 'Tipo de Cáncer'},
    points='all'
)
# Mostrar el gráfico en Streamlit
st.plotly_chart(fig_edad_cancer, use_container_width=True)
# Análisis estadístico: ANOVA para comparar la edad entre tipos de cáncer
from scipy.stats import f_oneway
# Agrupar por tipo de cáncer y obtener las edades
grupos_edad = [group['Edad'].values for name, group in df.groupby('Tipo de Cáncer')]
# Realizar ANOVA
anova_result = f_oneway(*grupos_edad)
# Conclusión del ANOVA
if anova_result.pvalue < 0.05:
    conclusion_anova = "Existe una diferencia estadísticamente significativa en la edad de los pacientes diagnosticados entre los diferentes tipos de cáncer (p < 0.05)."
else:
        conclusion_anova = "No se observa una diferencia estadísticamente significativa en la edad de los pacientes diagnosticados entre los diferentes tipos de cáncer (p ≥ 0.05)."
# Mostrar resultados del ANOVA
st.subheader("Resultados del ANOVA")
st.write(f"F-statistic: {anova_result.statistic:.4f}, p-valor: {anova_result.pvalue:.4f}")
st.info(conclusion_anova)
# Análisis de la edad de los pacientes diagnosticados por tipo de tratamiento
st.title("Análisis de la Edad de los Pacientes Diagnosticados por Tipo de Tratamiento")
# Gráfico de caja de la edad por tipo de tratamiento
fig_edad_tratamiento = px.box(
    df,
    x='Tipo de Tratamiento',
    y='Edad',
    title='Distribución de la Edad de los Pacientes por Tipo de Tratamiento',
    labels={'Edad': 'Edad del Paciente', 'Tipo de Tratamiento': 'Tipo de Tratamiento'},
    points='all'
)
# Mostrar el gráfico en Streamlit
st.plotly_chart(fig_edad_tratamiento, use_container_width=True)
# Análisis estadístico: ANOVA para comparar la edad entre tipos de tratamiento
grupos_edad_tratamiento = [group['Edad'].values for name, group in df.groupby('Tipo de Tratamiento')]
anova_result_tratamiento = f_oneway(*grupos_edad_tratamiento)
# Conclusión del ANOVA para tratamiento
if anova_result_tratamiento.pvalue < 0.05:
    conclusion_anova_tratamiento = "Existe una diferencia estadísticamente significativa en la edad de los pacientes diagnosticados entre los diferentes tipos de tratamiento (p < 0.05)."
else:
        conclusion_anova_tratamiento = "No se observa una diferencia estadísticamente significativa en la edad de los pacientes diagnosticados entre los diferentes tipos de tratamiento (p ≥ 0.05)."
# Mostrar resultados del ANOVA para tratamiento
st.subheader("Resultados del ANOVA para Tratamiento")
st.write(f"F-statistic: {anova_result_tratamiento.statistic:.4f}, p-valor: {anova_result_tratamiento.pvalue:.4f}")
st.info(conclusion_anova_tratamiento)
# Análisis de la edad de los pacientes diagnosticados por estado del resultado
st.title("Análisis de la Edad de los Pacientes Diagnosticados por Estado del Resultado")
# Gráfico de caja de la edad por estado del resultado
fig_edad_estado = px.box(
    df,
    x='Estado del Resultado',
    y='Edad',
    title='Distribución de la Edad de los Pacientes por Estado del Resultado',
    labels={'Edad': 'Edad del Paciente', 'Estado del Resultado': 'Estado del Resultado'},
    points='all'
)
# Mostrar el gráfico en Streamlit
st.plotly_chart(fig_edad_estado, use_container_width=True)
# Análisis estadístico: ANOVA para comparar la edad entre estados del resultado
grupos_edad_estado = [group['Edad'].values for name, group in df.groupby('Estado del Resultado')]
anova_result_estado = f_oneway(*grupos_edad_estado)
# Conclusión del ANOVA para estado del resultado
if anova_result_estado.pvalue < 0.05:
    conclusion_anova_estado = "Existe una diferencia estadísticamente significativa en la edad de los pacientes diagnosticados entre los diferentes estados del resultado (p < 0.05)."
else:
        conclusion_anova_estado = "No se observa una diferencia estadísticamente significativa en la edad de los pacientes diagnosticados entre los diferentes estados del resultado (p ≥ 0.05)."
# Mostrar resultados del ANOVA para estado del resultado
st.subheader("Resultados del ANOVA para Estado del Resultado")
st.write(f"F-statistic: {anova_result_estado.statistic:.4f}, p-valor: {anova_result_estado.pvalue:.4f}")
st.info(conclusion_anova_estado)
# Análisis de la edad de los pacientes diagnosticados por género
st.title("Análisis de la Edad de los Pacientes Diagnosticados por Género")
# Gráfico de caja de la edad por género
fig_edad_genero = px.box(
    df,
    x='Género',
    y='Edad',
    title='Distribución de la Edad de los Pacientes por Género',
    labels={'Edad': 'Edad del Paciente', 'Género': 'Género'},
    points='all'
)
# Mostrar el gráfico en Streamlit
st.plotly_chart(fig_edad_genero, use_container_width=True)
# Análisis estadístico: ANOVA para comparar la edad entre géneros
grupos_edad_genero = [group['Edad'].values for name, group in df.groupby('Género')]
anova_result_genero = f_oneway(*grupos_edad_genero)
# Conclusión del ANOVA para género
if anova_result_genero.pvalue < 0.05:
    conclusion_anova_genero = "Existe una diferencia estadísticamente significativa en la edad de los pacientes diagnosticados entre los géneros (p < 0.05)."
else:
        conclusion_anova_genero = "No se observa una diferencia estadísticamente significativa en la edad de los pacientes diagnosticados entre los géneros (p ≥ 0.05)."
# Mostrar resultados del ANOVA para género
st.subheader("Resultados del ANOVA para Género")
st.write(f"F-statistic: {anova_result_genero.statistic:.4f}, p-valor: {anova_result_genero.pvalue:.4f}")
st.info(conclusion_anova_genero)



# Análisis de la efectividad del tratamiento según el tipo de cáncer con selector
st.title("Análisis de la Efectividad del Tratamiento según el Tipo de Cáncer")

# Selector de tipo de cáncer
tipos_cancer = df['Tipo de Cáncer'].unique()
tipo_cancer_seleccionado = st.selectbox("Selecciona el tipo de cáncer:", tipos_cancer)

# Filtrar el DataFrame por el tipo de cáncer seleccionado
df_filtrado = df[df['Tipo de Cáncer'] == tipo_cancer_seleccionado].copy()

if not df_filtrado.empty:
    # Contar resultados por tipo de tratamiento y estado del resultado
    resumen = df_filtrado.groupby(['Tipo de Tratamiento', 'Estado del Resultado']).size().reset_index(name='Cantidad')
    total_tratamiento = resumen.groupby('Tipo de Tratamiento')['Cantidad'].transform('sum')
    resumen['Porcentaje'] = resumen['Cantidad'] / total_tratamiento * 100

    # Considerar "Remisión" como el mejor estado
    mejor_estado = "En Remisión"
    resumen_mejor = resumen[resumen['Estado del Resultado'] == mejor_estado]

    # Si no existe "Remisión", muestra todos los estados
    if resumen_mejor.empty:
        st.warning(f"No hay pacientes con estado '{mejor_estado}' (recuperado) para este tipo de cáncer. Se muestran todos los estados.")
        fig = px.bar(
            resumen,
            x='Tipo de Tratamiento',
            y='Porcentaje',
            color='Estado del Resultado',
            barmode='group',
            title=f"Porcentaje de resultados por tipo de tratamiento para {tipo_cancer_seleccionado}",
            labels={'Porcentaje': 'Porcentaje (%)', 'Tipo de Tratamiento': 'Tipo de Tratamiento'}
        )
    else:
        fig = px.bar(
            resumen_mejor,
            x='Tipo de Tratamiento',
            y='Porcentaje',
            color='Tipo de Tratamiento',
            title=f"Porcentaje de pacientes en remisión por tipo de tratamiento para {tipo_cancer_seleccionado}",
            labels={'Porcentaje': 'Porcentaje en Remisión (%)', 'Tipo de Tratamiento': 'Tipo de Tratamiento'},
            text_auto=True
        )
    st.plotly_chart(fig, use_container_width=True)

    # Análisis estadístico: prueba de chi-cuadrado para comparar la distribución de estados entre tratamientos
    tabla = pd.crosstab(df_filtrado['Tipo de Tratamiento'], df_filtrado['Estado del Resultado'])
    if tabla.shape[0] > 1 and tabla.shape[1] > 1:
        chi2, p, dof, expected = stats.chi2_contingency(tabla)
        st.subheader("Prueba de Chi-cuadrado de independencia entre tratamiento y estado del resultado")
        st.write(f"Chi2: {chi2:.4f}, p-valor: {p:.4f}, grados de libertad: {dof}")
        if p < 0.05:
            conclusion = "Existe una asociación estadísticamente significativa entre el tipo de tratamiento y el estado del resultado (p < 0.05)."
        else:
            conclusion = "No se observa una asociación estadísticamente significativa entre el tipo de tratamiento y el estado del resultado (p ≥ 0.05)."
        st.info(conclusion)
    else:
        st.info("No hay suficientes datos para realizar una prueba de chi-cuadrado en este tipo de cáncer.")
else:
    st.warning("No hay datos para este tipo de cáncer.")

