# Informe: Análisis de Comportamiento Académico con NCD/Gzip y Árboles Bayesianos

Este informe de investigación académica consolida los resultados del experimento automatizado llevado a cabo sobre el modelo de factores socioacadémicos utilizando la distancia de compresión normalizada (NCD) y **Árboles Bayesianos Probabilísticos (MST Dirigidos de Probabilidad Conjunta)**.

**Fecha de ejecución:** 16/07/2026 21:30  
**Total de estudiantes analizados:** 18000

---

## 1. Limpieza y Validación de Datos

El dataset original pasó por un proceso de limpieza para garantizar la calidad y lógica de los datos.

*   **Filas originales:** 18000
*   **Duplicados eliminados:** 0
*   **Filas nulas eliminadas:** 0
*   **Registros no numéricos eliminados:** 0
*   **Registros fuera de rango eliminados:** 0
*   **Filas finales retenidas:** 18000 (100.00%)

---

## 2. Definición de Grupos y Muestras

Los estudiantes se ordenaron de manera descendente según su rendimiento académico (**X11 - Promedio Final**) y se seleccionaron muestras en los extremos de rendimiento académico:

*   **Best (Alto rendimiento):** El porcentaje de estudiantes con mayor promedio.
*   **Worst (Bajo rendimiento):** El porcentaje de estudiantes con menor promedio.

Las muestras definidas fueron:
*   **12.5%:** 2250 estudiantes por subgrupo.
*   **25%:** 4500 estudiantes por subgrupo.
*   **50%:** 9000 estudiantes por subgrupo.

---

## 3. Matrices NCD (Normalized Compression Distance)

A continuación se presentan las matrices de distancia calculadas para cada grupo de rendimiento y nivel de partición. Un valor cercano a `0` indica alta similitud/relación y un valor cercano a `1` indica independencia.

### Matriz NCD - Best_12.5

| X1 | X2 | X3 | X4 | X5 | X6 | X7 | X8 | X9 | X10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.9361 | 1.0000 | 1.0000 | 0.9574 | 0.9985 | 0.9698 | 1.0000 | 1.0000 | 1.0000 |
| 0.9361 | 0.0000 | 1.0000 | 1.0000 | 0.9422 | 0.9621 | 0.9669 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9295 | 0.9977 | 1.0000 |
| 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 0.9574 | 0.9422 | 1.0000 | 1.0000 | 0.0000 | 0.8837 | 0.9740 | 1.0000 | 1.0000 | 0.9777 |
| 0.9985 | 0.9621 | 1.0000 | 1.0000 | 0.8837 | 0.0000 | 0.9902 | 1.0000 | 1.0000 | 0.9983 |
| 0.9698 | 0.9669 | 1.0000 | 1.0000 | 0.9740 | 0.9902 | 0.0000 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 1.0000 | 0.9295 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.9980 | 1.0000 |
| 1.0000 | 1.0000 | 0.9977 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9980 | 0.0000 | 1.0000 |
| 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9777 | 0.9983 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |

### Matriz NCD - Worst_12.5

| X1 | X2 | X3 | X4 | X5 | X6 | X7 | X8 | X9 | X10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.9436 | 1.0000 | 1.0000 | 0.9588 | 0.9726 | 0.9777 | 1.0000 | 1.0000 | 1.0000 |
| 0.9436 | 0.0000 | 1.0000 | 1.0000 | 0.8973 | 0.9245 | 0.9769 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9296 | 0.9981 | 0.9826 |
| 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 0.9588 | 0.8973 | 1.0000 | 1.0000 | 0.0000 | 0.8598 | 0.9753 | 1.0000 | 1.0000 | 1.0000 |
| 0.9726 | 0.9245 | 1.0000 | 1.0000 | 0.8598 | 0.0000 | 0.9713 | 1.0000 | 1.0000 | 1.0000 |
| 0.9777 | 0.9769 | 1.0000 | 1.0000 | 0.9753 | 0.9713 | 0.0000 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 1.0000 | 0.9296 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.9965 | 1.0000 |
| 1.0000 | 1.0000 | 0.9981 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9965 | 0.0000 | 1.0000 |
| 1.0000 | 1.0000 | 0.9826 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |

