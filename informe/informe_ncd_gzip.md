# Informe: Análisis de Comportamiento Académico por Bloques NCD/Gzip y Árboles Bayesianos

Este informe de investigación académica consolida los resultados del experimento automatizado llevado a cabo sobre el modelo de factores socioacadémicos utilizando la distancia de compresión normalizada (NCD), **particionamiento jerárquico por bloques de rendimiento (50%, 25%, 12.5%)** y **Árboles Bayesianos Probabilísticos (MST Dirigidos de Probabilidad Conjunta)**.

**Fecha de ejecución:** 30/07/2026 11:54  
**Total de estudiantes analizados:** 364

---

## 1. Limpieza y Validación de Datos

El dataset original pasó por un proceso de limpieza para garantizar la calidad y lógica de los datos.

*   **Filas originales:** 1000
*   **Duplicados eliminados:** 636
*   **Filas nulas eliminadas:** 0
*   **Registros no numéricos eliminados:** 0
*   **Registros fuera de rango eliminados:** 0
*   **Filas finales retenidas:** 364 (36.40%)

---

## 2. Definición de Bloques y Muestras por Nivel

Los estudiantes se ordenaron de manera descendente según su rendimiento académico (**X11 - Promedio Final**) y se generaron bloques continuos para 3 niveles de análisis:

*   **Nivel 50%:** 
    * `Best_50`: Top 50% (182 estudiantes)
    * `Worst_50`: Bottom 50% (182 estudiantes)
*   **Nivel 25% (4 Cuartiles):**
    * `Best_25_1` (0% - 25%), `Best_25_2` (25% - 50%), `Worst_25_1` (50% - 75%), `Worst_25_2` (75% - 100%)
*   **Nivel 12.5% (8 Octiles):**
    * `Best_12.5_1` a `Best_12.5_4` (Mejores) y `Worst_12.5_1` a `Worst_12.5_4` (Peores)

Todas las submuestras han sido almacenadas en sus carpetas correspondientes `results/nivel_<X>/tablas/`.

---

## 3. Matrices NCD (Normalized Compression Distance)

A continuación se presentan las matrices de distancia calculadas para cada bloque de rendimiento. Un valor cercano a `0` indica alta similitud/relación y un valor cercano a `1` indica independencia.

### Matriz NCD - Best_50 (Nivel 50%)

| having_IP_Address | URL_Length | Prefix_Suffix | having_Sub_Domain | SSLfinal_State | Domain_registeration_length | web_traffic | Google_Index |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.5946 | 0.6047 | 0.6887 | 0.6569 | 0.6964 | 0.6442 | 0.5493 |
| 0.5946 | 0.0000 | 0.6163 | 0.6792 | 0.6275 | 0.6786 | 0.6635 | 0.6216 |
| 0.6047 | 0.6163 | 0.0000 | 0.5566 | 0.5490 | 0.6071 | 0.6250 | 0.6047 |
| 0.6887 | 0.6792 | 0.5566 | 0.0000 | 0.5849 | 0.5804 | 0.5660 | 0.6887 |
| 0.6569 | 0.6275 | 0.5490 | 0.5849 | 0.0000 | 0.5536 | 0.5577 | 0.6667 |
| 0.6964 | 0.6786 | 0.6071 | 0.5804 | 0.5536 | 0.0000 | 0.6071 | 0.6875 |
| 0.6442 | 0.6635 | 0.6250 | 0.5660 | 0.5577 | 0.6071 | 0.0000 | 0.6827 |
| 0.5493 | 0.6216 | 0.6047 | 0.6887 | 0.6667 | 0.6875 | 0.6827 | 0.0000 |

### Matriz NCD - Worst_50 (Nivel 50%)

