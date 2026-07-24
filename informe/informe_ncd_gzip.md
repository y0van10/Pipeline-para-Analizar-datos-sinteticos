# Informe: Análisis de Comportamiento Académico por Bloques NCD/Gzip y Árboles Bayesianos

Este informe de investigación académica consolida los resultados del experimento automatizado llevado a cabo sobre el modelo de factores socioacadémicos utilizando la distancia de compresión normalizada (NCD), **particionamiento jerárquico por bloques de rendimiento (50%, 25%, 12.5%)** y **Árboles Bayesianos Probabilísticos (MST Dirigidos de Probabilidad Conjunta)**.

**Fecha de ejecución:** 20/07/2026 11:42  
**Total de estudiantes analizados:** 1000

---

## 1. Limpieza y Validación de Datos

El dataset original pasó por un proceso de limpieza para garantizar la calidad y lógica de los datos.

*   **Filas originales:** 1000
*   **Duplicados eliminados:** 0
*   **Filas nulas eliminadas:** 0
*   **Registros no numéricos eliminados:** 0
*   **Registros fuera de rango eliminados:** 0
*   **Filas finales retenidas:** 1000 (100.00%)

---

## 2. Definición de Bloques y Muestras por Nivel

Los estudiantes se ordenaron de manera descendente según su rendimiento académico (**X11 - Promedio Final**) y se generaron bloques continuos para 3 niveles de análisis:

*   **Nivel 50%:** 
    * `Best_50`: Top 50% (500 estudiantes)
    * `Worst_50`: Bottom 50% (500 estudiantes)
*   **Nivel 25% (4 Cuartiles):**
    * `Best_25_1` (0% - 25%), `Best_25_2` (25% - 50%), `Worst_25_1` (50% - 75%), `Worst_25_2` (75% - 100%)
*   **Nivel 12.5% (8 Octiles):**
    * `Best_12.5_1` a `Best_12.5_4` (Mejores) y `Worst_12.5_1` a `Worst_12.5_4` (Peores)

Todas las submuestras han sido almacenadas en sus carpetas correspondientes `results/nivel_<X>/tablas/`.

---

## 3. Matrices NCD (Normalized Compression Distance)

A continuación se presentan las matrices de distancia calculadas para cada bloque de rendimiento. Un valor cercano a `0` indica alta similitud/relación y un valor cercano a `1` indica independencia.

### Matriz NCD - Best_50 (Nivel 50%)

| gender | race/ethnicity | parental level of education | lunch | test preparation course | reading score | writing score |
| --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.9157 | 0.9211 | 0.8272 | 0.7889 | 1.0000 | 1.0000 |
| 0.9157 | 0.0000 | 0.9595 | 0.9458 | 0.9247 | 1.0000 | 1.0000 |
| 0.9211 | 0.9595 | 0.0000 | 0.9332 | 0.9150 | 1.0000 | 1.0000 |
| 0.8272 | 0.9458 | 0.9332 | 0.0000 | 0.8040 | 1.0000 | 1.0000 |
| 0.7889 | 0.9247 | 0.9150 | 0.8040 | 0.0000 | 1.0000 | 1.0000 |
| 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.8993 |
| 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.8993 | 0.0000 |

### Matriz NCD - Worst_50 (Nivel 50%)

| gender | race/ethnicity | parental level of education | lunch | test preparation course | reading score | writing score |
| --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.9191 | 0.9143 | 0.8286 | 0.7819 | 1.0000 | 1.0000 |
| 0.9191 | 0.0000 | 0.9571 | 0.9480 | 0.9220 | 1.0000 | 1.0000 |
| 0.9143 | 0.9571 | 0.0000 | 0.9367 | 0.9163 | 1.0000 | 1.0000 |
| 0.8286 | 0.9480 | 0.9367 | 0.0000 | 0.8190 | 1.0000 | 1.0000 |
| 0.7819 | 0.9220 | 0.9163 | 0.8190 | 0.0000 | 1.0000 | 1.0000 |
| 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.9026 |
| 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9026 | 0.0000 |

### Matriz NCD - Best_25_1 (Nivel 25%)

