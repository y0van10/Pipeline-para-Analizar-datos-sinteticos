# Informe: Análisis de Comportamiento Académico por Bloques NCD/Gzip y Árboles Bayesianos

Este informe de investigación académica consolida los resultados del experimento automatizado llevado a cabo sobre el modelo de factores socioacadémicos utilizando la distancia de compresión normalizada (NCD), **particionamiento jerárquico por bloques de rendimiento (50%, 25%, 12.5%)** y **Árboles Bayesianos Probabilísticos (MST Dirigidos de Probabilidad Conjunta)**.

**Fecha de ejecución:** 20/07/2026 08:29  
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

## 2. Definición de Bloques y Muestras por Nivel

Los estudiantes se ordenaron de manera descendente según su rendimiento académico (**X11 - Promedio Final**) y se generaron bloques continuos para 3 niveles de análisis:

*   **Nivel 50%:** 
    * `Best_50`: Top 50% (9000 estudiantes)
    * `Worst_50`: Bottom 50% (9000 estudiantes)
*   **Nivel 25% (4 Cuartiles):**
    * `Best_25_1` (0% - 25%), `Best_25_2` (25% - 50%), `Worst_25_1` (50% - 75%), `Worst_25_2` (75% - 100%)
*   **Nivel 12.5% (8 Octiles):**
    * `Best_12.5_1` a `Best_12.5_4` (Mejores) y `Worst_12.5_1` a `Worst_12.5_4` (Peores)

Todas las submuestras han sido almacenadas en sus carpetas correspondientes `results/nivel_<X>/tablas/`.

---

## 3. Matrices NCD (Normalized Compression Distance)

A continuación se presentan las matrices de distancia calculadas para cada bloque de rendimiento. Un valor cercano a `0` indica alta similitud/relación y un valor cercano a `1` indica independencia.

### Matriz NCD - Best_50 (Nivel 50%)

| X1_sexo | X2_zona | X3_ciclo | X4_ingreso_familiar | X5_trabaja | X6_beca | X7_educ_jefe | X8_tam_familiar | X9_asistencia | X10_cursos_desaprobados |
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

### Matriz NCD - Worst_50 (Nivel 50%)

| X1_sexo | X2_zona | X3_ciclo | X4_ingreso_familiar | X5_trabaja | X6_beca | X7_educ_jefe | X8_tam_familiar | X9_asistencia | X10_cursos_desaprobados |
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

### Matriz NCD - Best_25_1 (Nivel 25%)

| X1_sexo | X2_zona | X3_ciclo | X4_ingreso_familiar | X5_trabaja | X6_beca | X7_educ_jefe | X8_tam_familiar | X9_asistencia | X10_cursos_desaprobados |
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

### Matriz NCD - Best_25_2 (Nivel 25%)

| X1_sexo | X2_zona | X3_ciclo | X4_ingreso_familiar | X5_trabaja | X6_beca | X7_educ_jefe | X8_tam_familiar | X9_asistencia | X10_cursos_desaprobados |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.9899 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 0.9899 | 0.0000 | 1.0000 | 1.0000 | 0.9956 | 0.9929 | 0.9841 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9445 | 1.0000 | 1.0000 |
| 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 0.9956 | 1.0000 | 1.0000 | 0.0000 | 0.8622 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 0.9929 | 1.0000 | 1.0000 | 0.8622 | 0.0000 | 0.9985 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 0.9841 | 1.0000 | 1.0000 | 1.0000 | 0.9985 | 0.0000 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 1.0000 | 0.9445 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 |
| 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 |
| 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |

### Matriz NCD - Worst_25_1 (Nivel 25%)

| X1_sexo | X2_zona | X3_ciclo | X4_ingreso_familiar | X5_trabaja | X6_beca | X7_educ_jefe | X8_tam_familiar | X9_asistencia | X10_cursos_desaprobados |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.9757 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 0.9757 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9923 | 0.9882 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9420 | 1.0000 | 1.0000 |
| 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.9091 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 0.9923 | 1.0000 | 1.0000 | 0.9091 | 0.0000 | 0.9957 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 0.9882 | 1.0000 | 1.0000 | 1.0000 | 0.9957 | 0.0000 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 1.0000 | 0.9420 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 |
| 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 |
| 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |

