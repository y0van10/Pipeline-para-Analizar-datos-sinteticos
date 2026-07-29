# Informe: Análisis de Comportamiento Académico por Bloques NCD/Gzip y Árboles Bayesianos

Este informe de investigación académica consolida los resultados del experimento automatizado llevado a cabo sobre el modelo de factores socioacadémicos utilizando la distancia de compresión normalizada (NCD), **particionamiento jerárquico por bloques de rendimiento (50%, 25%, 12.5%)** y **Árboles Bayesianos Probabilísticos (MST Dirigidos de Probabilidad Conjunta)**.

**Fecha de ejecución:** 29/07/2026 18:33  
**Total de estudiantes analizados:** 1500

---

## 1. Limpieza y Validación de Datos

El dataset original pasó por un proceso de limpieza para garantizar la calidad y lógica de los datos.

*   **Filas originales:** 1500
*   **Duplicados eliminados:** 0
*   **Filas nulas eliminadas:** 0
*   **Registros no numéricos eliminados:** 0
*   **Registros fuera de rango eliminados:** 0
*   **Filas finales retenidas:** 1500 (100.00%)

---

## 2. Definición de Bloques y Muestras por Nivel

Los estudiantes se ordenaron de manera descendente según su rendimiento académico (**X11 - Promedio Final**) y se generaron bloques continuos para 3 niveles de análisis:

*   **Nivel 50%:** 
    * `Best_50`: Top 50% (750 estudiantes)
    * `Worst_50`: Bottom 50% (750 estudiantes)
*   **Nivel 25% (4 Cuartiles):**
    * `Best_25_1` (0% - 25%), `Best_25_2` (25% - 50%), `Worst_25_1` (50% - 75%), `Worst_25_2` (75% - 100%)
*   **Nivel 12.5% (8 Octiles):**
    * `Best_12.5_1` a `Best_12.5_4` (Mejores) y `Worst_12.5_1` a `Worst_12.5_4` (Peores)

Todas las submuestras han sido almacenadas en sus carpetas correspondientes `results/nivel_<X>/tablas/`.

---

## 3. Matrices NCD (Normalized Compression Distance)

A continuación se presentan las matrices de distancia calculadas para cada bloque de rendimiento. Un valor cercano a `0` indica alta similitud/relación y un valor cercano a `1` indica independencia.

### Matriz NCD - Best_50 (Nivel 50%)

| tipo_delito | medio_utilizado | rango_edad_victima | genero_victima | region | hora_incidente | antivirus_activo | doble_factor | denuncia_formal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.9415 | 0.9744 | 0.8945 | 0.9574 | 0.9575 | 0.9347 | 0.9322 | 0.9447 |
| 0.9415 | 0.0000 | 0.9968 | 0.9384 | 0.9795 | 0.9747 | 0.9589 | 0.9637 | 0.9747 |
| 0.9744 | 0.9968 | 0.0000 | 0.9581 | 0.9415 | 0.9172 | 0.9163 | 0.9186 | 0.9093 |
| 0.8945 | 0.9384 | 0.9581 | 0.0000 | 0.9681 | 0.9448 | 0.9184 | 0.9149 | 0.9220 |
| 0.9574 | 0.9795 | 0.9415 | 0.9681 | 0.0000 | 0.9220 | 0.9326 | 0.9326 | 0.9255 |
| 0.9575 | 0.9747 | 0.9172 | 0.9448 | 0.9220 | 0.0000 | 0.9045 | 0.9066 | 0.9023 |
| 0.9347 | 0.9589 | 0.9163 | 0.9184 | 0.9326 | 0.9045 | 0.0000 | 0.6954 | 0.7162 |
| 0.9322 | 0.9637 | 0.9186 | 0.9149 | 0.9326 | 0.9066 | 0.6954 | 0.0000 | 0.7205 |
| 0.9447 | 0.9747 | 0.9093 | 0.9220 | 0.9255 | 0.9023 | 0.7162 | 0.7205 | 0.0000 |

### Matriz NCD - Worst_50 (Nivel 50%)