| gender | race/ethnicity | parental level of education | lunch | test preparation course | reading score | writing score |
| --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.8465 | 0.8839 | 0.7479 | 0.7045 | 0.9669 | 0.9682 |
| 0.8465 | 0.0000 | 0.9226 | 0.8960 | 0.8515 | 1.0000 | 1.0000 |
| 0.8839 | 0.9226 | 0.0000 | 0.9129 | 0.8806 | 1.0000 | 1.0000 |
| 0.7479 | 0.8960 | 0.9129 | 0.0000 | 0.7727 | 0.9934 | 0.9904 |
| 0.7045 | 0.8515 | 0.8806 | 0.7727 | 0.0000 | 0.9768 | 0.9777 |
| 0.9669 | 1.0000 | 1.0000 | 0.9934 | 0.9768 | 0.0000 | 0.8121 |
| 0.9682 | 1.0000 | 1.0000 | 0.9904 | 0.9777 | 0.8121 | 0.0000 |

### Matriz NCD - Best_25_2 (Nivel 25%)

| gender | race/ethnicity | parental level of education | lunch | test preparation course | reading score | writing score |
| --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.8250 | 0.8644 | 0.7299 | 0.6846 | 0.9712 | 0.9644 |
| 0.8250 | 0.0000 | 0.8983 | 0.8600 | 0.8500 | 1.0000 | 1.0000 |
| 0.8644 | 0.8983 | 0.0000 | 0.8847 | 0.8644 | 1.0000 | 1.0000 |
| 0.7299 | 0.8600 | 0.8847 | 0.0000 | 0.7518 | 0.9968 | 0.9838 |
| 0.6846 | 0.8500 | 0.8644 | 0.7518 | 0.0000 | 0.9744 | 0.9676 |
| 0.9712 | 1.0000 | 1.0000 | 0.9968 | 0.9744 | 0.0000 | 0.8435 |
| 0.9644 | 1.0000 | 1.0000 | 0.9838 | 0.9676 | 0.8435 | 0.0000 |

### Matriz NCD - Worst_25_1 (Nivel 25%)

| gender | race/ethnicity | parental level of education | lunch | test preparation course | reading score | writing score |
| --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.8389 | 0.8667 | 0.7214 | 0.6992 | 0.9612 | 0.9619 |
| 0.8389 | 0.0000 | 0.9100 | 0.8531 | 0.8341 | 1.0000 | 1.0000 |
| 0.8667 | 0.9100 | 0.0000 | 0.8767 | 0.8667 | 1.0000 | 1.0000 |
| 0.7214 | 0.8531 | 0.8767 | 0.0000 | 0.7214 | 0.9773 | 0.9746 |
| 0.6992 | 0.8341 | 0.8667 | 0.7214 | 0.0000 | 0.9709 | 0.9714 |
| 0.9612 | 1.0000 | 1.0000 | 0.9773 | 0.9709 | 0.0000 | 0.8349 |
| 0.9619 | 1.0000 | 1.0000 | 0.9746 | 0.9714 | 0.8349 | 0.0000 |

### Matriz NCD - Worst_25_2 (Nivel 25%)

| gender | race/ethnicity | parental level of education | lunch | test preparation course | reading score | writing score |
| --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.8299 | 0.8710 | 0.7397 | 0.6780 | 0.9651 | 0.9684 |
| 0.8299 | 0.0000 | 0.9032 | 0.8402 | 0.8351 | 1.0000 | 1.0000 |
| 0.8710 | 0.9032 | 0.0000 | 0.8903 | 0.8806 | 1.0000 | 1.0000 |
| 0.7397 | 0.8402 | 0.8903 | 0.0000 | 0.7466 | 0.9937 | 0.9968 |
| 0.6780 | 0.8351 | 0.8806 | 0.7466 | 0.0000 | 0.9810 | 0.9842 |
| 0.9651 | 1.0000 | 1.0000 | 0.9937 | 0.9810 | 0.0000 | 0.8734 |
| 0.9684 | 1.0000 | 1.0000 | 0.9968 | 0.9842 | 0.8734 | 0.0000 |

### Matriz NCD - Best_12.5_1 (Nivel 12.5%)

| gender | race/ethnicity | parental level of education | lunch | test preparation course | reading score | writing score |
| --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.7984 | 0.8495 | 0.7308 | 0.7159 | 0.9353 | 0.9261 |
| 0.7984 | 0.0000 | 0.8544 | 0.8450 | 0.8217 | 0.9294 | 0.9545 |
| 0.8495 | 0.8544 | 0.0000 | 0.8738 | 0.8544 | 0.9854 | 1.0000 |
| 0.7308 | 0.8450 | 0.8738 | 0.0000 | 0.7500 | 0.9588 | 0.9545 |
| 0.7159 | 0.8217 | 0.8544 | 0.7500 | 0.0000 | 0.9353 | 0.9375 |
| 0.9353 | 0.9294 | 0.9854 | 0.9588 | 0.9353 | 0.0000 | 0.7045 |
| 0.9261 | 0.9545 | 1.0000 | 0.9545 | 0.9375 | 0.7045 | 0.0000 |