| having_IP_Address | URL_Length | Prefix_Suffix | having_Sub_Domain | SSLfinal_State | Domain_registeration_length | web_traffic | Google_Index |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.6296 | 0.6605 | 0.6514 | 0.5375 | 0.6514 | 0.6139 | 0.5211 |
| 0.6296 | 0.0000 | 0.6881 | 0.6789 | 0.5556 | 0.6789 | 0.6436 | 0.6543 |
| 0.6605 | 0.6881 | 0.0000 | 0.5780 | 0.6422 | 0.6055 | 0.5872 | 0.6972 |
| 0.6514 | 0.6789 | 0.5780 | 0.0000 | 0.6239 | 0.5596 | 0.5321 | 0.7064 |
| 0.5375 | 0.5556 | 0.6422 | 0.6239 | 0.0000 | 0.6789 | 0.5644 | 0.5500 |
| 0.6514 | 0.6789 | 0.6055 | 0.5596 | 0.6789 | 0.0000 | 0.5596 | 0.7064 |
| 0.6139 | 0.6436 | 0.5872 | 0.5321 | 0.5644 | 0.5596 | 0.0000 | 0.6634 |
| 0.5211 | 0.6543 | 0.6972 | 0.7064 | 0.5500 | 0.7064 | 0.6634 | 0.0000 |

### Matriz NCD - Best_25_1 (Nivel 25%)

| having_IP_Address | URL_Length | Prefix_Suffix | having_Sub_Domain | SSLfinal_State | Domain_registeration_length | web_traffic | Google_Index |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.5098 | 0.5965 | 0.6486 | 0.6269 | 0.6184 | 0.5833 | 0.4808 |
| 0.5098 | 0.0000 | 0.5789 | 0.6486 | 0.5672 | 0.6447 | 0.5694 | 0.5577 |
| 0.5965 | 0.5789 | 0.0000 | 0.5541 | 0.5224 | 0.5789 | 0.5556 | 0.5965 |
| 0.6486 | 0.6486 | 0.5541 | 0.0000 | 0.5270 | 0.4342 | 0.4459 | 0.6216 |
| 0.6269 | 0.5672 | 0.5224 | 0.5270 | 0.0000 | 0.4868 | 0.5417 | 0.6418 |
| 0.6184 | 0.6447 | 0.5789 | 0.4342 | 0.4868 | 0.0000 | 0.5000 | 0.6053 |
| 0.5833 | 0.5694 | 0.5556 | 0.4459 | 0.5417 | 0.5000 | 0.0000 | 0.6389 |
| 0.4808 | 0.5577 | 0.5965 | 0.6216 | 0.6418 | 0.6053 | 0.6389 | 0.0000 |

### Matriz NCD - Best_25_2 (Nivel 25%)

| having_IP_Address | URL_Length | Prefix_Suffix | having_Sub_Domain | SSLfinal_State | Domain_registeration_length | web_traffic | Google_Index |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.6379 | 0.5738 | 0.6000 | 0.6143 | 0.5897 | 0.6216 | 0.5102 |
| 0.6379 | 0.0000 | 0.6066 | 0.5733 | 0.6000 | 0.5897 | 0.5135 | 0.6034 |
| 0.5738 | 0.6066 | 0.0000 | 0.4800 | 0.5429 | 0.5513 | 0.5811 | 0.6230 |
| 0.6000 | 0.5733 | 0.4800 | 0.0000 | 0.5067 | 0.4615 | 0.4533 | 0.6400 |
| 0.6143 | 0.6000 | 0.5429 | 0.5067 | 0.0000 | 0.4872 | 0.4730 | 0.6286 |
| 0.5897 | 0.5897 | 0.5513 | 0.4615 | 0.4872 | 0.0000 | 0.4487 | 0.6026 |
| 0.6216 | 0.5135 | 0.5811 | 0.4533 | 0.4730 | 0.4487 | 0.0000 | 0.6351 |
| 0.5102 | 0.6034 | 0.6230 | 0.6400 | 0.6286 | 0.6026 | 0.6351 | 0.0000 |

### Matriz NCD - Worst_25_1 (Nivel 25%)