| tipo_delito | medio_utilizado | rango_edad_victima | genero_victima | region | hora_incidente | antivirus_activo | doble_factor | denuncia_formal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.9299 | 0.9777 | 0.9229 | 0.9826 | 0.9829 | 0.9709 | 0.9658 | 0.9675 |
| 0.9299 | 0.0000 | 0.9889 | 0.9347 | 0.9937 | 0.9809 | 0.9793 | 0.9761 | 0.9761 |
| 0.9777 | 0.9889 | 0.0000 | 0.9442 | 0.9462 | 0.9271 | 0.9005 | 0.9029 | 0.8981 |
| 0.9229 | 0.9347 | 0.9442 | 0.0000 | 0.9731 | 0.9542 | 0.9263 | 0.9228 | 0.9193 |
| 0.9826 | 0.9937 | 0.9462 | 0.9731 | 0.0000 | 0.9399 | 0.9462 | 0.9478 | 0.9399 |
| 0.9829 | 0.9809 | 0.9271 | 0.9542 | 0.9399 | 0.0000 | 0.9292 | 0.9250 | 0.9187 |
| 0.9709 | 0.9793 | 0.9005 | 0.9263 | 0.9462 | 0.9292 | 0.0000 | 0.6968 | 0.7240 |
| 0.9658 | 0.9761 | 0.9029 | 0.9228 | 0.9478 | 0.9250 | 0.6968 | 0.0000 | 0.7294 |
| 0.9675 | 0.9761 | 0.8981 | 0.9193 | 0.9399 | 0.9187 | 0.7240 | 0.7294 | 0.0000 |

### Matriz NCD - Best_25_1 (Nivel 25%)

| tipo_delito | medio_utilizado | rango_edad_victima | genero_victima | region | hora_incidente | antivirus_activo | doble_factor | denuncia_formal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.8917 | 0.9189 | 0.7933 | 0.8814 | 0.9068 | 0.8500 | 0.8375 | 0.8375 |
| 0.8917 | 0.0000 | 0.9471 | 0.8892 | 0.9118 | 0.9244 | 0.9244 | 0.9194 | 0.9219 |
| 0.9189 | 0.9471 | 0.0000 | 0.9073 | 0.8814 | 0.8674 | 0.8687 | 0.8764 | 0.8417 |
| 0.7933 | 0.8892 | 0.9073 | 0.0000 | 0.9017 | 0.8817 | 0.8492 | 0.8380 | 0.8324 |
| 0.8814 | 0.9118 | 0.8814 | 0.9017 | 0.0000 | 0.8576 | 0.8847 | 0.8814 | 0.8678 |
| 0.9068 | 0.9244 | 0.8674 | 0.8817 | 0.8576 | 0.0000 | 0.8638 | 0.8674 | 0.8387 |
| 0.8500 | 0.9244 | 0.8687 | 0.8492 | 0.8847 | 0.8638 | 0.0000 | 0.6496 | 0.6099 |
| 0.8375 | 0.9194 | 0.8764 | 0.8380 | 0.8814 | 0.8674 | 0.6496 | 0.0000 | 0.6525 |
| 0.8375 | 0.9219 | 0.8417 | 0.8324 | 0.8678 | 0.8387 | 0.6099 | 0.6525 | 0.0000 |

### Matriz NCD - Best_25_2 (Nivel 25%)

| tipo_delito | medio_utilizado | rango_edad_victima | genero_victima | region | hora_incidente | antivirus_activo | doble_factor | denuncia_formal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.8830 | 0.9275 | 0.8671 | 0.9239 | 0.9124 | 0.9275 | 0.9063 | 0.9214 |
| 0.8830 | 0.0000 | 0.9495 | 0.8883 | 0.9423 | 0.9282 | 0.9362 | 0.9202 | 0.9362 |
| 0.9275 | 0.9495 | 0.0000 | 0.9081 | 0.9003 | 0.8576 | 0.8713 | 0.8456 | 0.8603 |
| 0.8671 | 0.8883 | 0.9081 | 0.0000 | 0.9265 | 0.8949 | 0.8603 | 0.8268 | 0.8492 |
| 0.9239 | 0.9423 | 0.9003 | 0.9265 | 0.0000 | 0.8819 | 0.9029 | 0.8924 | 0.9003 |
| 0.9124 | 0.9282 | 0.8576 | 0.8949 | 0.8819 | 0.0000 | 0.8610 | 0.8542 | 0.8576 |
| 0.9275 | 0.9362 | 0.8713 | 0.8603 | 0.9029 | 0.8610 | 0.0000 | 0.5693 | 0.6014 |
| 0.9063 | 0.9202 | 0.8456 | 0.8268 | 0.8924 | 0.8542 | 0.5693 | 0.0000 | 0.6224 |
| 0.9214 | 0.9362 | 0.8603 | 0.8492 | 0.9003 | 0.8576 | 0.6014 | 0.6224 | 0.0000 |

