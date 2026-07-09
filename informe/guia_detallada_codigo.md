# 📘 Guía Técnica y Explicación del Código - Pipeline NCD/Gzip

Esta guía técnica proporciona una explicación detallada, línea por línea y función por función, de todo el código del sistema de análisis académico basado en **NCD/Gzip** (Normalized Compression Distance).

---

## 1. Módulos de Python (`src/`)

La carpeta `src/` contiene los 6 pasos independientes que conforman la tubería (pipeline) de procesamiento.

### 📄 `src/_01_limpieza.py` (Limpieza de Datos)
Este archivo se encarga de cargar el archivo CSV original, validar que tenga la estructura adecuada de 11 columnas (`X1` a `X11`) y remover datos sucios o inconsistentes.

#### Funciones clave:
*   `cargar_datos()`: Lee el CSV de forma robusta. Si el archivo viene con caracteres latinos no soportados por UTF-8, cambia automáticamente a la codificación `latin-1` para evitar caídas.
*   `validar_columnas(df)`: Compara los nombres de las columnas cargadas contra `COLUMNAS_ESPERADAS`. Si no coinciden pero tienen la misma longitud (11), las renombra por su orden posicional para asegurar compatibilidad.
*   `limpiar_datos(df)`: 
    *   **Duplicados:** Elimina filas idénticas repetidas mediante `df.drop_duplicates()`.
    *   **Nulos:** Identifica y reporta nulos por columna antes de eliminarlos (`df.dropna()`).
    *   **Conversión numérica:** Convierte variables continuas al tipo correcto (`pd.to_numeric()`).
    *   **Validaciones lógicas:** Filtra que el Promedio Final (`X11`) esté en la escala de $[0, 20]$, la asistencia (`X9`) entre $[0, 100]\%$, y que valores como el tamaño familiar (`X8`) y cursos desaprobados (`X10`) no sean negativos.
*   `ejecutar()`: Orquesta la carga, validación y limpieza, devolviendo el DataFrame limpio y un diccionario de reporte con las estadísticas de limpieza.

---

### 📄 `src/_02_particiones.py` (Particionamiento)
Divide el dataset de estudiantes en dos grupos según su promedio final (`X11`) y guarda las muestras correspondientes en archivos `.csv`.

#### Funciones clave:
*   `ejecutar(df)`:
    1.  Ordena el DataFrame original de forma descendente en base al promedio final (`X11`).
    2.  Para cada nivel de muestra seleccionado ($12.5\%$, $25\%$, $50\%$):
        *   Calcula el número de filas $K$ equivalente al porcentaje.
        *   Toma las primeras $K$ filas para el grupo **Best** (alto rendimiento).
        *   Toma las últimas $K$ filas para el grupo **Worst** (bajo rendimiento).
        *   Guarda cada partición como un archivo CSV en `results/tablas/` (ej: `Best_12.5.csv`).
    3.  Retorna un diccionario conteniendo los DataFrames de las 6 particiones.

---

### 📄 `src/_03_ncd_gzip.py` (Métrica NCD)
Calcula las matrices de distancia normalizada por compresión (NCD) de $10 \times 10$ entre las variables explicativas `X1` a `X10`.

#### Lógica del cálculo NCD:
Para evaluar la similitud entre dos columnas $x$ e $y$:
1.  Concatenamos todos los registros de cada columna en una única cadena de texto separada por saltos de línea.
2.  Medimos el peso en bytes al comprimir el texto de cada columna de forma individual: $C(x)$ y $C(y)$.
3.  Medimos el peso de ambas columnas concatenadas juntas: $C(xy)$.
4.  Aplicamos la fórmula matemática:
    $$NCD(x, y) = \frac{C(xy) - \min(C(x), C(y))}{\max(C(x), C(y))}$$

#### Funciones clave:
*   `columna_a_texto(serie)`: Convierte todas las celdas de una serie de pandas en texto continuo (`"\n".join()`).
*   `comprimir_y_medir(texto)`: Codifica el texto a UTF-8 y aplica compresión `gzip.compress` en nivel máximo de compresión (level=9), retornando su tamaño final en bytes.
*   `calcular_ncd(txt_x, txt_y)`: Implementa la fórmula NCD y acota los resultados en el intervalo $[0, 1]$.
*   `ejecutar(particiones)`: Para cada una de las 6 particiones del paso anterior, calcula de forma iterativa las distancias de todos los 45 pares únicos de variables, construye una matriz de $10 \times 10$ (como `DataFrame`), la guarda en `results/matrices/` y la retorna.

---

### 📄 `src/_04_topologias.py` (Modelado de Redes y Dendrogramas)
Construye modelos topológicos utilizando Árboles de Expansión Mínima (MST) y mapas de agrupamiento jerárquico (Dendrogramas).

#### Funciones clave:
*   `construir_grafo_completo(df_matriz)`: Transforma la matriz de distancias NCD en un grafo no directo donde cada variable es un nodo y el peso de cada arista es el valor de distancia NCD.
*   `extraer_mst(G)`: Obtiene el árbol que conecta todas las variables utilizando las aristas con menor distancia NCD posible (relaciones más fuertes).
*   `calcular_grado_ponderado(mst)`: Mide la centralidad de cada variable en la topología sumando el peso de las aristas del MST que pasan por ella.
*   `graficar_mst()`, `graficar_heatmap()`, `graficar_dendrograma()`: Guardan en la carpeta `results/graficos/` la representación visual del árbol de expansión mínima, del mapa de calor y del dendrograma individual respectivamente.
*   `graficar_dendrograma_comparativo(matrices, output_dir)`: Genera los gráficos comparativos de dendrogramas **lado a lado** para analizar visualmente cómo cambia la jerarquía de agrupamiento de variables entre estudiantes de alto y bajo rendimiento en un mismo porcentaje.

