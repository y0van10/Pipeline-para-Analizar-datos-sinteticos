import streamlit as st
import pandas as pd
import numpy as np
import os
import sys

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.pipeline_academico import PipelineAcademico
from src.convertidor_dataset import ConvertidorDataset

st.set_page_config(
    page_title="Pipeline POO NCD/Gzip & Redes Bayesianas",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🎓 Dashboard de Análisis Académico POO NCD/Gzip")
st.caption("Facultad de Ingeniería de Sistemas - UNA Puno | Ciberseguridad")

# ──────────────────────────────────────────────────
# SIDEBAR: Configuración
# ──────────────────────────────────────────────────
st.sidebar.header("⚙️ Configuración del Pipeline")
dataset_option = st.sidebar.radio(
    "Seleccionar Origen de Datos:",
    ["Dataset Predeterminado (data/estudiantes.csv)", "Cargar Cualquier Dataset (.csv)"]
)

ruta_datos = "data/estudiantes.csv"
necesita_mapeo = False

if dataset_option == "Cargar Cualquier Dataset (.csv)":
    uploaded_file = st.sidebar.file_uploader("Subir archivo CSV:", type=["csv"])
    if uploaded_file is not None:
        os.makedirs("data/temp", exist_ok=True)
        ruta_datos = os.path.join("data/temp", uploaded_file.name)
        with open(ruta_datos, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.sidebar.success(f"Archivo cargado: {uploaded_file.name}")

        # Verificar si necesita conversión
        try:
            df_test = pd.read_csv(ruta_datos)
        except UnicodeDecodeError:
            df_test = pd.read_csv(ruta_datos, encoding="latin-1")

        convertidor = ConvertidorDataset()
        if not convertidor.ya_es_compatible(df_test):
            necesita_mapeo = True
            st.sidebar.info(f"📋 Dataset cargado con **{df_test.shape[1]} columnas** y **{df_test.shape[0]} registros**. Selecciona qué columnas usar en la pestaña '🔄 Mapeo'.")
        else:
            st.sidebar.success("✅ Dataset compatible (11 columnas detectadas)")

gzip_level = st.sidebar.slider("Nivel de Compresión Gzip:", min_value=1, max_value=9, value=9)

# ──────────────────────────────────────────────────
# TABS principales
# ──────────────────────────────────────────────────
if necesita_mapeo:
    tab_map, tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔄 Mapeo de Columnas",
        "📊 Datos & Limpieza",
        "🗺️ Topologías MST & Heatmaps",
        "🌳 Árboles Bayesianos",
        "📈 Comparación Best vs Worst",
        "📄 Reporte"
    ])
else:
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Datos & Limpieza",
        "🗺️ Topologías MST & Heatmaps",
        "🌳 Árboles Bayesianos",
        "📈 Comparación Best vs Worst",
        "📄 Reporte"
    ])

