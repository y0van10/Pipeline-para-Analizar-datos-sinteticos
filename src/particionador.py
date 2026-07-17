import os
import pandas as pd

class ParticionadorEstudiantes:
    """
    Clase encargada de ordenar a los estudiantes por promedio final (X11) y
    particionarlos en subgrupos Best (alto rendimiento) y Worst (bajo rendimiento)
    según diferentes niveles de muestra.
    """
    def __init__(self, dir_salida="results/tablas", niveles=[0.125, 0.25, 0.50]):
        self.dir_salida = os.path.normpath(dir_salida)
        self.niveles = niveles
        self.particiones = {}

    def crear_particiones(self, df):
        os.makedirs(self.dir_salida, exist_ok=True)
        self.particiones = {}

        # Ordenar de mayor a menor promedio
        df_ordenado = df.sort_values("X11_promedio_final", ascending=False).copy()
        n = len(df_ordenado)

        for nivel in self.niveles:
            pct_label = f"{nivel * 100:.1f}".rstrip('0').rstrip('.')
            k = int(n * nivel)  # redondeo hacia abajo

            # Best (los k mejores)
            best = df_ordenado.head(k).copy()
            # Worst (los k peores)
            worst = df_ordenado.tail(k).copy()

            # Guardar en memoria
            nombre_best = f"Best_{pct_label}"
            nombre_worst = f"Worst_{pct_label}"
            self.particiones[nombre_best] = best
            self.particiones[nombre_worst] = worst

            # Guardar a disco
            path_best = os.path.join(self.dir_salida, f"{nombre_best}.csv")
            path_worst = os.path.join(self.dir_salida, f"{nombre_worst}.csv")
            best.to_csv(path_best, index=False)
            worst.to_csv(path_worst, index=False)

            print(f"   💾 Muestras {pct_label}% creadas:")
            print(f"       - {nombre_best}: {len(best)} estudiantes en {os.path.basename(path_best)}")
            print(f"       - {nombre_worst}: {len(worst)} estudiantes en {os.path.basename(path_worst)}")

        return self.particiones

    def ejecutar(self, df):
        print(f"   Iniciando particionamiento para niveles: {[f'{l*100}%' for l in self.niveles]}...")
        return self.crear_particiones(df)
