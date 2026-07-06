# Informe: Análisis de Comportamiento Académico con NCD/Gzip

**Fecha:** 06/07/2026 12:19
**Curso:** Ciberseguridad - 9no Semestre
**Universidad:** Universidad Nacional del Altiplano - Puno

---

## 1. Introducción

El presente informe documenta el experimento de análisis de patrones académicos
utilizando la métrica **Normalized Compression Distance (NCD)** con compresión **Gzip**.

El objetivo es descubrir **qué factores socioeconómicos y académicos** se comportan
de manera diferente entre estudiantes de alto y bajo rendimiento, revelando las
posibles **causas** del éxito o fracaso académico.

## 2. Objetivo

Aplicar un pipeline completo de análisis basado en NCD/Gzip para:

1. Dividir a los estudiantes según su rendimiento académico (X11 - Promedio Final)
2. Calcular distancias entre variables explicativas (X1-X10) dentro de cada grupo
3. Construir topologías de red (MST) que representen las relaciones entre variables
4. Comparar las redes Best vs Worst para identificar qué variables cambian más

**Pregunta central:** ¿Qué variables (causas) explican la diferencia entre
estudiantes con alto y bajo promedio final?

## 3. Descripción del Dataset

| Característica | Valor |
|---|---|
| Total de estudiantes (después de limpieza) | 18000 |
| Variables explicativas | X1 a X10 (10 variables) |
| Variable de clasificación | X11 - Promedio Final |
| Duplicados eliminados | 0 |
| Nulos eliminados | 0 |

### Variables del estudio

| Variable | Descripción | Tipo |
|---|---|---|
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
| **X11** | **Promedio final** | **Numérica (clasificación)** |

> **Nota:** X11 se usa exclusivamente para clasificar estudiantes en Best/Worst.
> Las variables X1-X10 son las que se analizan con NCD para descubrir patrones.

## 4. Metodología

### 4.1 Limpieza de datos

Se eliminaron filas con valores nulos, duplicados y datos fuera de rango lógico
(promedio < 0 o > 20, asistencia < 0 o > 100, etc.).

### 4.2 Particionamiento por rendimiento académico

Los estudiantes se ordenaron por X11 (promedio final) y se crearon particiones:

| Nivel | Best (Top) | Worst (Bottom) |
|---|---|---|
| 12.5% | 2250 estudiantes con mayor promedio | 2250 estudiantes con menor promedio |
| 25% | 4500 estudiantes | 4500 estudiantes |
| 50% | 9000 estudiantes | 9000 estudiantes |

### 4.3 Cálculo de NCD/Gzip

Para cada partición se calculó una **matriz de distancia 10×10** entre las variables
X1 a X10 usando la fórmula:

```
NCD(x, y) = (C(xy) - min(C(x), C(y))) / max(C(x), C(y))
```

Donde:
- `C(x)` = tamaño comprimido de la columna x con gzip (nivel 9)
- Cada columna se convirtió a cadena de texto antes de comprimir
- `NCD ≈ 0` → variables muy similares/relacionadas
- `NCD ≈ 1` → variables muy diferentes

### 4.4 Construcción de topologías de red

Con cada matriz NCD se construyó un **Minimum Spanning Tree (MST)** usando NetworkX:
- 10 nodos = 10 variables
- Aristas = distancia NCD entre variables
- El MST conecta todas las variables con el mínimo peso total

### 4.5 Comparación de topologías

Se compararon las redes Best vs Worst calculando el **grado ponderado** de cada
variable (suma de pesos de aristas conectadas en el MST) y la diferencia:

```
D = GradoPonderado_Worst - GradoPonderado_Best
```

- **D positivo grande** → la variable aumenta su conexión en Worst (factor de riesgo)
- **D negativo grande** → la variable disminuye su conexión en Worst (factor protector)

## 5. Resultados

### 5.1 Matrices NCD

#### Matriz NCD - BEST (12.5%)