### Matriz NCD - Best_12.5_2 (Nivel 12.5%)

| gender | race/ethnicity | parental level of education | lunch | test preparation course | reading score | writing score |
| --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.7955 | 0.8488 | 0.7253 | 0.6395 | 0.9034 | 0.9061 |
| 0.7955 | 0.0000 | 0.8488 | 0.8258 | 0.7879 | 0.9375 | 0.9448 |
| 0.8488 | 0.8488 | 0.0000 | 0.8585 | 0.8439 | 1.0000 | 1.0000 |
| 0.7253 | 0.8258 | 0.8585 | 0.0000 | 0.7143 | 0.9432 | 0.9558 |
| 0.6395 | 0.7879 | 0.8439 | 0.7143 | 0.0000 | 0.9205 | 0.9227 |
| 0.9034 | 0.9375 | 1.0000 | 0.9432 | 0.9205 | 0.0000 | 0.7348 |
| 0.9061 | 0.9448 | 1.0000 | 0.9558 | 0.9227 | 0.7348 | 0.0000 |

### Matriz NCD - Best_12.5_3 (Nivel 12.5%)

| gender | race/ethnicity | parental level of education | lunch | test preparation course | reading score | writing score |
| --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.7863 | 0.8317 | 0.7216 | 0.6437 | 0.9167 | 0.9143 |
| 0.7863 | 0.0000 | 0.8366 | 0.8092 | 0.7939 | 0.9611 | 0.9543 |
| 0.8317 | 0.8366 | 0.0000 | 0.8317 | 0.8267 | 1.0000 | 0.9950 |
| 0.7216 | 0.8092 | 0.8317 | 0.0000 | 0.7320 | 0.9444 | 0.9543 |
| 0.6437 | 0.7939 | 0.8267 | 0.7320 | 0.0000 | 0.9167 | 0.9257 |
| 0.9167 | 0.9611 | 1.0000 | 0.9444 | 0.9167 | 0.0000 | 0.7444 |
| 0.9143 | 0.9543 | 0.9950 | 0.9543 | 0.9257 | 0.7444 | 0.0000 |

### Matriz NCD - Best_12.5_4 (Nivel 12.5%)

| gender | race/ethnicity | parental level of education | lunch | test preparation course | reading score | writing score |
| --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.7910 | 0.8465 | 0.7444 | 0.7033 | 0.9399 | 0.9344 |
| 0.7910 | 0.0000 | 0.8416 | 0.8209 | 0.7985 | 0.9563 | 0.9454 |
| 0.8465 | 0.8416 | 0.0000 | 0.8515 | 0.8267 | 1.0000 | 0.9950 |
| 0.7444 | 0.8209 | 0.8515 | 0.0000 | 0.7143 | 0.9617 | 0.9399 |
| 0.7033 | 0.7985 | 0.8267 | 0.7143 | 0.0000 | 0.9454 | 0.9290 |
| 0.9399 | 0.9563 | 1.0000 | 0.9617 | 0.9454 | 0.0000 | 0.7486 |
| 0.9344 | 0.9454 | 0.9950 | 0.9399 | 0.9290 | 0.7486 | 0.0000 |

### Matriz NCD - Worst_12.5_1 (Nivel 12.5%)

| gender | race/ethnicity | parental level of education | lunch | test preparation course | reading score | writing score |
| --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.8162 | 0.8406 | 0.7444 | 0.6778 | 0.9261 | 0.9126 |
| 0.8162 | 0.0000 | 0.8551 | 0.8456 | 0.8088 | 0.9659 | 0.9508 |
| 0.8406 | 0.8551 | 0.0000 | 0.8502 | 0.8406 | 1.0000 | 0.9903 |
| 0.7444 | 0.8456 | 0.8502 | 0.0000 | 0.7333 | 0.9716 | 0.9399 |
| 0.6778 | 0.8088 | 0.8406 | 0.7333 | 0.0000 | 0.9375 | 0.9126 |
| 0.9261 | 0.9659 | 1.0000 | 0.9716 | 0.9375 | 0.0000 | 0.7322 |
| 0.9126 | 0.9508 | 0.9903 | 0.9399 | 0.9126 | 0.7322 | 0.0000 |

### Matriz NCD - Worst_12.5_2 (Nivel 12.5%)

