# 📊 Interpretación de Todas las Imágenes del Experimento NCD/Gzip

> **Proyecto:** Análisis de Rendimiento Académico con NCD/Gzip
> **Variables analizadas:** X1-X10 (factores socioacadémicos)
> **Variable clasificadora:** X11 (Promedio Final) → divide en Best y Worst
> **Particiones:** 12.5%, 25%, 50%

---

## Tabla de Variables (referencia rápida)

| Variable | Nombre | Tipo |
|----------|--------|------|
| X1 | Sexo | Categórica |
| X2 | Zona (Urbano/Rural) | Categórica |
| X3 | Ciclo Académico | Numérica |
| X4 | Ingreso Económico | Numérica |
| X5 | Trabaja (Sí/No) | Categórica |
| X6 | Beca (Sí/No) | Categórica |
| X7 | Educación del Jefe de Hogar | Categórica |
| X8 | Tamaño de Familia | Numérica |
| X9 | Asistencia | Numérica |
| X10 | Cursos Desaprobados | Numérica |

---

## 1. HEATMAPS DE MATRICES NCD

Los heatmaps muestran la **matriz de distancia NCD 10×10** entre todas las variables. El color indica qué tan diferentes son dos variables:
- **Amarillo claro (≈ 0)** = Variables MUY similares (se comprimen bien juntas)
- **Rojo oscuro (≈ 1)** = Variables MUY diferentes (no comparten información)

---

### 1.1 Heatmap Best 12.5% (Los 2,250 mejores estudiantes)

![Heatmap Best 12.5%](C:/Users/INTEL/.gemini/antigravity/brain/94f4f8d0-3815-4cec-b761-eccfa5501356/heatmap_Best_12.5.png)

**Interpretación:**
- La diagonal es 0 (cada variable es idéntica a sí misma).
- Se observa un **bloque de similitud fuerte** entre X1 (Sexo), X2 (Zona), X5 (Trabaja) y X6 (Beca), con valores NCD entre 0.88 y 0.96 — los más bajos fuera de la diagonal.
- Esto significa que en los **mejores estudiantes**, las variables categóricas socioeconómicas (sexo, zona, si trabaja, si tiene beca) están **fuertemente relacionadas entre sí**.
- **X3 (Ciclo) y X8 (Tam.Fam)** también muestran cercanía (NCD = 0.930), lo que sugiere que el ciclo y el tamaño familiar comparten patrones.
- **X4 (Ingreso)** está muy aislada (casi todo en 1.000), indicando que el ingreso económico **no comparte información** con las demás variables en este grupo.

---

### 1.2 Heatmap Worst 12.5% (Los 2,250 peores estudiantes)

![Heatmap Worst 12.5%](C:/Users/INTEL/.gemini/antigravity/brain/94f4f8d0-3815-4cec-b761-eccfa5501356/heatmap_Worst_12.5.png)

**Interpretación:**
- La estructura es **similar pero con diferencias sutiles importantes**.
- El bloque X5-X6 (Trabaja-Beca) tiene NCD = **0.860** (vs 0.884 en Best). Están **más cercanos** en el grupo Worst → la relación entre trabajar y tener beca se intensifica en los de bajo rendimiento.
- **X2 (Zona) vs X5 (Trabaja)**: NCD = 0.897 (vs 0.942 en Best), más similar en Worst → la zona de procedencia está más vinculada a si trabaja en los peores estudiantes.
- **X3-X10 (Ciclo-Desaprobados)**: aparece NCD = 0.983 en Worst (vs 1.000 en Best), sugiriendo que en los peores estudiantes el ciclo empieza a correlacionar con los desaprobados.

> **Conclusión clave:** En los peores estudiantes, las variables socioeconómicas (zona, trabajo, beca) se conectan más fuertemente entre sí. Esto sugiere un efecto acumulativo: la desventaja socioeconómica no actúa sola, sino en bloque.

---

## 2. ÁRBOLES DE EXPANSIÓN MÍNIMA (MST)

Los MST muestran la **estructura de conexiones más importante** entre variables. Cada nodo es una variable, cada arista tiene un peso NCD. El MST conecta todo usando las aristas de menor peso posible (las relaciones más fuertes).

- **Nodos naranjas** = Variables categóricas
- **Nodos azules** = Variables numéricas
- **Nodo grande** = Variable más central (más conexiones)

---

### 2.1 MST Best 12.5%

![MST Best 12.5%](C:/Users/INTEL/.gemini/antigravity/brain/94f4f8d0-3815-4cec-b761-eccfa5501356/mst_Best_12.5.png)