### Matriz NCD - Best_25

| X1 | X2 | X3 | X4 | X5 | X6 | X7 | X8 | X9 | X10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.9745 | 1.0000 | 1.0000 | 0.9915 | 1.0000 | 0.9936 | 1.0000 | 1.0000 | 1.0000 |
| 0.9745 | 0.0000 | 1.0000 | 1.0000 | 0.9772 | 0.9952 | 0.9831 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9452 | 1.0000 | 1.0000 |
| 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 0.9915 | 0.9772 | 1.0000 | 1.0000 | 0.0000 | 0.8993 | 0.9903 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 0.9952 | 1.0000 | 1.0000 | 0.8993 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 0.9936 | 0.9831 | 1.0000 | 1.0000 | 0.9903 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 1.0000 | 0.9452 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 |
| 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 |
| 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |

### Matriz NCD - Worst_25

| X1 | X2 | X3 | X4 | X5 | X6 | X7 | X8 | X9 | X10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.9722 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 0.9722 | 0.0000 | 1.0000 | 1.0000 | 0.9696 | 0.9785 | 0.9949 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9474 | 1.0000 | 1.0000 |
| 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 0.9696 | 1.0000 | 1.0000 | 0.0000 | 0.9206 | 0.9957 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 0.9785 | 1.0000 | 1.0000 | 0.9206 | 0.0000 | 0.9914 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 0.9949 | 1.0000 | 1.0000 | 0.9957 | 0.9914 | 0.0000 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 1.0000 | 0.9474 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.9999 | 1.0000 |
| 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9999 | 0.0000 | 1.0000 |
| 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |

### Matriz NCD - Best_50

| X1 | X2 | X3 | X4 | X5 | X6 | X7 | X8 | X9 | X10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9936 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9532 | 1.0000 | 1.0000 |
| 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.9167 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9167 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 0.9936 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 1.0000 | 0.9532 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 |
| 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 |
| 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |

### Matriz NCD - Worst_50

| X1 | X2 | X3 | X4 | X5 | X6 | X7 | X8 | X9 | X10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.9882 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 0.9882 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9589 | 1.0000 | 1.0000 |
| 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.9536 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9536 | 0.0000 | 0.9993 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9993 | 0.0000 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 1.0000 | 0.9589 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 |
| 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 |
| 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |

---

## 4. Comparación de Topologías (Best vs Worst)

Al extraer el Árbol de Expansión Mínima (MST) de cada grafo y calcular el **Grado Ponderado** (suma de pesos de aristas incidentes en el árbol), evaluamos qué tan conectada y central es cada variable dentro de la red del grupo.

La diferencia se calcula como:
$$D = Grado_{Worst} - Grado_{Best}$$

Un valor de $D$ muy positivo o muy negativo nos muestra variables que cambian drásticamente su rol en el comportamiento de los estudiantes de bajo rendimiento frente a los de alto rendimiento.

### Comparación para Partición 12.5%

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

*   🔴 **Máximo Cambio:** Variable `X5` (Trabaja) con una diferencia $|D| = 1.0466$
*   🟢 **Mínimo Cambio:** Variable `X4` (Ingreso) con una diferencia $|D| = 0.0000$

### Comparación para Partición 25%

| Variable | Nombre | Grado_Best | Grado_Worst | Diferencia_D | Abs_Diferencia |
| --- | --- | --- | --- | --- | --- |
| X6 | Beca | 0.8993 | 1.9121 | 1.0128 | 1.0128 |
| X1 | Sexo | 4.9745 | 3.9722 | -1.0023 | 1.0023 |
| X8 | Tam.Fam | 0.9452 | 1.9473 | 1.0021 | 1.0021 |
| X2 | Zona | 2.9348 | 1.9418 | -0.9930 | 0.9930 |
| X5 | Trabaja | 1.8765 | 1.8902 | 0.0138 | 0.0137 |
| X7 | Educ.Jefe | 0.9831 | 0.9914 | 0.0083 | 0.0083 |
| X3 | Ciclo | 1.9452 | 1.9474 | 0.0022 | 0.0022 |
| X9 | Asistencia | 1.0000 | 0.9999 | -0.0001 | 0.0001 |
| X4 | Ingreso | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| X10 | Desaprobados | 1.0000 | 1.0000 | 0.0000 | 0.0000 |