| having_IP_Address | URL_Length | Prefix_Suffix | having_Sub_Domain | SSLfinal_State | Domain_registeration_length | web_traffic | Google_Index |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.5614 | 0.6154 | 0.5867 | 0.5424 | 0.5811 | 0.5507 | 0.4600 |
| 0.5614 | 0.0000 | 0.5769 | 0.5600 | 0.4407 | 0.5676 | 0.5072 | 0.6491 |
| 0.6154 | 0.5769 | 0.0000 | 0.4872 | 0.5385 | 0.5256 | 0.4872 | 0.6282 |
| 0.5867 | 0.5600 | 0.4872 | 0.0000 | 0.5200 | 0.4667 | 0.4533 | 0.6400 |
| 0.5424 | 0.4407 | 0.5385 | 0.5200 | 0.0000 | 0.5405 | 0.4493 | 0.5593 |
| 0.5811 | 0.5676 | 0.5256 | 0.4667 | 0.5405 | 0.0000 | 0.4730 | 0.6351 |
| 0.5507 | 0.5072 | 0.4872 | 0.4533 | 0.4493 | 0.4730 | 0.0000 | 0.6087 |
| 0.4600 | 0.6491 | 0.6282 | 0.6400 | 0.5593 | 0.6351 | 0.6087 | 0.0000 |

### Matriz NCD - Worst_25_2 (Nivel 25%)

| having_IP_Address | URL_Length | Prefix_Suffix | having_Sub_Domain | SSLfinal_State | Domain_registeration_length | web_traffic | Google_Index |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.5370 | 0.6714 | 0.6447 | 0.5306 | 0.5811 | 0.6389 | 0.5102 |
| 0.5370 | 0.0000 | 0.6286 | 0.6316 | 0.5000 | 0.6216 | 0.5972 | 0.5741 |
| 0.6714 | 0.6286 | 0.0000 | 0.4474 | 0.6000 | 0.4324 | 0.4583 | 0.6429 |
| 0.6447 | 0.6316 | 0.4474 | 0.0000 | 0.6184 | 0.4868 | 0.4605 | 0.6711 |
| 0.5306 | 0.5000 | 0.6000 | 0.6184 | 0.0000 | 0.6351 | 0.5972 | 0.5208 |
| 0.5811 | 0.6216 | 0.4324 | 0.4868 | 0.6351 | 0.0000 | 0.4459 | 0.6486 |
| 0.6389 | 0.5972 | 0.4583 | 0.4605 | 0.5972 | 0.4459 | 0.0000 | 0.6667 |
| 0.5102 | 0.5741 | 0.6429 | 0.6711 | 0.5208 | 0.6486 | 0.6667 | 0.0000 |

### Matriz NCD - Best_12.5_1 (Nivel 12.5%)

| having_IP_Address | URL_Length | Prefix_Suffix | having_Sub_Domain | SSLfinal_State | Domain_registeration_length | web_traffic | Google_Index |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.4419 | 0.4773 | 0.5741 | 0.5000 | 0.4423 | 0.4400 | 0.3158 |
| 0.4419 | 0.0000 | 0.4773 | 0.4815 | 0.3542 | 0.5000 | 0.4200 | 0.4651 |
| 0.4773 | 0.4773 | 0.0000 | 0.4074 | 0.3333 | 0.4231 | 0.4600 | 0.5227 |
| 0.5741 | 0.4815 | 0.4074 | 0.0000 | 0.4259 | 0.3889 | 0.4259 | 0.5556 |
| 0.5000 | 0.3542 | 0.3333 | 0.4259 | 0.0000 | 0.4038 | 0.4200 | 0.5000 |
| 0.4423 | 0.5000 | 0.4231 | 0.3889 | 0.4038 | 0.0000 | 0.4231 | 0.5385 |
| 0.4400 | 0.4200 | 0.4600 | 0.4259 | 0.4200 | 0.4231 | 0.0000 | 0.5400 |
| 0.3158 | 0.4651 | 0.5227 | 0.5556 | 0.5000 | 0.5385 | 0.5400 | 0.0000 |

### Matriz NCD - Best_12.5_2 (Nivel 12.5%)