### Matriz NCD - Worst_25_2 (Nivel 25%)

| X1_sexo | X2_zona | X3_ciclo | X4_ingreso_familiar | X5_trabaja | X6_beca | X7_educ_jefe | X8_tam_familiar | X9_asistencia | X10_cursos_desaprobados |
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

### Matriz NCD - Best_12.5_1 (Nivel 12.5%)

| X1_sexo | X2_zona | X3_ciclo | X4_ingreso_familiar | X5_trabaja | X6_beca | X7_educ_jefe | X8_tam_familiar | X9_asistencia | X10_cursos_desaprobados |
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

### Matriz NCD - Best_12.5_2 (Nivel 12.5%)

| X1_sexo | X2_zona | X3_ciclo | X4_ingreso_familiar | X5_trabaja | X6_beca | X7_educ_jefe | X8_tam_familiar | X9_asistencia | X10_cursos_desaprobados |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.9489 | 1.0000 | 1.0000 | 0.9654 | 0.9925 | 0.9845 | 1.0000 | 1.0000 | 1.0000 |
| 0.9489 | 0.0000 | 1.0000 | 1.0000 | 0.9491 | 0.9540 | 0.9703 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9267 | 0.9969 | 1.0000 |
| 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 0.9654 | 0.9491 | 1.0000 | 1.0000 | 0.0000 | 0.8315 | 0.9791 | 1.0000 | 1.0000 | 1.0000 |
| 0.9925 | 0.9540 | 1.0000 | 1.0000 | 0.8315 | 0.0000 | 0.9852 | 1.0000 | 1.0000 | 1.0000 |
| 0.9845 | 0.9703 | 1.0000 | 1.0000 | 0.9791 | 0.9852 | 0.0000 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 1.0000 | 0.9267 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.9981 | 1.0000 |
| 1.0000 | 1.0000 | 0.9969 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9981 | 0.0000 | 1.0000 |
| 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |

### Matriz NCD - Best_12.5_3 (Nivel 12.5%)

| X1_sexo | X2_zona | X3_ciclo | X4_ingreso_familiar | X5_trabaja | X6_beca | X7_educ_jefe | X8_tam_familiar | X9_asistencia | X10_cursos_desaprobados |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.9609 | 1.0000 | 1.0000 | 0.9850 | 0.9970 | 0.9871 | 1.0000 | 1.0000 | 1.0000 |
| 0.9609 | 0.0000 | 1.0000 | 1.0000 | 0.9500 | 0.9548 | 0.9741 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9309 | 0.9978 | 1.0000 |
| 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 0.9850 | 0.9500 | 1.0000 | 1.0000 | 0.0000 | 0.7927 | 0.9810 | 1.0000 | 1.0000 | 1.0000 |
| 0.9970 | 0.9548 | 1.0000 | 1.0000 | 0.7927 | 0.0000 | 0.9844 | 1.0000 | 1.0000 | 1.0000 |
| 0.9871 | 0.9741 | 1.0000 | 1.0000 | 0.9810 | 0.9844 | 0.0000 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 1.0000 | 0.9309 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.9959 | 1.0000 |
| 1.0000 | 1.0000 | 0.9978 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9959 | 0.0000 | 1.0000 |
| 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |

### Matriz NCD - Best_12.5_4 (Nivel 12.5%)

| X1_sexo | X2_zona | X3_ciclo | X4_ingreso_familiar | X5_trabaja | X6_beca | X7_educ_jefe | X8_tam_familiar | X9_asistencia | X10_cursos_desaprobados |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.9552 | 1.0000 | 1.0000 | 1.0000 | 0.9940 | 0.9882 | 1.0000 | 1.0000 | 1.0000 |
| 0.9552 | 0.0000 | 1.0000 | 1.0000 | 0.9677 | 0.9645 | 0.9764 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9225 | 0.9968 | 1.0000 |
| 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 0.9677 | 1.0000 | 1.0000 | 0.0000 | 0.8313 | 0.9903 | 1.0000 | 1.0000 | 1.0000 |
| 0.9940 | 0.9645 | 1.0000 | 1.0000 | 0.8313 | 0.0000 | 0.9840 | 1.0000 | 1.0000 | 1.0000 |
| 0.9882 | 0.9764 | 1.0000 | 1.0000 | 0.9903 | 0.9840 | 0.0000 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 1.0000 | 0.9225 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.9963 | 1.0000 |
| 1.0000 | 1.0000 | 0.9968 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9963 | 0.0000 | 1.0000 |
| 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |

