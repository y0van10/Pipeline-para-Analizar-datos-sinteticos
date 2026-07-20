import pandas as pd
import numpy as np
import os

class ConvertidorDataset:
    """
    Clase encargada de convertir datasets externos al formato estándar de 11 columnas
    que el pipeline espera:
    X1_sexo, X2_zona, X3_ciclo, X4_ingreso_familiar, X5_trabaja, X6_beca,
    X7_educ_jefe, X8_tam_familiar, X9_asistencia, X10_cursos_desaprobados, X11_promedio_final
    """
    COLUMNAS_SALIDA = [
        "X1_sexo", "X2_zona", "X3_ciclo", "X4_ingreso_familiar",
        "X5_trabaja", "X6_beca", "X7_educ_jefe", "X8_tam_familiar",
        "X9_asistencia", "X10_cursos_desaprobados", "X11_promedio_final"
    ]

    # Mapeos conocidos de datasets populares
    MAPEOS_CONOCIDOS = {
        # Kaggle: Student Performance Factors (20 columnas)
        "student_performance_factors": {
            "columnas_clave": ["Hours_Studied", "Attendance", "Exam_Score", "Gender"],
            "mapeo": {
                "X1_sexo": "Gender",
                "X2_zona": "School_Type",
                "X3_ciclo": "Hours_Studied",
                "X4_ingreso_familiar": "Family_Income",
                "X5_trabaja": "Extracurricular_Activities",
                "X6_beca": "Internet_Access",
                "X7_educ_jefe": "Parental_Education_Level",
                "X8_tam_familiar": "Tutoring_Sessions",
                "X9_asistencia": "Attendance",
                "X10_cursos_desaprobados": "Previous_Scores",
                "X11_promedio_final": "Exam_Score"
            }
        },
        # UCI: Student Performance (33 columnas, student-mat.csv o student-por.csv)
        "uci_student_performance": {
            "columnas_clave": ["sex", "address", "G3", "Medu"],
            "mapeo": {
                "X1_sexo": "sex",
                "X2_zona": "address",
                "X3_ciclo": "age",
                "X4_ingreso_familiar": "famrel",
                "X5_trabaja": "paid",
                "X6_beca": "internet",
                "X7_educ_jefe": "Medu",
                "X8_tam_familiar": "famsize",
                "X9_asistencia": "absences",
                "X10_cursos_desaprobados": "failures",
                "X11_promedio_final": "G3"
            }
        }
    }

    def __init__(self):
        self.dataset_detectado = None

    def detectar_dataset(self, df):
        cols = set(df.columns)
        for nombre, config in self.MAPEOS_CONOCIDOS.items():
            if all(c in cols for c in config["columnas_clave"]):
                self.dataset_detectado = nombre
                print(f"   🔍 Dataset detectado: {nombre}")
                return nombre
        return None

    def ya_es_compatible(self, df):
        return list(df.columns) == self.COLUMNAS_SALIDA or df.shape[1] == len(self.COLUMNAS_SALIDA)

    def _convertir_student_performance_factors(self, df):
        """Convierte el dataset 'Student Performance Factors' de Kaggle (20 cols)"""
        df_out = pd.DataFrame()

        # X1_sexo: Gender (Male/Female -> Masculino/Femenino)
        df_out["X1_sexo"] = df["Gender"].apply(
            lambda x: "Masculino" if str(x).strip().lower() in ["male", "m"] else "Femenino"
        )

        # X2_zona: School_Type (Public -> Urbana, Private -> Rural como proxy)
        df_out["X2_zona"] = df["School_Type"].apply(
            lambda x: "Urbana" if str(x).strip().lower() == "public" else "Rural"
        )

        # X3_ciclo: Hours_Studied (1-44 -> escalado a 1-10 como ciclos)
        hs = pd.to_numeric(df["Hours_Studied"], errors="coerce").fillna(0)
        df_out["X3_ciclo"] = np.clip(np.round(hs / 4.4), 1, 10).astype(int)

        # X4_ingreso_familiar: Family_Income (Low/Medium/High -> 800/2500/5000)
        income_map = {"low": 800, "medium": 2500, "high": 5000}
        df_out["X4_ingreso_familiar"] = df["Family_Income"].apply(
            lambda x: income_map.get(str(x).strip().lower(), 2500)
        )

        # X5_trabaja: Extracurricular_Activities (Yes/No -> Sí/No)
        df_out["X5_trabaja"] = df["Extracurricular_Activities"].apply(
            lambda x: "No" if str(x).strip().lower() in ["no", "n"] else "Sí"
        )

        # X6_beca: Internet_Access (Yes/No -> Sí/No)
        df_out["X6_beca"] = df["Internet_Access"].apply(
            lambda x: "No" if str(x).strip().lower() in ["no", "n"] else "Sí"
        )

        # X7_educ_jefe: Parental_Education_Level
        educ_map = {
            "high school": "Secundaria",
            "college": "Superior técnica",
            "postgraduate": "Superior universitaria"
        }
        df_out["X7_educ_jefe"] = df["Parental_Education_Level"].apply(
            lambda x: educ_map.get(str(x).strip().lower(), "Secundaria")
        )

        # X8_tam_familiar: Tutoring_Sessions (0-8, usar como proxy de tamaño familiar 1-8)
        ts = pd.to_numeric(df["Tutoring_Sessions"], errors="coerce").fillna(3)
        df_out["X8_tam_familiar"] = np.clip(ts + 1, 1, 10).astype(int)

        # X9_asistencia: Attendance (ya es porcentaje 0-100)
        df_out["X9_asistencia"] = pd.to_numeric(df["Attendance"], errors="coerce").fillna(80)

        # X10_cursos_desaprobados: Previous_Scores invertido (bajo puntaje = más desaprobados)
        prev = pd.to_numeric(df["Previous_Scores"], errors="coerce").fillna(50)
        # Escalar: 100 puntos previos -> 0 desaprobados, 0 puntos -> 5 desaprobados
        df_out["X10_cursos_desaprobados"] = np.clip(np.round((100 - prev) / 20), 0, 5).astype(int)

        # X11_promedio_final: Exam_Score (0-100 -> escalar a 0-20)
        exam = pd.to_numeric(df["Exam_Score"], errors="coerce").fillna(50)
        df_out["X11_promedio_final"] = np.round(exam / 5, 1)

        return df_out

    def _convertir_uci_student_performance(self, df):
        """Convierte el dataset UCI Student Performance (33 cols)"""
        df_out = pd.DataFrame()

        # X1_sexo: sex (F/M -> Femenino/Masculino)
        df_out["X1_sexo"] = df["sex"].apply(
            lambda x: "Masculino" if str(x).strip().upper() == "M" else "Femenino"
        )

        # X2_zona: address (U/R -> Urbana/Rural)
        df_out["X2_zona"] = df["address"].apply(
            lambda x: "Urbana" if str(x).strip().upper() == "U" else "Rural"
        )

        # X3_ciclo: age (15-22 -> escalar a ciclos 1-10)
        age = pd.to_numeric(df["age"], errors="coerce").fillna(17)
        df_out["X3_ciclo"] = np.clip(age - 14, 1, 10).astype(int)

        # X4_ingreso_familiar: famrel (1-5 -> escalado a ingresos)
        famrel = pd.to_numeric(df["famrel"], errors="coerce").fillna(3)
        df_out["X4_ingreso_familiar"] = (famrel * 1000).astype(int)

        # X5_trabaja: paid (yes/no -> Sí/No)
        if "paid" in df.columns:
            df_out["X5_trabaja"] = df["paid"].apply(
                lambda x: "No" if str(x).strip().lower() in ["no", "n"] else "Sí"
            )
        else:
            df_out["X5_trabaja"] = "No"

        # X6_beca: internet (yes/no -> Sí/No)
        df_out["X6_beca"] = df["internet"].apply(
            lambda x: "No" if str(x).strip().lower() in ["no", "n"] else "Sí"
        )

        # X7_educ_jefe: Medu (0-4)
        educ_map = {0: "Sin educación", 1: "Primaria", 2: "Secundaria", 3: "Superior técnica", 4: "Superior universitaria"}
        medu = pd.to_numeric(df["Medu"], errors="coerce").fillna(2).astype(int)
        df_out["X7_educ_jefe"] = medu.map(educ_map).fillna("Secundaria")

        # X8_tam_familiar: famsize (GT3/LE3 -> 5/3)
        df_out["X8_tam_familiar"] = df["famsize"].apply(
            lambda x: 5 if str(x).strip().upper() == "GT3" else 3
        )

        # X9_asistencia: absences (invertir: más ausencias = menos asistencia)
        absences = pd.to_numeric(df["absences"], errors="coerce").fillna(5)
        df_out["X9_asistencia"] = np.clip(100 - absences * 2, 0, 100).round(1)

        # X10_cursos_desaprobados: failures (0-4)
        df_out["X10_cursos_desaprobados"] = pd.to_numeric(df["failures"], errors="coerce").fillna(0).astype(int)

        # X11_promedio_final: G3 (0-20, ya está en escala vigesimal)
        df_out["X11_promedio_final"] = pd.to_numeric(df["G3"], errors="coerce").fillna(10)

        return df_out

    def convertir(self, ruta_entrada, ruta_salida=None):
        print(f"\n   📂 Cargando dataset externo: {ruta_entrada}")
        try:
            df = pd.read_csv(ruta_entrada, encoding="utf-8")
        except UnicodeDecodeError:
            df = pd.read_csv(ruta_entrada, encoding="latin-1")

        print(f"   📊 Dimensiones: {df.shape[0]} filas × {df.shape[1]} columnas")
        print(f"   📋 Columnas: {list(df.columns)}")

        # Si ya es compatible, no convertir
        if self.ya_es_compatible(df):
            print("   ✅ Dataset ya es compatible, no requiere conversión.")
            return ruta_entrada

        # Detectar tipo de dataset
        tipo = self.detectar_dataset(df)
        if tipo is None:
            raise ValueError(
                f"❌ No se pudo detectar automáticamente el tipo de dataset.\n"
                f"   Columnas encontradas: {list(df.columns)}\n"
                f"   Datasets soportados: {list(self.MAPEOS_CONOCIDOS.keys())}"
            )

        # Convertir
        if tipo == "student_performance_factors":
            df_convertido = self._convertir_student_performance_factors(df)
        elif tipo == "uci_student_performance":
            df_convertido = self._convertir_uci_student_performance(df)
        else:
            raise ValueError(f"❌ Convertidor no implementado para: {tipo}")

        # Guardar
        if ruta_salida is None:
            base = os.path.splitext(ruta_entrada)[0]
            ruta_salida = f"{base}_convertido.csv"

        df_convertido.to_csv(ruta_salida, index=False)
        print(f"\n   ✅ Dataset convertido guardado en: {ruta_salida}")
        print(f"   📊 Dimensiones finales: {df_convertido.shape[0]} filas × {df_convertido.shape[1]} columnas")
        print(f"   📋 Columnas: {list(df_convertido.columns)}")
        print(f"\n   📌 Mapeo aplicado ({tipo}):")
        for col_out, col_in in self.MAPEOS_CONOCIDOS[tipo]["mapeo"].items():
            print(f"      {col_in:30s} → {col_out}")

        return ruta_salida