| gender | race/ethnicity | parental level of education | lunch | test preparation course | reading score | writing score |
| --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.7910 | 0.8485 | 0.7619 | 0.6667 | 0.9500 | 0.9379 |
| 0.7910 | 0.0000 | 0.8535 | 0.8209 | 0.7985 | 0.9667 | 0.9605 |
| 0.8485 | 0.8535 | 0.0000 | 0.8283 | 0.8131 | 1.0000 | 1.0000 |
| 0.7619 | 0.8209 | 0.8283 | 0.0000 | 0.7333 | 0.9722 | 0.9548 |
| 0.6667 | 0.7985 | 0.8131 | 0.7333 | 0.0000 | 0.9389 | 0.9322 |
| 0.9500 | 0.9667 | 1.0000 | 0.9722 | 0.9389 | 0.0000 | 0.7722 |
| 0.9379 | 0.9605 | 1.0000 | 0.9548 | 0.9322 | 0.7722 | 0.0000 |

### Matriz NCD - Worst_12.5_3 (Nivel 12.5%)

| gender | race/ethnicity | parental level of education | lunch | test preparation course | reading score | writing score |
| --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.7778 | 0.8381 | 0.7353 | 0.6867 | 0.9290 | 0.9396 |
| 0.7778 | 0.0000 | 0.8286 | 0.7857 | 0.7778 | 0.9617 | 0.9725 |
| 0.8381 | 0.8286 | 0.0000 | 0.8286 | 0.8333 | 0.9810 | 1.0000 |
| 0.7353 | 0.7857 | 0.8286 | 0.0000 | 0.7157 | 0.9508 | 0.9670 |
| 0.6867 | 0.7778 | 0.8333 | 0.7157 | 0.0000 | 0.9508 | 0.9560 |
| 0.9290 | 0.9617 | 0.9810 | 0.9508 | 0.9508 | 0.0000 | 0.7541 |
| 0.9396 | 0.9725 | 1.0000 | 0.9670 | 0.9560 | 0.7541 | 0.0000 |

### Matriz NCD - Worst_12.5_4 (Nivel 12.5%)

| gender | race/ethnicity | parental level of education | lunch | test preparation course | reading score | writing score |
| --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.8148 | 0.8485 | 0.7500 | 0.7000 | 0.9375 | 0.9503 |
| 0.8148 | 0.0000 | 0.8384 | 0.8074 | 0.8148 | 0.9489 | 0.9448 |
| 0.8485 | 0.8384 | 0.0000 | 0.8434 | 0.8333 | 1.0000 | 1.0000 |
| 0.7500 | 0.8074 | 0.8434 | 0.0000 | 0.7188 | 0.9659 | 0.9503 |
| 0.7000 | 0.8148 | 0.8333 | 0.7188 | 0.0000 | 0.9489 | 0.9503 |
| 0.9375 | 0.9489 | 1.0000 | 0.9659 | 0.9489 | 0.0000 | 0.7624 |
| 0.9503 | 0.9448 | 1.0000 | 0.9503 | 0.9503 | 0.7624 | 0.0000 |

---

## 4. Comparación de Topologías (Extremos de Rendimiento)

Al extraer el Árbol de Expansión Mínima (MST) de cada grafo y calcular el **Grado Ponderado** (suma de pesos de aristas incidentes en el árbol), evaluamos qué tan conectada y central es cada variable dentro de la red del grupo.

La diferencia se calcula entre los bloques de rendimiento extremo de cada nivel:
$$D = Grado_{Worst} - Grado_{Best}$$

Un valor de $D$ muy positivo o muy negativo muestra variables que cambian drásticamente su rol en el comportamiento de los estudiantes de bajo rendimiento frente a los de alto rendimiento.

### Comparación Extrema para Nivel 50%

| Variable | Nombre | Grado_Best | Grado_Worst | Diferencia_D | Abs_Diferencia |
| --- | --- | --- | --- | --- | --- |
| gender | gender | 2.7046 | 3.6153 | 0.9107 | 0.9107 |
| test preparation course | test preparation cou… | 2.5079 | 1.6010 | -0.9070 | 0.9070 |
| lunch | lunch | 0.8040 | 0.8190 | 0.0150 | 0.0150 |
| race/ethnicity | race/ethnicity | 0.9157 | 0.9191 | 0.0034 | 0.0034 |
| reading score | reading score | 1.8993 | 1.9026 | 0.0033 | 0.0033 |
| writing score | writing score | 0.8993 | 0.9026 | 0.0033 | 0.0033 |
| parental level of education | parental level of ed… | 0.9150 | 0.9143 | -0.0007 | 0.0007 |

