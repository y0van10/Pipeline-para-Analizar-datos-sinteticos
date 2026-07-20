# 📘 Guía Técnica y Explicación del Código - Pipeline POO NCD/Gzip (Sub-bloques & Árboles Bayesianos)

Esta guía técnica detalla la arquitectura de software basada en el **Paradigma de Programación Orientada a Objetos (POO)** implementada con soporte para **Particionamiento Jerárquico por Bloques Continuos (50%, 25% y 12.5%)**, lectura secuencial de archivos CSV almacenados en disco y **Árboles Bayesianos Probabilísticos**.

---

## 1. Organización del Directorio de Resultados (`results/`)

Para mayor limpieza y orden en la entrega académica, el sistema clasifica las tablas CSV y los gráficos PNG en carpetas dedicadas por nivel de partición:

```
results/
├── global/
│   ├── arbol_bayesiano_Completo.png
│   └── resumen_comparacion_global.png
├── nivel_50/
│   ├── tablas/ (Best_50.csv, Worst_50.csv, ncd_*.csv, comparacion_50.csv)
│   └── graficos/ (mst_*.png, heatmap_*.png, dendrograma_*.png, arbol_bayesiano_*.png)
├── nivel_25/
│   ├── tablas/ (Best_25_1.csv, Best_25_2.csv, Worst_25_1.csv, Worst_25_2.csv, ncd_*.csv, comparacion_25.csv)
│   └── graficos/ (mst_*.png, heatmap_*.png, dendrograma_*.png, arbol_bayesiano_*.png)
└── nivel_12.5/
    ├── tablas/ (Best_12.5_1..4.csv, Worst_12.5_1..4.csv, ncd_*.csv, comparacion_12.5.csv)
    └── graficos/ (mst_*.png, heatmap_*.png, dendrograma_*.png, arbol_bayesiano_*.png)
```

---

## 2. Arquitectura de Clases (`src/`)

### 📄 `src/limpiador_datos.py` (`class LimpiadorDatos`)
Carga, valida estructuralmente y depura los registros inconsistentes o fuera de rango lógico del dataset de entrada.

---

### 📄 `src/particionador.py` (`class ParticionadorEstudiantes`)
Clasifica y subdivide continuamente el dataset completo ordenado por promedio final (`X11_promedio_final`):
*   **Nivel 50% (2 Bloques):** `Best_50` (0-50%) y `Worst_50` (50-100%).
*   **Nivel 25% (4 Cuartiles):** `Best_25_1` (0-25%), `Best_25_2` (25-50%), `Worst_25_1` (50-75%) y `Worst_25_2` (75-100%).
*   **Nivel 12.5% (8 Octiles):** `Best_12.5_1` a `Best_12.5_4` (Superiores) y `Worst_12.5_1` a `Worst_12.5_4` (Inferiores).

Cada subgrupo se exporta automáticamente como un archivo CSV independiente en su carpeta `results/nivel_<X>/tablas/`.

---

### 📄 `src/analizador_ncd.py` (`class AnalizadorNCD`)
Lee directamente los archivos CSV creados en la carpeta de cada nivel y calcula la matriz de compresión Gzip ($10 \times 10$) para cada sub-bloque, almacenando los resultados como `ncd_<Nombre>.csv` en la misma carpeta del nivel.

---

### 📄 `src/gestor_topologias.py` (`class GestorTopologias`)
Construye el Árbol de Expansión Mínima (MST), Mapas de Calor (Heatmaps) y Dendrogramas para cada bloque. Genera dendrogramas comparativos entre los extremos de rendimiento de cada nivel.

---

### 📄 `src/comparador_topologias.py` (`class ComparadorTopologias`)
Compara el grado ponderado entre los bloques de rendimiento extremos (`Best` vs `Worst`) para evaluar la diferencia topológica:
$$D = Grado_{Worst} - Grado_{Best}$$
Exporta `comparacion_<nivel>.csv` e histogramas comparativos.

---

### 📄 `src/analizador_bayesiano.py` (`class AnalizadorBayesiano`)
Binariza el conjunto de datos de cada CSV de bloque, calcula la **probabilidad conjunta máxima** $P_{max}(X_i, X_j)$ para cada par de variables y genera el **Árbol Bayesiano Dirigido (MST Probabilístico)**.

---

### 📄 `src/generador_reportes.py` (`class GeneradorReportes`)
Compila todos los resultados y enlaces de imágenes en un informe Markdown consolidado (`informe/informe_ncd_gzip.md`).

---

## 3. ¿Cómo usar el Pipeline con un Dataset Real?

El sistema está diseñado de forma dinámica mediante **POO**. Para procesar un nuevo dataset real de estudiantes:

1. Coloca tu archivo en la carpeta `data/` (por ejemplo, `data/mis_estudiantes_reales.csv`).
2. Abre `main.py` y cambia la ruta del dataset:

```python
# main.py
from src.pipeline_academico import PipelineAcademico

if __name__ == "__main__":
    pipeline = PipelineAcademico(
        ruta_datos="data/mis_estudiantes_reales.csv",  # <--- Tu archivo real
        nivel_gzip=9
    )
    pipeline.ejecutar()
```

El pipeline ejecutará automáticamente la limpieza, la segmentación en bloques de 50%, 25% y 12.5%, la compresión NCD, las topologías de red y los Árboles Bayesianos sobre tus datos reales.