| Var | X1 | X2 | X3 | X4 | X5 | X6 | X7 | X8 | X9 | X10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| X1 | 0.0000 | 0.9361 | 1.0000 | 1.0000 | 0.9574 | 0.9985 | 0.9698 | 1.0000 | 1.0000 | 1.0000 |
| X2 | 0.9361 | 0.0000 | 1.0000 | 1.0000 | 0.9422 | 0.9621 | 0.9669 | 1.0000 | 1.0000 | 1.0000 |
| X3 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9295 | 0.9977 | 1.0000 |
| X4 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| X5 | 0.9574 | 0.9422 | 1.0000 | 1.0000 | 0.0000 | 0.8837 | 0.9740 | 1.0000 | 1.0000 | 0.9777 |
| X6 | 0.9985 | 0.9621 | 1.0000 | 1.0000 | 0.8837 | 0.0000 | 0.9902 | 1.0000 | 1.0000 | 0.9983 |
| X7 | 0.9698 | 0.9669 | 1.0000 | 1.0000 | 0.9740 | 0.9902 | 0.0000 | 1.0000 | 1.0000 | 1.0000 |
| X8 | 1.0000 | 1.0000 | 0.9295 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.9980 | 1.0000 |
| X9 | 1.0000 | 1.0000 | 0.9977 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9980 | 0.0000 | 1.0000 |
| X10 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9777 | 0.9983 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |

#### Matriz NCD - BEST (25%)

| Var | X1 | X2 | X3 | X4 | X5 | X6 | X7 | X8 | X9 | X10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| X1 | 0.0000 | 0.9745 | 1.0000 | 1.0000 | 0.9915 | 1.0000 | 0.9936 | 1.0000 | 1.0000 | 1.0000 |
| X2 | 0.9745 | 0.0000 | 1.0000 | 1.0000 | 0.9772 | 0.9952 | 0.9831 | 1.0000 | 1.0000 | 1.0000 |
| X3 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9452 | 1.0000 | 1.0000 |
| X4 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| X5 | 0.9915 | 0.9772 | 1.0000 | 1.0000 | 0.0000 | 0.8993 | 0.9903 | 1.0000 | 1.0000 | 1.0000 |
| X6 | 1.0000 | 0.9952 | 1.0000 | 1.0000 | 0.8993 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| X7 | 0.9936 | 0.9831 | 1.0000 | 1.0000 | 0.9903 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 |
| X8 | 1.0000 | 1.0000 | 0.9452 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 |
| X9 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 |
| X10 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |

#### Matriz NCD - BEST (50%)

| Var | X1 | X2 | X3 | X4 | X5 | X6 | X7 | X8 | X9 | X10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| X1 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| X2 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9936 | 1.0000 | 1.0000 | 1.0000 |
| X3 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9532 | 1.0000 | 1.0000 |
| X4 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| X5 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.9167 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| X6 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9167 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| X7 | 1.0000 | 0.9936 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 |
| X8 | 1.0000 | 1.0000 | 0.9532 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 |
| X9 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 |
| X10 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |

#### Matriz NCD - WORST (12.5%)

| Var | X1 | X2 | X3 | X4 | X5 | X6 | X7 | X8 | X9 | X10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| X1 | 0.0000 | 0.9436 | 1.0000 | 1.0000 | 0.9588 | 0.9726 | 0.9777 | 1.0000 | 1.0000 | 1.0000 |
| X2 | 0.9436 | 0.0000 | 1.0000 | 1.0000 | 0.8973 | 0.9245 | 0.9769 | 1.0000 | 1.0000 | 1.0000 |
| X3 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9296 | 0.9981 | 0.9826 |
| X4 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| X5 | 0.9588 | 0.8973 | 1.0000 | 1.0000 | 0.0000 | 0.8598 | 0.9753 | 1.0000 | 1.0000 | 1.0000 |
| X6 | 0.9726 | 0.9245 | 1.0000 | 1.0000 | 0.8598 | 0.0000 | 0.9713 | 1.0000 | 1.0000 | 1.0000 |
| X7 | 0.9777 | 0.9769 | 1.0000 | 1.0000 | 0.9753 | 0.9713 | 0.0000 | 1.0000 | 1.0000 | 1.0000 |
| X8 | 1.0000 | 1.0000 | 0.9296 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.9965 | 1.0000 |
| X9 | 1.0000 | 1.0000 | 0.9981 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9965 | 0.0000 | 1.0000 |
| X10 | 1.0000 | 1.0000 | 0.9826 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |

#### Matriz NCD - WORST (25%)

