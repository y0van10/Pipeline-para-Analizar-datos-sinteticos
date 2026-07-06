"""
=============================================================
  PASO 1: LIMPIEZA DE DATOS
=============================================================
Lee el dataset de estudiantes, elimina valores nulos,
duplicados e inconsistencias. Reporta estadísticas de
limpieza para documentar el proceso.
=============================================================
"""

import pandas as pd
import os

# ── CONFIGURACIÓN ──────────────────────────────────────────
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "estudiantes.csv")

COLUMNAS_ESPERADAS = [
    "X1_sexo", "X2_zona", "X3_ciclo", "X4_ingreso_familiar",
    "X5_trabaja", "X6_beca", "X7_educ_jefe", "X8_tam_familiar",
    "X9_asistencia", "X10_cursos_desaprobados", "X11_promedio_final"
]

# Variables que se usarán en el análisis NCD (sin X11 que es la de clasificación)
VARIABLES_ANALISIS = [
    "X1_sexo", "X2_zona", "X3_ciclo", "X4_ingreso_familiar",
    "X5_trabaja", "X6_beca", "X7_educ_jefe", "X8_tam_familiar",
    "X9_asistencia", "X10_cursos_desaprobados"
]

VARIABLE_OBJETIVO = "X11_promedio_final"
# ───────────────────────────────────────────────────────────


def cargar_datos():
    """
    Lee el CSV del dataset de estudiantes.
    Intenta con codificación utf-8, si falla usa latin-1.
    """
    path = os.path.normpath(DATA_PATH)
    print(f"   📂 Leyendo: {path}")

    try:
        df = pd.read_csv(path, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(path, encoding="latin-1")
        print("   ⚠️  Codificación cambiada a latin-1")

    print(f"   ✅ Datos cargados: {df.shape[0]} filas × {df.shape[1]} columnas")
    return df


def validar_columnas(df):
    """
    Verifica que el DataFrame tenga exactamente las 11 columnas esperadas.
    Si los nombres no coinciden, intenta renombrarlas por posición.
    """
    if list(df.columns) == COLUMNAS_ESPERADAS:
        print("   ✅ Columnas correctas")
        return df

    if df.shape[1] == len(COLUMNAS_ESPERADAS):
        print("   ⚠️  Nombres de columnas no coinciden, renombrando por posición...")
        df.columns = COLUMNAS_ESPERADAS
        print("   ✅ Columnas renombradas correctamente")
        return df

    raise ValueError(
        f"❌ El dataset tiene {df.shape[1]} columnas, se esperaban {len(COLUMNAS_ESPERADAS)}.\n"
        f"   Columnas encontradas: {list(df.columns)}"
    )


def limpiar_datos(df):
    """
    Proceso de limpieza:
    1. Eliminar filas completamente duplicadas
    2. Eliminar filas con valores nulos
    3. Convertir columnas numéricas al tipo correcto
    4. Eliminar valores fuera de rango lógico
    """
    n_original = len(df)
    reporte = {"original": n_original}

    # 1. Duplicados
    n_antes = len(df)
    df = df.drop_duplicates()
    n_dup = n_antes - len(df)
    reporte["duplicados_eliminados"] = n_dup
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
        for col, n in nulos_por_col[nulos_por_col > 0].items():
            print(f"       - {col}: {n} nulos")
        df = df.dropna()
        print(f"   🗑️  Filas eliminadas por nulos: {n_antes - len(df)}")
    else:
        print(f"   ✅ Sin valores nulos")
    reporte["nulos_eliminados"] = n_antes - len(df)

    # 3. Convertir columnas numéricas
    cols_numericas = ["X3_ciclo", "X4_ingreso_familiar", "X8_tam_familiar",
                      "X9_asistencia", "X10_cursos_desaprobados", "X11_promedio_final"]
    for col in cols_numericas:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Eliminar filas donde la conversión generó NaN
    n_antes = len(df)
    df = df.dropna()
    if n_antes - len(df) > 0:
        print(f"   🗑️  Filas con valores no numéricos eliminadas: {n_antes - len(df)}")
    reporte["no_numericos_eliminados"] = n_antes - len(df)

    # 4. Validaciones lógicas
    n_antes = len(df)
    df = df[df["X11_promedio_final"] >= 0]
    df = df[df["X11_promedio_final"] <= 20]
    df = df[df["X9_asistencia"] >= 0]
    df = df[df["X9_asistencia"] <= 100]
    df = df[df["X10_cursos_desaprobados"] >= 0]
    df = df[df["X4_ingreso_familiar"] >= 0]
    reporte["fuera_rango_eliminados"] = n_antes - len(df)
    if n_antes - len(df) > 0:
        print(f"   🗑️  Filas fuera de rango lógico: {n_antes - len(df)}")

    df = df.reset_index(drop=True)

    # Resumen
    reporte["final"] = len(df)
    reporte["total_eliminados"] = n_original - len(df)
    print(f"\n   📊 RESUMEN DE LIMPIEZA:")
    print(f"      Filas originales:  {reporte['original']}")
    print(f"      Filas eliminadas:  {reporte['total_eliminados']}")
    print(f"      Filas finales:     {reporte['final']}")
    print(f"      Retención:         {100 * reporte['final'] / reporte['original']:.1f}%")

    return df, reporte


def ejecutar():
    """Punto de entrada del paso 1."""
    print("\n   Cargando dataset...")
    df = cargar_datos()

    print("\n   Validando columnas...")
    df = validar_columnas(df)

    print("\n   Limpiando datos...")
    df, reporte = limpiar_datos(df)

    # Estadísticas descriptivas del dataset limpio
    print(f"\n   📋 ESTADÍSTICAS DEL DATASET LIMPIO:")
    print(f"      Estudiantes: {len(df)}")
    print(f"      Promedio final - Media:   {df['X11_promedio_final'].mean():.2f}")
    print(f"      Promedio final - Mediana: {df['X11_promedio_final'].median():.2f}")
    print(f"      Promedio final - Mín:     {df['X11_promedio_final'].min():.2f}")
    print(f"      Promedio final - Máx:     {df['X11_promedio_final'].max():.2f}")

    return df, reporte


if __name__ == "__main__":
    print("=" * 55)
    print("  PASO 1: LIMPIEZA DE DATOS")
    print("=" * 55)
    df, reporte = ejecutar()
