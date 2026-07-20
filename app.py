import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
import PIL.Image

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

# Sidebar
st.sidebar.header("⚙️ Configuración del Pipeline")
dataset_option = st.sidebar.radio(
    "Seleccionar Origen de Datos:",
    ["Dataset Predeterminado (data/estudiantes.csv)", "Cargar Dataset Real (.csv)"]
)

ruta_datos = "data/estudiantes.csv"
if dataset_option == "Cargar Dataset Real (.csv)":
    uploaded_file = st.sidebar.file_uploader("Subir archivo CSV de estudiantes:", type=["csv"])
    if uploaded_file is not None:
        os.makedirs("data/temp", exist_ok=True)
        ruta_datos = os.path.join("data/temp", uploaded_file.name)
        with open(ruta_datos, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.sidebar.success(f"Archivo cargado: {uploaded_file.name}")

        # Auto-detectar y convertir si es un dataset externo
        try:
            df_test = pd.read_csv(ruta_datos)
            convertidor = ConvertidorDataset()
            if not convertidor.ya_es_compatible(df_test):
                tipo = convertidor.detectar_dataset(df_test)
                if tipo:
                    st.sidebar.info(f"🔍 Dataset detectado: **{tipo}**. Se convertirá automáticamente.")
                    ruta_datos = convertidor.convertir(ruta_datos)
                    st.sidebar.success(f"✅ Dataset convertido a formato compatible (11 columnas)")
                else:
                    st.sidebar.error("❌ Dataset no reconocido. Debe tener 11 columnas o ser un formato soportado (Kaggle Student Performance Factors / UCI Student Performance).")
        except Exception as e:
            st.sidebar.error(f"Error al analizar el archivo: {e}")

gzip_level = st.sidebar.slider("Nivel de Compresión Gzip:", min_value=1, max_value=9, value=9)

if st.sidebar.button("🚀 Ejecutar Pipeline Completo (7 Pasos)", type="primary"):
    with st.spinner("Ejecutando pipeline POO... procesando bloques y redes..."):
        pipeline = PipelineAcademico(ruta_datos=ruta_datos, nivel_gzip=gzip_level)
        pipeline.ejecutar()
    st.sidebar.success("✅ ¡Pipeline ejecutado exitosamente!")

st.sidebar.markdown("---")
st.sidebar.header("📁 Explorador de Resultados")
nivel_sel = st.sidebar.selectbox("Seleccionar Nivel de Análisis:", ["nivel_50", "nivel_25", "nivel_12.5", "global"])

# Tabs de navegación
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Datos & Limpieza", 
    "🗺️ Topologías MST & Heatmaps", 
    "🌳 Árboles Bayesianos", 
    "📈 Comparación Best vs Worst",
    "📄 Reporte Markdown & Word"
])

# TAB 1: DATOS
with tab1:
    st.header("📊 Dataset & Limpieza de Datos")
    if os.path.exists(ruta_datos):
        df_raw = pd.read_csv(ruta_datos)
        st.write(f"**Registros totales en el archivo:** {len(df_raw)} filas × {len(df_raw.columns)} columnas")
        st.dataframe(df_raw.head(10), use_container_width=True)
    else:
        st.warning("No se encontró el archivo CSV en la ruta especificada.")

# TAB 2: TOPOLOGÍAS
with tab2:
    st.header("🗺️ Topologías de Red (MST), Heatmaps y Dendrogramas")
    dir_graf = os.path.join("results", nivel_sel, "graficos") if nivel_sel != "global" else os.path.join("results", "global")
    
    if os.path.exists(dir_graf):
        archivos_png = [f for f in os.listdir(dir_graf) if f.endswith(".png")]
        
        # Filtros por tipo
        mst_files = [f for f in archivos_png if f.startswith("mst_")]
        hm_files = [f for f in archivos_png if f.startswith("heatmap_")]
        dend_files = [f for f in archivos_png if f.startswith("dendrograma_")]
        
        block_sel = st.selectbox("Seleccionar Bloque:", sorted(list(set([f.replace("mst_", "").replace("heatmap_", "").replace("dendrograma_", "").replace(".png", "") for f in (mst_files + hm_files)]))))
        
        if block_sel:
            col_a, col_b = st.columns(2)
            path_mst = os.path.join(dir_graf, f"mst_{block_sel}.png")
            path_hm = os.path.join(dir_graf, f"heatmap_{block_sel}.png")
            path_dend = os.path.join(dir_graf, f"dendrograma_{block_sel}.png")
            
            with col_a:
                if os.path.exists(path_mst):
                    st.image(path_mst, caption=f"Árbol de Expansión Mínima (MST) - {block_sel}", use_column_width=True)
                if os.path.exists(path_dend):
                    st.image(path_dend, caption=f"Dendrograma Jerárquico - {block_sel}", use_column_width=True)
            
            with col_b:
                if os.path.exists(path_hm):
                    st.image(path_hm, caption=f"Matriz de Distancias NCD - {block_sel}", use_column_width=True)
    else:
        st.info("Ejecuta el pipeline desde el menú lateral para generar los gráficos.")

# TAB 3: ÁRBOLES BAYESIANOS
with tab3:
    st.header("🌳 Árboles Bayesianos Probabilísticos (Probabilidad Conjunta Máxima)")
    st.markdown("Redes dirigidas en donde las flechas representan la dependencia de probabilidad condicional entre factores.")
    
    dir_graf = os.path.join("results", nivel_sel, "graficos") if nivel_sel != "global" else os.path.join("results", "global")
    if os.path.exists(dir_graf):
        bayes_files = [f for f in os.listdir(dir_graf) if f.startswith("arbol_bayesiano_")]
        if bayes_files:
            b_sel = st.selectbox("Seleccionar Árbol Bayesiano:", bayes_files)
            path_bayes = os.path.join(dir_graf, b_sel)
            st.image(path_bayes, caption=f"Red Bayesiana: {b_sel}", use_column_width=True)
        else:
            st.warning("No se encontraron árboles bayesianos en este nivel.")
    else:
        st.info("Ejecuta el pipeline para visualizar las redes bayesianas.")

# TAB 4: COMPARACIÓN BEST VS WORST
with tab4:
    st.header("📈 Comparación Estructural Best vs Worst (Diferencia D)")
    
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
                st.image(ruta_img_comp, caption=f"Comparativa Grado Ponderado y D (Nivel {pct}%)", use_column_width=True)
                
    path_resumen = os.path.join("results", "global", "resumen_comparacion_global.png")
    if os.path.exists(path_resumen):
        st.markdown("---")
        st.subheader("Resumen Global de Diferencias Topológicas")
        st.image(path_resumen, use_column_width=True)

# TAB 5: REPORTE & DESCARGAS
with tab5:
    st.header("📄 Informe Técnico Final")
    ruta_md = "informe/informe_ncd_gzip.md"
    if os.path.exists(ruta_md):
        with open(ruta_md, "r", encoding="utf-8") as f:
            contenido_md = f.read()
        st.markdown(contenido_md)
        st.download_button("📥 Descargar Informe en Markdown (.md)", data=contenido_md, file_name="informe_ncd_gzip.md", mime="text/markdown")
    else:
        st.info("Ejecuta el pipeline para generar el informe técnico.")