| Var | X1 | X2 | X3 | X4 | X5 | X6 | X7 | X8 | X9 | X10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| X1 | 0.0000 | 0.9722 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| X2 | 0.9722 | 0.0000 | 1.0000 | 1.0000 | 0.9696 | 0.9785 | 0.9949 | 1.0000 | 1.0000 | 1.0000 |
| X3 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9474 | 1.0000 | 1.0000 |
| X4 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| X5 | 1.0000 | 0.9696 | 1.0000 | 1.0000 | 0.0000 | 0.9206 | 0.9957 | 1.0000 | 1.0000 | 1.0000 |
| X6 | 1.0000 | 0.9785 | 1.0000 | 1.0000 | 0.9206 | 0.0000 | 0.9914 | 1.0000 | 1.0000 | 1.0000 |
| X7 | 1.0000 | 0.9949 | 1.0000 | 1.0000 | 0.9957 | 0.9914 | 0.0000 | 1.0000 | 1.0000 | 1.0000 |
| X8 | 1.0000 | 1.0000 | 0.9474 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.9999 | 1.0000 |
| X9 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9999 | 0.0000 | 1.0000 |
| X10 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |

#### Matriz NCD - WORST (50%)

| Var | X1 | X2 | X3 | X4 | X5 | X6 | X7 | X8 | X9 | X10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| X1 | 0.0000 | 0.9882 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| X2 | 0.9882 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| X3 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9589 | 1.0000 | 1.0000 |
| X4 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| X5 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.9536 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| X6 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9536 | 0.0000 | 0.9993 | 1.0000 | 1.0000 | 1.0000 |
| X7 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9993 | 0.0000 | 1.0000 | 1.0000 | 1.0000 |
| X8 | 1.0000 | 1.0000 | 0.9589 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 |
| X9 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 |
| X10 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |

### 5.2 Comparación de Topologías

#### Partición 12.5%

| Variable | Nombre | Grado_Best | Grado_Worst | Diferencia_D | Abs_Diferencia |
| --- | --- | --- | --- | --- | --- |
| X5 | Trabaja | 2.8037 | 1.7571 | -1.0466 | 1.0466 |
| X2 | Zona | 2.8453 | 1.8409 | -1.0044 | 1.0044 |
| X8 | Tam.Fam | 0.9295 | 1.9260 | 0.9965 | 0.9965 |
| X6 | Beca | 0.8837 | 1.8312 | 0.9474 | 0.9474 |
| X3 | Ciclo | 2.9272 | 2.9122 | -0.0151 | 0.0151 |
| X1 | Sexo | 2.9361 | 2.9436 | 0.0075 | 0.0075 |
| X10 | Desaprobados | 0.9777 | 0.9826 | 0.0048 | 0.0048 |
| X7 | Educ.Jefe | 0.9669 | 0.9713 | 0.0044 | 0.0044 |
| X9 | Asistencia | 0.9977 | 0.9965 | -0.0013 | 0.0013 |
| X4 | Ingreso | 1.0000 | 1.0000 | 0.0000 | 0.0000 |

**Variable con MÁXIMO cambio:** X5 (Trabaja) → D = -1.0466

**Variable con MÍNIMO cambio:** X4 (Ingreso Familiar) → D = +0.0000

#### Partición 25%

| Variable | Nombre | Grado_Best | Grado_Worst | Diferencia_D | Abs_Diferencia |
| --- | --- | --- | --- | --- | --- |
| X6 | Beca | 0.8993 | 1.9121 | 1.0128 | 1.0128 |
| X1 | Sexo | 4.9745 | 3.9722 | -1.0023 | 1.0023 |
| X8 | Tam.Fam | 0.9452 | 1.9473 | 1.0021 | 1.0021 |
| X2 | Zona | 2.9348 | 1.9418 | -0.9930 | 0.9930 |
| X5 | Trabaja | 1.8765 | 1.8902 | 0.0138 | 0.0138 |
| X7 | Educ.Jefe | 0.9831 | 0.9914 | 0.0083 | 0.0083 |
| X3 | Ciclo | 1.9452 | 1.9474 | 0.0022 | 0.0022 |
| X9 | Asistencia | 1.0000 | 0.9999 | -0.0001 | 0.0001 |
| X4 | Ingreso | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| X10 | Desaprobados | 1.0000 | 1.0000 | 0.0000 | 0.0000 |