### Matriz NCD - Worst_25_1 (Nivel 25%)

| tipo_delito | medio_utilizado | rango_edad_victima | genero_victima | region | hora_incidente | antivirus_activo | doble_factor | denuncia_formal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.8787 | 0.9455 | 0.8886 | 0.9307 | 0.9332 | 0.9356 | 0.9307 | 0.9307 |
| 0.8787 | 0.0000 | 0.9345 | 0.8892 | 0.9244 | 0.9219 | 0.9270 | 0.9244 | 0.9219 |
| 0.9455 | 0.9345 | 0.0000 | 0.8812 | 0.8892 | 0.8596 | 0.8467 | 0.8544 | 0.8429 |
| 0.8886 | 0.8892 | 0.8812 | 0.0000 | 0.9197 | 0.8836 | 0.8424 | 0.8370 | 0.8315 |
| 0.9307 | 0.9244 | 0.8892 | 0.9197 | 0.0000 | 0.8670 | 0.8947 | 0.8920 | 0.8947 |
| 0.9332 | 0.9219 | 0.8596 | 0.8836 | 0.8670 | 0.0000 | 0.8527 | 0.8493 | 0.8562 |
| 0.9356 | 0.9270 | 0.8467 | 0.8424 | 0.8947 | 0.8527 | 0.0000 | 0.5725 | 0.6377 |
| 0.9307 | 0.9244 | 0.8544 | 0.8370 | 0.8920 | 0.8493 | 0.5725 | 0.0000 | 0.6250 |
| 0.9307 | 0.9219 | 0.8429 | 0.8315 | 0.8947 | 0.8562 | 0.6377 | 0.6250 | 0.0000 |

### Matriz NCD - Worst_25_2 (Nivel 25%)

| tipo_delito | medio_utilizado | rango_edad_victima | genero_victima | region | hora_incidente | antivirus_activo | doble_factor | denuncia_formal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.8830 | 0.9191 | 0.8738 | 0.9343 | 0.9191 | 0.9159 | 0.9094 | 0.9288 |
| 0.8830 | 0.0000 | 0.9338 | 0.8906 | 0.9369 | 0.9262 | 0.9313 | 0.9211 | 0.9313 |
| 0.9191 | 0.9338 | 0.0000 | 0.8664 | 0.9116 | 0.8641 | 0.8319 | 0.8190 | 0.8319 |
| 0.8738 | 0.8906 | 0.8664 | 0.0000 | 0.9369 | 0.9024 | 0.8525 | 0.8251 | 0.8579 |
| 0.9343 | 0.9369 | 0.9116 | 0.9369 | 0.0000 | 0.8939 | 0.9040 | 0.8965 | 0.9040 |
| 0.9191 | 0.9262 | 0.8641 | 0.9024 | 0.8939 | 0.0000 | 0.8606 | 0.8537 | 0.8537 |
| 0.9159 | 0.9313 | 0.8319 | 0.8525 | 0.9040 | 0.8606 | 0.0000 | 0.5734 | 0.6042 |
| 0.9094 | 0.9211 | 0.8190 | 0.8251 | 0.8965 | 0.8537 | 0.5734 | 0.0000 | 0.5903 |
| 0.9288 | 0.9313 | 0.8319 | 0.8579 | 0.9040 | 0.8537 | 0.6042 | 0.5903 | 0.0000 |

