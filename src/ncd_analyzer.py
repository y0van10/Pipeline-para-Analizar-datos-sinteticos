import os
import gzip
import numpy as np
import pandas as pd
from itertools import combinations

class NCDAnalyzer:
    """
    Clase encargada de calcular las matrices NCD (Normalized Compression Distance)
    para cada partición utilizando compresión Gzip.
    """
    VARIABLES_ANALISIS = [
        "X1_sexo", "X2_zona", "X3_ciclo", "X4_ingreso_familiar",
        "X5_trabaja", "X6_beca", "X7_educ_jefe", "X8_tam_familiar",
        "X9_asistencia", "X10_cursos_desaprobados"
    ]

    def __init__(self, output_dir="results/matrices", gzip_level=9):
        self.output_dir = os.path.normpath(output_dir)
        self.gzip_level = gzip_level
        self.matrices = {}

    def _columna_a_texto(self, serie):
        return "\n".join(serie.astype(str).values)

    def _comprimir_y_medir(self, texto):
        datos = texto.encode("utf-8")
        return len(gzip.compress(datos, compresslevel=self.gzip_level))

    def calcular_ncd(self, txt_x, txt_y):
        cx = self._comprimir_y_medir(txt_x)
        cy = self._comprimir_y_medir(txt_y)
        cxy = self._comprimir_y_medir(txt_x + "\n" + txt_y)
        
        ncd = (cxy - min(cx, cy)) / max(cx, cy)
        return float(np.clip(ncd, 0.0, 1.0))

    def procesar_particiones(self, particiones):
        os.makedirs(self.output_dir, exist_ok=True)
        self.matrices = {}

        for nombre, df in particiones.items():
            print(f"   📊 Calculando distancias NCD para {nombre} ({len(df)} filas)...")
            
            # Convertir todas las columnas de análisis a texto
            textos = {col: self._columna_a_texto(df[col]) for col in self.VARIABLES_ANALISIS}
            
            # Inicializar matriz vacía
            n_vars = len(self.VARIABLES_ANALISIS)
            matriz = np.zeros((n_vars, n_vars))
            
            # Rellenar diagonal con 0.0
            np.fill_diagonal(matriz, 0.0)

            # Calcular distancias para cada combinación de variables
            for i, j in combinations(range(n_vars), 2):
                col_i = self.VARIABLES_ANALISIS[i]
                col_j = self.VARIABLES_ANALISIS[j]
                
                dist = self.calcular_ncd(textos[col_i], textos[col_j])
                matriz[i, j] = dist
                matriz[j, i] = dist # la distancia es simétrica

            # Crear DataFrame con etiquetas cortas X1, X2... X10
            etiquetas = [f"X{k+1}" for k in range(n_vars)]
            df_matriz = pd.DataFrame(np.round(matriz, 6), index=etiquetas, columns=etiquetas)
            self.matrices[nombre] = df_matriz

            # Guardar a disco
            path = os.path.join(self.output_dir, f"ncd_{nombre}.csv")
            df_matriz.to_csv(path)
            print(f"      💾 Matriz guardada: ncd_{nombre}.csv")

        return self.matrices

    def ejecutar(self, particiones):
        return self.procesar_particiones(particiones)
