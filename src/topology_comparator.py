import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

class TopologyComparator:
    """
    Clase encargada de comparar las topologías Best vs Worst para cada partición,
    calcular el cambio en centralidad (D = Worst - Best) y graficar los resultados.
    """
    NOMBRES_COMPLETOS = {
        "X1": "Sexo", "X2": "Zona", "X3": "Ciclo",
        "X4": "Ingreso", "X5": "Trabaja", "X6": "Beca",
        "X7": "Educ.Jefe", "X8": "Tam.Fam", "X9": "Asistencia",
        "X10": "Desaprobados"
    }

    def __init__(self, output_dir_tablas="results/tablas", output_dir_graficos="results/graficos"):
        self.output_dir_tablas = os.path.normpath(output_dir_tablas)
        self.output_dir_graficos = os.path.normpath(output_dir_graficos)
        self.comparisons = {}

    def comparar_grados(self, grados_best, grados_worst):
        filas = []
        for var in sorted(grados_best.keys(), key=lambda x: int(x[1:])):
            g_b = grados_best.get(var, 0.0)
            g_w = grados_worst.get(var, 0.0)
            diff = g_w - g_b
            filas.append({
                "Variable": var,
                "Nombre": self.NOMBRES_COMPLETOS.get(var, var),
                "Grado_Best": g_b,
                "Grado_Worst": g_w,
                "Diferencia_D": round(diff, 6),
                "Abs_Diferencia": abs(diff)
            })
        
        df = pd.DataFrame(filas)
        df = df.sort_values("Abs_Diferencia", ascending=False).reset_index(drop=True)
        return df

    def graficar_comparacion(self, df_comp, nombre_base):
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))

        variables = df_comp.sort_values("Variable", key=lambda s: s.str.extract(r'(\d+)')[0].astype(int))

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
        ax1.set_title(f"Grado Ponderado por Variable\nPartición {nombre_base}%", fontsize=12, fontweight="bold")
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
        ax2.set_title(f"Cambio en la Topología (D)\nPartición {nombre_base}%", fontsize=12, fontweight="bold")
        ax2.grid(axis="x", alpha=0.3)

        # Anotar valores
        for bar, val in zip(bars, df_sorted["Diferencia_D"]):
            ax2.text(val + (0.002 if val >= 0 else -0.002),
                     bar.get_y() + bar.get_height()/2,
                     f"{val:+.4f}", va="center",
                     ha="left" if val >= 0 else "right",
                     fontsize=8, fontweight="bold")

        plt.tight_layout()
        path = os.path.join(self.output_dir_graficos, f"comparacion_{nombre_base}.png")
        plt.savefig(path, dpi=150, bbox_inches="tight")
        plt.close()
        return path

    def graficar_resumen_global(self, todas_comp):
        fig, ax = plt.subplots(figsize=(14, 7))

        niveles = sorted(todas_comp.keys(), key=lambda x: float(x))
        n_vars = len(todas_comp[niveles[0]])
        x = np.arange(n_vars)
        ancho = 0.25

        colores_nivel = {"12.5": "#FF7043", "25": "#AB47BC", "50": "#26A69A"}

        for idx, nivel in enumerate(niveles):
            tabla = todas_comp[nivel].sort_values(
                "Variable", key=lambda s: s.str.extract(r'(\d+)')[0].astype(int)
            )
            offset = (idx - len(niveles)/2 + 0.5) * ancho
            color = colores_nivel.get(nivel, "#78909C")

            ax.bar(x + offset, tabla["Diferencia_D"], ancho,
                   label=f"Partición {nivel}%", color=color, edgecolor="white", alpha=0.85)

        ax.axhline(y=0, color="black", linewidth=0.8)
        ax.set_ylabel("D = Grado_Worst − Grado_Best", fontsize=11)
        ax.set_xlabel("Variables", fontsize=11)
        ax.set_title("Cambio en Topología por Variable\nComparación entre Todas las Particiones",
                     fontsize=13, fontweight="bold")

        etiquetas_x = []
        tabla_ref = todas_comp[niveles[0]].sort_values(
            "Variable", key=lambda s: s.str.extract(r'(\d+)')[0].astype(int)
        )
        for _, row in tabla_ref.iterrows():
            etiquetas_x.append(f"{row['Variable']}\n{row['Nombre']}")

        ax.set_xticks(x)
        ax.set_xticklabels(etiquetas_x, fontsize=8)
        ax.legend(fontsize=10, loc="upper right")
        ax.grid(axis="y", alpha=0.3)

        plt.tight_layout()
        path = os.path.join(self.output_dir_graficos, "resumen_comparacion_global.png")
        plt.savefig(path, dpi=150, bbox_inches="tight")
        plt.close()
        return path

    def comparar_topologias(self, topologias):
        os.makedirs(self.output_dir_tablas, exist_ok=True)
        os.makedirs(self.output_dir_graficos, exist_ok=True)
        self.comparisons = {}

        # Identificar niveles (ej: 12.5, 25, 50)
        niveles = set(n.split("_")[1] for n in topologias.keys())
        
        for nivel in sorted(niveles, key=lambda x: float(x)):
            nombre_best = f"Best_{nivel}"
            nombre_worst = f"Worst_{nivel}"
            
            if nombre_best not in topologias or nombre_worst not in topologias:
                continue

            print(f"\n   ═══════════════════════════════════════════════════════")
            print(f"   📊 COMPARACIÓN: {nombre_best} vs {nombre_worst}")
            print(f"   ═══════════════════════════════════════════════════════")

            grados_best = topologias[nombre_best]["grados"]
            grados_worst = topologias[nombre_worst]["grados"]

            df_comp = self.comparar_grados(grados_best, grados_worst)
            self.comparisons[nivel] = df_comp

            # Identificar máximo y mínimo cambio para imprimir
            var_max_cambio = df_comp.iloc[0]
            var_min_cambio = df_comp.iloc[-1]

            print(f"\n   {'Variable':<10} {'Nombre':<14} {'Best':>10} {'Worst':>10} {'D=W-B':>10}")
            print(f"   " + "─" * 55)
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

            # Guardar tabla CSV
            path_csv = os.path.join(self.output_dir_tablas, f"comparacion_{nivel}.csv")
            df_comp.to_csv(path_csv, index=False)
            print(f"   💾 Tabla guardada: comparacion_{nivel}.csv")

            # Graficar
            self.graficar_comparacion(df_comp, nivel)

        # Generar gráfico resumen global
        self.graficar_resumen_global(self.comparisons)

        return self.comparisons

    def ejecutar(self, topologias):
        return self.comparar_topologias(topologias)
