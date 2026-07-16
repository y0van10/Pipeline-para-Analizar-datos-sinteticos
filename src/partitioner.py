import os
import pandas as pd

class StudentPartitioner:
    """
    Clase encargada de ordenar a los estudiantes por promedio final (X11) y
    particionarlos en subgrupos Best (alto rendimiento) y Worst (bajo rendimiento)
    según diferentes niveles de muestra.
    """
    def __init__(self, output_dir="results/tablas", levels=[0.125, 0.25, 0.50]):
        self.output_dir = os.path.normpath(output_dir)
        self.levels = levels
        self.partitions = {}

    def crear_particiones(self, df):
        os.makedirs(self.output_dir, exist_ok=True)
        self.partitions = {}

        # Ordenar de mayor a menor promedio
        df_sorted = df.sort_values("X11_promedio_final", ascending=False).copy()
        n = len(df_sorted)

        for nivel in self.levels:
            pct_label = f"{nivel * 100:.1f}".rstrip('0').rstrip('.')
            k = int(n * nivel)  # redondeo hacia abajo

            # Best (los k mejores)
            best = df_sorted.head(k).copy()
            # Worst (los k peores)
            worst = df_sorted.tail(k).copy()

            # Guardar en memoria
            nombre_best = f"Best_{pct_label}"
            nombre_worst = f"Worst_{pct_label}"
            self.partitions[nombre_best] = best
            self.partitions[nombre_worst] = worst

            # Guardar a disco
            path_best = os.path.join(self.output_dir, f"{nombre_best}.csv")
            path_worst = os.path.join(self.output_dir, f"{nombre_worst}.csv")
            best.to_csv(path_best, index=False)
            worst.to_csv(path_worst, index=False)

            print(f"   💾 Muestras {pct_label}% creadas:")
            print(f"       - {nombre_best}: {len(best)} estudiantes en {os.path.basename(path_best)}")
            print(f"       - {nombre_worst}: {len(worst)} estudiantes en {os.path.basename(path_worst)}")

        return self.partitions

    def ejecutar(self, df):
        print(f"   Iniciando particionamiento para niveles: {[f'{l*100}%' for l in self.levels]}...")
        return self.crear_particiones(df)
