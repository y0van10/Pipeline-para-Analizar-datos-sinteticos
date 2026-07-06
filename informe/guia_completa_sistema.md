# 📖 Guía Completa del Sistema NCD/Gzip - Análisis Académico

## Tabla de Contenidos

1. [Visión General del Sistema](#1-visión-general-del-sistema)
2. [Estructura de Archivos](#2-estructura-de-archivos)
3. [Flujo de Datos](#3-flujo-de-datos)
4. [Explicación de Cada Archivo](#4-explicación-de-cada-archivo)
5. [Cómo se Conectan los Archivos](#5-cómo-se-conectan-los-archivos)
6. [Conceptos Clave](#6-conceptos-clave)

---

## 1. Visión General del Sistema

### ¿Qué hace este proyecto?

Este proyecto responde una pregunta simple pero poderosa:

> **¿Qué factores (sexo, zona, beca, asistencia, etc.) causan que un estudiante tenga buen o mal rendimiento académico?**

Para responderla, usa una técnica llamada **NCD/Gzip** (Normalized Compression Distance) que mide qué tan parecidas son dos variables usando compresión de datos.

### La idea en 4 pasos

```
1. Tomas 18,000 estudiantes
2. Los divides en "mejores" (Best) y "peores" (Worst) según su promedio final
3. Para cada grupo, mides cómo se relacionan las variables X1-X10 entre sí
4. Comparas: si una variable cambia MUCHO su relación entre Best y Worst,
   entonces esa variable es una CAUSA importante del rendimiento
```

### Analogía simple

Imagina que tienes dos grupos de amigos: los que sacan buenas notas y los que no. Si en el grupo de buenos notas la "asistencia" está muy conectada con "beca", pero en el grupo de malas notas esa conexión desaparece, eso te dice que **la relación entre asistencia y beca funciona diferente según el rendimiento**.

---

## 2. Estructura de Archivos

```
proyecto_academico/
│
├── data/
│   └── estudiantes.csv              ← Los datos originales (18,000 filas)
│
├── src/                             ← Todo el código fuente
│   ├── __init__.py                  ← Marca la carpeta como paquete Python
│   ├── _01_limpieza.py              ← PASO 1: Limpiar datos sucios
│   ├── _02_particiones.py           ← PASO 2: Dividir en Best/Worst
│   ├── _03_ncd_gzip.py              ← PASO 3: Calcular distancias NCD
│   ├── _04_topologias.py            ← PASO 4: Construir redes/árboles
│   ├── _05_comparacion.py           ← PASO 5: Comparar redes Best vs Worst
│   └── _06_reporte_resultados.py    ← PASO 6: Generar informe automático
│
├── results/                         ← Resultados generados automáticamente
│   ├── matrices/                    ← Matrices de distancia NCD (CSV)
│   ├── graficos/                    ← Imágenes de redes y gráficos (PNG)
│   └── tablas/                      ← Tablas de datos y comparaciones (CSV)
│
├── informe/
│   └── informe_ncd_gzip.md          ← Informe completo auto-generado
│
├── main.py                          ← EL ARCHIVO PRINCIPAL - ejecuta todo
├── README.md                        ← Instrucciones del proyecto
└── requirements.txt                 ← Librerías necesarias
```

---

## 3. Flujo de Datos

### Diagrama del pipeline

```
  estudiantes.csv (18,000 filas, 11 columnas)
        │
        ▼
  ┌─────────────────────────────┐
  │  PASO 1: _01_limpieza.py   │   Elimina nulos, duplicados,
  │  Entrada: CSV crudo         │   valores fuera de rango
  │  Salida: DataFrame limpio   │
  └─────────┬───────────────────┘
            │ DataFrame en memoria
            ▼
  ┌─────────────────────────────┐
  │  PASO 2: _02_particiones.py │   Divide en 6 grupos:
  │  Entrada: DataFrame limpio  │   Best_12.5, Worst_12.5
  │  Salida: 6 particiones      │   Best_25, Worst_25
  │         + 6 CSVs guardados  │   Best_50, Worst_50
  └─────────┬───────────────────┘
            │ Diccionario de 6 DataFrames
            ▼
  ┌─────────────────────────────┐
  │  PASO 3: _03_ncd_gzip.py   │   Para cada partición:
  │  Entrada: 6 particiones     │   calcula NCD entre X1-X10
  │  Salida: 6 matrices 10×10  │   (45 pares por matriz)
  │         + 6 CSVs guardados  │
  └─────────┬───────────────────┘
            │ Diccionario de 6 matrices
            ▼
  ┌─────────────────────────────┐
  │  PASO 4: _04_topologias.py  │   Para cada matriz:
  │  Entrada: 6 matrices NCD    │   construye grafo → extrae MST
  │  Salida: 6 MSTs + grados   │   calcula grado ponderado
  │         + 12 PNGs (MST+heat)│
  └─────────┬───────────────────┘
            │ Diccionario de topologías
            ▼
  ┌─────────────────────────────┐
  │  PASO 5: _05_comparacion.py │   Para cada nivel (12.5%, 25%, 50%):
  │  Entrada: 6 topologías      │   D = Grado_Worst - Grado_Best
  │  Salida: 3 comparaciones    │   identifica MAX y MIN cambio
  │         + 3 CSVs + 4 PNGs   │
  └─────────┬───────────────────┘
            │ Resultados de comparación
            ▼
  ┌─────────────────────────────┐
  │  PASO 6: _06_reporte.py     │   Junta TODO en un informe:
  │  Entrada: todos los datos   │   metodología, matrices, tablas,
  │  Salida: informe_ncd_gzip.md│   conclusiones automáticas
  └─────────────────────────────┘
```

### ¿Qué pasa con los datos en cada paso?

```
CSV crudo (18,000 × 11)
    ↓ Paso 1
DataFrame limpio (18,000 × 11)
    ↓ Paso 2
6 DataFrames (ej: Best_12.5 = 2,250 × 11)
    ↓ Paso 3
6 matrices NCD (10 × 10 cada una)
    ↓ Paso 4
6 MSTs (9 aristas cada uno) + 6 vectores de grado (10 valores)
    ↓ Paso 5
3 tablas de diferencias (10 variables × 6 columnas)
    ↓ Paso 6
1 informe Markdown completo
```

---

## 4. Explicación de Cada Archivo

---

### 📄 `main.py` — El Director de Orquesta

**¿Qué hace?** Es el archivo principal. Ejecuta los 6 pasos en orden y mide el tiempo de cada uno.

**¿Cómo funciona?**

```python
# 1. Cambia al directorio del proyecto (para que las rutas funcionen)
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 2. Importa cada módulo
from src import _01_limpieza as p1
from src import _02_particiones as p2
# ... etc

# 3. Ejecuta cada paso pasando el resultado del anterior
df, reporte = p1.ejecutar()           # Paso 1 → devuelve datos limpios
particiones = p2.ejecutar(df)          # Paso 2 → recibe datos, devuelve particiones
matrices = p3.ejecutar(particiones)    # Paso 3 → recibe particiones, devuelve matrices
topologias = p4.ejecutar(matrices)     # Paso 4 → recibe matrices, devuelve topologías
comparaciones = p5.ejecutar(topologias) # Paso 5 → recibe topologías, devuelve comparaciones
p6.ejecutar(reporte, particiones, matrices, topologias, comparaciones)  # Paso 6
```

**Función clave: `paso()`**
```python
def paso(numero, titulo, funcion, *args):
    inicio = time.time()        # Marca el inicio
    resultado = funcion(*args)  # Ejecuta el paso
    fin = time.time()           # Marca el fin
    print(f"Tiempo: {fin - inicio:.2f}s")
    return resultado
```

**¿Cómo se ejecuta?**
```bash
python main.py
```

---

### 📄 `src/_01_limpieza.py` — El Filtro de Datos

**¿Qué hace?** Lee el CSV original y lo limpia eliminando datos basura.

**¿Qué problemas resuelve?**
- Filas con valores vacíos (nulos)
- Filas duplicadas exactas
- Valores imposibles (promedio < 0 o > 20, asistencia > 100%)
- Columnas con nombres incorrectos

**¿Cómo funciona internamente?**

```python
def ejecutar():
    # 1. CARGAR: Lee el CSV (intenta utf-8, si falla usa latin-1)
    df = pd.read_csv("data/estudiantes.csv")

    # 2. VALIDAR: Verifica que tenga 11 columnas con los nombres correctos
    #    Si no coinciden, las renombra por posición

    # 3. LIMPIAR:
    df = df.drop_duplicates()           # Elimina filas repetidas
    df = df.dropna()                     # Elimina filas con valores vacíos
    df["X11"] = pd.to_numeric(df["X11"]) # Convierte a número
    df = df[df["X11"] >= 0]              # Elimina promedios negativos
    df = df[df["X11"] <= 20]             # Elimina promedios > 20
    df = df[df["X9"] >= 0]              # Asistencia válida
    df = df[df["X9"] <= 100]

    return df, reporte  # Devuelve el DataFrame limpio + estadísticas
```

**Entrada:** `data/estudiantes.csv` (archivo CSV)
**Salida:** Un DataFrame de pandas limpio + un diccionario con las estadísticas de limpieza

---

### 📄 `src/_02_particiones.py` — El Clasificador

**¿Qué hace?** Ordena a los estudiantes por promedio final y los divide en grupos Best (mejores) y Worst (peores).

**¿Por qué 3 niveles?** Para ver si los resultados son consistentes:
- **12.5%** → Solo los extremos (2,250 mejores vs 2,250 peores)
- **25%** → Más amplios (4,500 vs 4,500)
- **50%** → La mitad superior vs la mitad inferior (9,000 vs 9,000)

**¿Cómo funciona internamente?**

```python
def crear_particiones(df):
    # Ordena de MAYOR a MENOR promedio
    df_sorted = df.sort_values("X11_promedio_final", ascending=False)

    for nivel in [0.125, 0.25, 0.50]:  # 12.5%, 25%, 50%
        k = int(len(df) * nivel)  # Cuántos estudiantes tomar

        best = df_sorted.head(k)   # Los k primeros = mejores
        worst = df_sorted.tail(k)  # Los k últimos = peores

        particiones[f"Best_{nivel*100}"] = best
        particiones[f"Worst_{nivel*100}"] = worst

    return particiones  # Diccionario con 6 DataFrames
```

**Ejemplo visual:**
```
Estudiantes ordenados por promedio (mayor → menor):
[20, 19, 18, 17, ... , 5, 4, 3, 2]

12.5% → Best: [20, 19, 18...] (2,250)  |  Worst: [...3, 2] (2,250)
25%   → Best: [20, 19, 18...] (4,500)  |  Worst: [...3, 2] (4,500)
50%   → Best: [20, 19, 18...] (9,000)  |  Worst: [...3, 2] (9,000)
```

**Entrada:** DataFrame limpio
**Salida:** Diccionario con 6 DataFrames + 6 archivos CSV en `results/tablas/`

---

### 📄 `src/_03_ncd_gzip.py` — El Calculador de Distancias

**¿Qué hace?** Mide qué tan "parecidas" son las variables X1-X10 entre sí usando compresión Gzip. Es el **corazón matemático** del proyecto.

**¿Qué es NCD?**

NCD (Normalized Compression Distance) mide similitud entre datos usando compresión:

```
NCD(x, y) = (C(xy) - min(C(x), C(y))) / max(C(x), C(y))
```

- `C(x)` = tamaño en bytes de x comprimido con gzip
- `C(xy)` = tamaño de x e y JUNTOS comprimidos
- Si x e y son parecidos → se comprimen muy bien juntos → NCD ≈ 0
- Si son diferentes → no se comprimen bien juntos → NCD ≈ 1

**¿Cómo funciona internamente?**

```python
# 1. Convierte cada columna a texto
def columna_a_texto(serie):
    # [Masculino, Femenino, Masculino] → "Masculino\nFemenino\nMasculino"
    return "\n".join(serie.astype(str).values)

# 2. Comprime el texto con gzip
def comprimir(texto):
    datos = texto.encode("utf-8")       # Texto → bytes
    return len(gzip.compress(datos))     # Comprime y devuelve el tamaño

# 3. Calcula NCD entre dos variables
def calcular_ncd(texto_x, texto_y):
    cx = comprimir(texto_x)              # Tamaño comprimido de X
    cy = comprimir(texto_y)              # Tamaño comprimido de Y
    cxy = comprimir(texto_x + "\n" + texto_y)  # Tamaño de ambos juntos

    ncd = (cxy - min(cx, cy)) / max(cx, cy)
    return ncd

# 4. Calcula la matriz 10×10
# Para cada PAR de variables (X1 vs X2, X1 vs X3, ..., X9 vs X10):
# → Son 45 pares en total (combinaciones de 10 en 2)
```

**Ejemplo:**
```
Si comprimes X9 (asistencia) → 50,000 bytes
Si comprimes X10 (desaprobados) → 48,000 bytes
Si comprimes AMBOS juntos → 95,000 bytes

NCD = (95000 - min(50000, 48000)) / max(50000, 48000)
NCD = (95000 - 48000) / 50000
NCD = 47000 / 50000
NCD = 0.94  → Son MUY DIFERENTES entre sí
```

**Entrada:** 6 DataFrames (particiones)
**Salida:** 6 matrices 10×10 (DataFrames) + 6 archivos CSV en `results/matrices/`

---

### 📄 `src/_04_topologias.py` — El Constructor de Redes

**¿Qué hace?** Convierte cada matriz NCD en un **grafo** (red de nodos y conexiones) y extrae el **Minimum Spanning Tree (MST)**.

**¿Qué es un MST?**

Un árbol de expansión mínima conecta TODOS los nodos (variables) usando las aristas (conexiones) con el menor peso (distancia NCD) total posible.

```
Grafo completo (todos conectados):     MST (mínimo necesario):

    X1 ──── X2                          X1 ──── X2
   / | \   / | \                         |
  X3  X4  X5  X6                        X4 ──── X5
   \  |  /  \ | /                         |
    X7 ── X8                             X7
     \   /
      X9 ── X10                          X9 ──── X10
```

**¿Cómo funciona internamente?**

```python
# 1. Crear grafo completo con NetworkX
G = nx.Graph()
for i, j en todas_las_parejas:
    G.add_edge("X1", "X2", weight=ncd_valor)  # Arista con peso = NCD

# 2. Extraer MST (NetworkX lo hace automáticamente)
mst = nx.minimum_spanning_tree(G, weight="weight")
# Resultado: 10 nodos, 9 aristas (siempre N-1 aristas en un MST)

# 3. Calcular grado ponderado de cada variable
# = Suma de los pesos de TODAS las aristas conectadas a esa variable
for nodo in mst.nodes():
    grado = sum(peso de cada arista conectada al nodo)
    # Si X1 está conectado a X2 (0.3) y X5 (0.7):
    # grado_X1 = 0.3 + 0.7 = 1.0
```

**¿Qué significan los grados ponderados?**
- **Grado alto** → Variable muy conectada, central en la red
- **Grado bajo** → Variable periférica, con pocas conexiones fuertes

**Gráficos que genera:**
- `mst_Best_12.5.png` — Red MST del grupo Best al 12.5%
- `heatmap_Best_12.5.png` — Mapa de calor de la matriz NCD
- (y así para cada partición: 6 MSTs + 6 heatmaps = 12 imágenes)

**Entrada:** 6 matrices NCD
**Salida:** 6 topologías (MST + grados) + 12 imágenes PNG

---

### 📄 `src/_05_comparacion.py` — El Comparador

**¿Qué hace?** Compara las redes Best vs Worst para cada nivel y encuentra qué variables cambian más. Es donde se responde la **pregunta central del proyecto**.

**¿Cómo funciona internamente?**

```python
# Para cada nivel (12.5%, 25%, 50%):

# 1. Toma los grados ponderados de Best y Worst
grados_best = topologias["Best_12.5"]["grados"]
# Ejemplo: {"X1": 2.94, "X2": 2.85, "X5": 2.80, ...}

grados_worst = topologias["Worst_12.5"]["grados"]
# Ejemplo: {"X1": 2.94, "X2": 1.84, "X5": 1.76, ...}

# 2. Calcula la diferencia D para cada variable
for variable en [X1, X2, ..., X10]:
    D = grados_worst[variable] - grados_best[variable]
    # X2: D = 1.84 - 2.85 = -1.01 (CAMBIÓ MUCHO → negativo)
    # X1: D = 2.94 - 2.94 = +0.01 (CASI NO CAMBIÓ)

# 3. Ordena por valor absoluto de D
# La variable con |D| más grande = MÁXIMO CAMBIO
# La variable con |D| más pequeño = MÍNIMO CAMBIO
```

**¿Cómo interpretar D?**

```
D = GradoPonderado_Worst - GradoPonderado_Best

D = +1.03 (X6 Beca)
  → En Worst, la beca está MÁS conectada en la red
  → Sugiere: la beca influye más en los de bajo rendimiento

D = -1.05 (X5 Trabaja)
  → En Best, trabajar está MÁS conectado en la red
  → Sugiere: trabajar influye más en los de alto rendimiento

D ≈ 0.00 (X4 Ingreso)
  → El ingreso tiene el MISMO rol en ambos grupos
  → Sugiere: el ingreso no diferencia Best de Worst
```

**Gráficos que genera:**
- `comparacion_12.5.png` — Barras comparativas Best vs Worst al 12.5%
- `comparacion_25.png` — ídem al 25%
- `comparacion_50.png` — ídem al 50%
- `resumen_comparacion_global.png` — Las 3 particiones juntas

**Entrada:** 6 topologías
**Salida:** 3 tablas de comparación + 4 gráficos PNG

---

### 📄 `src/_06_reporte_resultados.py` — El Escritor del Informe

**¿Qué hace?** Toma TODOS los datos generados y escribe un informe completo en formato Markdown automáticamente.

**¿Cómo funciona internamente?**

```python
def ejecutar(reporte_limpieza, particiones, matrices, topologias, comparaciones):
    md = ""

    # 1. Escribe la introducción con datos reales
    md += f"Dataset: {reporte_limpieza['final']} estudiantes"

    # 2. Convierte las matrices NCD a tablas Markdown
    for nombre, matriz in matrices.items():
        md += generar_tabla_markdown(matriz)

    # 3. Incluye las tablas de comparación con max/min cambio
    for nivel, comp in comparaciones.items():
        md += f"MAX CAMBIO: {comp['max_cambio']['Variable']}"

    # 4. Genera conclusiones automáticas
    # Cuenta qué variable aparece más veces como "max cambio"
    from collections import Counter
    variables_max = [comp["max_cambio"]["Variable"] for comp in comparaciones]
    freq = Counter(variables_max).most_common(3)

    # 5. Guarda como archivo .md
    with open("informe/informe_ncd_gzip.md", "w") as f:
        f.write(md)
```

**Entrada:** Todos los datos de los pasos anteriores
**Salida:** `informe/informe_ncd_gzip.md`

---

### 📄 `requirements.txt` — Las Dependencias

Lista las librerías de Python necesarias:

```
pandas       → Manejo de datos tabulares (DataFrames, CSV)
numpy        → Operaciones numéricas y matrices
networkx     → Grafos, redes y MST
matplotlib   → Gráficos y visualizaciones
scipy        → Funciones científicas auxiliares
```

Se instalan con: `pip install -r requirements.txt`

---

### 📄 `src/__init__.py` — El Marcador de Paquete

Solo tiene un comentario. Su existencia le dice a Python:

> "La carpeta `src/` es un paquete de Python. Puedes importar módulos desde aquí."

Sin este archivo, `from src import _01_limpieza` no funcionaría.

---

### 📄 `README.md` — La Documentación

Contiene:
- Descripción del proyecto
- Tabla de variables
- Instrucciones de instalación y ejecución
- Estructura de archivos
- Fórmula NCD explicada
- Cómo interpretar los resultados

---

## 5. Cómo se Conectan los Archivos

### Cadena de dependencias

```
main.py
  │
  ├── importa → _01_limpieza.py
  │     │ devuelve: DataFrame limpio + reporte
  │     ▼
  ├── importa → _02_particiones.py
  │     │ recibe: DataFrame limpio
  │     │ devuelve: 6 particiones
  │     ▼
  ├── importa → _03_ncd_gzip.py
  │     │ recibe: 6 particiones
  │     │ devuelve: 6 matrices NCD (10×10)
  │     ▼
  ├── importa → _04_topologias.py
  │     │ recibe: 6 matrices NCD
  │     │ devuelve: 6 topologías (MST + grados)
  │     ▼
  ├── importa → _05_comparacion.py
  │     │ recibe: 6 topologías
  │     │ devuelve: 3 comparaciones
  │     ▼
  └── importa → _06_reporte_resultados.py
          recibe: TODOS los datos anteriores
          genera: informe_ncd_gzip.md
```

### ¿Qué tipo de dato pasa entre archivos?

| De → A | Tipo de dato | Contenido |
|--------|-------------|-----------|
| Paso 1 → 2 | `pandas.DataFrame` | 18,000 filas × 11 columnas limpias |
| Paso 2 → 3 | `dict[str, DataFrame]` | 6 DataFrames con nombre ("Best_12.5", etc.) |
| Paso 3 → 4 | `dict[str, DataFrame]` | 6 matrices 10×10 de distancias NCD |
| Paso 4 → 5 | `dict[str, dict]` | 6 diccionarios con MST (grafo NetworkX) + grados |
| Paso 5 → 6 | `dict[str, dict]` | 3 comparaciones con tablas + max/min cambio |

### Archivos que se escriben en disco

```
Paso 2 escribe → results/tablas/Best_12.5.csv, Worst_12.5.csv, etc. (6 archivos)
Paso 3 escribe → results/matrices/ncd_Best_12.5.csv, etc. (6 archivos)
Paso 4 escribe → results/graficos/mst_*.png, heatmap_*.png (12 archivos)
Paso 5 escribe → results/tablas/comparacion_*.csv (3 archivos)
                  results/graficos/comparacion_*.png (3 archivos)
                  results/graficos/resumen_comparacion_global.png (1 archivo)
Paso 6 escribe → informe/informe_ncd_gzip.md (1 archivo)
                                                    TOTAL: 32 archivos
```

---

## 6. Conceptos Clave

### ¿Por qué X11 no se analiza con NCD?

**X11 (promedio final)** es la variable que usamos para **dividir** a los estudiantes en Best y Worst. Si la incluyéramos en el análisis NCD, estaríamos preguntando "¿el promedio se relaciona con el promedio?" — eso es **circular** y no aporta nada.

Lo que queremos saber es: **¿qué otras variables (X1-X10) se comportan diferente según el rendimiento?** Esas son las posibles **causas**.

### ¿Qué es un MST y por qué se usa?

Un **Minimum Spanning Tree** (Árbol de Expansión Mínima) es la forma más eficiente de conectar todos los nodos. Se usa porque:

1. Simplifica la red completa (de 45 conexiones a solo 9)
2. Mantiene las conexiones más importantes (las de menor distancia)
3. Revela la estructura principal de relaciones entre variables

### ¿Qué significa "grado ponderado"?

Es la **suma de pesos de las aristas** conectadas a un nodo. Ejemplo:

```
Si X2 (Zona) está conectado a:
  - X1 (Sexo) con peso 0.85
  - X5 (Trabaja) con peso 0.92
  - X7 (Educ.Jefe) con peso 0.98

Grado ponderado de X2 = 0.85 + 0.92 + 0.98 = 2.75
```

Un grado alto = la variable tiene muchas conexiones fuertes = es central en la red.

### ¿Cómo interpreto los resultados finales?

Los resultados del proyecto muestran:

| Partición | Mayor cambio | D | Significado |
|-----------|-------------|---|-------------|
| 12.5% | X5 (Trabaja) | −1.05 | En los extremos, trabajar diferencia mucho Best de Worst |
| 25% | X6 (Beca) | +1.01 | La beca tiene un rol muy diferente en cada grupo |
| 50% | X6 (Beca) | +1.04 | Patrón consistente: la beca es el factor clave |

**Conclusión principal:** La variable **X6 (Beca)** es el factor que más cambia su comportamiento entre estudiantes de alto y bajo rendimiento. Esto sugiere que la beca no solo es un apoyo financiero, sino que modifica toda la estructura de relaciones académicas del estudiante.