### Matriz NCD - Best_12.5_1 (Nivel 12.5%)

| tipo_delito | medio_utilizado | rango_edad_victima | genero_victima | region | hora_incidente | antivirus_activo | doble_factor | denuncia_formal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.8783 | 0.8554 | 0.7797 | 0.8177 | 0.8475 | 0.7317 | 0.7195 | 0.7473 |
| 0.8783 | 0.0000 | 0.9049 | 0.8555 | 0.8517 | 0.8859 | 0.9049 | 0.9087 | 0.9087 |
| 0.8554 | 0.9049 | 0.0000 | 0.8373 | 0.7956 | 0.7910 | 0.8494 | 0.8494 | 0.8072 |
| 0.7797 | 0.8555 | 0.8373 | 0.0000 | 0.8398 | 0.8249 | 0.8220 | 0.8136 | 0.8136 |
| 0.8177 | 0.8517 | 0.7956 | 0.8398 | 0.0000 | 0.7790 | 0.8453 | 0.8564 | 0.8287 |
| 0.8475 | 0.8859 | 0.7910 | 0.8249 | 0.7790 | 0.0000 | 0.8362 | 0.8531 | 0.8136 |
| 0.7317 | 0.9049 | 0.8494 | 0.8220 | 0.8453 | 0.8362 | 0.0000 | 0.5676 | 0.6264 |
| 0.7195 | 0.9087 | 0.8494 | 0.8136 | 0.8564 | 0.8531 | 0.5676 | 0.0000 | 0.6374 |
| 0.7473 | 0.9087 | 0.8072 | 0.8136 | 0.8287 | 0.8136 | 0.6264 | 0.6374 | 0.0000 |

### Matriz NCD - Best_12.5_2 (Nivel 12.5%)

| tipo_delito | medio_utilizado | rango_edad_victima | genero_victima | region | hora_incidente | antivirus_activo | doble_factor | denuncia_formal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.8571 | 0.8728 | 0.8074 | 0.8342 | 0.8652 | 0.8296 | 0.8296 | 0.8444 |
| 0.8571 | 0.0000 | 0.9008 | 0.8611 | 0.8413 | 0.8730 | 0.9048 | 0.8968 | 0.9008 |
| 0.8728 | 0.9008 | 0.0000 | 0.8671 | 0.8291 | 0.8034 | 0.8671 | 0.8439 | 0.8381 |
| 0.8074 | 0.8611 | 0.8671 | 0.0000 | 0.8543 | 0.8427 | 0.8087 | 0.8087 | 0.8261 |
| 0.8342 | 0.8413 | 0.8291 | 0.8543 | 0.0000 | 0.7940 | 0.8543 | 0.8442 | 0.8392 |
| 0.8652 | 0.8730 | 0.8034 | 0.8427 | 0.7940 | 0.0000 | 0.8427 | 0.8371 | 0.8146 |
| 0.8296 | 0.9048 | 0.8671 | 0.8087 | 0.8543 | 0.8427 | 0.0000 | 0.5926 | 0.5824 |
| 0.8296 | 0.8968 | 0.8439 | 0.8087 | 0.8442 | 0.8371 | 0.5926 | 0.0000 | 0.5934 |
| 0.8444 | 0.9008 | 0.8381 | 0.8261 | 0.8392 | 0.8146 | 0.5824 | 0.5934 | 0.0000 |

### Matriz NCD - Best_12.5_3 (Nivel 12.5%)