### Matriz NCD - Worst_12.5_1 (Nivel 12.5%)

| X1_sexo | X2_zona | X3_ciclo | X4_ingreso_familiar | X5_trabaja | X6_beca | X7_educ_jefe | X8_tam_familiar | X9_asistencia | X10_cursos_desaprobados |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.9460 | 1.0000 | 1.0000 | 1.0000 | 0.9985 | 0.9859 | 1.0000 | 1.0000 | 1.0000 |
| 0.9460 | 0.0000 | 1.0000 | 1.0000 | 0.9764 | 0.9578 | 0.9718 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9182 | 0.9963 | 1.0000 |
| 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 0.9764 | 1.0000 | 1.0000 | 0.0000 | 0.8421 | 0.9965 | 1.0000 | 1.0000 | 1.0000 |
| 0.9985 | 0.9578 | 1.0000 | 1.0000 | 0.8421 | 0.0000 | 0.9831 | 1.0000 | 1.0000 | 1.0000 |
| 0.9859 | 0.9718 | 1.0000 | 1.0000 | 0.9965 | 0.9831 | 0.0000 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 1.0000 | 0.9182 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.9979 | 1.0000 |
| 1.0000 | 1.0000 | 0.9963 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9979 | 0.0000 | 1.0000 |
| 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |

### Matriz NCD - Worst_12.5_2 (Nivel 12.5%)

| X1_sexo | X2_zona | X3_ciclo | X4_ingreso_familiar | X5_trabaja | X6_beca | X7_educ_jefe | X8_tam_familiar | X9_asistencia | X10_cursos_desaprobados |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.9423 | 1.0000 | 1.0000 | 1.0000 | 0.9985 | 0.9920 | 1.0000 | 1.0000 | 1.0000 |
| 0.9423 | 0.0000 | 1.0000 | 1.0000 | 0.9719 | 0.9491 | 0.9761 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9249 | 0.9947 | 1.0000 |
| 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 0.9719 | 1.0000 | 1.0000 | 0.0000 | 0.8604 | 0.9935 | 1.0000 | 1.0000 | 1.0000 |
| 0.9985 | 0.9491 | 1.0000 | 1.0000 | 0.8604 | 0.0000 | 0.9826 | 1.0000 | 1.0000 | 1.0000 |
| 0.9920 | 0.9761 | 1.0000 | 1.0000 | 0.9935 | 0.9826 | 0.0000 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 1.0000 | 0.9249 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.9968 | 1.0000 |
| 1.0000 | 1.0000 | 0.9947 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9968 | 0.0000 | 1.0000 |
| 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |

### Matriz NCD - Worst_12.5_3 (Nivel 12.5%)

| X1_sexo | X2_zona | X3_ciclo | X4_ingreso_familiar | X5_trabaja | X6_beca | X7_educ_jefe | X8_tam_familiar | X9_asistencia | X10_cursos_desaprobados |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.9335 | 1.0000 | 1.0000 | 0.9909 | 0.9864 | 0.9826 | 1.0000 | 1.0000 | 1.0000 |
| 0.9335 | 0.0000 | 1.0000 | 1.0000 | 0.9467 | 0.9428 | 0.9750 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9262 | 0.9957 | 1.0000 |
| 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 0.9909 | 0.9467 | 1.0000 | 1.0000 | 0.0000 | 0.8612 | 0.9795 | 1.0000 | 1.0000 | 1.0000 |
| 0.9864 | 0.9428 | 1.0000 | 1.0000 | 0.8612 | 0.0000 | 0.9811 | 1.0000 | 1.0000 | 1.0000 |
| 0.9826 | 0.9750 | 1.0000 | 1.0000 | 0.9795 | 0.9811 | 0.0000 | 1.0000 | 1.0000 | 1.0000 |
| 1.0000 | 1.0000 | 0.9262 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.9968 | 1.0000 |
| 1.0000 | 1.0000 | 0.9957 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9968 | 0.0000 | 1.0000 |
| 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |

