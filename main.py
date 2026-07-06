"""
=============================================================
  PIPELINE COMPLETO: NCD/Gzip - Análisis Académico
=============================================================
Ejecuta los 6 pasos del pipeline en secuencia:

  1. Limpieza de datos
  2. Particionamiento por rendimiento académico
  3. Cálculo de NCD/Gzip entre variables
  4. Construcción de topologías de red (MST)
  5. Comparación de topologías Best vs Worst
  6. Generación de informe de resultados

USO:
  python main.py

REQUISITOS:
  pip install -r requirements.txt
=============================================================
"""

import sys
import os
import time

# Asegurar que el directorio del script sea el directorio de trabajo
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


def separador(titulo):
    """Imprime un separador visual para cada etapa."""
    print("\n" + "█" * 60)
    print(f"  {titulo}")
    print("█" * 60)


def paso(numero, titulo, funcion, *args):
    """Ejecuta un paso del pipeline y mide el tiempo."""
    separador(f"PASO {numero}/6: {titulo}")
    inicio = time.time()
    resultado = funcion(*args)
    fin = time.time()
    print(f"\n   ⏱️  Tiempo del paso {numero}: {fin - inicio:.2f}s")
    return resultado


# ══════════════════════════════════════════════════════════
#   EJECUCIÓN DEL PIPELINE
# ══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("   🎓 PIPELINE NCD/Gzip - ANÁLISIS ACADÉMICO")
    print("   Cuantificación de Patrones de Comportamiento")
    print("=" * 60)

    inicio_total = time.time()

    # ── PASO 1: LIMPIEZA ──────────────────────────────────
    from src import _01_limpieza as p1
    df, reporte_limpieza = paso(1, "LIMPIEZA DE DATOS", p1.ejecutar)

    # ── PASO 2: PARTICIONAMIENTO ──────────────────────────
    from src import _02_particiones as p2
    particiones = paso(2, "PARTICIONAMIENTO POR RENDIMIENTO", p2.ejecutar, df)

    # ── PASO 3: NCD/GZIP ─────────────────────────────────
    from src import _03_ncd_gzip as p3
    matrices = paso(3, "CÁLCULO NCD/GZIP ENTRE VARIABLES", p3.ejecutar, particiones)

    # ── PASO 4: TOPOLOGÍAS ────────────────────────────────
    from src import _04_topologias as p4
    topologias = paso(4, "CONSTRUCCIÓN DE TOPOLOGÍAS (MST)", p4.ejecutar, matrices)

    # Dendrogramas comparativos Best vs Worst
    print("\n   🌳 Generando dendrogramas comparativos...")
    output_graficos = os.path.join(os.path.dirname(__file__), "results", "graficos")
    p4.graficar_dendrograma_comparativo(matrices, output_graficos)

    # ── PASO 5: COMPARACIÓN ───────────────────────────────
    from src import _05_comparacion as p5
    comparaciones = paso(5, "COMPARACIÓN BEST vs WORST", p5.ejecutar, topologias)

    # ── PASO 6: INFORME ──────────────────────────────────
    from src import _06_reporte_resultados as p6
    path_informe = paso(6, "GENERACIÓN DE INFORME",
                        p6.ejecutar, reporte_limpieza, particiones,
                        matrices, topologias, comparaciones)

    # ── RESUMEN FINAL ─────────────────────────────────────
    fin_total = time.time()

    print("\n" + "=" * 60)
    print(f"   ✅ PIPELINE COMPLETADO en {fin_total - inicio_total:.2f}s")
    print("=" * 60)
    print("""
   ARCHIVOS GENERADOS:
   ├── results/matrices/          → Matrices NCD 10×10 (6 archivos)
   ├── results/graficos/          → Gráficos MST, heatmaps, comparaciones
   ├── results/tablas/            → Particiones y tablas comparativas
   └── informe/
       └── informe_ncd_gzip.md   → Informe completo del experimento

   INTERPRETACIÓN:
   ┌──────────────────────────────────────────────────────┐
   │  X11 (Promedio Final) → CLASIFICA a los estudiantes │
   │  X1-X10 → Se analizan para encontrar las CAUSAS     │
   │  D = Grado_Worst - Grado_Best → CAMBIO por variable │
   │  D grande → Variable que más influye en rendimiento  │
   └──────────────────────────────────────────────────────┘
    """)