| tipo_delito | medio_utilizado | rango_edad_victima | genero_victima | region | hora_incidente | antivirus_activo | doble_factor | denuncia_formal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.8333 | 0.8646 | 0.8229 | 0.8475 | 0.8229 | 0.8594 | 0.8698 | 0.8490 |
| 0.8333 | 0.0000 | 0.8992 | 0.8605 | 0.8682 | 0.8682 | 0.8953 | 0.8953 | 0.8837 |
| 0.8646 | 0.8992 | 0.0000 | 0.8807 | 0.8559 | 0.7906 | 0.8295 | 0.8352 | 0.8125 |
| 0.8229 | 0.8605 | 0.8807 | 0.0000 | 0.8814 | 0.8325 | 0.8000 | 0.8174 | 0.7826 |
| 0.8475 | 0.8682 | 0.8559 | 0.8814 | 0.0000 | 0.8136 | 0.8686 | 0.8686 | 0.8475 |
| 0.8229 | 0.8682 | 0.7906 | 0.8325 | 0.8136 | 0.0000 | 0.8220 | 0.8168 | 0.7906 |
| 0.8594 | 0.8953 | 0.8295 | 0.8000 | 0.8686 | 0.8220 | 0.0000 | 0.5444 | 0.5484 |
| 0.8698 | 0.8953 | 0.8352 | 0.8174 | 0.8686 | 0.8168 | 0.5444 | 0.0000 | 0.5591 |
| 0.8490 | 0.8837 | 0.8125 | 0.7826 | 0.8475 | 0.7906 | 0.5484 | 0.5591 | 0.0000 |

### Matriz NCD - Best_12.5_4 (Nivel 12.5%)

| tipo_delito | medio_utilizado | rango_edad_victima | genero_victima | region | hora_incidente | antivirus_activo | doble_factor | denuncia_formal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.8095 | 0.8880 | 0.8400 | 0.8400 | 0.8760 | 0.8880 | 0.8920 | 0.8800 |
| 0.8095 | 0.0000 | 0.9087 | 0.8532 | 0.8532 | 0.8849 | 0.9008 | 0.8968 | 0.8929 |
| 0.8880 | 0.9087 | 0.0000 | 0.8452 | 0.8395 | 0.7921 | 0.8155 | 0.8274 | 0.8095 |
| 0.8400 | 0.8532 | 0.8452 | 0.0000 | 0.8724 | 0.8427 | 0.8145 | 0.8145 | 0.8226 |
| 0.8400 | 0.8532 | 0.8395 | 0.8724 | 0.0000 | 0.8230 | 0.8560 | 0.8683 | 0.8560 |
| 0.8760 | 0.8849 | 0.7921 | 0.8427 | 0.8230 | 0.0000 | 0.7921 | 0.8202 | 0.8034 |
| 0.8880 | 0.9008 | 0.8155 | 0.8145 | 0.8560 | 0.7921 | 0.0000 | 0.5843 | 0.5385 |
| 0.8920 | 0.8968 | 0.8274 | 0.8145 | 0.8683 | 0.8202 | 0.5843 | 0.0000 | 0.5934 |
| 0.8800 | 0.8929 | 0.8095 | 0.8226 | 0.8560 | 0.8034 | 0.5385 | 0.5934 | 0.0000 |

### Matriz NCD - Worst_12.5_1 (Nivel 12.5%)

| tipo_delito | medio_utilizado | rango_edad_victima | genero_victima | region | hora_incidente | antivirus_activo | doble_factor | denuncia_formal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.8175 | 0.9015 | 0.8504 | 0.8613 | 0.8759 | 0.8942 | 0.8978 | 0.8978 |
| 0.8175 | 0.0000 | 0.8973 | 0.8669 | 0.8669 | 0.8707 | 0.8973 | 0.9049 | 0.8973 |
| 0.9015 | 0.8973 | 0.0000 | 0.8529 | 0.8455 | 0.8142 | 0.8176 | 0.8294 | 0.8294 |
| 0.8504 | 0.8669 | 0.8529 | 0.0000 | 0.8755 | 0.8361 | 0.8033 | 0.8115 | 0.8033 |
| 0.8613 | 0.8669 | 0.8455 | 0.8755 | 0.0000 | 0.8112 | 0.8541 | 0.8498 | 0.8584 |
| 0.8759 | 0.8707 | 0.8142 | 0.8361 | 0.8112 | 0.0000 | 0.8197 | 0.8251 | 0.8306 |
| 0.8942 | 0.8973 | 0.8176 | 0.8033 | 0.8541 | 0.8197 | 0.0000 | 0.5667 | 0.6222 |
| 0.8978 | 0.9049 | 0.8294 | 0.8115 | 0.8498 | 0.8251 | 0.5667 | 0.0000 | 0.6092 |
| 0.8978 | 0.8973 | 0.8294 | 0.8033 | 0.8584 | 0.8306 | 0.6222 | 0.6092 | 0.0000 |

