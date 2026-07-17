# 📘 Guía Técnica y Explicación del Código - Pipeline POO NCD/Gzip (Español)

Esta guía técnica detalla la arquitectura de software basada en el **Paradigma de Programación Orientada a Objetos (POO)** implementada con nombres y clases completamente en español para facilitar su lectura y defensa académica.

---

## 1. Arquitectura de Clases (`src/`)

Cada paso de la tubería de datos está definido por una clase específica en la carpeta `src/`.

### 📄 `src/limpiador_datos.py` (`class LimpiadorDatos`)
Encapsula la carga, validación de estructura y depuración de registros en el dataset de entrada.

#### Métodos principales:
*   `cargar_datos()`: Lee el archivo CSV manejando de forma segura posibles excepciones de codificación (`UnicodeDecodeError`) intentando primero con UTF-8 y luego con Latin-1.
*   `validar_columnas()`: Compara estructuralmente las columnas encontradas y renombra a los nombres de variables estándar si es necesario.
*   `limpiar_datos()`: Elimina registros duplicados, vacíos (nulos), campos no numéricos en variables clave y filtra datos fuera de los rangos lógicos permitidos.
*   `ejecutar()`: Método orquestador principal de limpieza.

---

### 📄 `src/particionador.py` (`class ParticionadorEstudiantes`)
Se encarga de clasificar y separar a los estudiantes según su nivel de desempeño académico final.

#### Métodos principales:
*   `crear_particiones(df)`: 
    1.  Ordena el DataFrame completo de mayor a menor promedio de calificaciones (`X11_promedio_final`).
    2.  Extrae los $K$ mejores estudiantes (**Best**) y los $K$ peores (**Worst**) para las fracciones muestrales indicadas (ej: 12.5%, 25%, 50%).
    3.  Exporta estas submuestras como archivos CSV en `results/tablas/`.

---

### 📄 `src/analizador_ncd.py` (`class AnalizadorNCD`)
Implementa y ejecuta la fórmula matemática de la Distancia de Compresión Normalizada (NCD).

#### Métodos principales:
*   `_columna_a_texto(serie)`: Agrupa los valores de una variable como una cadena de texto continua separada por saltos de línea (`"\n"`).
*   `_comprimir_y_medir(texto)`: Comprime el texto en memoria usando `gzip.compress` en el nivel máximo de compresión (`nivel_gzip=9`) y calcula el tamaño resultante en bytes.
*   `calcular_ncd(txt_x, txt_y)`: Ejecuta la fórmula matemática:
    $$NCD(x, y) = \frac{C(xy) - \min(C(x), C(y))}{\max(C(x), C(y))}$$
*   `procesar_particiones(particiones)`: Calcula las matrices NCD de $10 \times 10$ para todas las variables explicativas (`X1` a `X10`) correspondientes a cada grupo.

---

### 📄 `src/gestor_topologias.py` (`class GestorTopologias`)
Genera los modelos de red complejos de las variables mediante grafos y clusters jerárquicos.

#### Métodos principales:
*   `construir_grafo_completo(df_matriz)`: Diseña un grafo conectado en NetworkX donde el peso de cada enlace es igual al valor NCD entre los nodos variables.
*   `extraer_mst(G)`: Calcula el Árbol de Expansión Mínima (MST).
*   `calcular_grado_ponderado(mst)`: Mide la centralidad sumando los pesos de las aristas que se conectan a cada nodo en el MST.
*   `graficar_mst()`, `graficar_heatmap()`, `graficar_dendrograma()`: Guarda las imágenes y gráficos en `results/graficos/`.
*   `graficar_dendrograma_comparativo(matrices)`: Dibuja los dendrogramas lado a lado para contrastar visualmente el comportamiento de los grupos.

---

### 📄 `src/comparador_topologias.py` (`class ComparadorTopologias`)
Calcula el grado de cambio o dinamismo de las variables socioacadémicas entre perfiles de estudiantes.

#### Métodos principales:
*   `comparar_grados(grados_best, grados_worst)`: Calcula la diferencia de centralidad topológica:
    $$D = Grado_{Worst} - Grado_{Best}$$
*   `comparar_topologias(topologias)`: Ordena las variables por su nivel absoluto de cambio, exporta tablas de diferencias en CSV e ilustra la variación con diagramas de barras.

---

### 📄 `src/generador_reportes.py` (`class GeneradorReportes`)
Compila todos los datos estadísticos y comparaciones en un informe de resultados formateado.

#### Métodos principales:
*   `escribir_reporte(...)`: Redacta automáticamente el archivo `informe/informe_ncd_gzip.md` con las conclusiones del experimento.

---

## 2. Clase Orquestadora (`src/pipeline_academico.py`)

La clase `PipelineAcademico` es el orquestador principal que automatiza de extremo a extremo la ejecución de los módulos individuales.

```python
# src/pipeline_academico.py
class PipelineAcademico:
    def __init__(self, ruta_datos, niveles_particion=[0.125, 0.25, 0.50], nivel_gzip=9):
        self.limpiador = LimpiadorDatos(ruta_datos)
        self.particionador = ParticionadorEstudiantes(niveles=niveles_particion)
        self.analizador = AnalizadorNCD(nivel_gzip=nivel_gzip)
        self.topologia = GestorTopologias()
        self.comparador = ComparadorTopologias()
        self.reportador = GeneradorReportes()

    def ejecutar(self):
        df, reporte_limpieza = self.limpiador.ejecutar()
        particiones = self.particionador.ejecutar(df)
        matrices = self.analizador.ejecutar(particiones)
        topologias = self.topologia.ejecutar(matrices)
        
        self.topologia.graficar_dendrograma_comparativo(matrices)
        comparaciones = self.comparador.ejecutar(topologias)
        self.reportador.ejecutar(reporte_limpieza, particiones, matrices, topologias, comparaciones)
```

---

## 3. Script Principal (`main.py`)

Configura la ruta de trabajo e inicializa el pipeline académico.

```python
# main.py
from src.pipeline_academico import PipelineAcademico

if __name__ == "__main__":
    pipeline = PipelineAcademico(
        ruta_datos="data/estudiantes.csv",
        niveles_particion=[0.125, 0.25, 0.50],
        nivel_gzip=9
    )
    pipeline.ejecutar()
```