**Interpretación:**
- **X1 (Sexo)** es el nodo más central con el mayor grado ponderado (2.94). Está conectado a X5, X6, X4, X10 y X2 indirectamente.
- Se forma una **cadena clara**: X6 (Beca) → X5 (Trabaja) → X1 (Sexo) → X2 (Zona) → X7 (Educ.Jefe), con pesos entre 0.884 y 0.967.
- **X3 (Ciclo)** actúa como hub secundario conectando X8 (Tam.Fam) y X9 (Asistencia).
- **X4 (Ingreso)** está conectado con peso 1.000 (máxima distancia), confirmando que es la variable más aislada.

> **Lectura:** En los mejores estudiantes, la red gira alrededor del **sexo**, que conecta el cluster socioeconómico (beca-trabajo-zona) con las variables académicas.

---

### 2.2 MST Worst 12.5%

![MST Worst 12.5%](C:/Users/INTEL/.gemini/antigravity/brain/94f4f8d0-3815-4cec-b761-eccfa5501356/mst_Worst_12.5.png)

**Interpretación:**
- **X1 (Sexo)** sigue siendo central (grado = 2.94), pero hay un **cambio estructural clave**:
- **X8 (Tam.Fam)** ahora conecta con **X10 (Desaprobados)** con peso 0.983. En Best, X10 estaba conectado a X5. Este cambio indica que en Worst, **el tamaño de familia se asocia con los cursos desaprobados**.
- **X6 (Beca)** gana conexiones: ahora se conecta a X1 directamente y a X5 (peso 0.860, más fuerte que en Best).
- **X2 (Zona)** pierde centralidad: su grado cae de 2.85 a 1.84.

> **Cambio importante:** En los peores estudiantes, la red "rota": X5 (Trabaja) pierde centralidad y X8 (Tam.Fam) gana conexiones. Esto sugiere que el trabajo deja de ser un factor diferenciador y el tamaño de familia empieza a pesar más.

---

### 2.3 MST Best 25%

![MST Best 25%](C:/Users/INTEL/.gemini/antigravity/brain/94f4f8d0-3815-4cec-b761-eccfa5501356/mst_Best_25.png)

**Interpretación:**
- **X1 (Sexo)** se convierte en el **hub absoluto** con grado = 4.97. Está conectado directamente a 5 variables (X6, X5, X4, X10, X2).
- Esto indica que en el 25% mejor, el sexo es el factor que más organiza la red de relaciones.
- **X6 (Beca)** es ahora periférica (grado = 0.90), solo conectada a X1.
- La cadena X5 → X2 → X7 se mantiene en la periferia.

---

### 2.4 MST Worst 25%

![MST Worst 25%](C:/Users/INTEL/.gemini/antigravity/brain/94f4f8d0-3815-4cec-b761-eccfa5501356/mst_Worst_25.png)

**Interpretación:**
- **X1 (Sexo)** sigue central pero con **menor grado (3.97 vs 4.97 en Best)**. Pierde una conexión.
- **X6 (Beca)** gana centralidad: ahora está conectada a X1 Y a X5 (peso 0.921), con grado = 1.91 (vs 0.90 en Best). **La beca duplica su importancia en la red Worst.**
- **X8 (Tam.Fam)** conecta con X10 (Desaprobados) de nuevo, patrón que se repite del 12.5%.

> **Hallazgo:** La beca pasa de ser periférica en Best a ser central en Worst. Esto sugiere que para los peores estudiantes, la beca se convierte en un factor estructural que conecta con trabajo y sexo.

---

### 2.5 MST Best 50% y Worst 50%

````carousel
![MST Best 50%](C:/Users/INTEL/.gemini/antigravity/brain/94f4f8d0-3815-4cec-b761-eccfa5501356/mst_Best_50.png)
<!-- slide -->
![MST Worst 50%](C:/Users/INTEL/.gemini/antigravity/brain/94f4f8d0-3815-4cec-b761-eccfa5501356/mst_Worst_50.png)
````

**Interpretación al 50%:**
- La estructura se estabiliza: ambos MSTs son muy similares.
- **X1 (Sexo)** domina en ambos (grado ≈ 6.0), conectado a 6 variables.
- La diferencia principal: **X2 (Zona)** tiene grado 1.99 en Best pero solo 0.99 en Worst (D = −1.005).
- **X6 (Beca)** mantiene su patrón: grado 0.92 en Best → 1.95 en Worst (D = +1.04).
- Al incluir más estudiantes, el efecto de X5 (Trabaja) se diluye y X6 (Beca) se consolida como la variable más diferenciadora.

---

## 3. DENDROGRAMAS COMPARATIVOS

Los dendrogramas muestran cómo las variables se **agrupan jerárquicamente** por similitud NCD. Las variables que se unen más abajo (menor distancia Ward) son más similares. Los colores de las ramas indican clusters naturales.

---

### 3.1 Dendrograma Comparativo — Partición 12.5%