### Matriz NCD - Worst_12.5_2 (Nivel 12.5%)

| tipo_delito | medio_utilizado | rango_edad_victima | genero_victima | region | hora_incidente | antivirus_activo | doble_factor | denuncia_formal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.8178 | 0.8996 | 0.8736 | 0.8773 | 0.8810 | 0.8959 | 0.8996 | 0.8922 |
| 0.8178 | 0.0000 | 0.8931 | 0.8779 | 0.8626 | 0.8740 | 0.8855 | 0.8931 | 0.8931 |
| 0.8996 | 0.8931 | 0.0000 | 0.8580 | 0.8465 | 0.7849 | 0.8107 | 0.8166 | 0.8047 |
| 0.8736 | 0.8779 | 0.8580 | 0.0000 | 0.8772 | 0.8387 | 0.7917 | 0.8000 | 0.8167 |
| 0.8773 | 0.8626 | 0.8465 | 0.8772 | 0.0000 | 0.8070 | 0.8377 | 0.8509 | 0.8421 |
| 0.8810 | 0.8740 | 0.7849 | 0.8387 | 0.8070 | 0.0000 | 0.8065 | 0.8172 | 0.8065 |
| 0.8959 | 0.8855 | 0.8107 | 0.7917 | 0.8377 | 0.8065 | 0.0000 | 0.5055 | 0.5368 |
| 0.8996 | 0.8931 | 0.8166 | 0.8000 | 0.8509 | 0.8172 | 0.5055 | 0.0000 | 0.5684 |
| 0.8922 | 0.8931 | 0.8047 | 0.8167 | 0.8421 | 0.8065 | 0.5368 | 0.5684 | 0.0000 |

### Matriz NCD - Worst_12.5_3 (Nivel 12.5%)

| tipo_delito | medio_utilizado | rango_edad_victima | genero_victima | region | hora_incidente | antivirus_activo | doble_factor | denuncia_formal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.8352 | 0.8686 | 0.8475 | 0.8740 | 0.8814 | 0.8898 | 0.8941 | 0.8898 |
| 0.8352 | 0.0000 | 0.8927 | 0.8736 | 0.8736 | 0.8851 | 0.9004 | 0.9080 | 0.9004 |
| 0.8686 | 0.8927 | 0.0000 | 0.8235 | 0.8537 | 0.7872 | 0.8039 | 0.8170 | 0.7909 |
| 0.8475 | 0.8736 | 0.8235 | 0.0000 | 0.8821 | 0.8404 | 0.7851 | 0.8264 | 0.8099 |
| 0.8740 | 0.8736 | 0.8537 | 0.8821 | 0.0000 | 0.8211 | 0.8659 | 0.8740 | 0.8577 |
| 0.8814 | 0.8851 | 0.7872 | 0.8404 | 0.8211 | 0.0000 | 0.8138 | 0.8191 | 0.7979 |
| 0.8898 | 0.9004 | 0.8039 | 0.7851 | 0.8659 | 0.8138 | 0.0000 | 0.6067 | 0.5851 |
| 0.8941 | 0.9080 | 0.8170 | 0.8264 | 0.8740 | 0.8191 | 0.6067 | 0.0000 | 0.5638 |
| 0.8898 | 0.9004 | 0.7909 | 0.8099 | 0.8577 | 0.7979 | 0.5851 | 0.5638 | 0.0000 |

### Matriz NCD - Worst_12.5_4 (Nivel 12.5%)