---

### 📄 `src/_05_comparacion.py` (Análisis de Cambio D)
Mide el cambio topológico entre los grupos de alto y bajo rendimiento mediante la diferencia matemática:
$$D = GradoPonderado_{Worst} - GradoPonderado_{Best}$$

#### Funciones clave:
*   `ejecutar(topologias)`:
    *   Para cada nivel ($12.5\%$, $25\%$, $50\%$), extrae los vectores de grado ponderado de los subgrupos Best y Worst correspondientes.
    *   Calcula la diferencia $D$ para cada una de las 10 variables explicativas.
    *   Identifica la variable de **máximo cambio** (mayor valor absoluto $|D|$) y la de **mínimo cambio** (menor valor absoluto $|D|$).
    *   Guarda tablas CSV con las comparaciones en `results/tablas/` y genera gráficos de barras en `results/graficos/`.
    *   Genera `resumen_comparacion_global.png` que consolida las diferencias de las tres particiones en una única visualización de contraste.

---

### 📄 `src/_06_reporte_resultados.py` (Generación de Reporte Markdown)
Compila de forma estructurada toda la información generada a lo largo del pipeline y produce el archivo `informe/informe_ncd_gzip.md`.

#### Funciones clave:
*   `generar_tabla_markdown(df)`: Convierte cualquier DataFrame de pandas a formato de tablas Markdown.
*   `ejecutar(...)`: Genera el texto del informe integrando de manera automática las estadísticas de la limpieza, las matrices NCD formateadas, los hallazgos de máximo y mínimo cambio y un apartado sintáctico de conclusiones.

---

## 2. Orquestador del Sistema (`main.py`)

Ubicado en la raíz del proyecto, actúa como el punto de inicio y sincronización de los 6 pasos.

```python
import os
import time

# Configura el directorio activo del script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Define una envoltura para registrar tiempos de ejecución
def paso(numero, titulo, funcion, *args):
    print(f"PASO {numero}: {titulo}")
    inicio = time.time()
    resultado = funcion(*args)
    print(f"Completado en {time.time() - inicio:.2f}s\n")
    return resultado

if __name__ == "__main__":
    # Ejecuta el flujo en cadena
    df, reporte = paso(1, "LIMPIEZA", p1.ejecutar)
    particiones = paso(2, "PARTICIONES", p2.ejecutar, df)
    matrices = paso(3, "NCD/GZIP", p3.ejecutar, particiones)
    topologias = paso(4, "MST", p4.ejecutar, matrices)
    
    # Genera dendrogramas comparativos adicionales
    p4.graficar_dendrograma_comparativo(matrices, "results/graficos")
    
    comparaciones = paso(5, "COMPARACIÓN", p5.ejecutar, topologias)
    paso(6, "REPORTE MD", p6.ejecutar, reporte, particiones, matrices, topologias, comparaciones)
```

---

## 3. Generador de Documentos Word (`informe.js`)

Es un script de **Node.js** que crea un documento formal de Word (`.docx`) conteniendo la estructura completa del informe técnico del experimento.

### Componentes principales del código:

1.  **Librerías y Configuración:**
    Utiliza el paquete `docx` para construir el árbol de elementos XML que conforman un archivo de Word.
    ```javascript
    const fs = require("fs");
    const { Document, Packer, Paragraph, TextRun, Table, ... } = require("docx");
    ```
2.  **Funciones de Estilo Auxiliares:**
    *   `headerCell(text, width)` y `bodyCell(text, width, opts)`: Crean celdas con bordes delgados de color negro (`CELL_BORDERS`) y configuraciones específicas de fuentes (Calibri, tamaño, negritas y alineaciones).
    *   `makeTable(headers, rows, colWidthsDxa)`: Agrupa celdas en filas (`TableRow`) y columnas alineadas para conformar tablas.
    *   `h1(text)`, `h2(text)`, `h3(text)`, `p(text)`: Retornan bloques de párrafo formateados como títulos principales, subtítulos o cuerpo de texto normal.
3.  **Matrices y Datos Integrados:**
    Para asegurar que el informe pueda generarse de forma rápida sin dependencias de bases de datos o lecturas de archivos pesados en tiempo real, el script tiene **quemados (hardcoded)** los resultados exactos del experimento en constantes como `M_BEST_125`, `comp125`, `comp25`, etc.
4.  **Generación de Portada y Cuerpo:**
    Carga el logotipo local (`logo.png`) como un búfer binario e inserta una portada formal con la información de la institución y del estudiante. Después, añade en un arreglo lineal (`children`) el desglose de secciones y tablas.
5.  **Compilación y Escritura:**
    Genera el archivo empaquetado final:
    ```javascript
    Packer.toBuffer(doc).then(buf => {
      fs.writeFileSync("informe/Informe_NCD_Gzip_Ciberseguridad.docx", buf);
      console.log("done");
    });
    ```
