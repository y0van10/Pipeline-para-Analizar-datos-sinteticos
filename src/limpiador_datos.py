import pandas as pd
import numpy as np
import os

class LimpiadorDatos:
    """
    Clase encargada de cargar, validar y limpiar cualquier dataset CSV.
    Funciona con cualquier número de columnas; solo requiere que la columna
    objetivo (col_objetivo) exista y tenga valores numéricos.
    """
    def __init__(self, ruta_datos, col_objetivo=None):
        self.ruta_datos = os.path.normpath(ruta_datos)
        self.col_objetivo = col_objetivo  # columna a predecir/analizar
        self.df_original = None
        self.df_limpio = None
        self.reporte = {}

    def cargar_datos(self):
        print(f"   📂 Leyendo: {self.ruta_datos}")
        try:
            self.df_original = pd.read_csv(self.ruta_datos, encoding="utf-8")
        except UnicodeDecodeError:
            self.df_original = pd.read_csv(self.ruta_datos, encoding="latin-1")
            print("   ⚠️  Codificación cambiada a latin-1")
        print(f"   ✅ Datos cargados: {self.df_original.shape[0]} filas × {self.df_original.shape[1]} columnas")
        return self.df_original

    def detectar_col_objetivo(self):
        """
        Si no se indicó col_objetivo, intenta detectarla automáticamente
        buscando palabras clave en los nombres de las columnas numéricas.
        """
        if self.col_objetivo and self.col_objetivo in self.df_original.columns:
            return self.col_objetivo

        keywords = [
            "promedio", "final", "score", "exam", "grade", "gpa",
            "nota", "rendimiento", "resultado", "average", "mark", "g3", "x11"
        ]
        cols_numericas = self.df_original.select_dtypes(include=[np.number]).columns.tolist()

        for kw in keywords:
            for col in cols_numericas:
                if kw in col.lower():
                    print(f"   🔍 Variable objetivo detectada automáticamente: '{col}'")
                    self.col_objetivo = col
                    return col

        # Si no encuentra nada, usa la última columna numérica
        if cols_numericas:
            self.col_objetivo = cols_numericas[-1]
            print(f"   ⚠️  No se detectó variable objetivo. Usando última columna numérica: '{self.col_objetivo}'")
            return self.col_objetivo

        raise ValueError("❌ No se encontró ninguna columna numérica para usar como variable objetivo.")

    def validar_columnas(self):
        if self.df_original is None:
            raise ValueError("❌ No hay datos cargados. Llama a cargar_datos() primero.")

        n_cols = self.df_original.shape[1]
        if n_cols < 2:
            raise ValueError(f"❌ El dataset necesita al menos 2 columnas. Solo tiene {n_cols}.")

        # Detectar/verificar columna objetivo
        self.detectar_col_objetivo()

        print(f"   ✅ Dataset válido: {n_cols} columnas | Objetivo: '{self.col_objetivo}'")
        print(f"   📋 Columnas: {list(self.df_original.columns)}")

    def limpiar_datos(self):
        if self.df_original is None:
            raise ValueError("❌ No hay datos cargados.")

        df = self.df_original.copy()
        n_original = len(df)
        self.reporte = {"original": n_original, "col_objetivo": self.col_objetivo}

        # 1. Duplicados
        n_antes = len(df)
        df = df.drop_duplicates()
        n_dup = n_antes - len(df)
        self.reporte["duplicados_eliminados"] = n_dup
        print(f"    {'Duplicados eliminados: ' + str(n_dup) if n_dup > 0 else 'Sin duplicados'}")

        # 2. Valores nulos
        n_antes = len(df)
        nulos_total = df.isnull().sum().sum()
        if nulos_total > 0:
            print(f"     Valores nulos encontrados: {nulos_total}")
            df = df.dropna(subset=[self.col_objetivo])  # solo eliminamos si falta el objetivo
            # Rellenar nulos en otras columnas con mediana (numéricas) o moda (categóricas)
            for col in df.columns:
                if col == self.col_objetivo:
                    continue
                if df[col].dtype in [np.float64, np.int64, float, int]:
                    df[col] = df[col].fillna(df[col].median())
                else:
                    df[col] = df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else "Desconocido")
        else:
            print(f"    Sin valores nulos")
        self.reporte["nulos_eliminados"] = n_antes - len(df)

        # 3. Convertir columna objetivo a numérica
        df[self.col_objetivo] = pd.to_numeric(df[self.col_objetivo], errors="coerce")
        n_antes = len(df)
        df = df.dropna(subset=[self.col_objetivo])
        self.reporte["no_numericos_eliminados"] = n_antes - len(df)

        # 4. Eliminar filas donde el objetivo sea negativo (si aplica)
        n_antes = len(df)
        df = df[df[self.col_objetivo] >= 0]
        self.reporte["fuera_rango_eliminados"] = n_antes - len(df)

        df = df.reset_index(drop=True)
        self.df_limpio = df

        self.reporte["final"] = len(df)
        self.reporte["total_eliminados"] = n_original - len(df)
        self.reporte["columnas"] = list(df.columns)

        print(f"\n    RESUMEN DE LIMPIEZA:")
        print(f"      Filas originales:  {self.reporte['original']}")
        print(f"      Filas eliminadas:  {self.reporte['total_eliminados']}")
        print(f"      Filas finales:     {self.reporte['final']}")
        print(f"      Retención:         {100 * self.reporte['final'] / self.reporte['original']:.1f}%\n")

        return self.df_limpio

    def ejecutar(self):
        self.cargar_datos()
        self.validar_columnas()
        self.limpiar_datos()
        return self.df_limpio, self.reporte
