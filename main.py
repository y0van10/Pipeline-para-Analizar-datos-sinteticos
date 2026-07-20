"""
=============================================================
  PIPELINE POO: NCD/Gzip - Análisis Académico (Español)
=============================================================

USO PRINCIPAL (Interfaz Web Streamlit):
  python main.py

USO MODO CONSOLA / TERMINAL:
  python main.py --cli [ruta_csv] [columna_objetivo]

=============================================================
"""

import sys
import os
import subprocess

# Asegurar que el directorio del script sea el directorio de trabajo
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.pipeline_academico import PipelineAcademico

def ejecutar_cli():
    ruta_datos = sys.argv[2] if len(sys.argv) > 2 else "data/estudiantes.csv"
    col_objetivo = sys.argv[3] if len(sys.argv) > 3 else None

    print(f"🚀 Ejecutando Pipeline en modo Consola...")
    print(f"📂 Dataset: {ruta_datos}")
    if col_objetivo:
        print(f"🎯 Columna Objetivo: {col_objetivo}")

    pipeline = PipelineAcademico(
        ruta_datos=ruta_datos,
        nivel_gzip=9,
        col_objetivo=col_objetivo
    )
    pipeline.ejecutar()

def lanzar_streamlit():
    print("🌐 Iniciando Dashboard Interactivo en Streamlit (app.py)...")
    cmd = [sys.executable, "-m", "streamlit", "run", "app.py"]
    subprocess.run(cmd)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        ejecutar_cli()
    else:
        lanzar_streamlit()
