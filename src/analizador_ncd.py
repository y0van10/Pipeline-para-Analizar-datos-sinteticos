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
        # Convierte una columna de Pandas a un string plano uniendo sus filas con saltos de línea
        # Esto prepara la variable para que sea tratada como un archivo de texto por el compresor gzip.
        return "\n".join(serie.astype(str).values)

    def _comprimir_y_medir(self, texto):
        # Codifica el texto en formato binario UTF-8
        datos = texto.encode("utf-8")
        # Retorna el tamaño en bytes de los datos comprimidos con Gzip en el nivel especificado.
        # Sirve como una aproximación de la Complejidad de Kolmogorov K(X).
        return len(gzip.compress(datos, compresslevel=self.nivel_gzip))

    def calcular_ncd(self, txt_x, txt_y):
        """
        Calcula la Distancia de Compresión Normalizada (NCD):
        NCD(X, Y) = ( K(X, Y) - min(K(X), K(Y)) ) / max(K(X), K(Y))
        Donde:
          - K(X) y K(Y) son los tamaños comprimidos individuales.
          - K(X, Y) es el tamaño comprimido de la concatenación de X e Y (información conjunta).
        NCD tiende a 0 si las variables comparten muchos patrones idénticos,
        y tiende a 1 si son estadísticamente independientes.
        """
        cx  = self._comprimir_y_medir(txt_x) # K(X)
        cy  = self._comprimir_y_medir(txt_y) # K(Y)
        cxy = self._comprimir_y_medir(txt_x + "\n" + txt_y) # K(X, Y)
        
        # Aplicamos la ecuación clásica de la métrica NCD
        ncd = (cxy - min(cx, cy)) / max(cx, cy)
        
        # Limitamos el rango de salida matemáticamente a [0, 1] por estabilidad numérica
        return float(np.clip(ncd, 0.0, 1.0))

    def obtener_columnas_analisis(self, df):
        """
        Devuelve todas las columnas del CSV excepto la variable objetivo.
        """
        cols = [c for c in df.columns if c != self.col_objetivo]
        return cols

    def procesar_particiones(self, particiones):
        """
        Itera sobre todas las particiones del dataset (niveles 50%, 25%, 12.5% y global),
        calcula la matriz de distancias NCD de todas las variables contra todas (todos contra todos)
        y las guarda como archivos CSV de resultados.
        """
        self.matrices = {}

        for nombre, info in particiones.items():
            nivel     = info["nivel"]
            ruta_csv  = info["ruta_csv"]

            df = pd.read_csv(ruta_csv)
            variables = self.obtener_columnas_analisis(df)
            n_vars = len(variables)

            print(f"   📊 NCD desde {os.path.basename(ruta_csv)} ({len(df)} filas, {n_vars} variables)...")

            # Convertimos cada columna entera del dataset a su equivalente en texto plano
            textos = {col: self._columna_a_texto(df[col]) for col in variables}

            # Inicializamos la matriz de distancias con ceros en la diagonal
            matriz = np.zeros((n_vars, n_vars))
            np.fill_diagonal(matriz, 0.0)

            # Calculamos las combinaciones simétricas (evita calcular dos veces NCD(A,B) y NCD(B,A))
            for i, j in combinations(range(n_vars), 2):
                dist = self.calcular_ncd(textos[variables[i]], textos[variables[j]])
                matriz[i, j] = dist
                matriz[j, i] = dist

            # Convertimos la matriz numpy a un DataFrame de Pandas estructurado con los nombres reales de las variables
            etiquetas = variables  
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