| having_IP_Address | URL_Length | Prefix_Suffix | having_Sub_Domain | SSLfinal_State | Domain_registeration_length | web_traffic | Google_Index |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.4359 | 0.3778 | 0.4912 | 0.4898 | 0.5385 | 0.4808 | 0.3590 |
| 0.4359 | 0.0000 | 0.3556 | 0.4737 | 0.4694 | 0.4808 | 0.4231 | 0.4359 |
| 0.3778 | 0.3556 | 0.0000 | 0.4035 | 0.3878 | 0.4231 | 0.4231 | 0.4889 |
| 0.4912 | 0.4737 | 0.4035 | 0.0000 | 0.4737 | 0.4386 | 0.4386 | 0.5965 |
| 0.4898 | 0.4694 | 0.3878 | 0.4737 | 0.0000 | 0.4423 | 0.5000 | 0.5714 |
| 0.5385 | 0.4808 | 0.4231 | 0.4386 | 0.4423 | 0.0000 | 0.4231 | 0.5000 |
| 0.4808 | 0.4231 | 0.4231 | 0.4386 | 0.5000 | 0.4231 | 0.0000 | 0.5577 |
| 0.3590 | 0.4359 | 0.4889 | 0.5965 | 0.5714 | 0.5000 | 0.5577 | 0.0000 |

### Matriz NCD - Best_12.5_3 (Nivel 12.5%)

| having_IP_Address | URL_Length | Prefix_Suffix | having_Sub_Domain | SSLfinal_State | Domain_registeration_length | web_traffic | Google_Index |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.4359 | 0.4043 | 0.5741 | 0.4792 | 0.4706 | 0.5000 | 0.3333 |
| 0.4359 | 0.0000 | 0.4894 | 0.4630 | 0.5208 | 0.4706 | 0.5179 | 0.4103 |
| 0.4043 | 0.4894 | 0.0000 | 0.3148 | 0.4167 | 0.4510 | 0.4464 | 0.4681 |
| 0.5741 | 0.4630 | 0.3148 | 0.0000 | 0.4815 | 0.4815 | 0.4107 | 0.5556 |
| 0.4792 | 0.5208 | 0.4167 | 0.4815 | 0.0000 | 0.3725 | 0.4464 | 0.5000 |
| 0.4706 | 0.4706 | 0.4510 | 0.4815 | 0.3725 | 0.0000 | 0.3750 | 0.4902 |
| 0.5000 | 0.5179 | 0.4464 | 0.4107 | 0.4464 | 0.3750 | 0.0000 | 0.5357 |
| 0.3333 | 0.4103 | 0.4681 | 0.5556 | 0.5000 | 0.4902 | 0.5357 | 0.0000 |

### Matriz NCD - Best_12.5_4 (Nivel 12.5%)

| having_IP_Address | URL_Length | Prefix_Suffix | having_Sub_Domain | SSLfinal_State | Domain_registeration_length | web_traffic | Google_Index |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.4667 | 0.5111 | 0.5208 | 0.5294 | 0.5172 | 0.5400 | 0.4211 |
| 0.4667 | 0.0000 | 0.4667 | 0.4375 | 0.4706 | 0.4483 | 0.4600 | 0.5111 |
| 0.5111 | 0.4667 | 0.0000 | 0.4583 | 0.4510 | 0.4138 | 0.4800 | 0.5111 |
| 0.5208 | 0.4375 | 0.4583 | 0.0000 | 0.4118 | 0.3966 | 0.4200 | 0.5417 |
| 0.5294 | 0.4706 | 0.4510 | 0.4118 | 0.0000 | 0.3966 | 0.4118 | 0.5882 |
| 0.5172 | 0.4483 | 0.4138 | 0.3966 | 0.3966 | 0.0000 | 0.4655 | 0.6207 |
| 0.5400 | 0.4600 | 0.4800 | 0.4200 | 0.4118 | 0.4655 | 0.0000 | 0.5800 |
| 0.4211 | 0.5111 | 0.5111 | 0.5417 | 0.5882 | 0.6207 | 0.5800 | 0.0000 |

### Matriz NCD - Worst_12.5_1 (Nivel 12.5%)

