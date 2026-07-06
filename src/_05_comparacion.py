"""
=============================================================
  PASO 5: COMPARACIÓN DE TOPOLOGÍAS BEST vs WORST
=============================================================
Compara las redes MST entre grupos Best y Worst para cada
nivel de partición (12.5%, 25%, 50%).

Para cada variable calcula:
  D = GradoPonderado_Worst - GradoPonderado_Best

- D positivo grande → la variable AUMENTA su conexión en
  el grupo de bajo rendimiento (potencial factor de riesgo)
- D negativo grande → la variable DISMINUYE su conexión en
  el grupo de bajo rendimiento (potencial factor protector)
- D ≈ 0 → la variable mantiene su rol similar en ambos grupos

Esto revela QUÉ VARIABLES cambian su comportamiento entre
estudiantes de alto y bajo rendimiento, respondiendo la
pregunta: ¿Por qué algunos estudiantes tienen mejor promedio?
=============================================================
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ── CONFIGURACIÓN ──────────────────────────────────────────
NOMBRES_COMPLETOS = {
    "X1": "Sexo", "X2": "Zona", "X3": "Ciclo",
    "X4": "Ingreso", "X5": "Trabaja", "X6": "Beca",
    "X7": "Educ.Jefe", "X8": "Tam.Fam", "X9": "Asistencia",
    "X10": "Desaprobados"
}

OUTPUT_DIR_TABLAS = os.path.join(os.path.dirname(__file__), "..", "results", "tablas")
OUTPUT_DIR_GRAFICOS = os.path.join(os.path.dirname(__file__), "..", "results", "graficos")
# ───────────────────────────────────────────────────────────


def comparar_topologias(topologias):
    """
    Compara las topologías Best vs Worst para cada nivel.
    Retorna las tablas de diferencias.
    """
    os.makedirs(OUTPUT_DIR_TABLAS, exist_ok=True)
    os.makedirs(OUTPUT_DIR_GRAFICOS, exist_ok=True)

    # Identificar los niveles de partición
    niveles = set()
    for nombre in topologias.keys():
        pct = nombre.split("_")[1]
        niveles.add(pct)

    niveles = sorted(niveles, key=lambda x: float(x))
    comparaciones = {}

    for nivel in niveles:
        nombre_best = f"Best_{nivel}"
        nombre_worst = f"Worst_{nivel}"

        if nombre_best not in topologias or nombre_worst not in topologias:
            print(f"   ⚠️  Falta {nombre_best} o {nombre_worst}, saltando...")
            continue

        grados_best = topologias[nombre_best]["grados"]
        grados_worst = topologias[nombre_worst]["grados"]

        # Calcular diferencias: D = T_Worst - T_Best
        filas = []
        for var in sorted(grados_best.keys(), key=lambda x: int(x[1:])):
            gb = grados_best.get(var, 0)
            gw = grados_worst.get(var, 0)
            diff = gw - gb

            filas.append({
                "Variable": var,
                "Nombre": NOMBRES_COMPLETOS.get(var, ""),
                "Grado_Best": round(gb, 6),
                "Grado_Worst": round(gw, 6),
                "Diferencia_D": round(diff, 6),
                "Abs_Diferencia": round(abs(diff), 6)
            })

        df_comp = pd.DataFrame(filas)
        df_comp = df_comp.sort_values("Abs_Diferencia", ascending=False).reset_index(drop=True)

        # Identificar máximo y mínimo cambio
        var_max_cambio = df_comp.iloc[0]
        var_min_cambio = df_comp.iloc[-1]

        print(f"\n   {'═' * 55}")
        print(f"   📊 COMPARACIÓN: Best_{nivel} vs Worst_{nivel}")
        print(f"   {'═' * 55}")
        print(f"\n   {'Variable':<10} {'Nombre':<14} {'Best':>10} {'Worst':>10} {'D=W-B':>10}")
        print(f"   {'─' * 55}")
        for _, row in df_comp.iterrows():
            indicador = ""
            if row["Variable"] == var_max_cambio["Variable"]:
                indicador = " ← MAX CAMBIO"
            elif row["Variable"] == var_min_cambio["Variable"]:
                indicador = " ← MIN CAMBIO"
            print(f"   {row['Variable']:<10} {row['Nombre']:<14} "
                  f"{row['Grado_Best']:>10.4f} {row['Grado_Worst']:>10.4f} "
                  f"{row['Diferencia_D']:>+10.4f}{indicador}")

        print(f"\n   🔴 MÁXIMO CAMBIO: {var_max_cambio['Variable']} ({var_max_cambio['Nombre']}) "
              f"| D = {var_max_cambio['Diferencia_D']:+.4f}")
        print(f"   🟢 MÍNIMO CAMBIO: {var_min_cambio['Variable']} ({var_min_cambio['Nombre']}) "
              f"| D = {var_min_cambio['Diferencia_D']:+.4f}")

        # Guardar tabla
        path_csv = os.path.join(OUTPUT_DIR_TABLAS, f"comparacion_{nivel}.csv")
        df_comp.to_csv(path_csv, index=False)
        print(f"   💾 Tabla: comparacion_{nivel}.csv")

        # Generar gráfico de barras
        graficar_comparacion(df_comp, nivel)

        comparaciones[nivel] = {
            "tabla": df_comp,
            "max_cambio": var_max_cambio,
            "min_cambio": var_min_cambio
        }

    # Generar gráfico resumen con todas las particiones
    if comparaciones:
        graficar_resumen_global(comparaciones)

    return comparaciones


def graficar_comparacion(df_comp, nivel):
    """Genera gráfico de barras comparativo Best vs Worst."""
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    variables = df_comp.sort_values("Variable", key=lambda x: x.str.extract(r'(\d+)')[0].astype(int))

    # --- Subplot 1: Grado ponderado Best vs Worst ---
    ax1 = axes[0]
    x = np.arange(len(variables))
    ancho = 0.35

    bars_best = ax1.bar(x - ancho/2, variables["Grado_Best"], ancho,
                        label="Best (Alto rendimiento)", color="#42A5F5", edgecolor="white")
    bars_worst = ax1.bar(x + ancho/2, variables["Grado_Worst"], ancho,
                         label="Worst (Bajo rendimiento)", color="#EF5350", edgecolor="white")

    ax1.set_xlabel("Variables", fontsize=10)
    ax1.set_ylabel("Grado Ponderado (suma pesos MST)", fontsize=10)
    ax1.set_title(f"Grado Ponderado por Variable\nPartición {nivel}%", fontsize=12, fontweight="bold")
    ax1.set_xticks(x)
    etiq = [f"{row['Variable']}\n{row['Nombre']}" for _, row in variables.iterrows()]
    ax1.set_xticklabels(etiq, fontsize=7, rotation=45, ha="right")
    ax1.legend(fontsize=9)
    ax1.grid(axis="y", alpha=0.3)

    # --- Subplot 2: Diferencia D = Worst - Best ---
    ax2 = axes[1]
    df_sorted = df_comp.sort_values("Diferencia_D")
    colores = ["#EF5350" if d > 0 else "#42A5F5" for d in df_sorted["Diferencia_D"]]

    bars = ax2.barh(
        [f"{row['Variable']} ({row['Nombre']})" for _, row in df_sorted.iterrows()],
        df_sorted["Diferencia_D"],
        color=colores, edgecolor="white"
    )

    ax2.axvline(x=0, color="black", linewidth=0.8)
    ax2.set_xlabel("D = Grado_Worst − Grado_Best", fontsize=10)
    ax2.set_title(f"Cambio en la Topología (D)\nPartición {nivel}%", fontsize=12, fontweight="bold")
    ax2.grid(axis="x", alpha=0.3)

    # Anotar valores
    for bar, val in zip(bars, df_sorted["Diferencia_D"]):
        ax2.text(val + (0.002 if val >= 0 else -0.002),
                 bar.get_y() + bar.get_height()/2,
                 f"{val:+.4f}", va="center",
                 ha="left" if val >= 0 else "right",
                 fontsize=8, fontweight="bold")

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR_GRAFICOS, f"comparacion_{nivel}.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"   💾 Gráfico: comparacion_{nivel}.png")


def graficar_resumen_global(comparaciones):
    """Genera un gráfico resumen con las diferencias de todas las particiones."""
    fig, ax = plt.subplots(figsize=(14, 7))

    niveles = sorted(comparaciones.keys(), key=lambda x: float(x))
    n_vars = len(comparaciones[niveles[0]]["tabla"])
    x = np.arange(n_vars)
    ancho = 0.25

    colores_nivel = {"12.5": "#FF7043", "25": "#AB47BC", "50": "#26A69A"}

    for idx, nivel in enumerate(niveles):
        tabla = comparaciones[nivel]["tabla"].sort_values(
            "Variable", key=lambda s: s.str.extract(r'(\d+)')[0].astype(int)
        )
        offset = (idx - len(niveles)/2 + 0.5) * ancho
        color = colores_nivel.get(nivel, "#78909C")

        ax.bar(x + offset, tabla["Diferencia_D"], ancho,
               label=f"Partición {nivel}%", color=color, edgecolor="white", alpha=0.85)

    ax.axhline(y=0, color="black", linewidth=0.8)
    ax.set_xlabel("Variables", fontsize=11)
    ax.set_ylabel("D = Grado_Worst − Grado_Best", fontsize=11)
    ax.set_title("Cambio en Topología por Variable\nComparación entre Todas las Particiones",
                 fontsize=13, fontweight="bold")

    etiquetas_x = []
    tabla_ref = comparaciones[niveles[0]]["tabla"].sort_values(
        "Variable", key=lambda s: s.str.extract(r'(\d+)')[0].astype(int)
    )
    for _, row in tabla_ref.iterrows():
        etiquetas_x.append(f"{row['Variable']}\n{row['Nombre']}")

    ax.set_xticks(x)
    ax.set_xticklabels(etiquetas_x, fontsize=8)
    ax.legend(fontsize=10, loc="upper right")
    ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR_GRAFICOS, "resumen_comparacion_global.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"\n   💾 Resumen global: resumen_comparacion_global.png")


def ejecutar(topologias):
    """Punto de entrada del paso 5."""
    print("\n   Comparando topologías Best vs Worst...")
    comparaciones = comparar_topologias(topologias)
    print(f"\n   ✅ {len(comparaciones)} comparaciones realizadas")
    return comparaciones


if __name__ == "__main__":
    print("=" * 55)
    print("  PASO 5: COMPARACIÓN DE TOPOLOGÍAS")
    print("=" * 55)
    print("  Ejecuta desde main.py para obtener las topologías.")