*   🔴 **Máximo Cambio:** Variable `gender` (gender) con una diferencia $|D| = 0.9107$
*   🟢 **Mínimo Cambio:** Variable `parental level of education` (parental level of ed…) con una diferencia $|D| = 0.0007$

### Comparación Extrema para Nivel 25%

| Variable | Nombre | Grado_Best | Grado_Worst | Diferencia_D | Abs_Diferencia |
| --- | --- | --- | --- | --- | --- |
| test preparation course | test preparation cou… | 1.5852 | 0.6780 | -0.9072 | 0.9072 |
| gender | gender | 3.2659 | 4.0836 | 0.8178 | 0.8178 |
| writing score | writing score | 0.8121 | 0.8734 | 0.0613 | 0.0613 |
| reading score | reading score | 1.7790 | 1.8385 | 0.0595 | 0.0595 |
| race/ethnicity | race/ethnicity | 0.8465 | 0.8299 | -0.0166 | 0.0166 |
| parental level of education | parental level of ed… | 0.8806 | 0.8710 | -0.0097 | 0.0097 |
| lunch | lunch | 0.7479 | 0.7397 | -0.0082 | 0.0082 |

*   🔴 **Máximo Cambio:** Variable `test preparation course` (test preparation cou…) con una diferencia $|D| = 0.9072$
*   🟢 **Mínimo Cambio:** Variable `lunch` (lunch) con una diferencia $|D| = 0.0082$

### Comparación Extrema para Nivel 12.5%

| Variable | Nombre | Grado_Best | Grado_Worst | Diferencia_D | Abs_Diferencia |
| --- | --- | --- | --- | --- | --- |
| gender | gender | 4.0208 | 1.6375 | -2.3833 | 2.3833 |
| test preparation course | test preparation cou… | 0.7159 | 2.2521 | 1.5362 | 1.5362 |
| reading score | reading score | 0.7045 | 1.6999 | 0.9954 | 0.9954 |
| writing score | writing score | 1.6307 | 0.7624 | -0.8682 | 0.8683 |
| lunch | lunch | 0.7308 | 1.5262 | 0.7954 | 0.7954 |
| parental level of education | parental level of ed… | 0.8495 | 0.8333 | -0.0162 | 0.0162 |
| race/ethnicity | race/ethnicity | 0.7984 | 0.8074 | 0.0090 | 0.0090 |

*   🔴 **Máximo Cambio:** Variable `gender` (gender) con una diferencia $|D| = 2.3833$
*   🟢 **Mínimo Cambio:** Variable `race/ethnicity` (race/ethnicity) con una diferencia $|D| = 0.0090$

---

## 5. Análisis de Árboles Bayesianos (MST Dirigidos de Probabilidad Conjunta)

Para validar las dependencias de forma puramente probabilística, binarizamos todas las variables. Para cada par de variables $(X_i, X_j)$, encontramos la combinación de estados $(a, b)$ que maximiza su **Probabilidad Conjunta**:
$$P_{max}(X_i, X_j) = \max_{a,b} P(X_i=a, X_j=b)$$

Extraemos un Árbol de Expansión Mínima sobre las distancias $1 - P_{max}$ y lo orientamos de $X_i 	o X_j$ si $P(X_i = a) \le P(X_j = b)$.

Esto produce las redes dirigidas almacenadas en `results/nivel_<X>/graficos/arbol_bayesiano_*.png` y `results/global/arbol_bayesiano_Completo.png`.

---

## 6. Conclusiones y Discusión Académica

El análisis comparativo de las topologías y las dependencias bayesianas revela cambios estructurales críticos en las relaciones de los estudiantes:

1.  **Factores Determinantes:** Al comparar los bloques extremos (el 12.5% mejor vs el 12.5% peor), las variables cuyas relaciones y centralidad topológica cambian de forma más radical son **gender (gender)** y **test preparation cou… (test preparation course)**.
2.  **Mecánica de Impacto:** La variable `gender` pasa de tener un grado de 4.0208 en los mejores estudiantes a 1.6375 en los peores ($D = -2.3833$).
3.  **Variables Invariantes:** Las variables que mostraron menor variación o que permanecieron casi idénticas en ambas redes son aquellas al final del ranking, lideradas por **race/ethnicity (race/ethnicity)**.

Este experimento demuestra empíricamente que la causa del bajo rendimiento académico no puede explicarse evaluando variables de manera aislada, sino a través de la **reorganización estructural de las variables socioeconómicas y de comportamiento académico**, lo cual queda plasmado en la direccionalidad de las dependencias probabilísticas en los Árboles Bayesianos generados.