### Matriz NCD - Worst_12.5_4 (Nivel 12.5%)

| X1_sexo | X2_zona | X3_ciclo | X4_ingreso_familiar | X5_trabaja | X6_beca | X7_educ_jefe | X8_tam_familiar | X9_asistencia | X10_cursos_desaprobados |
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

---

## 4. Comparación de Topologías (Extremos de Rendimiento)

Al extraer el Árbol de Expansión Mínima (MST) de cada grafo y calcular el **Grado Ponderado** (suma de pesos de aristas incidentes en el árbol), evaluamos qué tan conectada y central es cada variable dentro de la red del grupo.

La diferencia se calcula entre los bloques de rendimiento extremo de cada nivel:
$$D = Grado_{Worst} - Grado_{Best}$$

Un valor de $D$ muy positivo o muy negativo muestra variables que cambian drásticamente su rol en el comportamiento de los estudiantes de bajo rendimiento frente a los de alto rendimiento.

### Comparación Extrema para Nivel 50%

| Variable | Nombre | Grado_Best | Grado_Worst | Diferencia_D | Abs_Diferencia |
| --- | --- | --- | --- | --- | --- |
| X6_beca | X6_beca | 0.9167 | 1.9530 | 1.0362 | 1.0362 |
| X2_zona | X2_zona | 1.9936 | 0.9882 | -1.0054 | 1.0054 |
| X5_trabaja | X5_trabaja | 1.9167 | 1.9536 | 0.0369 | 0.0369 |
| X1_sexo | X1_sexo | 6.0000 | 5.9882 | -0.0118 | 0.0118 |
| X7_educ_jefe | X7_educ_jefe | 0.9936 | 0.9993 | 0.0057 | 0.0057 |
| X8_tam_familiar | X8_tam_familiar | 0.9532 | 0.9589 | 0.0057 | 0.0057 |
| X3_ciclo | X3_ciclo | 1.9532 | 1.9589 | 0.0057 | 0.0057 |
| X10_cursos_desaprobados | X10_cursos_desaproba… | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| X4_ingreso_familiar | X4_ingreso_familiar | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| X9_asistencia | X9_asistencia | 1.0000 | 1.0000 | 0.0000 | 0.0000 |

*   🔴 **Máximo Cambio:** Variable `X6_beca` (X6_beca) con una diferencia $|D| = 1.0362$
*   🟢 **Mínimo Cambio:** Variable `X9_asistencia` (X9_asistencia) con una diferencia $|D| = 0.0000$

### Comparación Extrema para Nivel 25%

| Variable | Nombre | Grado_Best | Grado_Worst | Diferencia_D | Abs_Diferencia |
| --- | --- | --- | --- | --- | --- |
| X6_beca | X6_beca | 0.8993 | 1.9121 | 1.0128 | 1.0128 |
| X1_sexo | X1_sexo | 4.9745 | 3.9722 | -1.0023 | 1.0023 |
| X8_tam_familiar | X8_tam_familiar | 0.9452 | 1.9473 | 1.0021 | 1.0021 |
| X2_zona | X2_zona | 2.9348 | 1.9418 | -0.9930 | 0.9930 |
| X5_trabaja | X5_trabaja | 1.8765 | 1.8902 | 0.0138 | 0.0137 |
| X7_educ_jefe | X7_educ_jefe | 0.9831 | 0.9914 | 0.0083 | 0.0083 |
| X3_ciclo | X3_ciclo | 1.9452 | 1.9474 | 0.0022 | 0.0022 |
| X9_asistencia | X9_asistencia | 1.0000 | 0.9999 | -0.0001 | 0.0001 |
| X10_cursos_desaprobados | X10_cursos_desaproba… | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| X4_ingreso_familiar | X4_ingreso_familiar | 1.0000 | 1.0000 | 0.0000 | 0.0000 |