# ──────────────────────────────────────────────────
# TAB MAPEO (solo si el dataset necesita conversión)
# ──────────────────────────────────────────────────
if necesita_mapeo:
    with tab_map:
        st.header("🔄 Mapeo Universal de Columnas")
        st.markdown("""
        Tu dataset tiene **columnas diferentes** a las 11 que el pipeline espera.  
        Selecciona qué columna de tu CSV corresponde a cada variable del pipeline.  
        El sistema **auto-sugiere** las mejores coincidencias basándose en los nombres.
        """)

        convertidor = ConvertidorDataset()
        try:
            df_ext = pd.read_csv(ruta_datos)
        except UnicodeDecodeError:
            df_ext = pd.read_csv(ruta_datos, encoding="latin-1")

        columnas_ext = ["(ninguna)"] + list(df_ext.columns)
        sugerencias = convertidor.auto_sugerir(list(df_ext.columns))

        st.subheader("📋 Vista previa del dataset cargado")
        st.dataframe(df_ext.head(5), use_container_width=True)
        st.caption(f"Dimensiones: {df_ext.shape[0]} filas × {df_ext.shape[1]} columnas")

        st.subheader("🎯 Asignar columnas")
        st.markdown("Para cada variable del pipeline, selecciona la columna correspondiente de tu dataset:")

        mapeo_usuario = {}
        col_izq, col_der = st.columns(2)

        for idx, var_destino in enumerate(convertidor.COLUMNAS_SALIDA):
            desc = convertidor.DESCRIPCIONES[var_destino]
            sugerida = sugerencias.get(var_destino, "(ninguna)")
            default_idx = columnas_ext.index(sugerida) if sugerida in columnas_ext else 0

            contenedor = col_izq if idx < 6 else col_der
            with contenedor:
                seleccion = st.selectbox(
                    f"**{var_destino}** — {desc}",
                    columnas_ext,
                    index=default_idx,
                    key=f"map_{var_destino}"
                )
                if seleccion != "(ninguna)":
                    mapeo_usuario[var_destino] = seleccion

        st.markdown("---")

        # Mostrar resumen del mapeo
        if mapeo_usuario:
            st.subheader("📌 Resumen del Mapeo Configurado")
            resumen_data = []
            for var_destino in convertidor.COLUMNAS_SALIDA:
                col_origen = mapeo_usuario.get(var_destino, "⚠️ Sin asignar (se usará valor por defecto)")
                resumen_data.append({"Variable Pipeline": var_destino, "Columna de tu CSV": col_origen})
            st.table(pd.DataFrame(resumen_data))

        # Botón para convertir y ejecutar
        if st.button("🚀 Convertir Dataset y Ejecutar Pipeline (7 Pasos)", type="primary"):
            if "X11_promedio_final" not in mapeo_usuario:
                st.error("❌ Debes asignar al menos la variable **X11_promedio_final** (nota/promedio final).")
            else:
                with st.spinner("Convirtiendo dataset y ejecutando pipeline..."):
                    ruta_convertido, df_convertido = convertidor.convertir_y_guardar(ruta_datos, mapeo_usuario)
                    st.success(f"✅ Dataset convertido: {df_convertido.shape[0]} filas × {df_convertido.shape[1]} columnas")
                    st.dataframe(df_convertido.head(5), use_container_width=True)

                    pipeline = PipelineAcademico(ruta_datos=ruta_convertido, nivel_gzip=gzip_level)
                    pipeline.ejecutar()
                st.success("✅ ¡Pipeline ejecutado exitosamente con tu dataset!")
                st.balloons()

# ──────────────────────────────────────────────────
# Botón de ejecución para datasets ya compatibles
# ──────────────────────────────────────────────────
if not necesita_mapeo:
    if st.sidebar.button("🚀 Ejecutar Pipeline Completo (7 Pasos)", type="primary"):
        with st.spinner("Ejecutando pipeline POO... procesando bloques y redes..."):
            pipeline = PipelineAcademico(ruta_datos=ruta_datos, nivel_gzip=gzip_level)
            pipeline.ejecutar()
        st.sidebar.success("✅ ¡Pipeline ejecutado exitosamente!")

st.sidebar.markdown("---")
st.sidebar.header("📁 Explorador de Resultados")
nivel_sel = st.sidebar.selectbox("Seleccionar Nivel de Análisis:", ["nivel_50", "nivel_25", "nivel_12.5", "global"])

# ──────────────────────────────────────────────────
# TAB 1: DATOS
# ──────────────────────────────────────────────────
with tab1:
    st.header("📊 Dataset & Limpieza de Datos")
    if os.path.exists(ruta_datos):
        try:
            df_raw = pd.read_csv(ruta_datos)
        except:
            df_raw = pd.read_csv(ruta_datos, encoding="latin-1")
        st.write(f"**Registros totales:** {len(df_raw)} filas × {len(df_raw.columns)} columnas")
        st.dataframe(df_raw.head(10), use_container_width=True)
    else:
        st.warning("No se encontró el archivo CSV.")

# ──────────────────────────────────────────────────
# TAB 2: TOPOLOGÍAS
# ──────────────────────────────────────────────────
with tab2:
    st.header("🗺️ Topologías de Red (MST), Heatmaps y Dendrogramas")
    dir_graf = os.path.join("results", nivel_sel, "graficos") if nivel_sel != "global" else os.path.join("results", "global")

    if os.path.exists(dir_graf):
        archivos_png = sorted([f for f in os.listdir(dir_graf) if f.endswith(".png")])

        mst_files = [f for f in archivos_png if f.startswith("mst_")]
        hm_files = [f for f in archivos_png if f.startswith("heatmap_")]

        bloques = sorted(list(set(
            [f.replace("mst_", "").replace("heatmap_", "").replace("dendrograma_", "").replace(".png", "")
             for f in (mst_files + hm_files)]
        )))

        if bloques:
            block_sel = st.selectbox("Seleccionar Bloque:", bloques)
            if block_sel:
                col_a, col_b = st.columns(2)
                path_mst = os.path.join(dir_graf, f"mst_{block_sel}.png")
                path_hm = os.path.join(dir_graf, f"heatmap_{block_sel}.png")
                path_dend = os.path.join(dir_graf, f"dendrograma_{block_sel}.png")

                with col_a:
                    if os.path.exists(path_mst):
                        st.image(path_mst, caption=f"MST - {block_sel}", use_column_width=True)
                    if os.path.exists(path_dend):
                        st.image(path_dend, caption=f"Dendrograma - {block_sel}", use_column_width=True)
                with col_b:
                    if os.path.exists(path_hm):
                        st.image(path_hm, caption=f"Heatmap NCD - {block_sel}", use_column_width=True)
    else:
        st.info("Ejecuta el pipeline para generar los gráficos.")

