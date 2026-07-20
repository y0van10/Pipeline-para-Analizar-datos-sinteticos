import os
import pandas as pd

class ParticionadorEstudiantes:
    """
    Clase encargada de ordenar los registros por la columna objetivo y
    particionarlos jerárquicamente en bloques (50%, 25% y 12.5%) guardando
    los archivos CSV en carpetas organizadas por nivel.
    Funciona con cualquier dataset y cualquier columna objetivo.
    """
    def __init__(self, dir_base="results", col_objetivo=None):
        self.dir_base = os.path.normpath(dir_base)
        self.col_objetivo = col_objetivo  # columna que define el ranking
        self.particiones = {}

    def crear_particiones(self, df):
        """
        Ordena el dataset de mayor a menor valor en col_objetivo
        y genera bloques contiguos para 50%, 25% y 12.5%.
        """
        if not self.col_objetivo or self.col_objetivo not in df.columns:
            # Buscar automáticamente la última columna numérica
            cols_num = df.select_dtypes(include="number").columns.tolist()
            self.col_objetivo = cols_num[-1] if cols_num else df.columns[-1]
            print(f"   ⚠️  col_objetivo no especificada. Usando: '{self.col_objetivo}'")

        self.particiones = {}
        df_ordenado = df.sort_values(self.col_objetivo, ascending=False).reset_index(drop=True)
        n = len(df_ordenado)
        print(f"   📊 Ordenando {n} registros por '{self.col_objetivo}' (mayor → menor)...")

        # ─────────────────────────────────────────────
        # NIVEL 50%
        # ─────────────────────────────────────────────
        dir_50 = os.path.join(self.dir_base, "nivel_50", "tablas")
        os.makedirs(dir_50, exist_ok=True)
        k50 = int(n * 0.50)

        best_50  = df_ordenado.iloc[0:k50].copy()
        worst_50 = df_ordenado.iloc[k50:n].copy()

        b_50_path = os.path.join(dir_50, "Best_50.csv")
        w_50_path = os.path.join(dir_50, "Worst_50.csv")
        best_50.to_csv(b_50_path, index=False)
        worst_50.to_csv(w_50_path, index=False)

        self.particiones["Best_50"]  = {"nivel": "50",  "ruta_csv": b_50_path, "df": best_50}
        self.particiones["Worst_50"] = {"nivel": "50",  "ruta_csv": w_50_path, "df": worst_50}

        print(f"   💾 Nivel 50% guardado en {dir_50}:")
        print(f"       - Best_50:  {len(best_50)} filas (0% - 50%)")
        print(f"       - Worst_50: {len(worst_50)} filas (50% - 100%)")

        # ─────────────────────────────────────────────
        # NIVEL 25%
        # ─────────────────────────────────────────────
        dir_25 = os.path.join(self.dir_base, "nivel_25", "tablas")
        os.makedirs(dir_25, exist_ok=True)
        k25 = int(n * 0.25)

        bloques_25 = [
            ("Best_25_1",  df_ordenado.iloc[0:k25].copy(),        "0% - 25%"),
            ("Best_25_2",  df_ordenado.iloc[k25:2*k25].copy(),    "25% - 50%"),
            ("Worst_25_1", df_ordenado.iloc[2*k25:3*k25].copy(),  "50% - 75%"),
            ("Worst_25_2", df_ordenado.iloc[3*k25:n].copy(),      "75% - 100%"),
        ]

        print(f"   💾 Nivel 25% guardado en {dir_25}:")
        for nombre, sub_df, rango in bloques_25:
            ruta = os.path.join(dir_25, f"{nombre}.csv")
            sub_df.to_csv(ruta, index=False)
            self.particiones[nombre] = {"nivel": "25", "ruta_csv": ruta, "df": sub_df}
            print(f"       - {nombre}: {len(sub_df)} filas ({rango})")

        # ─────────────────────────────────────────────
        # NIVEL 12.5%
        # ─────────────────────────────────────────────
        dir_125 = os.path.join(self.dir_base, "nivel_12.5", "tablas")
        os.makedirs(dir_125, exist_ok=True)
        k125 = int(n * 0.125)

        bloques_125 = [
            ("Best_12.5_1",  df_ordenado.iloc[0:k125].copy(),          "0% - 12.5%"),
            ("Best_12.5_2",  df_ordenado.iloc[k125:2*k125].copy(),     "12.5% - 25%"),
            ("Best_12.5_3",  df_ordenado.iloc[2*k125:3*k125].copy(),   "25% - 37.5%"),
            ("Best_12.5_4",  df_ordenado.iloc[3*k125:4*k125].copy(),   "37.5% - 50%"),
            ("Worst_12.5_1", df_ordenado.iloc[4*k125:5*k125].copy(),   "50% - 62.5%"),
            ("Worst_12.5_2", df_ordenado.iloc[5*k125:6*k125].copy(),   "62.5% - 75%"),
            ("Worst_12.5_3", df_ordenado.iloc[6*k125:7*k125].copy(),   "75% - 87.5%"),
            ("Worst_12.5_4", df_ordenado.iloc[7*k125:n].copy(),        "87.5% - 100%"),
        ]

        print(f"   💾 Nivel 12.5% guardado en {dir_125}:")
        for nombre, sub_df, rango in bloques_125:
            ruta = os.path.join(dir_125, f"{nombre}.csv")
            sub_df.to_csv(ruta, index=False)
            self.particiones[nombre] = {"nivel": "12.5", "ruta_csv": ruta, "df": sub_df}
            print(f"       - {nombre}: {len(sub_df)} filas ({rango})")

        return self.particiones

    def ejecutar(self, df):
        print("   Iniciando particionamiento jerárquico por bloques (50%, 25%, 12.5%)...")
        return self.crear_particiones(df)
