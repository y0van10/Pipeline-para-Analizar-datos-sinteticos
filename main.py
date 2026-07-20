"""
=============================================================
  PIPELINE POO: NCD/Gzip - Análisis Académico (Español)
=============================================================

USO:
  python main.py

REQUISITOS:
  pip install -r requirements.txt
=============================================================
"""

import sys
import os

# Asegurar que el directorio del script sea el directorio de trabajo
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.pipeline_academico import PipelineAcademico

if __name__ == "__main__":
    # Inicializar el pipeline en base a la clase orquestadora POO en español
    pipeline = PipelineAcademico(
        ruta_datos="data/estudiantes.csv",
        nivel_gzip=9
    )
    
    # Iniciar ejecución
    pipeline.ejecutar()