*   🔴 **Máximo Cambio:** Variable `X6_beca` (X6_beca) con una diferencia $|D| = 1.0128$
*   🟢 **Mínimo Cambio:** Variable `X4_ingreso_familiar` (X4_ingreso_familiar) con una diferencia $|D| = 0.0000$

### Comparación Extrema para Nivel 12.5%

| Variable | Nombre | Grado_Best | Grado_Worst | Diferencia_D | Abs_Diferencia |
| --- | --- | --- | --- | --- | --- |
| X5_trabaja | X5_trabaja | 2.8037 | 1.7571 | -1.0466 | 1.0466 |
| X2_zona | X2_zona | 2.8453 | 1.8409 | -1.0044 | 1.0044 |
| X8_tam_familiar | X8_tam_familiar | 0.9295 | 1.9260 | 0.9965 | 0.9965 |
| X6_beca | X6_beca | 0.8837 | 1.8312 | 0.9474 | 0.9474 |
| X3_ciclo | X3_ciclo | 2.9272 | 2.9122 | -0.0151 | 0.0151 |
| X1_sexo | X1_sexo | 2.9361 | 2.9436 | 0.0075 | 0.0075 |
| X10_cursos_desaprobados | X10_cursos_desaproba… | 0.9777 | 0.9826 | 0.0048 | 0.0048 |
| X7_educ_jefe | X7_educ_jefe | 0.9669 | 0.9713 | 0.0044 | 0.0044 |
| X9_asistencia | X9_asistencia | 0.9977 | 0.9965 | -0.0013 | 0.0013 |
| X4_ingreso_familiar | X4_ingreso_familiar | 1.0000 | 1.0000 | 0.0000 | 0.0000 |

*   🔴 **Máximo Cambio:** Variable `X5_trabaja` (X5_trabaja) con una diferencia $|D| = 1.0466$
*   🟢 **Mínimo Cambio:** Variable `X4_ingreso_familiar` (X4_ingreso_familiar) con una diferencia $|D| = 0.0000$

---

## 5. Análisis de Árboles Bayesianos (MST Dirigidos de Probabilidad Conjunta)

Para validar las dependencias de forma puramente probabilística, binarizamos todas las variables. Para cada par de variables $(X_i, X_j)$, encontramos la combinación de estados $(a, b)$ que maximiza su **Probabilidad Conjunta**:
$$P_{max}(X_i, X_j) = \max_{a,b} P(X_i=a, X_j=b)$$

Extraemos un Árbol de Expansión Mínima sobre las distancias $1 - P_{max}$ y lo orientamos de $X_i 	o X_j$ si $P(X_i = a) \le P(X_j = b)$.

Esto produce las redes dirigidas almacenadas en `results/nivel_<X>/graficos/arbol_bayesiano_*.png` y `results/global/arbol_bayesiano_Completo.png`.

---

## 6. Conclusiones y Discusión Académica

El análisis comparativo de las topologías y las dependencias bayesianas revela cambios estructurales críticos en las relaciones de los estudiantes:

1.  **Factores Determinantes:** Al comparar los bloques extremos (el 12.5% mejor vs el 12.5% peor), las variables cuyas relaciones y centralidad topológica cambian de forma más radical son **X5_trabaja (X5_trabaja)** y **X2_zona (X2_zona)**.
2.  **Mecánica de Impacto:** La variable `X5_trabaja` pasa de tener un grado de 2.8037 en los mejores estudiantes a 1.7571 en los peores ($D = -1.0466$).
3.  **Variables Invariantes:** Las variables que mostraron menor variación o que permanecieron casi idénticas en ambas redes son aquellas al final del ranking, lideradas por **X4_ingreso_familiar (X4_ingreso_familiar)**.

Este experimento demuestra empíricamente que la causa del bajo rendimiento académico no puede explicarse evaluando variables de manera aislada, sino a través de la **reorganización estructural de las variables socioeconómicas y de comportamiento académico**, lo cual queda plasmado en la direccionalidad de las dependencias probabilísticas en los Árboles Bayesianos generados.
