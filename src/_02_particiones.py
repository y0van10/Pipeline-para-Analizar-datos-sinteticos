"""
=============================================================
  PASO 2: PARTICIONAMIENTO POR RENDIMIENTO ACADÉMICO
=============================================================
Ordena a los estudiantes por X11_promedio_final y crea
particiones Best (mejores) y Worst (peores) en tres niveles:

  - 12.5% superior vs 12.5% inferior
  - 25% superior   vs 25% inferior
  - 50% superior   vs 50% inferior

X11 es la variable de CLASIFICACIÓN: divide a los estudiantes
en grupos. Luego, las variables X1-X10 se analizarán con NCD
para descubrir QUÉ FACTORES causan o se asocian con un mejor
o peor rendimiento académico.
=============================================================
"""

import pandas as pd
import numpy as np
import os

# ── CONFIGURACIÓN ──────────────────────────────────────────
NIVELES_PARTICION = [0.125, 0.25, 0.50]  # 12.5%, 25%, 50%
VARIABLE_CORTE = "X11_promedio_final"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "results", "tablas")
# ───────────────────────────────────────────────────────────


def crear_particiones(df):
    """
    Ordena por promedio final y crea particiones Best/Worst
    para cada nivel porcentual.

    Retorna un diccionario:
    {
        "Best_12.5": DataFrame,
        "Worst_12.5": DataFrame,
        "Best_25.0": DataFrame,
        ...
    }
    """
    # Ordenar de mayor a menor promedio
    df_sorted = df.sort_values(VARIABLE_CORTE, ascending=False).reset_index(drop=True)
    n = len(df_sorted)

    particiones = {}

    print(f"\n   📊 Total de estudiantes: {n}")
    print(f"   📊 Promedio final - Rango: [{df[VARIABLE_CORTE].min():.2f}, {df[VARIABLE_CORTE].max():.2f}]")
    print()

    for nivel in NIVELES_PARTICION:
        pct_label = f"{nivel * 100:.1f}".rstrip('0').rstrip('.')
        k = int(n * nivel) #importante redondear hacia abajo para evitar problemas con decimales

        # Best = los k primeros (mayor promedio)
        best = df_sorted.head(k).copy()
        # Worst = los k últimos (menor promedio)
        worst = df_sorted.tail(k).copy()

        nombre_best = f"Best_{pct_label}"
        nombre_worst = f"Worst_{pct_label}"

        particiones[nombre_best] = best
        particiones[nombre_worst] = worst

        print(f"   {'─' * 50}")
        print(f"   📌 Partición {pct_label}% ({k} estudiantes por grupo)")
        print(f"      {nombre_best}:")
        print(f"         Promedio final: [{best[VARIABLE_CORTE].min():.2f} - {best[VARIABLE_CORTE].max():.2f}]")
        print(f"         Media: {best[VARIABLE_CORTE].mean():.2f}")
        print(f"      {nombre_worst}:")
        print(f"         Promedio final: [{worst[VARIABLE_CORTE].min():.2f} - {worst[VARIABLE_CORTE].max():.2f}]")
        print(f"         Media: {worst[VARIABLE_CORTE].mean():.2f}")
        print(f"      Diferencia de medias: {best[VARIABLE_CORTE].mean() - worst[VARIABLE_CORTE].mean():.2f}")

    return particiones


def guardar_particiones(particiones):
    """Guarda cada partición como archivo CSV."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"\n   💾 Guardando particiones en: {os.path.normpath(OUTPUT_DIR)}")
    for nombre, df_part in particiones.items():
        path = os.path.join(OUTPUT_DIR, f"{nombre}.csv")
        df_part.to_csv(path, index=False)
        print(f"      → {nombre}.csv ({len(df_part)} filas)")


def ejecutar(df):
    """Punto de entrada del paso 2."""
    print("\n   Creando particiones por rendimiento académico...")
    particiones = crear_particiones(df)

    guardar_particiones(particiones)

    print(f"\n   ✅ {len(particiones)} particiones generadas")
    print(f"      (Best y Worst para {len(NIVELES_PARTICION)} niveles: "
          f"{', '.join(str(int(n*100)) + '%' for n in NIVELES_PARTICION)})")

    return particiones


if __name__ == "__main__":
    print("=" * 55)
    print("  PASO 2: PARTICIONAMIENTO")
    print("=" * 55)
    from src.paso01_limpieza import ejecutar as limpiar
    df, _ = limpiar()
    ejecutar(df)
