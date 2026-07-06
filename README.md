# 🎓 Pipeline NCD/Gzip - Análisis de Comportamiento Académico

Proyecto de análisis de patrones académicos usando **Normalized Compression Distance (NCD)** con compresión **Gzip** para identificar qué variables socioeconómicas y académicas influyen más en el rendimiento estudiantil.

## 📋 Descripción

Este pipeline analiza un dataset de 18,000 estudiantes para responder:

> **¿Qué factores (variables X1-X10) causan o se asocian con un mejor o peor rendimiento académico (X11)?**

### Metodología

1. **Limpieza** → Elimina nulos, duplicados e inconsistencias
2. **Particionamiento** → Divide en Best (Top) y Worst (Bottom) al 12.5%, 25% y 50%
3. **NCD/Gzip** → Calcula distancias entre variables X1-X10 dentro de cada grupo
4. **Topologías** → Construye árboles de expansión mínima (MST) con NetworkX
5. **Comparación** → Compara redes Best vs Worst, identifica variables con mayor cambio
6. **Informe** → Genera reporte automático en Markdown

## 📊 Variables del Dataset

| Variable | Descripción | Tipo |
|----------|-------------|------|
| X1 | Sexo | Categórica |
| X2 | Zona geográfica | Categórica |
| X3 | Ciclo académico | Numérica |
| X4 | Ingreso familiar | Numérica |
| X5 | Trabaja | Categórica |
| X6 | Beca | Categórica |
| X7 | Educación del jefe de familia | Categórica |
| X8 | Tamaño familiar | Numérica |
| X9 | Asistencia (%) | Numérica |
| X10 | Cursos desaprobados | Numérica |
| **X11** | **Promedio final (clasificación)** | **Numérica** |

## 🚀 Cómo ejecutar

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Colocar el dataset

Asegúrate de que `data/estudiantes.csv` existe con las 11 columnas.

### 3. Ejecutar el pipeline completo

```bash
python main.py
```

## 📁 Estructura del proyecto

```
proyecto_academico/
├── data/
│   └── estudiantes.csv              ← Dataset de estudiantes
├── src/
│   ├── _01_limpieza.py              ← Paso 1: Limpieza de datos
│   ├── _02_particiones.py           ← Paso 2: Particiones Best/Worst
│   ├── _03_ncd_gzip.py              ← Paso 3: Cálculo NCD entre variables
│   ├── _04_topologias.py            ← Paso 4: MST con NetworkX
│   ├── _05_comparacion.py           ← Paso 5: Comparar topologías
│   └── _06_reporte_resultados.py    ← Paso 6: Generar informe
├── results/
│   ├── matrices/                    ← Matrices NCD 10×10 (CSV)
│   ├── graficos/                    ← Gráficos MST, heatmaps, comparaciones
│   └── tablas/                      ← Tablas comparativas (CSV)
├── informe/
│   └── informe_ncd_gzip.md          ← Informe automático
├── main.py                          ← Ejecuta TODO el pipeline
├── README.md
└── requirements.txt
```

## 📐 Fórmula NCD

```
NCD(x, y) = (C(xy) - min(C(x), C(y))) / max(C(x), C(y))
```

- `C(x)` = tamaño comprimido de la variable x con gzip
- `NCD ≈ 0` → variables muy similares/relacionadas
- `NCD ≈ 1` → variables muy diferentes

## 🔍 Interpretación de resultados

La comparación de topologías calcula:

```
D = GradoPonderado_Worst - GradoPonderado_Best
```

- **D positivo grande** → Variable que aumenta su conexión en el grupo Worst (factor de riesgo)
- **D negativo grande** → Variable que disminuye su conexión en Worst (factor protector)
- **D ≈ 0** → Variable con comportamiento similar en ambos grupos

## 📦 Requisitos

- Python 3.8+
- pandas
- numpy
- networkx
- matplotlib
- scipy
