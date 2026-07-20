import pandas as pd
import numpy as np
import os

class ConvertidorDataset:
    """
    Convertidor Universal de Datasets.
    Recibe cualquier CSV y permite mapear sus columnas al formato estándar de 11 variables
    del pipeline NCD/Gzip. Incluye auto-sugerencias inteligentes por nombre de columna.
    """
    COLUMNAS_SALIDA = [
        "X1_sexo", "X2_zona", "X3_ciclo", "X4_ingreso_familiar",
        "X5_trabaja", "X6_beca", "X7_educ_jefe", "X8_tam_familiar",
        "X9_asistencia", "X10_cursos_desaprobados", "X11_promedio_final"
    ]

    DESCRIPCIONES = {
        "X1_sexo": "Sexo / Género (categórica: Masculino/Femenino)",
        "X2_zona": "Zona geográfica (categórica: Urbana/Rural)",
        "X3_ciclo": "Ciclo / Año / Nivel académico (numérica)",
        "X4_ingreso_familiar": "Ingreso familiar (numérica)",
        "X5_trabaja": "¿Trabaja? (categórica: Sí/No)",
        "X6_beca": "¿Tiene beca/apoyo? (categórica: Sí/No)",
        "X7_educ_jefe": "Educación del jefe de familia (categórica ordinal)",
        "X8_tam_familiar": "Tamaño familiar (numérica)",
        "X9_asistencia": "Asistencia % (numérica 0-100)",
        "X10_cursos_desaprobados": "Cursos desaprobados / Fallos (numérica)",
        "X11_promedio_final": "Nota / Promedio final (numérica, variable objetivo)"
    }

    # Palabras clave para auto-sugerencia (idioma neutral)
    KEYWORDS = {
        "X1_sexo": ["sex", "gender", "genero", "sexo", "male", "female"],
        "X2_zona": ["zone", "zona", "address", "area", "urban", "rural", "school_type", "region", "location"],
        "X3_ciclo": ["cycle", "ciclo", "year", "age", "grade", "level", "semester", "hours_studied", "study"],
        "X4_ingreso_familiar": ["income", "ingreso", "salary", "earning", "family_income", "economic"],
        "X5_trabaja": ["work", "trabaja", "job", "employ", "extracurricular", "paid", "activity"],
        "X6_beca": ["scholarship", "beca", "internet", "access", "support", "aid", "financial"],
        "X7_educ_jefe": ["education", "educ", "parent", "mother", "father", "medu", "fedu", "parental_education"],
        "X8_tam_familiar": ["family_size", "famsize", "familiar", "household", "members", "tutoring", "sleep"],
        "X9_asistencia": ["attendance", "asistencia", "absence", "present", "absent"],
        "X10_cursos_desaprobados": ["fail", "failure", "desaprob", "disapproved", "previous_scores", "repeat"],
        "X11_promedio_final": ["score", "grade", "promedio", "final", "exam", "gpa", "average", "result", "mark", "g3", "g1", "g2"]
    }

    def __init__(self):
        pass

    def ya_es_compatible(self, df):
        return list(df.columns) == self.COLUMNAS_SALIDA or df.shape[1] == len(self.COLUMNAS_SALIDA)

    def auto_sugerir(self, columnas_origen):
        """
        Dado un listado de columnas del CSV externo, sugiere automáticamente
        cuál columna origen es la mejor candidata para cada variable destino.
        Devuelve dict {variable_destino: columna_origen_sugerida}
        """
        sugerencias = {}
        usadas = set()

        for var_destino, keywords in self.KEYWORDS.items():
            mejor_match = None
            mejor_score = 0
            for col in columnas_origen:
                col_lower = col.lower().replace("_", " ").replace("-", " ")
                score = sum(1 for kw in keywords if kw in col_lower)
                if score > mejor_score and col not in usadas:
                    mejor_score = score
                    mejor_match = col
            if mejor_match:
                sugerencias[var_destino] = mejor_match
                usadas.add(mejor_match)

        return sugerencias

    def transformar_columna(self, serie, var_destino):
        """
        Transforma inteligentemente una columna al formato esperado por el pipeline,
        detectando automáticamente si es numérica o categórica.
        """
        # Variables categóricas binarias (Sí/No)
        if var_destino in ("X5_trabaja", "X6_beca"):
            if serie.dtype == object or serie.nunique() <= 5:
                vals_unicos = serie.dropna().unique()
                # Detectar si es yes/no, true/false, 1/0, si/no
                positivos = {"yes", "y", "true", "1", "si", "sí", "s", "male", "1.0"}
                return serie.apply(
                    lambda x: "Sí" if str(x).strip().lower() in positivos else "No"
                )
            else:
                # Numérica: binarizar por mediana
                mediana = pd.to_numeric(serie, errors="coerce").median()
                return serie.apply(
                    lambda x: "Sí" if pd.to_numeric(x, errors="coerce") is not None 
                    and float(pd.to_numeric(x, errors="coerce") or 0) >= mediana else "No"
                )

        # X1_sexo
        if var_destino == "X1_sexo":
            map_sexo = {
                "male": "Masculino", "m": "Masculino", "masculino": "Masculino", "hombre": "Masculino", "1": "Masculino",
                "female": "Femenino", "f": "Femenino", "femenino": "Femenino", "mujer": "Femenino", "0": "Femenino", "2": "Femenino"
            }
            return serie.apply(lambda x: map_sexo.get(str(x).strip().lower(), "Masculino"))

        # X2_zona
        if var_destino == "X2_zona":
            map_zona = {
                "urban": "Urbana", "u": "Urbana", "urbana": "Urbana", "city": "Urbana", "public": "Urbana",
                "rural": "Rural", "r": "Rural", "private": "Rural", "near": "Urbana", "far": "Rural", "moderate": "Urbana"
            }
            return serie.apply(lambda x: map_zona.get(str(x).strip().lower(), "Urbana"))

        # X7_educ_jefe
        if var_destino == "X7_educ_jefe":
            if serie.dtype == object:
                map_educ = {
                    "none": "Sin educación", "sin": "Sin educación", "0": "Sin educación",
                    "primary": "Primaria", "primaria": "Primaria", "elementary": "Primaria", "1": "Primaria",
                    "secondary": "Secundaria", "secundaria": "Secundaria", "high school": "Secundaria", "high_school": "Secundaria", "2": "Secundaria",
                    "college": "Superior técnica", "technical": "Superior técnica", "associate": "Superior técnica", "3": "Superior técnica",
                    "university": "Superior universitaria", "postgraduate": "Superior universitaria", "master": "Superior universitaria",
                    "bachelor": "Superior universitaria", "4": "Superior universitaria"
                }
                return serie.apply(lambda x: map_educ.get(str(x).strip().lower(), "Secundaria"))
            else:
                niveles = {0: "Sin educación", 1: "Primaria", 2: "Secundaria", 3: "Superior técnica", 4: "Superior universitaria"}
                vals = pd.to_numeric(serie, errors="coerce").fillna(2).clip(0, 4).astype(int)
                return vals.map(niveles)

        # Variables numéricas
        vals = pd.to_numeric(serie, errors="coerce")
        if vals.isna().all():
            # Categórica con valores de texto -> codificar ordinalmente
            categorias = serie.dropna().unique()
            cat_map = {c: i for i, c in enumerate(sorted(categorias))}
            vals = serie.map(cat_map).fillna(0)

        vals = vals.fillna(vals.median() if not vals.isna().all() else 0)

        # Escalar según la variable destino
        if var_destino == "X11_promedio_final":
            # Escalar a rango 0-20
            vmin, vmax = vals.min(), vals.max()
            if vmax > vmin:
                vals = ((vals - vmin) / (vmax - vmin)) * 20
            return vals.round(1)

        if var_destino == "X9_asistencia":
            # Escalar a 0-100
            vmin, vmax = vals.min(), vals.max()
            if vmax > 100:
                vals = ((vals - vmin) / (vmax - vmin)) * 100
            return vals.clip(0, 100).round(1)

        if var_destino == "X10_cursos_desaprobados":
            return vals.clip(0, None).astype(int)

        if var_destino == "X4_ingreso_familiar":
            # Si los valores son categoricos como Low/Medium/High
            if serie.dtype == object:
                income_map = {"low": 800, "medium": 2500, "high": 5000}
                return serie.apply(lambda x: income_map.get(str(x).strip().lower(), 2500))
            return vals.clip(0, None)

        # X3_ciclo, X8_tam_familiar y otros numéricos genéricos
        return vals

    def convertir(self, df, mapeo):
        """
        Convierte un DataFrame usando el mapeo {variable_destino: columna_origen}.
        Aplica transformaciones inteligentes automáticamente.
        """
        df_out = pd.DataFrame()

        for var_destino in self.COLUMNAS_SALIDA:
            col_origen = mapeo.get(var_destino)
            if col_origen and col_origen in df.columns:
                df_out[var_destino] = self.transformar_columna(df[col_origen].copy(), var_destino)
            else:
                # Rellenar con valor por defecto
                if var_destino in ("X1_sexo",):
                    df_out[var_destino] = "Masculino"
                elif var_destino in ("X2_zona",):
                    df_out[var_destino] = "Urbana"
                elif var_destino in ("X5_trabaja", "X6_beca"):
                    df_out[var_destino] = "No"
                elif var_destino == "X7_educ_jefe":
                    df_out[var_destino] = "Secundaria"
                else:
                    df_out[var_destino] = 0

        return df_out

    def convertir_y_guardar(self, ruta_entrada, mapeo, ruta_salida=None):
        """Lee un CSV, aplica el mapeo y guarda el resultado."""
        try:
            df = pd.read_csv(ruta_entrada, encoding="utf-8")
        except UnicodeDecodeError:
            df = pd.read_csv(ruta_entrada, encoding="latin-1")

        df_convertido = self.convertir(df, mapeo)

        if ruta_salida is None:
            base = os.path.splitext(ruta_entrada)[0]
            ruta_salida = f"{base}_convertido.csv"

        df_convertido.to_csv(ruta_salida, index=False)
        return ruta_salida, df_convertido
