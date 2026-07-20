import os
import sys

# ─────────────────────────────────────────────────────────────
# FIX CRÍTICO PYARROW / STREAMLIT LARGEUTF8 (Error 20 JS):
# Parchear PyArrow para que convierta 'large_string' a 'string' (utf8)
# evitando que el frontend JavaScript de Streamlit falle con "Unrecognized type: LargeUtf8"
# ─────────────────────────────────────────────────────────────
import pyarrow as pa
import pyarrow.lib as palib
import streamlit.elements.arrow as st_arrow

_orig_table_from_pandas = pa.Table.from_pandas

def _patched_table_from_pandas(df, *args, **kwargs):
    t = _orig_table_from_pandas(df, *args, **kwargs)
    new_fields = []
    need_cast = False
    for f in t.schema:
        if f.type == pa.large_string() or str(f.type) == 'large_string':
            new_fields.append(f.with_type(pa.string()))
            need_cast = True
        elif str(f.type).startswith('dictionary<values=large_string'):
            new_fields.append(f.with_type(pa.dictionary(f.type.index_type, pa.string(), f.type.ordered)))
            need_cast = True
        else:
            new_fields.append(f)
    if need_cast:
        new_schema = pa.schema(new_fields, metadata=t.schema.metadata)
        return t.cast(new_schema)
    return t

class _PatchedPyArrowTable:
    from_pandas = staticmethod(_patched_table_from_pandas)
    def __getattr__(self, name):
        return getattr(pa.Table, name)

pa.Table = _PatchedPyArrowTable
if hasattr(st_arrow, "pa"):
    st_arrow.pa.Table = _PatchedPyArrowTable

# ─────────────────────────────────────────────────────────────
import streamlit as st
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.pipeline_academico import PipelineAcademico

st.set_page_config(
    page_title="Pipeline NCD/Gzip — Análisis Académico",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🎓 Dashboard de Análisis Académico — NCD/Gzip")
st.caption("Facultad de Ingeniería de Sistemas · UNA Puno · Ciberseguridad")

# ──────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────
st.sidebar.header("⚙️ Configuración del Pipeline")

dataset_option = st.sidebar.radio(
    "Origen de Datos:",
    ["Dataset Predeterminado (data/estudiantes.csv)", "Cargar Cualquier CSV"]
)

ruta_datos   = "data/estudiantes.csv"
col_objetivo = None   # se detectará automáticamente si no se indica
df_cargado   = None

# ── Carga de archivo externo ──
if dataset_option == "Cargar Cualquier CSV":
    uploaded_file = st.sidebar.file_uploader("Subir archivo CSV:", type=["csv"])
    if uploaded_file is not None:
        os.makedirs("data/temp", exist_ok=True)
        ruta_datos = os.path.join("data/temp", uploaded_file.name)
        with open(ruta_datos, "wb") as f:
            f.write(uploaded_file.getbuffer())

        try:
            df_cargado = pd.read_csv(ruta_datos)
        except UnicodeDecodeError:
            df_cargado = pd.read_csv(ruta_datos, encoding="latin-1")

        st.sidebar.info(
            f"📋 **{uploaded_file.name}** cargado\n\n"
            f"🔢 {df_cargado.shape[0]} filas · {df_cargado.shape[1]} columnas"
        )

        # Selección de columna objetivo
        cols_num = df_cargado.select_dtypes(include="number").columns.tolist()
        if cols_num:
            keywords = ["score", "exam", "grade", "promedio", "final", "gpa",
                        "nota", "rendimiento", "resultado", "average", "mark"]
            sugerida = cols_num[-1]  # default: última numérica
            for kw in keywords:
                for c in cols_num:
                    if kw in c.lower():
                        sugerida = c
                        break

            col_objetivo = st.sidebar.selectbox(
                "🎯 Columna objetivo (la que se analizará como resultado):",
                cols_num,
                index=cols_num.index(sugerida),
                help="El pipeline usará esta columna para ordenar y particionar los registros (mejor→peor)."
            )
        else:
            st.sidebar.warning("⚠️ No se detectaron columnas numéricas en el CSV.")

# ── Dataset predeterminado ──
else:
    try:
        df_cargado = pd.read_csv(ruta_datos)
        col_objetivo = "X11_promedio_final"
        st.sidebar.info(f"📋 **estudiantes.csv** cargado\n\n🔢 {df_cargado.shape[0]} filas · {df_cargado.shape[1]} columnas")
    except Exception:
        st.sidebar.warning("Dataset predeterminado no encontrado.")

gzip_level = st.sidebar.slider("Nivel de Compresión Gzip:", min_value=1, max_value=9, value=9)

ejecutar = st.sidebar.button("🚀 Ejecutar Pipeline Completo (7 Pasos)", type="primary")

# ── Ejecución del pipeline ──
if ejecutar:
    if ruta_datos and col_objetivo:
        with st.spinner(f"Ejecutando pipeline con '{col_objetivo}' como variable objetivo..."):
            try:
                pipeline = PipelineAcademico(
                    ruta_datos=ruta_datos,
                    nivel_gzip=gzip_level,
                    col_objetivo=col_objetivo
                )
                pipeline.ejecutar()
                st.sidebar.success("✅ ¡Pipeline ejecutado exitosamente!")
                st.balloons()
            except Exception as e:
                st.sidebar.error(f"❌ Error: {e}")
                st.exception(e)
    else:
        st.sidebar.warning("Primero carga un CSV y selecciona la columna objetivo.")

st.sidebar.markdown("---")
st.sidebar.header("📁 Explorador de Resultados")
nivel_sel = st.sidebar.selectbox(
    "Seleccionar Nivel de Análisis:",
    ["nivel_50", "nivel_25", "nivel_12.5", "global"]
)

# ──────────────────────────────────────────────────
# TABS
# ──────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Datos & Limpieza",
    "🗺️ Topologías MST & Heatmaps",
    "🌳 Árboles Bayesianos",
    "📈 Comparación Best vs Worst",
    "📄 Reporte"
])

