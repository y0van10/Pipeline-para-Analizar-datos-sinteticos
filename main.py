"""
=============================================================
  PIPELINE POO: NCD/Gzip - Análisis Académico
=============================================================
Ejecuta el pipeline completo estructurado bajo el paradigma
de Programación Orientada a Objetos (POO).

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

from src.pipeline import AcademicPipeline

if __name__ == "__main__":
    # Inicializar el pipeline en base a la clase orquestadora POO
    pipeline = AcademicPipeline(
        dataset_path="data/estudiantes.csv",
        partition_levels=[0.125, 0.25, 0.50],
        gzip_level=9
    )
    
    # Iniciar ejecución
    pipeline.run()
