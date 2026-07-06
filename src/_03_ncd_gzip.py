"""
=============================================================
  PASO 3: CÁLCULO DE NCD/GZIP ENTRE VARIABLES
=============================================================
Para cada partición (Best/Worst en 12.5%, 25%, 50%):

1. Toma las columnas X1 a X10 (variables explicativas)
2. Convierte cada columna a una cadena de texto
3. Calcula NCD entre cada par de variables usando compresión Gzip
4. Genera una matriz de distancia 10×10

NCD (Normalized Compression Distance):
  NCD(x, y) = (C(xy) - min(C(x), C(y))) / max(C(x), C(y))

- C(x) = tamaño comprimido de x con gzip
- NCD ≈ 0 → variables muy similares/relacionadas
- NCD ≈ 1 → variables muy diferentes/sin relación

¿POR QUÉ NCD ENTRE VARIABLES?
  Al medir la distancia entre variables DENTRO de un grupo,
  descubrimos cómo se relacionan los factores socioeconómicos
  y académicos. Si esas relaciones CAMBIAN entre Best y Worst,
  significa que esos factores se comportan distinto según el
  rendimiento, revelando las CAUSAS del éxito o fracaso académico.
=============================================================
"""

import os
import gzip
import numpy as np
import pandas as pd

# ── CONFIGURACIÓN ──────────────────────────────────────────
VARIABLES_ANALISIS = [
    "X1_sexo", "X2_zona", "X3_ciclo", "X4_ingreso_familiar",
    "X5_trabaja", "X6_beca", "X7_educ_jefe", "X8_tam_familiar",
    "X9_asistencia", "X10_cursos_desaprobados"
]

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "results", "matrices")
# ───────────────────────────────────────────────────────────


def columna_a_texto(serie):
    """
    Convierte una columna (Series) a una cadena de texto.
    Cada valor se separa con salto de línea.
    Esto permite que Gzip encuentre patrones de compresión.
    """
    return "\n".join(serie.astype(str).values)


def comprimir(texto):
    """Retorna el tamaño en bytes del texto comprimido con gzip nivel 9."""
    datos = texto.encode("utf-8")
    return len(gzip.compress(datos, compresslevel=9))


def calcular_ncd(texto_x, texto_y):
    """
    Calcula la Normalized Compression Distance entre dos textos.

    NCD(x, y) = (C(xy) - min(C(x), C(y))) / max(C(x), C(y))

    Donde C(x) = tamaño comprimido de x.
    """
    cx = comprimir(texto_x)
    cy = comprimir(texto_y)
    # Concatenar ambos textos con un separador
    cxy = comprimir(texto_x + "\n" + texto_y)

    numerador = cxy - min(cx, cy)
    denominador = max(cx, cy)

    if denominador == 0:
        return 0.0

    ncd = numerador / denominador
    # NCD puede dar valores ligeramente mayores a 1 por artefactos de compresión
    return max(0.0, min(1.0, ncd))


def calcular_matriz_ncd(df_particion, nombre_particion):
    """
    Calcula la matriz NCD 10×10 entre las variables X1-X10
    para una partición dada.
    """
    n_vars = len(VARIABLES_ANALISIS)
    matriz = np.zeros((n_vars, n_vars))

    # Convertir cada columna a texto
    textos = {}
    for var in VARIABLES_ANALISIS:
        textos[var] = columna_a_texto(df_particion[var])

    # Calcular NCD para cada par de variables
    total_pares = n_vars * (n_vars - 1) // 2
    contador = 0

    for i in range(n_vars):
        for j in range(i + 1, n_vars):
            var_i = VARIABLES_ANALISIS[i]
            var_j = VARIABLES_ANALISIS[j]

            ncd_val = calcular_ncd(textos[var_i], textos[var_j])
            matriz[i][j] = ncd_val
            matriz[j][i] = ncd_val

            contador += 1

    # Etiquetas cortas para las variables
    etiquetas = [f"X{k+1}" for k in range(n_vars)]

    df_matriz = pd.DataFrame(
        np.round(matriz, 6),
        index=etiquetas,
        columns=etiquetas
    )

    return df_matriz


def guardar_matriz(df_matriz, nombre, output_dir):
    """Guarda una matriz NCD como archivo CSV."""
    path = os.path.join(output_dir, f"ncd_{nombre}.csv")
    df_matriz.to_csv(path)
    return path


def ejecutar(particiones):
    """
    Punto de entrada del paso 3.
    Calcula matrices NCD para todas las particiones.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    matrices = {}
    total = len(particiones)

    for idx, (nombre, df_part) in enumerate(particiones.items(), 1):
        print(f"\n   [{idx}/{total}] Calculando NCD para {nombre} ({len(df_part)} estudiantes)...")
        df_matriz = calcular_matriz_ncd(df_part, nombre)
        matrices[nombre] = df_matriz

        path = guardar_matriz(df_matriz, nombre, OUTPUT_DIR)
        print(f"      💾 Guardada: {os.path.basename(path)}")

        # Mostrar resumen de la matriz
        valores = df_matriz.values[np.triu_indices_from(df_matriz.values, k=1)]
        print(f"      📊 NCD promedio: {valores.mean():.4f}")
        print(f"      📊 NCD mín: {valores.min():.4f} | NCD máx: {valores.max():.4f}")

    print(f"\n   ✅ {len(matrices)} matrices NCD calculadas y guardadas")
    return matrices


if __name__ == "__main__":
    print("=" * 55)
    print("  PASO 3: NCD / GZIP")
    print("=" * 55)
    print("  Ejecuta desde main.py para obtener las particiones.")