# ── TAB 1: DATOS ──
with tab1:
    st.header("📊 Dataset Cargado")
    if df_cargado is not None:
        st.write(f"**{df_cargado.shape[0]}** registros · **{df_cargado.shape[1]}** columnas")
        if col_objetivo:
            st.info(f"🎯 Variable objetivo seleccionada: **{col_objetivo}**")

        st.dataframe(df_cargado.head(15), use_container_width=True)

        st.subheader("📊 Estadísticas Descriptivas")
        st.dataframe(df_cargado.describe().reset_index(), use_container_width=True)
    else:
        st.info("Carga un CSV desde la barra lateral para ver los datos aquí.")

# ── TAB 2: TOPOLOGÍAS ──
with tab2:
    st.header("🗺️ Topologías de Red (MST), Heatmaps y Dendrogramas")
    dir_graf = (os.path.join("results", nivel_sel, "graficos")
                if nivel_sel != "global"
                else os.path.join("results", "global"))

    if os.path.exists(dir_graf):
        archivos_png = sorted([f for f in os.listdir(dir_graf) if f.endswith(".png")])
        mst_files  = [f for f in archivos_png if f.startswith("mst_")]
        hm_files   = [f for f in archivos_png if f.startswith("heatmap_")]

        bloques = sorted(list(set(
            f.replace("mst_", "").replace("heatmap_", "").replace("dendrograma_", "").replace(".png", "")
            for f in (mst_files + hm_files)
        )))

        if bloques:
            block_sel = st.selectbox("Seleccionar Bloque:", bloques)
            col_a, col_b = st.columns(2)
            path_mst  = os.path.join(dir_graf, f"mst_{block_sel}.png")
            path_hm   = os.path.join(dir_graf, f"heatmap_{block_sel}.png")
            path_dend = os.path.join(dir_graf, f"dendrograma_{block_sel}.png")

            with col_a:
                if os.path.exists(path_mst):
                    st.image(path_mst, caption=f"MST — {block_sel}", use_column_width=True)
                if os.path.exists(path_dend):
                    st.image(path_dend, caption=f"Dendrograma — {block_sel}", use_column_width=True)
            with col_b:
                if os.path.exists(path_hm):
                    st.image(path_hm, caption=f"Heatmap NCD — {block_sel}", use_column_width=True)
        else:
            st.info("Ejecuta el pipeline para generar los gráficos.")
    else:
        st.info("Ejecuta el pipeline primero.")

# ── TAB 3: BAYESIANOS ──
with tab3:
    st.header("🌳 Árboles Bayesianos Causales Jerárquicos")
    st.markdown("Redes dirigidas donde las **flechas** representan el flujo causal de probabilidad conjunta.")
    dir_graf = (os.path.join("results", nivel_sel, "graficos")
                if nivel_sel != "global"
                else os.path.join("results", "global"))

    if os.path.exists(dir_graf):
        bayes_files = sorted([f for f in os.listdir(dir_graf) if f.startswith("arbol_bayesiano_")])
        radar_files = sorted([f for f in os.listdir(dir_graf) if f.startswith("radar_")])

        if bayes_files:
            b_sel = st.selectbox("Seleccionar Árbol Bayesiano:", bayes_files)
            st.image(os.path.join(dir_graf, b_sel), caption=b_sel, use_column_width=True)
        else:
            st.info("Ejecuta el pipeline para visualizar los árboles bayesianos.")

        if radar_files:
            st.subheader("🕸️ Gráficos de Radar (Telaraña)")
            for rf in radar_files:
                st.image(os.path.join(dir_graf, rf), caption=rf, use_column_width=True)
    else:
        st.info("Ejecuta el pipeline primero.")

# ── TAB 4: COMPARACIÓN ──
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
                st.subheader(f"Tabla D — Nivel {pct}%")
                st.dataframe(df_c, use_container_width=True)
            else:
                st.info("Ejecuta el pipeline para ver la comparación.")
        with col2:
            if os.path.exists(ruta_img_comp):
                st.image(ruta_img_comp, caption=f"Comparativa Nivel {pct}%", use_column_width=True)

    path_resumen = os.path.join("results", "global", "resumen_comparacion_global.png")
    if os.path.exists(path_resumen):
        st.markdown("---")
        st.subheader("Resumen Global — Diferencias por Variable")
        st.image(path_resumen, use_column_width=True)

# ── TAB 5: REPORTE ──
with tab5:
    st.header("📄 Informe Técnico Final")
    ruta_md = "informe/informe_ncd_gzip.md"
    if os.path.exists(ruta_md):
        with open(ruta_md, "r", encoding="utf-8") as f:
            contenido_md = f.read()
        st.markdown(contenido_md)
        st.download_button(
            "📥 Descargar Informe (.md)",
            data=contenido_md,
            file_name="informe_ncd_gzip.md",
            mime="text/markdown"
        )
    else:
        st.info("Ejecuta el pipeline para generar el informe.")
