import pandas as pd
import os

class DataCleaner:
    """
    Clase encargada de cargar, validar y limpiar el dataset de estudiantes.
    """
    COLUMNAS_ESPERADAS = [
        "X1_sexo", "X2_zona", "X3_ciclo", "X4_ingreso_familiar",
        "X5_trabaja", "X6_beca", "X7_educ_jefe", "X8_tam_familiar",
        "X9_asistencia", "X10_cursos_desaprobados", "X11_promedio_final"
    ]

    def __init__(self, data_path):
        self.data_path = os.path.normpath(data_path)
        self.raw_df = None
        self.cleaned_df = None
        self.report = {}

    def cargar_datos(self):
        print(f"   📂 Leyendo: {self.data_path}")
        try:
            self.raw_df = pd.read_csv(self.data_path, encoding="utf-8")
        except UnicodeDecodeError:
            self.raw_df = pd.read_csv(self.data_path, encoding="latin-1")
            print("   ⚠️  Codificación cambiada a latin-1")
        print(f"   ✅ Datos cargados: {self.raw_df.shape[0]} filas × {self.raw_df.shape[1]} columnas")
        return self.raw_df

    def validar_columnas(self):
        if self.raw_df is None:
            raise ValueError("❌ No hay datos cargados. Llama a cargar_datos() primero.")
            
        if list(self.raw_df.columns) == self.COLUMNAS_ESPERADAS:
            print("   ✅ Columnas correctas")
            return
            
        if self.raw_df.shape[1] == len(self.COLUMNAS_ESPERADAS):
            print("   ⚠️  Nombres de columnas no coinciden, renombrando por posición...")
            self.raw_df.columns = self.COLUMNAS_ESPERADAS
            print("   ✅ Columnas renombradas correctamente")
            return

        raise ValueError(
            f"❌ El dataset tiene {self.raw_df.shape[1]} columnas, se esperaban {len(self.COLUMNAS_ESPERADAS)}.\n"
            f"   Columnas encontradas: {list(self.raw_df.columns)}"
        )

    def limpiar_datos(self):
        if self.raw_df is None:
            raise ValueError("❌ No hay datos cargados. Llama a cargar_datos() primero.")

        df = self.raw_df.copy()
        n_original = len(df)
        self.report = {"original": n_original}

        # 1. Duplicados
        n_antes = len(df)
        df = df.drop_duplicates()
        n_dup = n_antes - len(df)
        self.report["duplicados_eliminados"] = n_dup
        if n_dup > 0:
            print(f"   🗑️  Duplicados eliminados: {n_dup}")
        else:
            print(f"   ✅ Sin duplicados")

        # 2. Valores nulos
        n_antes = len(df)
        nulos_por_col = df.isnull().sum()
        nulos_total = nulos_por_col.sum()
        if nulos_total > 0:
            print(f"   ⚠️  Valores nulos encontrados: {nulos_total}")
            df = df.dropna()
            print(f"   🗑️  Filas eliminadas por nulos: {n_antes - len(df)}")
        else:
            print(f"   ✅ Sin valores nulos")
        self.report["nulos_eliminados"] = n_antes - len(df)

        # 3. Convertir columnas numéricas
        cols_numericas = ["X3_ciclo", "X4_ingreso_familiar", "X8_tam_familiar",
                          "X9_asistencia", "X10_cursos_desaprobados", "X11_promedio_final"]
        for col in cols_numericas:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        n_antes = len(df)
        df = df.dropna()
        self.report["no_numericos_eliminados"] = n_antes - len(df)

        # 4. Validaciones lógicas
        n_antes = len(df)
        df = df[df["X11_promedio_final"] >= 0]
        df = df[df["X11_promedio_final"] <= 20]
        df = df[df["X9_asistencia"] >= 0]
        df = df[df["X9_asistencia"] <= 100]
        df = df[df["X10_cursos_desaprobados"] >= 0]
        df = df[df["X4_ingreso_familiar"] >= 0]
        self.report["fuera_rango_eliminados"] = n_antes - len(df)

        df = df.reset_index(drop=True)
        self.cleaned_df = df

        self.report["final"] = len(df)
        self.report["total_eliminados"] = n_original - len(df)

        print(f"\n   📊 RESUMEN DE LIMPIEZA:")
        print(f"      Filas originales:  {self.report['original']}")
        print(f"      Filas eliminadas:  {self.report['total_eliminados']}")
        print(f"      Filas finales:     {self.report['final']}")
        print(f"      Retención:         {100 * self.report['final'] / self.report['original']:.1f}%\n")
        
        return self.cleaned_df

    def ejecutar(self):
        self.cargar_datos()
        self.validar_columnas()
        self.limpiar_datos()
        return self.cleaned_df, self.report