*   🔴 **Máximo Cambio:** Variable `X6` (Beca) con una diferencia $|D| = 1.0128$
*   🟢 **Mínimo Cambio:** Variable `X10` (Desaprobados) con una diferencia $|D| = 0.0000$

### Comparación para Partición 50%

| Variable | Nombre | Grado_Best | Grado_Worst | Diferencia_D | Abs_Diferencia |
| --- | --- | --- | --- | --- | --- |
| X6 | Beca | 0.9167 | 1.9530 | 1.0362 | 1.0362 |
| X2 | Zona | 1.9936 | 0.9882 | -1.0054 | 1.0054 |
| X5 | Trabaja | 1.9167 | 1.9536 | 0.0369 | 0.0369 |
| X1 | Sexo | 6.0000 | 5.9882 | -0.0118 | 0.0118 |
| X7 | Educ.Jefe | 0.9936 | 0.9993 | 0.0057 | 0.0057 |
| X8 | Tam.Fam | 0.9532 | 0.9589 | 0.0057 | 0.0057 |
| X3 | Ciclo | 1.9532 | 1.9589 | 0.0057 | 0.0057 |
| X4 | Ingreso | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| X9 | Asistencia | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| X10 | Desaprobados | 1.0000 | 1.0000 | 0.0000 | 0.0000 |

*   🔴 **Máximo Cambio:** Variable `X6` (Beca) con una diferencia $|D| = 1.0362$
*   🟢 **Mínimo Cambio:** Variable `X10` (Desaprobados) con una diferencia $|D| = 0.0000$

---

## 5. Análisis de Árboles Bayesianos (MST Dirigidos de Probabilidad Conjunta)

Para validar las dependencias de forma puramente probabilística, binarizamos todas las variables (utilizando la mediana para numéricas, el umbral de aprobación $\ge 11$ para promedio final, y el mapeo categórico para binarias).

Para cada par de variables $(X_i, X_j)$, encontramos la combinación de estados $(a, b)$ que maximiza su **Probabilidad Conjunta**:
$$P_{max}(X_i, X_j) = \max_{a,b} P(X_i=a, X_j=b)$$

Definimos una métrica de distancia de separación como $D(X_i, X_j) = 1 - P_{max}(X_i, X_j)$, con la cual extraemos un Árbol de Expansión Mínima. Para transformarlo en un **Árbol Bayesiano Dirigido**, cada arista del árbol se orienta de $X_i 	o X_j$ si su probabilidad condicional es mayor en ese sentido, es decir, si $P(X_i = a) \le P(X_j = b)$.

Esto produce las redes dirigidas almacenadas en `results/graficos/arbol_bayesiano_*.png`. El flujo de flechas ilustra la jerarquía de causa y efecto probabilístico entre los factores socioeconómicos y el rendimiento final académico.

---

## 6. Conclusiones y Discusión Académica

El análisis comparativo de las topologías y las dependencias bayesianas revela cambios estructurales críticos en las relaciones de los estudiantes:

1.  **Factores Determinantes:** Al comparar los extremos de rendimiento académico (el 12.5% superior e inferior), las variables cuyas relaciones y centralidad topológica cambian de forma más radical son **Trabaja (X5)** y **Zona (X2)**.
2.  **Mecánica de Impacto:** La variable `X5` pasa de tener un grado de 2.8037 en los mejores estudiantes a 1.7571 en los peores. Este cambio drástico ($D = -1.0466$) demuestra que su influencia en la red socioacadémica cambia significativamente según el rendimiento final.
3.  **Variables Invariantes:** Las variables que mostraron menor variación o que permanecieron casi idénticas en ambas redes son aquellas al final del ranking, lideradas por **Ingreso (X4)**, sugiriendo que su rol es neutro o estable en este contexto experimental.

Este experimento demuestra empíricamente que la causa del bajo rendimiento académico (X11) no puede explicarse evaluando variables de manera aislada, sino a través de la **reorganización estructural de las variables socioeconómicas y de comportamiento académico**, lo cual queda plasmado en la direccionalidad de las dependencias probabilísticas en los Árboles Bayesianos generados.