# ──────────────────────────────────────────────────
# TAB 3: ÁRBOLES BAYESIANOS
# ──────────────────────────────────────────────────
with tab3:
    st.header("🌳 Árboles Bayesianos Causales Jerárquicos")
    st.markdown("Redes dirigidas donde las flechas representan el flujo causal probabilístico.")

    dir_graf = os.path.join("results", nivel_sel, "graficos") if nivel_sel != "global" else os.path.join("results", "global")
    if os.path.exists(dir_graf):
        bayes_files = sorted([f for f in os.listdir(dir_graf) if f.startswith("arbol_bayesiano_")])
        radar_files = sorted([f for f in os.listdir(dir_graf) if f.startswith("radar_")])

        if bayes_files:
            b_sel = st.selectbox("Seleccionar Árbol Bayesiano:", bayes_files)
            st.image(os.path.join(dir_graf, b_sel), caption=f"Red Bayesiana: {b_sel}", use_column_width=True)

        if radar_files:
            st.subheader("🕸️ Gráficos de Radar (Telaraña)")
            for rf in radar_files:
                st.image(os.path.join(dir_graf, rf), caption=rf, use_column_width=True)
    else:
        st.info("Ejecuta el pipeline para visualizar las redes bayesianas.")

# ──────────────────────────────────────────────────
# TAB 4: COMPARACIÓN BEST vs WORST
# ──────────────────────────────────────────────────
with tab4:
    st.header("📈 Comparación Estructural Best vs Worst")

    if nivel_sel in ["nivel_50", "nivel_25", "nivel_12.5"]:
        pct = nivel_sel.replace("nivel_", "")
        ruta_csv_comp = os.path.join("results", nivel_sel, "tablas", f"comparacion_{pct}.csv")
        ruta_img_comp = os.path.join("results", nivel_sel, "graficos", f"comparacion_{pct}.png")

        col1, col2 = st.columns(2)
        with col1:
            if os.path.exists(ruta_csv_comp):
                df_c = pd.read_csv(ruta_csv_comp)
                st.subheader(f"Tabla de Diferencias D (Nivel {pct}%)")
                st.dataframe(df_c, use_container_width=True)
        with col2:
            if os.path.exists(ruta_img_comp):
                st.image(ruta_img_comp, caption=f"Comparativa (Nivel {pct}%)", use_column_width=True)

    path_resumen = os.path.join("results", "global", "resumen_comparacion_global.png")
    if os.path.exists(path_resumen):
        st.markdown("---")
        st.subheader("Resumen Global de Diferencias Topológicas")
        st.image(path_resumen, use_column_width=True)

# ──────────────────────────────────────────────────
# TAB 5: REPORTE
# ──────────────────────────────────────────────────
with tab5:
    st.header("📄 Informe Técnico Final")
    ruta_md = "informe/informe_ncd_gzip.md"
    if os.path.exists(ruta_md):
        with open(ruta_md, "r", encoding="utf-8") as f:
            contenido_md = f.read()
        st.markdown(contenido_md)
        st.download_button("📥 Descargar Informe (.md)", data=contenido_md, file_name="informe_ncd_gzip.md", mime="text/markdown")

    ruta_docx = "informe/Informe_NCD_Gzip_Ciberseguridad.docx"
    if os.path.exists(ruta_docx):
        with open(ruta_docx, "rb") as f:
            st.download_button("📥 Descargar Informe Word (.docx)", data=f, file_name="Informe_NCD_Gzip_Ciberseguridad.docx")