![Dendrograma Comparativo 12.5%](C:/Users/INTEL/.gemini/antigravity/brain/94f4f8d0-3815-4cec-b761-eccfa5501356/dendrograma_comparativo_12.5.png)

**Interpretación:**

**BEST (izquierda):**
- Primer agrupamiento (más fuerte): **X5 (Trabaja) + X6 (Beca)** se unen a distancia ≈ 0.88. Son las variables más similares.
- Segundo: **X1 (Sexo) + X2 (Zona)** se unen a ≈ 0.93.
- Tercero: X3 (Ciclo) se une con X8 (Tam.Fam) a ≈ 0.93.
- Las variables numéricas (X4, X9, X10) se mantienen separadas hasta el nivel más alto.

**WORST (derecha):**
- El primer agrupamiento cambia: **X2 (Zona) + X5 (Trabaja)** se unen primero a ≈ 0.85 (más fuerte que en Best).
- **X6 (Beca)** se une después con X3 (Ciclo) a ≈ 0.93, cambiando de cluster.
- **X8 (Tam.Fam) + X1 (Sexo)** forman un nuevo par a ≈ 0.96.

> **Cambio clave:** En Best, Trabaja y Beca van juntos. En Worst, Trabaja se empareja con Zona y Beca se aleja. Las relaciones socioeconómicas se reorganizan completamente.

---

### 3.2 Dendrograma Comparativo — Partición 25%

![Dendrograma Comparativo 25%](C:/Users/INTEL/.gemini/antigravity/brain/94f4f8d0-3815-4cec-b761-eccfa5501356/dendrograma_comparativo_25.png)

**Interpretación:**

**BEST:**
- **X5 + X6** siguen siendo el par más fuerte (≈ 0.90).
- X3 (Ciclo) se une temprano con X8 (Tam.Fam) a ≈ 0.95.
- X1 (Sexo) es el último en integrarse, confirmando su rol de hub.

**WORST:**
- **X5 + X6** también se emparejan primero (≈ 0.92), pero a mayor distancia.
- La diferencia principal: **X3 + X8 se unen más temprano** (≈ 0.95) y atraen a X1 (Sexo).
- **X2 (Zona)** queda más aislada en Worst.

> **Patrón:** A medida que el grupo crece (25%), las estructuras se parecen más, pero X2 (Zona) y X6 (Beca) siguen mostrando los mayores cambios de posición.

---

### 3.3 Dendrograma Comparativo — Partición 50%

![Dendrograma Comparativo 50%](C:/Users/INTEL/.gemini/antigravity/brain/94f4f8d0-3815-4cec-b761-eccfa5501356/dendrograma_comparativo_50.png)

**Interpretación:**

**BEST:**
- **X5 + X6** mantienen su unión temprana (≈ 0.91).
- Se forma un super-cluster socioeconómico: {X5, X6, X3, X8, X7 (Zona)}.
- Las variables académicas (X10, X9) son las últimas en unirse.

**WORST:**
- Estructura muy similar, pero **X2 (Zona)** cambia de posición: se agrupa después con X1 (Sexo), en lugar de con el bloque socioeconómico.
- La distancia de fusión general es ligeramente mayor en Worst (las variables son más "dispersas").

> **Conclusión:** Al 50%, las diferencias son sutiles pero consistentes. La reorganización de X2 (Zona) y X6 (Beca) se mantiene en todas las particiones.

---

## 4. GRÁFICOS DE COMPARACIÓN (Best vs Worst)

Estos gráficos muestran dos paneles: (1) barras de grado ponderado Best vs Worst, y (2) la diferencia D = Grado_Worst − Grado_Best.

---

### 4.1 Comparación — Partición 12.5%

![Comparación 12.5%](C:/Users/INTEL/.gemini/antigravity/brain/94f4f8d0-3815-4cec-b761-eccfa5501356/comparacion_12.5.png)

**Interpretación:**
- **Panel izquierdo (barras):** Se ve claramente que X2 (Zona) y X5 (Trabaja) tienen barras azules (Best) mucho más altas que las rojas (Worst). Están más conectadas en Best.
- **Panel derecho (D):** 
  - **X5 (Trabaja): D = −1.05** → La variable que MÁS cambia. En Best tiene grado 2.80 vs 1.76 en Worst. Trabajar organiza mucho más la red en los buenos estudiantes.
  - **X8 (Tam.Fam): D = +1.00** → En Worst, el tamaño de familia gana mucha centralidad. La familia grande afecta más negativamente.
  - **X6 (Beca): D = +0.95** → La beca también gana peso en Worst.
  - **X4 (Ingreso): D = 0.00** → El ingreso no cambia nada. Es irrelevante para diferenciar ambos grupos.

---

### 4.2 Comparación — Partición 25%

![Comparación 25%](C:/Users/INTEL/.gemini/antigravity/brain/94f4f8d0-3815-4cec-b761-eccfa5501356/comparacion_25.png)