| having_IP_Address | URL_Length | Prefix_Suffix | having_Sub_Domain | SSLfinal_State | Domain_registeration_length | web_traffic | Google_Index |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.5455 | 0.5385 | 0.5417 | 0.4783 | 0.4727 | 0.4600 | 0.2821 |
| 0.5455 | 0.0000 | 0.4423 | 0.5208 | 0.4783 | 0.4727 | 0.5000 | 0.4545 |
| 0.5385 | 0.4423 | 0.0000 | 0.5385 | 0.4808 | 0.4182 | 0.4808 | 0.5000 |
| 0.5417 | 0.5208 | 0.5385 | 0.0000 | 0.3542 | 0.4545 | 0.5200 | 0.4792 |
| 0.4783 | 0.4783 | 0.4808 | 0.3542 | 0.0000 | 0.5091 | 0.4600 | 0.4783 |
| 0.4727 | 0.4727 | 0.4182 | 0.4545 | 0.5091 | 0.0000 | 0.4182 | 0.5273 |
| 0.4600 | 0.5000 | 0.4808 | 0.5200 | 0.4600 | 0.4182 | 0.0000 | 0.4800 |
| 0.2821 | 0.4545 | 0.5000 | 0.4792 | 0.4783 | 0.5273 | 0.4800 | 0.0000 |

### Matriz NCD - Worst_12.5_2 (Nivel 12.5%)

| having_IP_Address | URL_Length | Prefix_Suffix | having_Sub_Domain | SSLfinal_State | Domain_registeration_length | web_traffic | Google_Index |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.4103 | 0.5439 | 0.4909 | 0.4359 | 0.5400 | 0.3590 | 0.3000 |
| 0.4103 | 0.0000 | 0.5439 | 0.4909 | 0.4615 | 0.4800 | 0.4359 | 0.4250 |
| 0.5439 | 0.5439 | 0.0000 | 0.3860 | 0.6491 | 0.4912 | 0.6140 | 0.5789 |
| 0.4909 | 0.4909 | 0.3860 | 0.0000 | 0.6000 | 0.5091 | 0.5455 | 0.5455 |
| 0.4359 | 0.4615 | 0.6491 | 0.6000 | 0.0000 | 0.5000 | 0.4103 | 0.4000 |
| 0.5400 | 0.4800 | 0.4912 | 0.5091 | 0.5000 | 0.0000 | 0.5400 | 0.5200 |
| 0.3590 | 0.4359 | 0.6140 | 0.5455 | 0.4103 | 0.5400 | 0.0000 | 0.4000 |
| 0.3000 | 0.4250 | 0.5789 | 0.5455 | 0.4000 | 0.5200 | 0.4000 | 0.0000 |

### Matriz NCD - Worst_12.5_3 (Nivel 12.5%)

| having_IP_Address | URL_Length | Prefix_Suffix | having_Sub_Domain | SSLfinal_State | Domain_registeration_length | web_traffic | Google_Index |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.4737 | 0.4800 | 0.5192 | 0.3846 | 0.5000 | 0.5000 | 0.4211 |
| 0.4737 | 0.0000 | 0.5000 | 0.5385 | 0.2308 | 0.5000 | 0.4600 | 0.3947 |
| 0.4800 | 0.5000 | 0.0000 | 0.4808 | 0.4800 | 0.4615 | 0.4000 | 0.5400 |
| 0.5192 | 0.5385 | 0.4808 | 0.0000 | 0.5000 | 0.4231 | 0.4423 | 0.5577 |
| 0.3846 | 0.2308 | 0.4800 | 0.5000 | 0.0000 | 0.5192 | 0.4200 | 0.4103 |
| 0.5000 | 0.5000 | 0.4615 | 0.4231 | 0.5192 | 0.0000 | 0.4615 | 0.5769 |
| 0.5000 | 0.4600 | 0.4000 | 0.4423 | 0.4200 | 0.4615 | 0.0000 | 0.5200 |
| 0.4211 | 0.3947 | 0.5400 | 0.5577 | 0.4103 | 0.5769 | 0.5200 | 0.0000 |

### Matriz NCD - Worst_12.5_4 (Nivel 12.5%)