| tipo_delito | medio_utilizado | rango_edad_victima | genero_victima | region | hora_incidente | antivirus_activo | doble_factor | denuncia_formal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.8464 | 0.8588 | 0.8192 | 0.8784 | 0.8413 | 0.8588 | 0.8644 | 0.8701 |
| 0.8464 | 0.0000 | 0.9101 | 0.8764 | 0.8764 | 0.8727 | 0.9026 | 0.8989 | 0.9139 |
| 0.8588 | 0.9101 | 0.0000 | 0.8323 | 0.8745 | 0.8042 | 0.8000 | 0.8000 | 0.7935 |
| 0.8192 | 0.8764 | 0.8323 | 0.0000 | 0.8824 | 0.8201 | 0.8095 | 0.7857 | 0.8254 |
| 0.8784 | 0.8764 | 0.8745 | 0.8824 | 0.0000 | 0.8275 | 0.8667 | 0.8627 | 0.8745 |
| 0.8413 | 0.8727 | 0.8042 | 0.8201 | 0.8275 | 0.0000 | 0.8042 | 0.7937 | 0.7989 |
| 0.8588 | 0.9026 | 0.8000 | 0.8095 | 0.8667 | 0.8042 | 0.0000 | 0.5567 | 0.5464 |
| 0.8644 | 0.8989 | 0.8000 | 0.7857 | 0.8627 | 0.7937 | 0.5567 | 0.0000 | 0.5263 |
| 0.8701 | 0.9139 | 0.7935 | 0.8254 | 0.8745 | 0.7989 | 0.5464 | 0.5263 | 0.0000 |

---

## 4. Comparación de Topologías (Extremos de Rendimiento)

Al extraer el Árbol de Expansión Mínima (MST) de cada grafo y calcular el **Grado Ponderado** (suma de pesos de aristas incidentes en el árbol), evaluamos qué tan conectada y central es cada variable dentro de la red del grupo.

La diferencia se calcula entre los bloques de rendimiento extremo de cada nivel:
$$D = Grado_{Worst} - Grado_{Best}$$

Un valor de $D$ muy positivo o muy negativo muestra variables que cambian drásticamente su rol en el comportamiento de los estudiantes de bajo rendimiento frente a los de alto rendimiento.

### Comparación Extrema para Nivel 50%

| Variable | Nombre | Grado_Best | Grado_Worst | Diferencia_D | Abs_Diferencia |
| --- | --- | --- | --- | --- | --- |
| tipo_delito | tipo_delito | 0.8945 | 1.8529 | 0.9584 | 0.9584 |
| denuncia_formal | denuncia_formal | 2.5278 | 3.4601 | 0.9323 | 0.9323 |
| doble_factor | doble_factor | 1.6103 | 0.6968 | -0.9135 | 0.9135 |
| genero_victima | genero_victima | 2.7478 | 1.8422 | -0.9055 | 0.9055 |
| hora_incidente | hora_incidente | 1.8243 | 1.8586 | 0.0343 | 0.0343 |
| region | region | 0.9220 | 0.9399 | 0.0179 | 0.0179 |
| rango_edad_victima | rango_edad_victima | 0.9093 | 0.8981 | -0.0112 | 0.0112 |
| antivirus_activo | antivirus_activo | 1.4116 | 1.4208 | 0.0092 | 0.0092 |
| medio_utilizado | medio_utilizado | 0.9384 | 0.9299 | -0.0085 | 0.0085 |

*   🔴 **Máximo Cambio:** Variable `tipo_delito` (tipo_delito) con una diferencia $|D| = 0.9584$
*   🟢 **Mínimo Cambio:** Variable `medio_utilizado` (medio_utilizado) con una diferencia $|D| = 0.0085$

### Comparación Extrema para Nivel 25%

| Variable | Nombre | Grado_Best | Grado_Worst | Diferencia_D | Abs_Diferencia |
| --- | --- | --- | --- | --- | --- |
| doble_factor | doble_factor | 0.6496 | 3.6615 | 3.0119 | 3.0119 |
| denuncia_formal | denuncia_formal | 3.1227 | 0.5903 | -2.5325 | 2.5325 |
| tipo_delito | tipo_delito | 0.7933 | 1.7567 | 0.9634 | 0.9634 |
| genero_victima | genero_victima | 2.5149 | 1.6989 | -0.8159 | 0.8159 |
| antivirus_activo | antivirus_activo | 1.2595 | 0.5734 | -0.6861 | 0.6861 |
| hora_incidente | hora_incidente | 1.6963 | 1.7476 | 0.0513 | 0.0513 |
| region | region | 0.8576 | 0.8939 | 0.0363 | 0.0363 |
| rango_edad_victima | rango_edad_victima | 0.8417 | 0.8190 | -0.0227 | 0.0227 |
| medio_utilizado | medio_utilizado | 0.8892 | 0.8830 | -0.0062 | 0.0062 |