**Interpretación:**
- **X6 (Beca): D = +1.01** → Ahora es la variable de MÁXIMO cambio. En Best tiene grado 0.90 (periférica) pero en Worst sube a 1.91 (central). **La beca se vuelve un factor estructural en los peores estudiantes.**
- **X1 (Sexo): D = −1.00** → El sexo pierde centralidad en Worst (de 4.97 a 3.97).
- **X8 (Tam.Fam): D = +1.00** → Consistente con el 12.5%: la familia grande pesa más en Worst.
- **X5 (Trabaja): D = +0.01** → Trabajar ya no diferencia a este nivel. Solo fue relevante en los extremos (12.5%).

---

### 4.3 Comparación — Partición 50%

![Comparación 50%](C:/Users/INTEL/.gemini/antigravity/brain/94f4f8d0-3815-4cec-b761-eccfa5501356/comparacion_50.png)

**Interpretación:**
- **X6 (Beca): D = +1.04** → Confirma el patrón. La beca es el factor más diferenciador en 2 de 3 particiones.
- **X2 (Zona): D = −1.01** → La zona pierde mucha centralidad en Worst. En Best, zona conecta más variables.
- Las demás variables tienen D ≈ 0 → la estructura se estabiliza con más datos.

---

### 4.4 Resumen Global — Todas las Particiones

![Resumen Global](C:/Users/INTEL/.gemini/antigravity/brain/94f4f8d0-3815-4cec-b761-eccfa5501356/resumen_comparacion_global.png)

**Interpretación del resumen:**
- Las barras muestran el cambio D para cada variable en las 3 particiones (naranja = 12.5%, morado = 25%, verde = 50%).
- **Variables con cambios consistentes (barras altas en las 3 particiones):**
  - **X6 (Beca):** Siempre positiva (~+1). Siempre gana centralidad en Worst.
  - **X2 (Zona):** Siempre negativa (~−1). Siempre pierde centralidad en Worst.
  - **X8 (Tam.Fam):** Positiva en 12.5% y 25%, luego se estabiliza.
- **Variables inestables (cambian según la partición):**
  - **X5 (Trabaja):** Muy negativa solo al 12.5%, casi nula al 25% y 50%.
  - **X1 (Sexo):** Negativa solo al 25%.
- **Variables estables (D ≈ 0 siempre):**
  - **X4 (Ingreso), X9 (Asistencia), X10 (Desaprobados):** No cambian. Son factores "neutros" que no diferencian Best de Worst.

---

## 5. CONCLUSIONES GENERALES

### ¿Qué variables causan las diferencias en rendimiento?

| Ranking | Variable | Efecto | Evidencia |
|---------|----------|--------|-----------|
| 🥇 1° | **X6 (Beca)** | Gana centralidad en Worst | D ≈ +1.0 en 3/3 particiones |
| 🥈 2° | **X2 (Zona)** | Pierde centralidad en Worst | D ≈ −1.0 en 3/3 particiones |
| 🥉 3° | **X5 (Trabaja)** | Pierde centralidad en Worst (extremos) | D = −1.05 solo al 12.5% |
| 4° | **X8 (Tam.Fam)** | Gana centralidad en Worst | D ≈ +1.0 al 12.5% y 25% |
| 5° | **X1 (Sexo)** | Hub en ambos, pierde peso en Worst | D = −1.0 solo al 25% |

### ¿Por qué X11 (promedio final) afecta a estas variables?

X11 no es una "causa" — es el **efecto**. Lo que el análisis muestra es:

1. **La beca (X6)** cambia su rol en la red según el rendimiento. En estudiantes de bajo rendimiento, la beca se vuelve un nodo central que conecta con trabajo, sexo y zona. Esto sugiere que los estudiantes que necesitan beca están sujetos a una **red de vulnerabilidades interconectadas**.

2. **La zona (X2)** pierde conexiones en Worst. En los buenos estudiantes, la zona está muy conectada con trabajo y educación del jefe. En los peores, esa cadena se rompe, sugiriendo que la zona deja de ser un factor organizador y otros factores (beca, familia) toman su lugar.

3. **Trabajar (X5)** solo diferencia en los extremos (12.5%). En los casos más severos de bajo rendimiento, el trabajo deja de conectar con la estructura y se aísla, sugiriendo que en los peores estudiantes trabajar no interactúa con las demás variables de la misma forma.

### Mensaje final

> El rendimiento académico (X11) no es causado por una sola variable. Lo que cambia entre Buenos y Malos estudiantes es la **estructura de relaciones** entre las variables socioeconómicas. La beca, la zona y el trabajo son los factores cuyas relaciones más se reorganizan, lo que indica que son las claves para entender (y potencialmente intervenir en) el rendimiento estudiantil.