| having_IP_Address | URL_Length | Prefix_Suffix | having_Sub_Domain | SSLfinal_State | Domain_registeration_length | web_traffic | Google_Index |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 0.3810 | 0.5094 | 0.5283 | 0.3947 | 0.5000 | 0.5357 | 0.3500 |
| 0.3810 | 0.0000 | 0.5472 | 0.4906 | 0.3810 | 0.4815 | 0.4286 | 0.4048 |
| 0.5094 | 0.5472 | 0.0000 | 0.4340 | 0.5472 | 0.4815 | 0.4107 | 0.5283 |
| 0.5283 | 0.4906 | 0.4340 | 0.0000 | 0.5094 | 0.4630 | 0.3750 | 0.5472 |
| 0.3947 | 0.3810 | 0.5472 | 0.5094 | 0.0000 | 0.5370 | 0.4821 | 0.4250 |
| 0.5000 | 0.4815 | 0.4815 | 0.4630 | 0.5370 | 0.0000 | 0.3750 | 0.5370 |
| 0.5357 | 0.4286 | 0.4107 | 0.3750 | 0.4821 | 0.3750 | 0.0000 | 0.5357 |
| 0.3500 | 0.4048 | 0.5283 | 0.5472 | 0.4250 | 0.5370 | 0.5357 | 0.0000 |

---

## 4. Comparación de Topologías (Extremos de Rendimiento)

Al extraer el Árbol de Expansión Mínima (MST) de cada grafo y calcular el **Grado Ponderado** (suma de pesos de aristas incidentes en el árbol), evaluamos qué tan conectada y central es cada variable dentro de la red del grupo.

La diferencia se calcula entre los bloques de rendimiento extremo de cada nivel:
$$D = Grado_{Worst} - Grado_{Best}$$

Un valor de $D$ muy positivo o muy negativo muestra variables que cambian drásticamente su rol en el comportamiento de los estudiantes de bajo rendimiento frente a los de alto rendimiento.

### Comparación Extrema para Nivel 50%

| Variable | Nombre | Grado_Best | Grado_Worst | Diferencia_D | Abs_Diferencia |
| --- | --- | --- | --- | --- | --- |
| Prefix_Suffix | Prefix_Suffix | 1.7103 | 0.5780 | -1.1323 | 1.1323 |
| having_Sub_Domain | having_Sub_Domain | 0.5566 | 1.6697 | 1.1131 | 1.1131 |
| having_IP_Address | having_IP_Address | 1.7485 | 1.0586 | -0.6899 | 0.6899 |
| web_traffic | web_traffic | 0.5577 | 1.0965 | 0.5388 | 0.5388 |
| URL_Length | URL_Length | 0.5946 | 0.5556 | -0.0390 | 0.0390 |
| Google_Index | Google_Index | 0.5493 | 0.5211 | -0.0282 | 0.0282 |
| Domain_registeration_length | Domain_registeration… | 0.5536 | 0.5596 | 0.0061 | 0.0061 |
| SSLfinal_State | SSLfinal_State | 1.6603 | 1.6574 | -0.0029 | 0.0029 |

*   🔴 **Máximo Cambio:** Variable `Prefix_Suffix` (Prefix_Suffix) con una diferencia $|D| = 1.1323$
*   🟢 **Mínimo Cambio:** Variable `SSLfinal_State` (SSLfinal_State) con una diferencia $|D| = 0.0029$

### Comparación Extrema para Nivel 25%

| Variable | Nombre | Grado_Best | Grado_Worst | Diferencia_D | Abs_Diferencia |
| --- | --- | --- | --- | --- | --- |
| URL_Length | URL_Length | 1.0770 | 0.5000 | -0.5770 | 0.5770 |
| SSLfinal_State | SSLfinal_State | 1.5764 | 1.0208 | -0.5556 | 0.5556 |
| Google_Index | Google_Index | 0.4808 | 1.0310 | 0.5503 | 0.5503 |
| Domain_registeration_length | Domain_registeration… | 0.9211 | 1.4595 | 0.5384 | 0.5384 |
| having_Sub_Domain | having_Sub_Domain | 0.8802 | 0.4474 | -0.4328 | 0.4328 |
| Prefix_Suffix | Prefix_Suffix | 0.5224 | 0.8798 | 0.3574 | 0.3574 |
| having_IP_Address | having_IP_Address | 0.9906 | 1.0913 | 0.1007 | 0.1007 |
| web_traffic | web_traffic | 0.4459 | 0.4459 | 0.0000 | 0.0000 |