*   🔴 **Máximo Cambio:** Variable `doble_factor` (doble_factor) con una diferencia $|D| = 3.0119$
*   🟢 **Mínimo Cambio:** Variable `medio_utilizado` (medio_utilizado) con una diferencia $|D| = 0.0062$

### Comparación Extrema para Nivel 12.5%

| Variable | Nombre | Grado_Best | Grado_Worst | Diferencia_D | Abs_Diferencia |
| --- | --- | --- | --- | --- | --- |
| genero_victima | genero_victima | 0.7797 | 1.6049 | 0.8253 | 0.8253 |
| doble_factor | doble_factor | 1.2871 | 2.1057 | 0.8186 | 0.8186 |
| rango_edad_victima | rango_edad_victima | 1.5982 | 0.7935 | -0.8046 | 0.8046 |
| region | region | 1.6307 | 0.8275 | -0.8033 | 0.8033 |
| antivirus_activo | antivirus_activo | 1.1939 | 0.5464 | -0.6475 | 0.6476 |
| denuncia_formal | denuncia_formal | 1.4336 | 1.8663 | 0.4327 | 0.4327 |
| tipo_delito | tipo_delito | 1.4992 | 1.6657 | 0.1665 | 0.1665 |
| hora_incidente | hora_incidente | 1.5700 | 1.6211 | 0.0511 | 0.0511 |
| medio_utilizado | medio_utilizado | 0.8517 | 0.8464 | -0.0053 | 0.0053 |

*   🔴 **Máximo Cambio:** Variable `genero_victima` (genero_victima) con una diferencia $|D| = 0.8253$
*   🟢 **Mínimo Cambio:** Variable `medio_utilizado` (medio_utilizado) con una diferencia $|D| = 0.0053$

---

## 5. Análisis de Árboles Bayesianos (MST Dirigidos de Probabilidad Conjunta)

Para validar las dependencias de forma puramente probabilística, binarizamos todas las variables. Para cada par de variables $(X_i, X_j)$, encontramos la combinación de estados $(a, b)$ que maximiza su **Probabilidad Conjunta**:
$$P_{max}(X_i, X_j) = \max_{a,b} P(X_i=a, X_j=b)$$

Extraemos un Árbol de Expansión Mínima sobre las distancias $1 - P_{max}$ y lo orientamos de $X_i 	o X_j$ si $P(X_i = a) \le P(X_j = b)$.

Esto produce las redes dirigidas almacenadas en `results/nivel_<X>/graficos/arbol_bayesiano_*.png` y `results/global/arbol_bayesiano_Completo.png`.

---

## 6. Conclusiones y Discusión Académica

El análisis comparativo de las topologías y las dependencias bayesianas revela cambios estructurales críticos en las relaciones de los estudiantes:

1.  **Factores Determinantes:** Al comparar los bloques extremos (el 12.5% mejor vs el 12.5% peor), las variables cuyas relaciones y centralidad topológica cambian de forma más radical son **genero_victima (genero_victima)** y **doble_factor (doble_factor)**.
2.  **Mecánica de Impacto:** La variable `genero_victima` pasa de tener un grado de 0.7797 en los mejores estudiantes a 1.6049 en los peores ($D = +0.8253$).
3.  **Variables Invariantes:** Las variables que mostraron menor variación o que permanecieron casi idénticas en ambas redes son aquellas al final del ranking, lideradas por **medio_utilizado (medio_utilizado)**.

Este experimento demuestra empíricamente que la causa del bajo rendimiento académico no puede explicarse evaluando variables de manera aislada, sino a través de la **reorganización estructural de las variables socioeconómicas y de comportamiento académico**, lo cual queda plasmado en la direccionalidad de las dependencias probabilísticas en los Árboles Bayesianos generados.
