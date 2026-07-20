import os
import gzip
import numpy as np
import pandas as pd
from itertools import combinations

class AnalizadorNCD:
    """
    Clase encargada de calcular las matrices NCD (Normalized Compression Distance)
    para cada partición leyendo directamente los archivos CSV generados.
    """
    VARIABLES_ANALISIS = [
        "X1_sexo", "X2_zona", "X3_ciclo", "X4_ingreso_familiar",
        "X5_trabaja", "X6_beca", "X7_educ_jefe", "X8_tam_familiar",
        "X9_asistencia", "X10_cursos_desaprobados"
    ]

    def __init__(self, dir_base="results", nivel_gzip=9):
        self.dir_base = os.path.normpath(dir_base)
        self.nivel_gzip = nivel_gzip
        self.matrices = {}

    def _columna_a_texto(self, serie):
        return "\n".join(serie.astype(str).values)

    def _comprimir_y_medir(self, texto):
        datos = texto.encode("utf-8")
        return len(gzip.compress(datos, compresslevel=self.nivel_gzip))

    def calcular_ncd(self, txt_x, txt_y):
        cx = self._comprimir_y_medir(txt_x)
        cy = self._comprimir_y_medir(txt_y)
        cxy = self._comprimir_y_medir(txt_x + "\n" + txt_y)
        
        ncd = (cxy - min(cx, cy)) / max(cx, cy)
        return float(np.clip(ncd, 0.0, 1.0))

    def procesar_particiones(self, particiones):
        self.matrices = {}

        for nombre, info in particiones.items():
            nivel = info["nivel"]
            ruta_csv = info["ruta_csv"]

            # Cargar desde disco el CSV generado en el paso anterior
            df = pd.read_csv(ruta_csv)
            print(f"   📊 Calculando NCD desde {os.path.basename(ruta_csv)} ({len(df)} filas)...")

            # Convertir todas las columnas de análisis a texto
            textos = {col: self._columna_a_texto(df[col]) for col in self.VARIABLES_ANALISIS}
            
            n_vars = len(self.VARIABLES_ANALISIS)
            matriz = np.zeros((n_vars, n_vars))
            np.fill_diagonal(matriz, 0.0)

            for i, j in combinations(range(n_vars), 2):
                col_i = self.VARIABLES_ANALISIS[i]
                col_j = self.VARIABLES_ANALISIS[j]
                dist = self.calcular_ncd(textos[col_i], textos[col_j])
                matriz[i, j] = dist
                matriz[j, i] = dist

            etiquetas = [f"X{k+1}" for k in range(n_vars)]
            df_matriz = pd.DataFrame(np.round(matriz, 6), index=etiquetas, columns=etiquetas)

            # Carpeta especifica de tablas del nivel
            dir_tablas = os.path.join(self.dir_base, f"nivel_{nivel}", "tablas")
            os.makedirs(dir_tablas, exist_ok=True)
            path_out = os.path.join(dir_tablas, f"ncd_{nombre}.csv")
            df_matriz.to_csv(path_out)

            self.matrices[nombre] = {
                "nivel": nivel,
                "df_matriz": df_matriz,
                "ruta_matriz": path_out,
                "ruta_csv_origen": ruta_csv
            }
            print(f"      💾 Matriz guardada: {path_out}")

        return self.matrices

    def ejecutar(self, particiones):
        return self.procesar_particiones(particiones)
