import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

class ComparadorTopologias:
    """
    Clase encargada de comparar las topologías de rendimiento extremo (Best vs Worst)
    para cada nivel (50%, 25%, 12.5%).
    Funciona con cualquier número de variables y cualquier nombre de columna.
    """
    def __init__(self, dir_base="results"):
        self.dir_base = os.path.normpath(dir_base)
        self.comparaciones = {}

    def comparar_grados(self, grados_best, grados_worst):
        """Compara el grado ponderado de cada variable entre Best y Worst."""
        # Unión de todas las variables presentes en ambos bloques
        todas_vars = sorted(set(grados_best.keys()) | set(grados_worst.keys()))
        filas = []
        for var in todas_vars:
            g_b = grados_best.get(var, 0.0)
            g_w = grados_worst.get(var, 0.0)
            diff = g_w - g_b
            # Nombre corto para mostrar en tablas (máx 20 caracteres)
            nombre_corto = var[:20] + "…" if len(var) > 20 else var
            filas.append({
                "Variable":      var,
                "Nombre":        nombre_corto,
                "Grado_Best":    g_b,
                "Grado_Worst":   g_w,
                "Diferencia_D":  round(diff, 6),
                "Abs_Diferencia": abs(diff),
            })

        df = pd.DataFrame(filas)
        df = df.sort_values("Abs_Diferencia", ascending=False).reset_index(drop=True)
        return df

    def graficar_comparacion(self, df_comp, nivel, nombre_best, nombre_worst):
        fig, axes = plt.subplots(1, 2, figsize=(18, max(6, len(df_comp) * 0.5 + 2)))

        variables = df_comp.sort_values("Variable")

        # ─ Subplot 1: grado ponderado Best vs Worst ─
        ax1 = axes[0]
        x     = np.arange(len(variables))
        ancho = 0.35

        ax1.bar(x - ancho/2, variables["Grado_Best"],  ancho,
                label=f"Best ({nombre_best})",  color="#42A5F5", edgecolor="white")
        ax1.bar(x + ancho/2, variables["Grado_Worst"], ancho,
                label=f"Worst ({nombre_worst})", color="#EF5350", edgecolor="white")

        ax1.set_xlabel("Variables", fontsize=9)
        ax1.set_ylabel("Grado Ponderado MST", fontsize=9)
        ax1.set_title(f"Grado Ponderado — Nivel {nivel}%\n({nombre_best} vs {nombre_worst})",
                      fontsize=11, fontweight="bold")
        ax1.set_xticks(x)
        etiq = [row["Nombre"] for _, row in variables.iterrows()]
        ax1.set_xticklabels(etiq, fontsize=7, rotation=45, ha="right")
        ax1.legend(fontsize=8)
        ax1.grid(axis="y", alpha=0.3)

        # ─ Subplot 2: diferencia D = Worst - Best ─
        ax2 = axes[1]
        df_ord  = df_comp.sort_values("Diferencia_D")
        colores = ["#EF5350" if d > 0 else "#42A5F5" for d in df_ord["Diferencia_D"]]

        bars = ax2.barh(
            df_ord["Nombre"].tolist(),
            df_ord["Diferencia_D"].tolist(),
            color=colores, edgecolor="white",
        )

        ax2.axvline(x=0, color="black", linewidth=0.8)
        ax2.set_xlabel("D = Grado_Worst − Grado_Best", fontsize=9)
        ax2.set_title(f"Cambio en Topología (D) — Nivel {nivel}%",
                      fontsize=11, fontweight="bold")
        ax2.grid(axis="x", alpha=0.3)

        for bar, val in zip(bars, df_ord["Diferencia_D"]):
            ax2.text(val + (0.002 if val >= 0 else -0.002),
                     bar.get_y() + bar.get_height() / 2,
                     f"{val:+.4f}", va="center",
                     ha="left" if val >= 0 else "right",
                     fontsize=7, fontweight="bold")

        plt.tight_layout()
        dir_g = os.path.join(self.dir_base, f"nivel_{nivel}", "graficos")
        os.makedirs(dir_g, exist_ok=True)
        path = os.path.join(dir_g, f"comparacion_{nivel}.png")
        plt.savefig(path, dpi=150, bbox_inches="tight")
        plt.close()
        return path

    def graficar_resumen_global(self, todas_comp):
        niveles = sorted(todas_comp.keys(), key=lambda x: float(x))
        if not niveles:
            return

        # Tomamos la referencia de variables del primer nivel disponible
        vars_ref = list(todas_comp[niveles[0]]["Variable"])
        n_vars   = len(vars_ref)
        x        = np.arange(n_vars)
        ancho    = 0.25
        colores_nivel = {"12.5": "#FF7043", "25": "#AB47BC", "50": "#26A69A"}

        fig, ax = plt.subplots(figsize=(max(14, n_vars * 0.8), 7))

        for idx, nivel in enumerate(niveles):
            tabla  = todas_comp[nivel].set_index("Variable").reindex(vars_ref).reset_index()
            offset = (idx - len(niveles) / 2 + 0.5) * ancho
            color  = colores_nivel.get(nivel, "#78909C")
            ax.bar(x + offset, tabla["Diferencia_D"].fillna(0), ancho,
                   label=f"Extremos Nivel {nivel}%", color=color,
                   edgecolor="white", alpha=0.85)

        ax.axhline(y=0, color="black", linewidth=0.8)
        ax.set_ylabel("D = Grado_Worst − Grado_Best", fontsize=11)
        ax.set_xlabel("Variables", fontsize=11)
        ax.set_title("Cambio en Topología por Variable (Best vs Worst)\nComparación entre Todos los Niveles",
                     fontsize=13, fontweight="bold")

        nombres_cortos = [v[:14] + "…" if len(v) > 14 else v for v in vars_ref]
        ax.set_xticks(x)
        ax.set_xticklabels(nombres_cortos, fontsize=8, rotation=30, ha="right")
        ax.legend(fontsize=10, loc="upper right")
        ax.grid(axis="y", alpha=0.3)

        plt.tight_layout()
        dir_global = os.path.join(self.dir_base, "global")
        os.makedirs(dir_global, exist_ok=True)
        path = os.path.join(dir_global, "resumen_comparacion_global.png")
        plt.savefig(path, dpi=150, bbox_inches="tight")
        plt.close()
        return path

    def comparar_topologias(self, topologias):
        self.comparaciones = {}

        pares_comparativos = [
            ("50",  "Best_50",     "Worst_50"),
            ("25",  "Best_25_1",   "Worst_25_2"),
            ("12.5","Best_12.5_1", "Worst_12.5_4"),
        ]

        for nivel, nombre_best, nombre_worst in pares_comparativos:
            if nombre_best not in topologias or nombre_worst not in topologias:
                continue

            print(f"\n   ═══════════════════════════════════════════════════════")
            print(f"   📊 COMPARACIÓN NIVEL {nivel}%: {nombre_best} vs {nombre_worst}")
            print(f"   ═══════════════════════════════════════════════════════")

            grados_best  = topologias[nombre_best]["grados"]
            grados_worst = topologias[nombre_worst]["grados"]

            df_comp = self.comparar_grados(grados_best, grados_worst)
            self.comparaciones[nivel] = df_comp

            var_max = df_comp.iloc[0]
            var_min = df_comp.iloc[-1]

            print(f"\n   {'Variable':<30} {'Best':>10} {'Worst':>10} {'D=W-B':>12}")
            print(f"   {'─' * 65}")
            for _, row in df_comp.iterrows():
                indicador = ""
                if row["Variable"] == var_max["Variable"]:
                    indicador = " ← MAX CAMBIO"
                elif row["Variable"] == var_min["Variable"]:
                    indicador = " ← MIN CAMBIO"
                nombre_disp = row["Nombre"]
                print(f"   {nombre_disp:<30} {row['Grado_Best']:>10.4f} "
                      f"{row['Grado_Worst']:>10.4f} {row['Diferencia_D']:>+12.4f}{indicador}")

            print(f"\n   🔴 MÁXIMO CAMBIO: {var_max['Nombre']} | D = {var_max['Diferencia_D']:+.4f}")
            print(f"   🟢 MÍNIMO CAMBIO: {var_min['Nombre']} | D = {var_min['Diferencia_D']:+.4f}")

            dir_t    = os.path.join(self.dir_base, f"nivel_{nivel}", "tablas")
            os.makedirs(dir_t, exist_ok=True)
            path_csv = os.path.join(dir_t, f"comparacion_{nivel}.csv")
            df_comp.to_csv(path_csv, index=False)
            print(f"   💾 Tabla guardada: {path_csv}")

            self.graficar_comparacion(df_comp, nivel, nombre_best, nombre_worst)

        if self.comparaciones:
            self.graficar_resumen_global(self.comparaciones)
            print(f"\n   💾 Resumen global guardado en results/global/resumen_comparacion_global.png")

        return self.comparaciones

    def ejecutar(self, topologias):
        return self.comparar_topologias(topologias)