*   🔴 **Máximo Cambio:** Variable `URL_Length` (URL_Length) con una diferencia $|D| = 0.5770$
*   🟢 **Mínimo Cambio:** Variable `web_traffic` (web_traffic) con una diferencia $|D| = 0.0000$

### Comparación Extrema para Nivel 12.5%

| Variable | Nombre | Grado_Best | Grado_Worst | Diferencia_D | Abs_Diferencia |
| --- | --- | --- | --- | --- | --- |
| web_traffic | web_traffic | 0.8600 | 1.5893 | 0.7293 | 0.7293 |
| SSLfinal_State | SSLfinal_State | 1.0913 | 0.3810 | -0.7104 | 0.7104 |
| Domain_registeration_length | Domain_registeration… | 0.7927 | 0.3750 | -0.4177 | 0.4177 |
| URL_Length | URL_Length | 0.7742 | 1.1905 | 0.4163 | 0.4163 |
| Prefix_Suffix | Prefix_Suffix | 0.3333 | 0.4107 | 0.0774 | 0.0774 |
| Google_Index | Google_Index | 0.3158 | 0.3500 | 0.0342 | 0.0342 |
| having_IP_Address | having_IP_Address | 0.7558 | 0.7310 | -0.0248 | 0.0248 |
| having_Sub_Domain | having_Sub_Domain | 0.3889 | 0.3750 | -0.0139 | 0.0139 |

*   🔴 **Máximo Cambio:** Variable `web_traffic` (web_traffic) con una diferencia $|D| = 0.7293$
*   🟢 **Mínimo Cambio:** Variable `having_Sub_Domain` (having_Sub_Domain) con una diferencia $|D| = 0.0139$

---

## 5. Análisis de Árboles Bayesianos (MST Dirigidos de Probabilidad Conjunta)

Para validar las dependencias de forma puramente probabilística, binarizamos todas las variables. Para cada par de variables $(X_i, X_j)$, encontramos la combinación de estados $(a, b)$ que maximiza su **Probabilidad Conjunta**:
$$P_{max}(X_i, X_j) = \max_{a,b} P(X_i=a, X_j=b)$$

Extraemos un Árbol de Expansión Mínima sobre las distancias $1 - P_{max}$ y lo orientamos de $X_i 	o X_j$ si $P(X_i = a) \le P(X_j = b)$.

Esto produce las redes dirigidas almacenadas en `results/nivel_<X>/graficos/arbol_bayesiano_*.png` y `results/global/arbol_bayesiano_Completo.png`.

---

## 6. Conclusiones y Discusión Académica

El análisis comparativo de las topologías y las dependencias bayesianas revela cambios estructurales críticos en las relaciones de los estudiantes:

1.  **Factores Determinantes:** Al comparar los bloques extremos (el 12.5% mejor vs el 12.5% peor), las variables cuyas relaciones y centralidad topológica cambian de forma más radical son **web_traffic (web_traffic)** y **SSLfinal_State (SSLfinal_State)**.
2.  **Mecánica de Impacto:** La variable `web_traffic` pasa de tener un grado de 0.8600 en los mejores estudiantes a 1.5893 en los peores ($D = +0.7293$).
3.  **Variables Invariantes:** Las variables que mostraron menor variación o que permanecieron casi idénticas en ambas redes son aquellas al final del ranking, lideradas por **having_Sub_Domain (having_Sub_Domain)**.

Este experimento demuestra empíricamente que la causa del bajo rendimiento académico no puede explicarse evaluando variables de manera aislada, sino a través de la **reorganización estructural de las variables socioeconómicas y de comportamiento académico**, lo cual queda plasmado en la direccionalidad de las dependencias probabilísticas en los Árboles Bayesianos generados.
