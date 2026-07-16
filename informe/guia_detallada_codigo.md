# 📘 Guía Técnica y Explicación del Código - Pipeline POO NCD/Gzip

Esta guía técnica detalla la arquitectura de software basada en el **Paradigma de Programación Orientada a Objetos (POO)** implementada para el análisis de rendimiento académico mediante distancias de compresión NCD.

---

## 1. Arquitectura de Clases (`src/`)

Cada paso del pipeline se ha rediseñado como una clase independiente dentro de la carpeta `src/`. Esto encapsula los datos y el comportamiento de cada etapa del experimento.

### 📄 `src/data_cleaner.py` (`class DataCleaner`)
Encapsula la carga de archivos, validación estructural y limpieza física/lógica del dataset.

#### Métodos principales:
*   `cargar_datos()`: Lee el archivo CSV de forma robusta e implementa el manejo de excepciones de codificación (`UnicodeDecodeError`), intentando primero con UTF-8 y luego con Latin-1.
*   `validar_columnas()`: Compara estructuralmente las columnas del archivo contra `COLUMNAS_ESPERADAS` y renombra los campos si es necesario.
*   `limpiar_datos()`: Filtra duplicados, nulos, variables no numéricas y aplica límites lógicos de dominio (ej. promedios en $[0, 20]$ y asistencia en $[0, 100]$).
*   `ejecutar()`: Método orquestador que devuelve el DataFrame limpio e informes de la limpieza.

---

### 📄 `src/partitioner.py` (`class StudentPartitioner`)
Encargada de dividir la muestra completa en subconjuntos de estudiantes basados en el rendimiento académico.

#### Métodos principales:
*   `crear_particiones(df)`: 
    1.  Ordena los datos de mayor a menor según el promedio final (`X11_promedio_final`).
    2.  Para cada fracción de porcentaje parametrizada (ej: 12.5%, 25%, 50%), toma los primeros $K$ alumnos para el grupo **Best** (alto rendimiento) y los últimos $K$ alumnos para el grupo **Worst** (bajo rendimiento).
    3.  Exporta los resultados a la carpeta `results/tablas/` como archivos CSV individuales.

---

### 📄 `src/ncd_analyzer.py` (`class NCDAnalyzer`)
Implementa el cálculo computacional de la distancia de compresión normalizada (NCD).

#### Métodos principales:
*   `_columna_a_texto(serie)`: Agrupa todas las entradas de una variable en una única cadena separada por saltos de línea (`"\n"`).
*   `_comprimir_y_medir(texto)`: Comprime los datos en memoria utilizando `gzip.compress` en el nivel máximo configurado (`gzip_level=9`) y mide su longitud en bytes.
*   `calcular_ncd(txt_x, txt_y)`: Ejecuta la fórmula matemática:
    $$NCD(x, y) = \frac{C(xy) - \min(C(x), C(y))}{\max(C(x), C(y))}$$
*   `procesar_particiones(particiones)`: Itera sobre todas las particiones del experimento y crea la matriz NCD de $10 \times 10$ con etiquetas simplificadas de variables (`X1` a `X10`).

---

### 📄 `src/topology_manager.py` (`class TopologyManager`)
Maneja el modelado de redes y agrupamiento jerárquico.

#### Métodos principales:
*   `construir_grafo_completo(df_matriz)`: Crea un grafo ponderado de NetworkX donde cada variable representa un nodo y el valor NCD es el peso de la arista.
*   `extraer_mst(G)`: Obtiene el Árbol de Expansión Mínima (MST) con menor suma de pesos.
*   `calcular_grado_ponderado(mst)`: Mide la centralidad sumando las distancias de las aristas del MST que inciden en cada variable.
*   `graficar_mst()`, `graficar_heatmap()`, `graficar_dendrograma()`: Guardan visualizaciones gráficas en la carpeta `results/graficos/`.
*   `graficar_dendrograma_comparativo(matrices)`: Dibuja dendrogramas comparativos **lado a lado** (Best vs Worst) para la misma partición, revelando visualmente la reestructuración de clusters de variables.

---

### 📄 `src/topology_comparator.py` (`class TopologyComparator`)
Determina el nivel de variación estructural de las variables explicativas entre grupos de alumnos.

#### Métodos principales:
*   `comparar_grados(grados_best, grados_worst)`: Calcula la métrica de cambio topológico:
    $$D = Grado_{Worst} - Grado_{Best}$$
*   `comparar_topologias(topologias)`: Compara los MSTs correspondientes por partición, ordena los resultados de mayor a menor cambio absoluto, guarda tablas CSV y genera histogramas visuales.
*   `graficar_resumen_global(todas_comp)`: Crea el gráfico consolidado `resumen_comparacion_global.png` cruzando las diferencias de todas las particiones.

---

### 📄 `src/report_generator.py` (`class ReportGenerator`)
Encargada de redactar el informe técnico general de salida.

#### Métodos principales:
*   `escribir_reporte(...)`: Integra las estadísticas de limpieza, las matrices NCD y los cambios máximos/mínimos en un archivo Markdown (`informe/informe_ncd_gzip.md`).

---

## 2. Clase Orquestadora (`src/pipeline.py`)

La clase `AcademicPipeline` conecta y coordina el flujo secuencial de datos de todas las clases del experimento.

```python
# src/pipeline.py
class AcademicPipeline:
    def __init__(self, dataset_path, partition_levels=[0.125, 0.25, 0.50], gzip_level=9):
        # Inicialización de objetos con configuración encapsulada
        self.cleaner = DataCleaner(dataset_path)
        self.partitioner = StudentPartitioner(levels=partition_levels)
        self.analyzer = NCDAnalyzer(gzip_level=gzip_level)
        self.topology = TopologyManager()
        self.comparator = TopologyComparator()
        self.generator = ReportGenerator()

    def run(self):
        # Flujo ordenado del pipeline
        df, reporte_limpieza = self.cleaner.ejecutar()
        particiones = self.partitioner.ejecutar(df)
        matrices = self.analyzer.ejecutar(particiones)
        topologias = self.topology.ejecutar(matrices)
        
        # Dendrogramas comparativos
        self.topology.graficar_dendrograma_comparativo(matrices)
        
        comparaciones = self.comparator.ejecutar(topologias)
        self.generator.ejecutar(reporte_limpieza, particiones, matrices, topologias, comparaciones)
```

---

## 3. Punto de Entrada (`main.py`)

Configura el directorio activo del sistema e inicializa la clase orquestadora.

```python
# main.py
import sys
import os
from src.pipeline import AcademicPipeline

# Asegurar que el directorio del script sea el directorio de trabajo
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

if __name__ == "__main__":
    pipeline = AcademicPipeline(
        dataset_path="data/estudiantes.csv",
        partition_levels=[0.125, 0.25, 0.50],
        gzip_level=9
    )
    pipeline.run()
```
