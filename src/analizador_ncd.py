import os
import gzip
import numpy as np
import pandas as pd
from itertools import combinations

class AnalizadorNCD:
    """
    Clase encargada de calcular las matrices NCD (Normalized Compression Distance)
    para cada partición leyendo directamente los archivos CSV generados.
    Funciona con cualquier dataset: usa todas las columnas excepto la objetivo.
    """
    def __init__(self, dir_base="results", nivel_gzip=9, col_objetivo=None):
        self.dir_base = os.path.normpath(dir_base)
        self.nivel_gzip = nivel_gzip
        self.col_objetivo = col_objetivo  # se excluye del análisis NCD
        self.matrices = {}

    def _columna_a_texto(self, serie):
        return "\n".join(serie.astype(str).values)

    def _comprimir_y_medir(self, texto):
        datos = texto.encode("utf-8")
        return len(gzip.compress(datos, compresslevel=self.nivel_gzip))

    def calcular_ncd(self, txt_x, txt_y):
        cx  = self._comprimir_y_medir(txt_x)
        cy  = self._comprimir_y_medir(txt_y)
        cxy = self._comprimir_y_medir(txt_x + "\n" + txt_y)
        ncd = (cxy - min(cx, cy)) / max(cx, cy)
        return float(np.clip(ncd, 0.0, 1.0))

    def obtener_columnas_analisis(self, df):
        """
        Devuelve todas las columnas del CSV excepto la variable objetivo.
        """
        cols = [c for c in df.columns if c != self.col_objetivo]
        return cols

    def procesar_particiones(self, particiones):
        self.matrices = {}

        for nombre, info in particiones.items():
            nivel     = info["nivel"]
            ruta_csv  = info["ruta_csv"]

            df = pd.read_csv(ruta_csv)
            variables = self.obtener_columnas_analisis(df)
            n_vars = len(variables)

            print(f"   📊 NCD desde {os.path.basename(ruta_csv)} ({len(df)} filas, {n_vars} variables)...")

            textos = {col: self._columna_a_texto(df[col]) for col in variables}

            matriz = np.zeros((n_vars, n_vars))
            np.fill_diagonal(matriz, 0.0)

            for i, j in combinations(range(n_vars), 2):
                dist = self.calcular_ncd(textos[variables[i]], textos[variables[j]])
                matriz[i, j] = dist
                matriz[j, i] = dist

            # Etiquetas cortas para la matriz (nombre real de columna)
            etiquetas = variables  # usamos el nombre real, no "X1", "X2"...
            df_matriz = pd.DataFrame(np.round(matriz, 6), index=etiquetas, columns=etiquetas)

            dir_tablas = os.path.join(self.dir_base, f"nivel_{nivel}", "tablas")
            os.makedirs(dir_tablas, exist_ok=True)
            path_out = os.path.join(dir_tablas, f"ncd_{nombre}.csv")
            df_matriz.to_csv(path_out)

            self.matrices[nombre] = {
                "nivel":           nivel,
                "df_matriz":       df_matriz,
                "ruta_matriz":     path_out,
                "ruta_csv_origen": ruta_csv,
                "variables":       variables,
            }
            print(f"      💾 Matriz guardada: {path_out}")

        return self.matrices

    def ejecutar(self, particiones):
        return self.procesar_particiones(particiones)