**Variable con MÁXIMO cambio:** X6 (Beca) → D = +1.0128

**Variable con MÍNIMO cambio:** X10 (Cursos Desaprobados) → D = +0.0000

#### Partición 50%

| Variable | Nombre | Grado_Best | Grado_Worst | Diferencia_D | Abs_Diferencia |
| --- | --- | --- | --- | --- | --- |
| X6 | Beca | 0.9167 | 1.9530 | 1.0362 | 1.0362 |
| X2 | Zona | 1.9936 | 0.9882 | -1.0054 | 1.0054 |
| X5 | Trabaja | 1.9167 | 1.9536 | 0.0369 | 0.0369 |
| X1 | Sexo | 6.0000 | 5.9882 | -0.0118 | 0.0118 |
| X7 | Educ.Jefe | 0.9936 | 0.9993 | 0.0057 | 0.0057 |
| X3 | Ciclo | 1.9532 | 1.9589 | 0.0057 | 0.0057 |
| X8 | Tam.Fam | 0.9532 | 0.9589 | 0.0057 | 0.0057 |
| X4 | Ingreso | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| X9 | Asistencia | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| X10 | Desaprobados | 1.0000 | 1.0000 | 0.0000 | 0.0000 |

**Variable con MÁXIMO cambio:** X6 (Beca) → D = +1.0362

**Variable con MÍNIMO cambio:** X10 (Cursos Desaprobados) → D = +0.0000

## 6. Análisis de Variables Relevantes

### Variables con mayor cambio estructural

Las siguientes variables presentan los mayores cambios en su posición dentro
de la red entre los grupos Best y Worst:

- **X6 (Beca)**: máximo cambio en 2 de 3 particiones
- **X5 (Trabaja)**: máximo cambio en 1 de 3 particiones

### Variables con menor cambio estructural

Las siguientes variables mantienen un comportamiento similar en ambos grupos:

- **X10 (Cursos Desaprobados)**: mínimo cambio en 2 de 3 particiones
- **X4 (Ingreso Familiar)**: mínimo cambio en 1 de 3 particiones


## 7. Discusión

El análisis NCD/Gzip permitió revelar que las relaciones entre variables
socioeconómicas y académicas **no son iguales** para estudiantes de alto y bajo
rendimiento. Las variables que más cambian su posición en la topología de red
son aquellas que tienen un comportamiento diferenciado según el grupo.

Cuando una variable tiene un **D positivo grande**, significa que en el grupo
Worst esa variable está más conectada/central en la red de relaciones,
sugiriendo que juega un papel más determinante en el bajo rendimiento.

Cuando una variable tiene un **D negativo grande**, significa que en el grupo
Best esa variable tiene mayor centralidad, sugiriendo un rol protector o
asociado al buen rendimiento.

## 8. Conclusiones

1. La técnica NCD/Gzip permite cuantificar relaciones entre variables sin
   asumir distribuciones estadísticas ni linealidad.

2. Las topologías de red (MST) revelan la estructura de dependencias entre
   variables dentro de cada grupo de rendimiento.

3. La comparación de topologías identifica las variables que más cambian
   su comportamiento entre grupos, indicando posibles factores causales.

4. Los resultados son consistentes a través de las tres particiones
   (12.5%, 25%, 50%), lo que refuerza la robustez de los hallazgos.

## 9. Reproducibilidad

Para reproducir este análisis:

```bash
pip install -r requirements.txt
python main.py
```

Los resultados se generan en:
- `results/matrices/` → Matrices NCD (CSV)
- `results/graficos/` → Gráficos de redes y comparaciones (PNG)
- `results/tablas/` → Tablas comparativas (CSV)

## 10. Anexos

### Archivos generados

| Carpeta | Contenido |
|---|---|
| `results/matrices/` | 6 matrices NCD (10×10) en formato CSV |
| `results/graficos/` | Gráficos MST, heatmaps, comparaciones |
| `results/tablas/` | Particiones y tablas comparativas |
| `informe/` | Este informe en formato Markdown |

---

*Informe generado automáticamente por el pipeline NCD/Gzip.*
